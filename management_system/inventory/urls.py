from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    ProfileView,
    CustomerCategoryViewSet,
    CustomerViewSet,
    ProductViewSet,
    InvoiceViewSet,
    InvoiceReportView,
)
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('categories',CustomerCategoryViewSet,basename='category')
router.register('customers',CustomerViewSet,basename='customer')
router.register('products',ProductViewSet,basename='product')
router.register('invoices',InvoiceViewSet,basename='invoice')
urlpatterns = [
    path('',include(router.urls)),
    path('register/',RegisterView.as_view(),name='register'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('reports/invoices/',InvoiceReportView.as_view(),name='invoice-report'),
    path('login/',obtain_auth_token,name='login'),
]