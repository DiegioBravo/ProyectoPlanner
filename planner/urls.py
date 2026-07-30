from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'planner'

urlpatterns = [
    path('', views.index, name='index'),

    # Redirección para /day/ → hoy
    path('day/', views.today_redirect, name='today'),

    # Vista del día con fecha
    path('day/<str:date_str>/', views.day_view, name='day_view'),

    # Tasks
    path('hourslot/<int:hourslot_id>/add/', views.add_task, name='add_task'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/attach/',views.add_attachment,name='add_attachment'),
    path('attachment/<int:attachment_id>/delete/',views.delete_attachment,name='delete_attachment'),


    path('checklist/add/', views.add_checklist_item, name='add_checklist'),
    path('checklist/toggle/<int:item_id>/', views.toggle_checklist, name='toggle_checklist'),
    path('checklist/delete/<int:item_id>/', views.delete_checklist, name='delete_checklist'),

    path('checklist/<int:pk>/urgencia/',views.actualizar_urgencia_checklist,name='actualizar_urgencia_checklist'),
    # Para Subtareas
    path('checklist/<int:checklist_id>/subtasks/', views.subtasks_list),
    path('subtask/add/', views.add_subtask),
    path('subtask/<int:pk>/toggle/', views.toggle_subtask),
    path('subtask/<int:pk>/delete/', views.delete_subtask),
    path('subtask/<int:subtask_id>/edit/',views.edit_subtask,name='edit_subtask'),

    # Autenticación
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
]
