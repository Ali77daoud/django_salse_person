from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import *

urlpatterns = [
    path('login/', obtain_auth_token),
    path('set-company/', SetCompanyView.as_view()),
    path('sales-person/', SalespeopleListCreateView.as_view()),
    path('sales-person/<int:pk>/', SalespeopleDetailView.as_view()),
    path('commission/add/', CreateCommissionView.as_view()),
    path('commission/', RetrieveCommissionView.as_view()),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
