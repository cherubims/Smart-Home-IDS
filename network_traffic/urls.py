from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path('admin-credentials/', views.admin_credentials, name='admin-credentials'),
    path('api/traffic', NetworkTrafficListView.as_view(), name='traffic-list'),
    path('api/traffic/<int:pk>/', NetworkTrafficDetailView.as_view(), name='traffic-detail'),
    path('api/traffic/create/', NetworkTrafficCreateView.as_view(), name='traffic-create'),
    path('api/traffic/update/<int:pk>/', NetworkTrafficUpdateView.as_view(), name='traffic-update'),
    path('api/traffic/delete/<int:pk>/', NetworkTrafficDeleteView.as_view(), name='traffic-delete'),
    path('api/traffic/anomalous/', AnomalousTrafficView.as_view(), name='anomalous-traffic'),
    path('api/traffic/filter/service/<str:service>/', NetworkTrafficFilterByServiceView.as_view(), name='traffic-filter-service'),
    path('api/traffic/filter/attack/', NetworkTrafficFilterByAttackView.as_view(), name='traffic-filter-attack'),
    path('traffic/complex-filters/', NetworkTrafficComplexFiltersView.as_view(), name='traffic-complex-filters'),

]