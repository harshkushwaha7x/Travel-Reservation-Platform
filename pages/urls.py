from django.urls import path
from . import views
urlpatterns = [
    path('payment_page', views.payment_page, name="payment_page"),
    path('checkout_page', views.checkout_page, name="checkout_page"),
    path('', views.accuile_page, name="accuilepage"),
    path('login',views.login_SingUp_Page, name="login_SingUp_Page"),
    path('contact-us',views.contact_us_page, name="contact_us_page"),
    path('about-us',views.about_us_page, name="about_us_page"),
    path('package',views.package_page, name='package_page'),
    path('offers',views.offers_page, name='offers_page'),
    path('login_validation',views.login_validation, name='login_validation'),
    path('signup_validation',views.signup_validation, name='signup_validation'),

    path('change_password',views.change_password, name='change_password'),
    path('logout',views.logout_view, name='logout'),
    path('update_profile',views.update_profile, name='update_profile'),

    path('Code_validation',views.get_verificaioncode, name='Code_validation'),
    path('signup_validation1',views.email_validation, name='signup_validation1'),
    path('client_message',views.client_message, name='client_message'),
    path('client_profil_message',views.client_profil_message, name='client_profil_message'),
    path('testmail',views.simple_mail),

    path('offer_details/<int:offer_id>/', views.offer_details, name='offer_details'),
    path('reserver_offre/<int:offer_id>/', views.reserver_offre, name='reserver_offre'),
  
    path('forgot_password_email_validation',views.forgot_password_email_validation , name="forgot_password_email_validation"),
    path('forgot_password',views.forgot_password,name="forgot_password"),
    path('forgot_password_update',views.forgot_password_update,name="forgot_password_update"),
    path('forgot_password_veri',views.forgot_password_veri,name="forgot_password_veri")
]
