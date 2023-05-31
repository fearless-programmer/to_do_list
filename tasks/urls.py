from django.urls import path
from tasks import views

urlpatterns = [
    path('', views.index, name = 'dashboard'),
    path('add_task/<str:pk>/', views.create_task, name='create-task'),
    path('add_new_task/', views.create_new_task, name='create-new-task'),
    path('update_task/<str:pk>/', views.updateTask, name = 'update-task'),
    path('update_plan/<str:pk>/', views.updatePlan, name = 'update-plan'),
    path('confirm task delete/<str:pk>/', views.deleteViewTask, name = 'confirm-task-delete'),
    path('confirm plan delete/<str:pk>/', views.deleteViewPlan, name = 'confirm-plan-delete'),
    path('delete-task/<str:pk>/', views.deleteTask, name = 'delete-task'),
    path('delete-plan/<str:pk>/', views.deletePlan, name = 'delete-plan'),
    path('statistics/', views.statistics, name ='statistics'),
    path('task-list/', views.task_list, name='task_list'),
    path('add_plan/', views.createPlan, name ='add-plan'),
    path('task/<str:pk>/', views.task_view, name='task_view'),
  ]