from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # REGISTER & LOGIN URL PATHS
    path('register/', registerPage, name='registerPage'),
    path('login/', loginPage, name='loginPage'),
    path('logout/', logoutUser, name='logout'),

    path('', home, name="home"),

    path('list_items/', list_items,  name="list_items"),
    path('add_items/', add_items,  name="add_items"),
    path('update_items/<str:pk>/', update_items, name="update_items"),
    path('delete_items/<str:pk>/', delete_items, name="delete_items"),
    path('item_details/<str:pk>/', item_details, name="item_details"),
    path('issue_item/<str:pk>/', issue_item, name="issue_item"),
    path('receive_item/<str:pk>/', receive_item, name="receive_item"),
    path('reorder_level/<str:pk>/', reorder_level, name="reorder_level"),

    # PASSWORD RESET URL PATHS
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="password_reset.html"), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset_sent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_form.html"), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset_done.html"), name="password_reset_complete"),
]
