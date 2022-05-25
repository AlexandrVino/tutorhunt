import mimetypes
import os

from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView

from bunch.models import Bunch
from follow.models import Follow
from tutorhunt import settings
from users.models import Role
from .forms import AssignmentForm, HometaskForm, IsCompletedForm
from .models import Assignment, Hometask

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

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role != Role.TEACHER:
            return redirect(reverse("user_detail", args=(user.id,)))

        return super(HometaskCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST, request.FILES)
        user = request.user

        if user.role != Role.TEACHER:
            redirect(reverse("user_detail", args=(user.id,)))

        if form.is_valid():
            hometask, created = Hometask.manager.get_or_create(
                **form.cleaned_data, teacher=user
            )
            hometask.save()
        else:
            return super().get(request, *args, **kwargs)
        return redirect(reverse("hometasks"))


class HometasksView(ListView):
    model = Hometask
    template_name = HOMETASKS
    context_object_name = "hometasks"
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
    object = None

    def get_object(self, queryset=None):
        if self.object:
            return self.object
        obj = self.model.manager.get_teachers(id=self.kwargs.get("pk"))
        self.object = obj and obj[0]
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = Assignment.manager.get_students(hometask=self.object)
        context["bunches"] = set(
            map(
                lambda x: (x.student.id, x.student.first_name),
                Bunch.manager.get_teacher_students(
                    self.current_user,
                    "student__first_name",
                ),
            )
        )

        context["user"] = self.current_user
        return context

    def get(self, request, *args, **kwargs):
        self.current_user = request.user
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        hometask = self.get_object()
        student_id = request.POST.get("student-id")

        if student_id:
            assign, is_created = Assignment.manager.get_or_create(
                student_id=int(student_id), hometask=hometask
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
