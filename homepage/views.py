from django.contrib.auth import get_user_model
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from homepage.forms import SearchForm

HOMEPAGE_TEMPLATE = "homepage/homepage.html"
FIND_TEMPLATE = "homepage/find.html"
User = get_user_model()


class HomepageView(TemplateView, FormView):
    template_name = HOMEPAGE_TEMPLATE
    form_class = SearchForm
    users = []
    messages = []
    is_post = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = self.messages if self.users else self.messages + (
            ["По вашему запросу не нашлось учителя"] if self.is_post else [])
        context["objects"] = self.users
        return context

    def get(self, request, *args, **kwargs):
        self.is_post = False
        return super(HomepageView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.is_post = True

        if form.is_valid():
            value = form.cleaned_data["value"]
            self.users = User.manager.get_objects_with_filter(bio__contains=value.lower())
        else:
            self.messages.append(form.errors)

        return super().get(request, *args, **kwargs)


# class FindView(ListView):
#     template_name = FIND_TEMPLATE
