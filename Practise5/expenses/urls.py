from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # points to views.home
    path('expenses/', views.expense_list, name='expense_list'),  # <--- points here
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/<int:pk>/edit/', views.edit_expense, name='edit_expense'),
    path('expenses/<int:pk>/delete/', views.delete_expense, name='delete_expense'),
    
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),

    path('group-expenses/', views.group_expense_list, name='group_expense_list'),
    path('group-expenses/add/', views.add_group_expense, name='add_group_expense'),
    path('group-expenses/<int:pk>/edit/', views.edit_group_expense, name='edit_group_expense'),
    path('group-expenses/<int:pk>/delete/', views.delete_group_expense, name='delete_group_expense'),
]
