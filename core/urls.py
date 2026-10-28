from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from home import views as home_views
from vege import views as vege_views

urlpatterns = [
    path('', home_views.home, name='home'),
    path('about/', home_views.about, name='about'),
    path('contact/', home_views.contact, name='contact'),
    path('livingroom/', home_views.livingroom, name='livingroom'),
    path('send-email/', home_views.send_email_view, name='send_email'),

    path('receipes/', vege_views.receipes, name='receipes'),
    path('update_receipe/<int:id>/', vege_views.update_receipe, name='update_receipe'),
    path('delete_receipe/<int:id>/', vege_views.delete_receipe, name='delete_receipe'),
    path('login/', vege_views.login_page, name='login_page'),
    path('logout/', vege_views.logout_page, name='logout_page'),
    path('register/', vege_views.register, name='register'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)