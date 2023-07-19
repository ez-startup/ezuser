
from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path, include
from django.conf.urls.static import static
from oauth2_provider.views import TokenView, RevokeTokenView
from oauth2_provider.views.application import ApplicationRegistration, ApplicationDetail, ApplicationList
from oauth2_provider.views.introspect import IntrospectTokenView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("usermanager.urls")), # User Manager URL
    path('', include('productmanager.urls')), # Product Manager URL
    path("__reload__/", include("django_browser_reload.urls")),
    path('api/v1/', include('rest_framework.urls')),
    # path('auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('auth/token/', TokenView.as_view(), name='token'),  # Custom token endpoint URL
    path('auth/revoke_token/', RevokeTokenView.as_view(), name='revoke-token'),  # Custom token revocation URL
    path('auth/applications/register/', ApplicationRegistration.as_view(template_name='/oauth2_provider/register_application.html'), name='register'), # Register application route
    path('auth/applications/<int:pk>/', ApplicationDetail.as_view(template_name='./oauth2_provider/application.html'), name='application_detail'), # Auth Application Detail
    path('auth/applications/', ApplicationList.as_view(), name='oauth2_provider_application_list'), # Auth Application List
    path('auth/introspect/', IntrospectTokenView.as_view(), name='introspect'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Localization URL patterns
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)