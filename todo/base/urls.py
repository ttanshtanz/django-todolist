from django.urls import path
from .views import ListView, TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage, toggle_task_status
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>', TaskDelete.as_view(), name='task-delete'),
    path('toggle-task/<int:pk>/', toggle_task_status, name='toggle-task'),
]
