from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models import Avg, Count
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, FormView, ModelFormMixin

from follow.forms import FollowForm
from follow.models import Follow
from rating.forms import RatingForm
from rating.models import Rating
from .backends import EmailAuthBackend, EmailUniqueFailed
from .forms import EditProfileForm, LoginForm, RegisterForm
from .models import User
from .utils import edit_user_data

SIGNUP_TEMPLATE = "users/signup.html"
LOGIN_WITH_USERNAME_TEMPLATE = "users/login_with_username.html"
LOGIN_WITH_EMAIL_TEMPLATE = "users/login_with_email.html"
USER_LIST_TEMPLATE = "users/user_list.html"
CUR_USER_TEMPLATE = "users/user_detail.html"
EDIT_PROFILE_TEMPLATE = "users/edit_profile.html"


class UserListView(ListView):
    """Возвращает страничку Списка пользователей"""

    template_name = USER_LIST_TEMPLATE
    queryset = User.objects.all()
    context_object_name = "users"


class UserDetailView(DetailView, FormView):
    """Возвращает страничку конкретного пользователя"""

    template_name = CUR_USER_TEMPLATE
    model = User
    context_object_name = "user_detail"
    pk_url_kwarg = "user_id"
    form_class = FollowForm
    current_user = None
    object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user"] = self.current_user

        context["follows"] = Follow.manager.get_followers(
            None, "user_from__first_name", "user_from__photo", user_to=self.object)
        context["already_follow"] = any(
            [follow.user_from.id == self.current_user and follow.active for follow in context["follows"]])

        context["rating_form"] = RatingForm()
        try:
            context["rating"] = Rating.manager.get_objects_with_filter(
                user_from=self.current_user, user_to=self.object
            )
            context["rating"] = context["rating"][0] if context["rating"] else 0
        except Rating.DoesNotExist:
            context["rating"] = 0

        context["rating_form"].fields["star"].initial = context["rating"]

        context["all_ratings"] = Rating.manager.get_objects_with_filter(
            user_to=self.object, star__in=[1, 2, 3, 4, 5]
        ).aggregate(Avg("star"), Count("star"))

        return context

    def get_object(self, queryset=None):
        if self.object:
            return self.object
        return super(UserDetailView, self).get_object(queryset)

    def get(self, request, *args, **kwargs):
        self.current_user = request.user
        if self.current_user.id == self.kwargs.get("user_id"):
            self.object = self.current_user
        self.current_user = self.current_user.id

        return super(UserDetailView, self).get(request, *args, **kwargs)

    @method_decorator(login_required, name="dispatch")
    def post(self, request, *args, **kwargs):
        user_from = request.user

        if self.kwargs.get("user_id") == user_from.id:
            return self.get(request, *args, **kwargs)
        user_to = self.get_object()

        if "rating_form" in request.POST:
            rating, created = Rating.manager.get_or_create(
                user_to=user_to, user_from=user_from
            )
            rating.star = int(request.POST["star"])
            rating.save()
        else:
            follow, is_created = Follow.manager.get_or_create(user_to=user_to, user_from=user_from)
            if not is_created:
                follow.active = not follow.active
                follow.save()

        self.current_user = user_from.id
        return self.get(request, *args, **kwargs)


class LoginWithEmailView(FormView):
    """Возвращает страничку регистрации пользователя"""

    form_class = LoginForm
    template_name = LOGIN_WITH_EMAIL_TEMPLATE
    messages = []

    def get_success_url(self):
        return reverse("users")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = self.messages
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = EmailAuthBackend.authenticate(
                request, email=email, password=password
            )

            if user is not None:
                if user.is_active:
                    EmailAuthBackend.authenticate(request, email, password)
                    return redirect(reverse("user_detail", args=(user.id,)))
            self.messages.append("Неверный логин или пароль!")

            return self.get(request, *args, **kwargs)

        self.messages.append("Заполните форму корректно!")
        return super().get(request, *args, **kwargs)


class SignupView(CreateView):
    """Регистрация"""

    template_name = SIGNUP_TEMPLATE
    model = User
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("login")

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST, request.FILES)
        errors = []
        if form.is_valid():
            try:

                new_user = EmailAuthBackend.create_user(**form.cleaned_data)
                current_site = get_current_site(request)
                mail_subject = "Activation link has been sent to your email id"

                message = render_to_string(
                    "users/acc_active_email.html",
                    {
                        "user": new_user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(new_user.pk)),
                        "token": default_token_generator.make_token(new_user),
                    },
                )

                EmailMessage(mail_subject, message, to=[new_user.email]).send()
                return HttpResponse("Подтвердите почту")

            except (IntegrityError, ValidationError, EmailUniqueFailed) as err:

                if type(err) is ValidationError:
                    err = "\n".join(err.messages)

                if type(err) is IntegrityError:
                    err = "Пользователь с таким именем уже сооздан"

                if type(err) is EmailUniqueFailed:
                    err = str(err)

                errors.append(err)

        errors += [err[0] for err in list(form.errors.values())]
        return render(request, self.template_name, {"form": form, "chats": set(errors)})


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            EmailAuthBackend.authenticate(request, user=user)

            return redirect(reverse("user_detail", args=(user.id,)))
        else:
            return HttpResponse("Activation link is invalid!")


@method_decorator(login_required, name="dispatch")
class ProfileView(TemplateView, ModelFormMixin):
    """Возвращает страничку профиля пользователя"""

    template_name = EDIT_PROFILE_TEMPLATE
    context_object_name = "user"
    model = User
    form_class = EditProfileForm

    def get(self, request, *args, **kwargs):
        self.object = request.user
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("users")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = request.user
            if user.id:
                edit_user_data(user, **form.cleaned_data)
                return redirect(reverse("user_detail", args=(user.id,)))

        return self.get(request, *args, **kwargs)
