from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomStudentView, CartViewSet, ClasseViewSet, SchoolViewSet, StudentViewSet

router = DefaultRouter()
router.register(r'schools', SchoolViewSet)
router.register(r'classes', ClasseViewSet)
router.register(r'students', StudentViewSet)
router.register(r'carts',CartViewSet)

urlpatterns = [
    path('students/registers/',CustomStudentView.as_view(),name='students_register'),
    path('', include(router.urls)),
    
]
