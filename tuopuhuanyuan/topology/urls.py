from django.urls import path
from . import views

app_name = 'topology'

urlpatterns = [
    path("api/topology/", views.net_topology_api, name="net_topology_api")# API endpoints
] 