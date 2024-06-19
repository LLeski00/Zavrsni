from django.urls import path
from .views import StudentView, CreateStudentView, GetStudent, ExtractStudentInfo
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('student', StudentView.as_view()),
    path('create-student', CreateStudentView.as_view()),
    path('get-student', GetStudent.as_view()),
    path('extract', ExtractStudentInfo.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html', 'pdf'])