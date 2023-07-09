from django.urls import path
from . import views


urlpatterns = [
    path('', views.index,name= "index"),
    path('projects/',views.projects,name= "projects"),
    path('projects/<int:id>',views.project_detail,name= "project_detail"),
    path('tasks/', views.tasks,name= "tasks"),
    path('create_task/', views.create_task,name= "create_task"),
    path('create_project/', views.create_project,name= "create_project"),
    path('signup/', views.signup,name= "signup"),
    path('logout/', views.signout,name= "logout"),
    path('signin/',views.signin,name= "signin"),
    path('tasks/<int:id>',views.update_task,name= "update_task"),
    path('tasks/<int:id>/complete',views.complete_task,name= "complete_task"),
    path('tasks/<int:id>/delete',views.delete_task,name= "delete_task"),
    path('projects/<int:id>/delete',views.delete_project,name= "delete_project"),
]
