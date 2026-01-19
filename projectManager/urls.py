from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("create_project", views.create_project, name="create_project"),
    path("add_technology", views.add_technology, name="add_technology"),
    path("project/<int:id>", views.project, name="project"),
    path("delete_project/<int:id>", views.delete_project, name="delete_project"),
]
