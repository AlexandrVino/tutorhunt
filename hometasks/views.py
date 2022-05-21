import os
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView, FormView
from django.views.generic import ListView
from django.core.files import File
from pathlib import Path
from django.views.generic import DetailView
import mimetypes
from django.contrib.auth import get_user_model

from tutorhunt import settings
from users.models import Follow

from .forms import HometaskForm, AssignmentForm, IsCompletedForm
from .models import Hometask, Assignment


HOMETASK_CREATE = "hometasks/hometask_create.html"
HOMETASKS = "hometasks/hometasks.html"
HOMETASK_TEACHER_DETAIL = "hometasks/hometask_teacher_detail.html"
HOMETASK_STUDENT_DETAIL = "hometasks/hometask_student_detail.html"

User = get_user_model()


class HometaskCreateView(CreateView):
    model = Hometask
    template_name = HOMETASK_CREATE
    form_class = HometaskForm
    success_url = "hometasks"

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST, request.FILES)
        if form.is_valid():
            hometask, created = Hometask.manager.get_or_create(
                **form.cleaned_data, teacher=request.user
            )
            hometask.save()
        return redirect(reverse("hometasks"))


class HometasksView(ListView):
    model = Hometask
    template_name = HOMETASKS
    context_object_name = "hometasks"
    paginate_by = 5
    current_user = None

    def dispatch(self, request, *args, **kwargs):
        self.current_user = request.user
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        if self.current_user.role == "Teacher":
            return Hometask.manager.get_objects_with_filter(teacher=self.current_user)
        else:
            return Assignment.manager.get_objects_with_filter(
                student=self.current_user, is_completed=False
            )


class HometaskTeacherDetailView(DetailView, FormView):
    template_name = HOMETASK_TEACHER_DETAIL
    model = Hometask
    current_user = None
    context_object_name = "hometask"
    form_class = AssignmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = Assignment.manager.get_students(hometask=self.get_object())
        context["students"] = Follow.manager.get_followers(
            None,
            "user_from__first_name",
            "user_from__photo",
            user_to=self.current_user,
        )
        context["user"] = self.current_user
        return context

    def get(self, request, *args, **kwargs):
        self.current_user = request.user
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        for i in request.POST.getlist("choose"):
            assign, is_created = Assignment.manager.get_or_create(
                student_id=int(i), hometask=self.get_object()
            )
            assign.save()
        return self.get(request, *args, **kwargs)


def hometask_download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT / "uploads" / "hometasks", path)
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            mime_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(fh.read(), content_type=mime_type)
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                file_path
            )
            return response
    raise Http404


class HometaskStudentDetailView(DetailView):
    template_name = HOMETASK_STUDENT_DETAIL
    model = Hometask
    current_user = None
    context_object_name = "hometask"
    form_class = IsCompletedForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.current_user
        return context

    def get(self, request, *args, **kwargs):
        self.current_user = request.user
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        assign, is_created = Assignment.manager.get_or_create(
            student_id=request.user.id, hometask=self.get_object()
        )
        assign.is_completed = True
        assign.save()
        return redirect(reverse("hometasks"))


# def mark_as_solved(request, pk):
#     task = get_object_or_404(Hometask, pk=pk)

#     if request.method == "POST":
#         task.delete()
#         return redirect(reverse("hometasks"))
