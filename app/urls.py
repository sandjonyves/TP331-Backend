from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, ClasseViewSet, SchoolViewSet, StudentViewSet

router = DefaultRouter()
router.register(r'schools', SchoolViewSet)
router.register(r'classes', ClasseViewSet)
router.register(r'students', StudentViewSet)
router.register(r'Carts',CartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
