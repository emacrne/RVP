from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_tool, name='add_tool'),
    path('edit/<str:pk>/', views.edit_tool, name='edit_tool'),
    path('delete/<str:pk>/', views.delete_tool, name='delete_tool'),
    path('scan/', views.scan_barcode, name='scan_barcode'),
    path('save_barcode/', views.save_barcode, name='save_barcode'),
    path('find/<str:barcode>/', views.find_tool_by_barcode, name='find_tool_by_barcode'),
    path('tool/<str:pk>/', views.tool_detail, name='tool_detail'),
]