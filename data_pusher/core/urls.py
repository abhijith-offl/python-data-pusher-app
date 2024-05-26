from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, DestinationViewSet, DataHandlerViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'destinations', DestinationViewSet)
router.register(r'data_handler', DataHandlerViewSet, basename='data_handler')

urlpatterns = [
    path('', include(router.urls)),
]
