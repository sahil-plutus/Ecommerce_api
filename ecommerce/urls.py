from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('product.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('carts.urls')),
]

