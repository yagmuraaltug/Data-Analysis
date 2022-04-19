from django.urls import path
from .views import add_purchase_view, chart_select_view, sales_dist_view

app_name = 'products'

urlpatterns = [
    path('', chart_select_view, name='product_view'),
    path('add/', add_purchase_view, name='add_purchase'),
    path('sales/', sales_dist_view, name='sales'),

]

