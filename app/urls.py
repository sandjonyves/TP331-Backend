from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  CustomStudentView, CardViewSet, ClasseViewSet, SchoolViewSet, StudentViewSet,RenderPDFView,CardPrototypeView
# from django.confurls import url
# from wkhtmltopdf.views import PDFTemplateView




router = DefaultRouter()
router.register(r'schools', SchoolViewSet)
router.register(r'classes', ClasseViewSet)
router.register(r'students', StudentViewSet)
router.register(r'cards',CardViewSet)
router.register(r'prototype',CardPrototypeView)
# router.register(r'pdf',RenderPDFView,basename='test')

urlpatterns = [
    path('students/registers/',CustomStudentView.as_view(),name='students_register'),
    path('', include(router.urls)),
    path('pdf/', RenderPDFView.as_view(), name='render-pdf'),
    
    #  path('pdf/', RenderPDFView.as_view(), name='pdf'),
                                  

    # path('test/',render_pdf_view,name='render-pdf')
    
    
]
