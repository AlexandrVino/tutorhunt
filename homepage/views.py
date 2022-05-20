from msilib.schema import ListView
from django.views.generic.base import TemplateView

HOMEPAGE_TEMPLATE = "homepage/homepage.html"
FIND_TEMPLATE = "homepage/find.html"


class HomepageView(TemplateView):
    template_name = HOMEPAGE_TEMPLATE


# class FindView(ListView):
#     template_name = FIND_TEMPLATE
