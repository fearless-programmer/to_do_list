from django.urls import path
from . import views 

urlpatterns=[
    path('dark', views.dark_index, name = 'darkboard'),
   path('add_task/<str:pk>/', views.create_task, name='create-task2'),
    path('add_new_task/', views.create_new_task, name='create-new-task2'),
    path('update_task/<str:pk>/', views.updateTask, name = 'update-task2'),
    path('update_plan/<str:pk>/', views.updatePlan, name = 'update-plan2'),
    path('confirm task delete/<str:pk>/', views.deleteViewTask, name = 'confirm-task-delete2'),
    path('confirm plan delete/<str:pk>/', views.deleteViewPlan, name = 'confirm-plan-delete2'),
    path('delete-task/<str:pk>/', views.deleteTask, name = 'delete-task2'),
    path('delete-plan/<str:pk>/', views.deletePlan, name = 'delete-plan2'),
    path('statistics/', views.statistics, name ='statistics2'),
    path('task-list/', views.task_list, name='task_list2'),
    path('add_plan/', views.createPlan, name ='add-plan2'),
    path('task/<str:pk>/', views.task_view, name='task_view2'),
    path('change_password/', views.change_password, name='change_password2'),
    path('profile/', views.profile, name='profile2'),
    path('update_profile/', views.update_profile, name='update_profile2'),
]