from django.contrib import admin
from django.urls import path, include
from wishes.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wishes.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
]