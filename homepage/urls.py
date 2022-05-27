from django.urls import path

from homepage.views import HomepageView

urlpatterns = [
    path("", HomepageView.as_view(), name="homepage")
]
