from django.urls import path
from .views import StudentView, CreateStudentView, GetStudent, ExtractStudentInfo, GetData, DeletePdfFile, GetMajorData, GetTrasferData
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('student', StudentView.as_view()),
    path('create-student', CreateStudentView.as_view()),
    path('get-student', GetStudent.as_view()),
    path('extract', ExtractStudentInfo.as_view()),
    path('get-data', GetData.as_view()),
    path('get-major-data', GetMajorData.as_view()),
    path('delete-pdf-file', DeletePdfFile.as_view()),
    path('get-transfer-data', GetTrasferData.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html', 'pdf'])