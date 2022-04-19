from django.urls import path,include
from .views import customer_corr_view

app_name = 'customers'

urlpatterns = [
    path('', customer_corr_view, name='cutomer_view')
]