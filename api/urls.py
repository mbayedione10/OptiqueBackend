from django.urls import path
from django.conf.urls  import url, include
from . import views
from django.conf import settings
#voir signets
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView,
)
from rest_framework.authtoken import views as vw
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token, verify_jwt_token
from django.conf.urls.static import static


urlpatterns = [
    url(r'^home', views.index, name = 'home'),

    url(r'^signup/$', views.RegistrationAPIView.as_view(), name='signup'),

    url(r'^api-token-auth/', obtain_jwt_token),

    url(r'^login', views.login, name = 'login'),

    path('logout/', LogoutView.as_view(), name="logout"),

    path('password_change/', PasswordChangeView.as_view( success_url='accounts/password_change/done/'), name="password_change"),

    path('password_change/done/', PasswordChangeDoneView.as_view(), name="password_change_done"),

    path('password_reset/', PasswordResetView.as_view(success_url='done/'), name="password_reset"),

    path('password_reset/done/', PasswordResetDoneView.as_view(), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view( success_url='/accounts/reset/done/'), name="password_reset_confirm"),

    path('reset/done/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    url(r'^client/$', views.ClientCreateView.as_view(), name='client'),

    url(r'^clientupdate/(?P<pk>[0-9]+)/$', views.ClientUpdateView.as_view()),

    url(r'^clientdelete/(?P<pk>[0-9]+)/$', views.ClientDeleteView.as_view()),

    url(r'^clientByCommande/(?P<pk>[0-9]+)/$',views.ClientByCommandeView.as_view()),

    url(r'^commande/$', views.CommandeCreateView.as_view(), name='commande'),

    url(r'^commandeupdate/(?P<pk>[0-9]+)/$', views.CommandeUpdateView.as_view()),

    url(r'^commandedelete/(?P<pk>[0-9]+)/$', views.CommandeDeleteView.as_view()),

    url(r'^commandeById/(?P<pk>[0-9]+)/$',views.CommandeByIdView.as_view()),

    url(r'^lunette/$', views.LunetteCreateView.as_view(), name='lunette'),

    url(r'^lunetteupdate/(?P<pk>[0-9]+)/$', views.LunetteUpdateView.as_view()),

    url(r'^lunettedelete/(?P<pk>[0-9]+)/$', views.LunetteDeleteView.as_view()),

    url(r'^lunetteById/(?P<pk>[0-9]+)/$',views.LunetteByIdView.as_view()),

    url(r'^lunetteByCommande/(?P<pk>[0-9]+)/$',views.LunetteByCommandeView.as_view()),

    url(r'^clientById/(?P<pk>[0-9]+)/$',views.ClientByIdView.as_view()),

    url(r'^userByCommande/(?P<pk>[0-9]+)/$',views.UserByCommandeView.as_view()),



]
