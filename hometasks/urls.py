from django.urls import path

from .views import (
    HometaskCreateView,
    HometasksView,
    HometaskTeacherDetailView,
    hometask_download,
    HometaskStudentDetailView,
)


urlpatterns = [
    path("hometasks/", HometasksView.as_view(), name="hometasks"),
    path("hometask_create/", HometaskCreateView.as_view(), name="hometask_create"),
    path(
        "hometask_teacher_detail/<int:pk>",
        HometaskTeacherDetailView.as_view(),
        name="hometask_teacher_detail",
    ),
    path("hometask_download/<str:path>", hometask_download, name="hometask_download"),
    path(
        "hometask_student_detail/<int:pk>",
        HometaskStudentDetailView.as_view(),
        name="hometask_student_detail",
    ),
]
