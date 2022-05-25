from django.urls import path

from bunch.views import BunchView, EditBunchView

urlpatterns = [
    path("add_bunch/<int:user_to>/<int:day>/<int:time>/", BunchView.as_view(), name="add_bunch"),
    path("edit_bunch/<int:day>/<int:time>/", EditBunchView.as_view(), name="edit_bunch"),
]
