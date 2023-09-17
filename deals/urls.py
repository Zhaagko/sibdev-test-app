from django.urls import path

from .views import DealViewSet

urlpatterns = [
    path("", DealViewSet.as_view(actions={"post": "create", "get": "list"})),
]
