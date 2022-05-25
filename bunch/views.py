from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import ModelFormMixin

from bunch.forms import AddBunchForm, EditBunchForm
from bunch.models import Bunch, BunchStatus
from users.utils import add_busy_hours

ADD_BUNCH_TEMPLATE = "users/add_bunch.html"
EDIT_BUNCH_TEMPLATE = "users/edit_bunch.html"

User = get_user_model()


@method_decorator(login_required, name="dispatch")
class BunchView(TemplateView, ModelFormMixin):
    """
    ViewClass для создания запроса на связь (занятие)
    """

    template_name = ADD_BUNCH_TEMPLATE
    context_object_name = "bunch"
    model = Bunch
    form_class = AddBunchForm
    object = None

    def get_datetime(self) -> str:
        """
        :return: str
        Метод, возвращающий время связи (занятия) в формате день:час
        """

        return f'{self.kwargs.get("day")}:{self.kwargs.get("time")}'

    def get_context_data(self, **kwargs) -> dict:
        """

        :param kwargs: словарь контекста
        :return: dict

        Метод, получающий контекст для шаблонов

        """

        context = super().get_context_data(**kwargs)
        context["form"].fields["day"].initial = self.kwargs.get("day")
        context["form"].fields["time"].initial = self.kwargs.get("time")

        return context

    def get_success_url(self) -> str:
        """
        :return: str
        Метод, получающий url для успешной переадрисации
        """

        return reverse("user_detail", args=(self.kwargs.get("user_to"), ))

    def get(self, request, *args, **kwargs):
        """

        :param request: запрос
        :param args: картеж контекста
        :param kwargs: сдлварь контекста
        :return:

        Метод ответа на GET запрос клиента

        """

        if not self.object:
            bunch = self.model.manager.filter(student=request.user, datetime=self.get_datetime())
            self.object = bunch[0] if bunch else None

        if self.object:
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """

        :param request: запрос
        :param args: картеж контекста
        :param kwargs: сдлварь контекста
        :return:

        Метод ответа на POST запрос клиента

        """

        form = self.get_form()
        if form.is_valid():

            user_from = request.user

            if self.kwargs.get("user_id") == user_from.id:
                return self.get(request, *args, **kwargs)

            user_to = User.manager.get(pk=self.kwargs.get("user_to"))
            teacher = user_from if user_from.role == "teacher" else user_to
            student = user_from if user_from is not teacher else user_to

            if student == teacher:
                return self.get(request, *args, **kwargs)

            day = form.cleaned_data["day"]
            time = form.cleaned_data["time"]

            bunch, is_created = Bunch.manager.get_or_create(student=student, teacher=teacher, datetime=f"{day}:{time}")

            if is_created:
                bunch.status = BunchStatus.WAITING
                bunch.save()

            if user_from.id:
                return redirect(self.get_success_url())

        return self.get(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class EditBunchView(TemplateView, ModelFormMixin):
    """
    ViewClass для редактирования запроса на связь (занятие)
    """

    template_name = EDIT_BUNCH_TEMPLATE
    context_object_name = "bunch"
    model = Bunch
    form_class = EditBunchForm
    object = None

    def get_datetime(self) -> str:
        """
        :return: str
        Метод, возвращающий время связи (занятия) в формате день:час
        """

        return f'{self.kwargs.get("day")}:{self.kwargs.get("time")}'

    def get_context_data(self, **kwargs):
        """

        :param kwargs: словарь контекста
        :return: dict

        Метод, получающий контекст для шаблонов

        """

        context = super().get_context_data(**kwargs)

        context["form"].fields["day"].initial = self.kwargs.get("day")
        context["form"].fields["time"].initial = self.kwargs.get("time")

        if self.object:
            context["form"].fields["status"].initial = self.object.status

        self.kwargs["old_day"] = self.kwargs.get("day")
        self.kwargs["old_time"] = self.kwargs.get("time")

        return context

    def get_success_url(self):
        """
        :return: str
        Метод, получающий url для успешной переадрисации
        """

        return reverse("user_detail", args=(self.request.user.id,))

    def get(self, request, *args, **kwargs):
        """

        :param request: запрос
        :param args: картеж контекста
        :param kwargs: сдлварь контекста
        :return:

        Метод ответа на GET запрос клиента

        """

        if not self.object:
            bunch = self.model.manager.filter(teacher=request.user, datetime=self.get_datetime())
            self.object = bunch[0] if bunch else None

            if self.object is None:
                return redirect(self.get_success_url())

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """

        :param request: запрос
        :param args: картеж контекста
        :param kwargs: сдлварь контекста
        :return:

        Метод ответа на POST запрос клиента

        """

        form = self.get_form()

        if form.is_valid():

            teacher = request.user

            if teacher.id:
                day = form.cleaned_data["day"]
                time = form.cleaned_data["time"]

                status = form.cleaned_data["status"]

                datetime = f"{day}:{time}"

                if not self.object:
                    bunch = self.model.manager.filter(teacher=request.user, datetime=self.get_datetime())
                    self.object = bunch[0] if bunch else None

                new_bunch = Bunch.manager.filter(teacher__id=teacher.id, datetime=datetime, status=BunchStatus.ACCEPTED)

                if new_bunch and not (new_bunch[0] == self.object):
                    return self.get(request, *args, **kwargs)

                if status == BunchStatus.ACCEPTED:
                    add_busy_hours(teacher, bunch=self.object, value=True)
                else:
                    add_busy_hours(teacher, bunch=self.object, value=False)

                if self.object:
                    self.object.datetime = datetime
                    self.object.status = status
                    self.object.save()

                return redirect(self.get_success_url())

        return self.get(request, *args, **kwargs)
