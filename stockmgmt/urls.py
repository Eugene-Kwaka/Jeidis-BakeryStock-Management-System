from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('list_items/', list_items,  name="list_items"),
    path('add_items/', add_items,  name="add_items"),
    path('update_items/<str:pk>/', update_items, name="update_items"),
    path('delete_items/<str:pk>/', delete_items, name="delete_items"),
    path('item_details/<str:pk>/', item_details, name="item_details"),
    path('issue_item/<str:pk>/', issue_item, name="issue_item"),
    path('receive_item/<str:pk>/', receive_item, name="receive_item"),
    path('reorder_level/<str:pk>/', reorder_level, name="reorder_level"),

]
