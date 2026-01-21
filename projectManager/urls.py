from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("create_project", views.create_project, name="create_project"),
    path("edit_project/<int:id>", views.edit_project, name="edit_project"),
    path("mark_project_complete/<int:id>", views.mark_project_complete, name="mark_project_complete"),
    path("add_technology", views.add_technology, name="add_technology"),
    path("project/<int:id>", views.project, name="project"),
    path("delete_project/<int:id>", views.delete_project, name="delete_project"),
    path("mark_task_complete/<int:id>", views.mark_task_complete, name="mark_task_complete"),
    path("edit_task/<int:id>", views.edit_task, name="edit_task"),
    path("add_task/<int:id>", views.add_task, name="add_task"),
    path("delete_task/<int:id>", views.delete_task, name="delete_task"),
]
