from django.contrib.auth import get_user_model, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic.edit import CreateView, FormView

from .backends import EmailAuthBackend, EmailUniqueFailed
from .forms import LoginForm, RegisterForm
from .models import User

SIGNUP_TEMPLATE = "users/signup.html"
LOGIN_WITH_USERNAME_TEMPLATE = "users/login_with_username.html"
LOGIN_WITH_EMAIL_TEMPLATE = "users/login_with_email.html"
PROFILE_TEMPLATE = "users/profile.html"


class LoginWithEmailView(FormView):
    """Возвращает страничку регистрации пользователя"""

    form_class = LoginForm
    template_name = LOGIN_WITH_EMAIL_TEMPLATE

    def get_success_url(self):
        return reverse("profile")

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
                    return redirect(self.get_success_url())

        return super().post(request, *args, **kwargs)


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
        return reverse("profile")

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)
        errors = []
        if form.is_valid():
            try:
                print(form.cleaned_data)
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
                print(err)
                if type(err) is ValidationError:
                    err = "\n".join(err.messages)

                if type(err) is IntegrityError:
                    err = "Пользователь с таким именем уже сооздан"

                if type(err) is EmailUniqueFailed:
                    err = str(err)

                errors.append(err)

        errors += [err[0] for err in list(form.errors.values())]
        return render(request, self.template_name,
                      {"form": form, "errors": set(errors)})


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user,
                                                                    token):
            user.is_active = True
            user.save()

            return redirect("/auth/profile")
        else:
            return HttpResponse("Activation link is invalid!")
