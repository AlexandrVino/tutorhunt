from django.urls import path

from homepage.views import HomepageView


urlpatterns = [
    # path("find/", FindView.as_view(), name="find"),
    path("", HomepageView.as_view(), name="homepage")
]
