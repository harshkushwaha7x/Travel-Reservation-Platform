from django.urls import path
from . import views
urlpatterns = [
    path('', views.accuile_page, name="admindashboard"),
    path('client', views.client_page, name="client"),
    path('offers', views.offers_page, name="offers"),
    path('category', views.category_page, name="category"),
    path('promotion', views.promotion_page, name="promotion"),
    path('contactus', views.contactus_page, name="contactus"),
    path('settings', views.settings_page, name="settings"),
    path('newclient', views.newclient_page, name="newclient"),
    path('newcategory', views.newcategory_page, name="newcategory"),
    path('newoffer', views.newoffer_page, name="newoffer"),
    path('newpromotion', views.newpromotion_page, name="newpromotion"),
    

    path('delete_client/<int:client_id>/', views.delete_client, name='delete_client'),
    path('edit_client/<int:client_id>/', views.edit_client, name='edit_client'),
    path('create_client', views.create_client, name="create_client"),

    path('create_category', views.create_category, name="create_category"),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),

    path('create_offer', views.create_offer, name="create_offer"),
    path('delete_offer/<int:offer_id>/', views.delete_offer, name='delete_offer'),
    path('edit_offer/<int:offer_id>/', views.edit_offer, name='edit_offer'),

    path('create_promotion', views.create_promotion, name="create_promotion"),
    path('delete_promotion/<int:promotion_id>/', views.delete_promotion, name='delete_promotion'),
    path('edit_promotion/<int:promotion_id>/', views.edit_promotion, name='edit_promotion'),
    path('send_message_to_client',views.send_message_to_client, name="send_message_to_client")

]
