from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    TaskView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    SignUpView, 
    MarkTaskCompletedView,
    ToggleTaskStatusView,
)

urlpatterns = [
    # Task 
    path('', TaskView.as_view(), name='home'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task/create/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/complete/', MarkTaskCompletedView.as_view(), name='mark-task-completed'),
     path('toggle-task/<int:pk>/', ToggleTaskStatusView.as_view(), name='toggle-task'),
    # Authentication 
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
]
