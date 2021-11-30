from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', DeskList.as_view(), name='main'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('desk-create/', DeskCreate.as_view(), name='desk-create'),
    path('desk-update/<int:pk>/', DeskUpdate.as_view(), name='desk-update'),
    path('desk-delete/<int:pk>/', DeleteDesk.as_view(), name='desk-delete'),
    path('desk/<int:pk>/', task_list, name='desk'),
    path('task/<int:pk>/', Task.as_view(), name='task'),
    path('task-create/<int:pk>', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteTask.as_view(), name='task-delete'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="list/password_reset.html"),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="list/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="list/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="list/password_reset_done.html"), name='password_reset_complete'),
]