from django.urls import include, path
from .geoip import GeoIPView
from . import views
from django.conf import settings

# Oauth2
import oauth2_provider.views as oauth2_views
from .views import ApiEndpoint

# OAuth2 provider endpoints
oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        path('application/', oauth2_views.ApplicationList.as_view(), name="list"),
        path('application/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('application/<pk>/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        path('application/<pk>/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('application/<pk>/update/', oauth2_views.ApplicationUpdate.as_view(), name="update")
    ]
    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        path('authorized-tokens/<pk>/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(), name="authorized-token-delete"),
    ]
    

urlpatterns = [
    path("", views.index, name="home" ),
    path("geoip/", GeoIPView, name="IPInfoView"),
    path('auth/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace="oauth2_provider")),
    path('api/hello', ApiEndpoint.as_view()),  # an example resource endpoint
    path('secret', views.secret_page, name='secret'),
    path("account/login/", views.UserLogin, name="login"),
]
