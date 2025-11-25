from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    path('become-a-supplier/', views.become_supplier, name='become_supplier'),
    path('seller-registration/step1/', views.seller_registration_step1, name='seller_registration_step1'),
    path('seller-registration/step2/', views.seller_registration_step2, name='seller_registration_step2'),
    path('seller-registration/step3/', views.seller_registration_step3, name='seller_registration_step3'),
    path('seller-registration/step4/', views.seller_registration_step4, name='seller_registration_step4'),
    path('setup/', views.setup_store, name='setup_store'),
    path('dashboard/', views.vendor_dashboard, name='dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
