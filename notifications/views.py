from ctypes import Union
from typing import Any, Dict, Type
from unicodedata import category
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from notifications.models import NotificationModel, NotificationQueryset
from notifications.forms import AdminFilterNotificationsForm, FilterNotificationsForm


@method_decorator(login_required, name="dispatch")
class NotificationListView(TemplateView):
    template_name = "notifications/view_notifications.html"
    paginate_by = 5
    queryset = NotificationModel.objects.all()
    form_initial: Dict[str, Any] = {}
    
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.kwargs.setdefault("page", 1)
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self) -> Type[ModelForm]:
        if self.request.user.is_staff:
            return AdminFilterNotificationsForm
        return FilterNotificationsForm
    
    def get_queryset(self) -> NotificationQueryset:
        if self.request.user.is_staff:
            return self.queryset.order_by("-creation")
        return (
            self.queryset
                .by_recipient(self.request.user)
                .order_by("-creation")
        )

    def get_paginator(self) -> Paginator:
        return Paginator(self.get_queryset(), per_page=self.paginate_by, orphans=3)

    def get_form(self):
        return self.get_form_class()(initial=self.get_form_initial())

    def get_form_initial(self) -> Dict[str, Any]:
        initial = self.form_initial

        if self.request.user.is_staff:
            initial.setdefault("recipient", self.request.user)

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["form"] = self.get_form()

        paginator = self.get_paginator()
        context["objects"] = paginator.page(self.kwargs["page"])
        context["num_page"] = paginator.num_pages

        return context
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.get_queryset().by_recipient(request.user).mark_read()

        if self.kwargs["page"] > self.get_paginator().num_pages:
            return redirect(reverse("notifications"))

        return super().get(request, *args, **kwargs)
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.form_initial = self.request.POST.dict()
        
        category, recipient = (self.request.POST.get("category"),
                               self.request.POST.get("recipient"))

        if recipient:
            self.queryset = self.queryset.by_recipient(recipient)
        if category:
            self.queryset = self.queryset.by_category(category)

        return self.get(request, *args, **kwargs)
