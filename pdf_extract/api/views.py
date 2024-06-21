from django.shortcuts import render
from rest_framework import generics, status
from .serializers import StudentSerializer, CreateStudentSerializer
from .models import Student
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import UploadFileForm
from django.http import HttpResponse
import csv
import fitz  # PyMuPDF, imported as fitz for backward compatibility reasons
import cv2
import pytesseract
import os
import re
from django.core.files.storage import FileSystemStorage
from django.utils import decorators
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

class StudentView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class GetStudent(APIView):

    def get(self,request, format=None):
        majors = "kumpr"

        return Response(majors, status=status.HTTP_200_OK)
    
class GetData(APIView):

    def get(self,request, format=None):
        majors = [
		{ "id": 110, "name": "SVEUČILIŠNI - ELEKTROTEHNIKA I INFORMACIJSKA TEHNOLOGIJA" },
		{ "id": 111, "name": "SVEUČILIŠNI - AUTOMATIKA I SUSTAVI" },
		{ "id": 112, "name": "SVEUČILIŠNI - ELEKTRONIKA I RAČUNALNO INŽENJERSTVO" },
		{ "id": 113, "name": "SVEUČILIŠNI - ELEKTROTEHNIKA" },
		{ "id": 114, "name": "SVEUČILIŠNI - KOMUNIKACIJSKA I INFORMACIJSKA TEHNOLOGIJA" },
		{ "id": 120, "name": "SVEUČILIŠNI - RAČUNARSTVO" },
		{ "id": 510, "name": "STRUČNI - ELEKTROTEHNIKA" },
		{ "id": 511, "name": "STRUČNI - ELEKTROENERGETIKA" },
		{ "id": 512, "name": "STRUČNI - ELEKTRONIKA" },
		{ "id": 550, "name": "STRUČNI - RAČUNARSTVO" }
	    ]
        return Response(majors, status=status.HTTP_200_OK)
    
class GetMajorData(APIView):

    def post(self,request, format=None):

        match request.body.decode('utf-8'):
            case "110":
                subjects = {"1": [
                    { "id": 1, "name": "Matematika 1", "isElective": False, "ects": 7 },
                    { "id": 2, "name": "Osnove elektrotehnike 1", "isElective": False, "ects": 7 },
                    { "id": 3, "name": "Računala i programiranje", "isElective": False, "ects": 6 },
                    { "id": 4, "name": "Inženjerska grafika i prezentacija", "isElective": False, "ects": 4 },
                    { "id": 5, "name": "Komunikacijske vještine", "isElective": False, "ects": 3 },
                    { "id": 6, "name": "Engleski jezik 1", "isElective": False, "ects": 3 }
                ],
                "2": [
                    { "id": 7, "name": "Matematika 2", "isElective": False, "ects": 7 },
                    { "id": 8, "name": "Fizika 1", "isElective": False, "ects": 7 },
                    { "id": 9, "name": "Osnove elektrotehnike 2", "isElective": False, "ects": 6 },
                    { "id": 10, "name": "Digitalna elektronika", "isElective": False, "ects": 6 },
                    { "id": 11, "name": "Engleski jezik 2", "isElective": False, "ects": 4 }
                ],
                "3": [
                    { "id": 12, "name": "Matematika 3", "isElective": False, "ects": 5 },
                    { "id": 13, "name": "Fizika 2", "isElective": False, "ects": 7 },
                    { "id": 14, "name": "Elektronički elementi i sklopovi", "isElective": False, "ects": 6 },
                    { "id": 15, "name": "Električna mjerenja", "isElective": False, "ects": 6 },
                    { "id": 16, "name": "Ekonomika i organizacija proizvodnje", "isElective": False, "ects": 3 },
                    { "id": 17, "name": "Engleski jezik 3", "isElective": False, "ects": 3 }
                ],
                "4": [
                    { "id": 18, "name": "Vjerojatnost i statistika", "isElective": False, "ects": 5 },
                    { "id": 19, "name": "Programiranje", "isElective": False, "ects": 6 },
                    { "id": 20, "name": "Teorija sustava", "isElective": False, "ects": 5 },
                    { "id": 21, "name": "Informacije i komunikacije", "isElective": False, "ects": 5 },
                    { "id": 22, "name": "Osnove elektroenergetike", "isElective": False, "ects": 5 },
                    { "id": 23, "name": "Elektrotehnički materijali i tehnologije", "isElective": False, "ects": 4 }]}
                return Response(subjects, status=status.HTTP_200_OK)
            case "111": 
                subjects={
                "1": [
                    { "id": 1, "name": "Matematika 1", "isElective": False, "ects": 7 },
                    { "id": 2, "name": "Osnove elektrotehnike 1", "isElective": False, "ects": 7 },
                    { "id": 3, "name": "Računala i programiranje", "isElective": False, "ects": 6 },
                    { "id": 4, "name": "Inženjerska grafika i prezentacija", "isElective": False, "ects": 4 },
                    { "id": 5, "name": "Komunikacijske vještine", "isElective": False, "ects": 3 },
                    { "id": 6, "name": "Engleski jezik 1", "isElective": False, "ects": 3 }
                ],
                "2": [
                    { "id": 7, "name": "Matematika 2", "isElective": False, "ects": 7 },
                    { "id": 8, "name": "Fizika 1", "isElective": False, "ects": 7 },
                    { "id": 9, "name": "Osnove elektrotehnike 2", "isElective": False, "ects": 6 },
                    { "id": 10, "name": "Digitalna elektronika", "isElective": False, "ects": 6 },
                    { "id": 11, "name": "Engleski jezik 2", "isElective": False, "ects": 4 }
                ],
                "3": [
                    { "id": 12, "name": "Matematika 3", "isElective": False, "ects": 5 },
                    { "id": 13, "name": "Fizika 2", "isElective": False, "ects": 7 },
                    { "id": 14, "name": "Elektronički elementi i sklopovi", "isElective": False, "ects": 6 },
                    { "id": 15, "name": "Električna mjerenja", "isElective": False, "ects": 6 },
                    { "id": 16, "name": "Ekonomika i organizacija proizvodnje", "isElective": False, "ects": 3 },
                    { "id": 17, "name": "Engleski jezik 3", "isElective": False, "ects": 3 }
                ],
                "4": [
                    { "id": 18, "name": "Vjerojatnost i statistika", "isElective": False, "ects": 5 },
                    { "id": 19, "name": "Programiranje", "isElective": False, "ects": 6 },
                    { "id": 20, "name": "Teorija sustava", "isElective": False, "ects": 5 },
                    { "id": 21, "name": "Informacije i komunikacije", "isElective": False, "ects": 5 },
                    { "id": 22, "name": "Osnove elektroenergetike", "isElective": False, "ects": 5 },
                    { "id": 23, "name": "Elektrotehnički materijali i tehnologije", "isElective": False, "ects": 4 }
                ],
                "5": [
                    { "id": 24, "name": "Automatska regulacija 1", "isElective": False, "ects": 5 },
                    { "id": 25, "name": "Elektronički sklopovi", "isElective": False, "ects": 5 },
                    { "id": 26, "name": "Analiza mreža", "isElective": False, "ects": 5 },
                    { "id": 27, "name": "Simulacijsko modeliranje", "isElective": False, "ects": 5 },
                    { "id": 28, "name": "Objektno orijentirano programiranje", "isElective": False, "ects": 5 },
                    { "id": 29, "name": "Programiranje za Internet", "isElective": True, "ects": 5 },
                    { "id": 30, "name": "Numeričke metode u elektronici", "isElective": True, "ects": 5 },
                    { "id": 31, "name": "Računarske metode u biomehanici", "isElective": True, "ects": 5 },
                    { "id": 32, "name": "Arhitektura računala", "isElective": True, "ects": 5 },
                    { "id": 33, "name": "Tehnička mehanika", "isElective": True, "ects": 5 },
                    { "id": 34, "name": "Sigurnost računala i sustava", "isElective": True, "ects": 5 },
                    { "id": 35, "name": "Komunikacijski sustavi i protokoli", "isElective": True, "ects": 5 }
                ],
                "6": [
                    { "id": 36, "name": "Impulsni i digitalni sklopovi", "isElective": False, "ects": 4 },
                    { "id": 37, "name": "Automatska regulacija 2", "isElective": False, "ects": 5 },
                    { "id": 38, "name": "Digitalna instrumentacija 1", "isElective": False, "ects": 5 },
                    { "id": 39, "name": "Završni rad", "isElective": False, "ects": 12 },
                    { "id": 41, "name": "Mjerni pretvornici i izvršne sprave", "isElective": True, "ects": 4 },
                    { "id": 42, "name": "Elementi automatizacije industrijskih procesa", "isElective": True, "ects": 5 },
                    { "id": 43, "name": "Digitalna obradba signala", "isElective": True, "ects": 5 },
                    { "id": 44, "name": "Bežične senzorske mreže", "isElective": True, "ects": 5 },
                    { "id": 45, "name": "Baze podataka", "isElective": True, "ects": 5 },
                    { "id": 46, "name": "Stručna praksa", "isElective": True, "ects": 5 }
                ]
                }
                return Response(subjects, status=status.HTTP_200_OK)
            case "112":
                subjects={
                "1": [
                    { "id": 1, "name": "Matematika 1", "isElective": False, "ects": 7 },
                    { "id": 2, "name": "Osnove elektrotehnike 1", "isElective": False, "ects": 7 },
                    { "id": 3, "name": "Računala i programiranje", "isElective": False, "ects": 6 },
                    { "id": 4, "name": "Inženjerska grafika i prezentacija", "isElective": False, "ects": 4 },
                    { "id": 5, "name": "Komunikacijske vještine", "isElective": False, "ects": 3 },
                    { "id": 6, "name": "Engleski jezik 1", "isElective": False, "ects": 3 }
                ],
                "2": [
                    { "id": 7, "name": "Matematika 2", "isElective": False, "ects": 7 },
                    { "id": 8, "name": "Fizika 1", "isElective": False, "ects": 7 },
                    { "id": 9, "name": "Osnove elektrotehnike 2", "isElective": False, "ects": 6 },
                    { "id": 10, "name": "Digitalna elektronika", "isElective": False, "ects": 6 },
                    { "id": 11, "name": "Engleski jezik 2", "isElective": False, "ects": 4 }
                ],
                "3": [
                    { "id": 12, "name": "Matematika 3", "isElective": False, "ects": 5 },
                    { "id": 13, "name": "Fizika 2", "isElective": False, "ects": 7 },
                    { "id": 14, "name": "Elektronički elementi i sklopovi", "isElective": False, "ects": 6 },
                    { "id": 15, "name": "Električna mjerenja", "isElective": False, "ects": 6 },
                    { "id": 16, "name": "Ekonomika i organizacija proizvodnje", "isElective": False, "ects": 3 },
                    { "id": 17, "name": "Engleski jezik 3", "isElective": False, "ects": 3 }
                ],
                "4": [
                    { "id": 18, "name": "Vjerojatnost i statistika", "isElective": False, "ects": 5 },
                    { "id": 19, "name": "Programiranje", "isElective": False, "ects": 6 },
                    { "id": 20, "name": "Teorija sustava", "isElective": False, "ects": 5 },
                    { "id": 21, "name": "Informacije i komunikacije", "isElective": False, "ects": 5 },
                    { "id": 22, "name": "Osnove elektroenergetike", "isElective": False, "ects": 5 },
                    { "id": 23, "name": "Elektrotehnički materijali i tehnologije", "isElective": False, "ects": 4 }
                ],
                "5": [
                    { "id": 47, "name": "Računalne mreže", "isElective": False, "ects": 5 },
                    { "id": 48, "name": "Elektronički sklopovi", "isElective": False, "ects": 5 },
                    { "id": 49, "name": "Analiza mreža", "isElective": False, "ects": 5 },
                    { "id": 50, "name": "Arhitektura računala", "isElective": False, "ects": 5 },
                    { "id": 51, "name": "Objektno orijentirano programiranje", "isElective": False, "ects": 5 },
                    { "id": 52, "name": "Simulacijsko modeliranje", "isElective": True, "ects": 5 },
                    { "id": 53, "name": "Programiranje za Internet", "isElective": True, "ects": 5 },
                    { "id": 54, "name": "Komunikacijski sustavi i protokoli", "isElective": True, "ects": 5 },
                    { "id": 55, "name": "Automatska regulacija 1", "isElective": True, "ects": 5 }
                ],
                "6": [
                    { "id": 56, "name": "Impulsni i digitalni sklopovi", "isElective": False, "ects": 4 },
                    { "id": 57, "name": "Operacijski sustavi", "isElective": False, "ects": 5 },
                    { "id": 58, "name": "Digitalna instrumentacija 1", "isElective": False, "ects": 5 },
                    { "id": 59, "name": "Završni rad", "isElective": False, "ects": 12 },
                    { "id": 60, "name": "Digitalna obradba signala", "isElective": True, "ects": 5 },
                    { "id": 61, "name": "Baze podataka", "isElective": True, "ects": 5 },
                    { "id": 62, "name": "Dijagnostičke metode u vozilima", "isElective": True, "ects": 5 },
                    { "id": 63, "name": "Stručna praksa", "isElective": True, "ects": 5 }
                ]
                }
                return Response(subjects, status=status.HTTP_200_OK)
            case "113":
                subjects = {
                "1": [
                    { "id": 1, "name": "Matematika 1", "isElective": False, "ects": 7 },
                    { "id": 2, "name": "Osnove elektrotehnike 1", "isElective": False, "ects": 7 },
                    { "id": 3, "name": "Računala i programiranje", "isElective": False, "ects": 6 },
                    { "id": 4, "name": "Inženjerska grafika i prezentacija", "isElective": False, "ects": 4 },
                    { "id": 5, "name": "Komunikacijske vještine", "isElective": False, "ects": 3 },
                    { "id": 6, "name": "Engleski jezik 1", "isElective": False, "ects": 3 }
                ],
                "2": [
                    { "id": 7, "name": "Matematika 2", "isElective": False, "ects": 7 },
                    { "id": 8, "name": "Fizika 1", "isElective": False, "ects": 7 },
                    { "id": 9, "name": "Osnove elektrotehnike 2", "isElective": False, "ects": 6 },
                    { "id": 10, "name": "Digitalna elektronika", "isElective": False, "ects": 6 },
                    { "id": 11, "name": "Engleski jezik 2", "isElective": False, "ects": 4 }
                ],
                "3": [
                    { "id": 12, "name": "Matematika 3", "isElective": False, "ects": 5 },
                    { "id": 13, "name": "Fizika 2", "isElective": False, "ects": 7 },
                    { "id": 14, "name": "Elektronički elementi i sklopovi", "isElective": False, "ects": 6 },
                    { "id": 15, "name": "Električna mjerenja", "isElective": False, "ects": 6 },
                    { "id": 16, "name": "Ekonomika i organizacija proizvodnje", "isElective": False, "ects": 3 },
                    { "id": 17, "name": "Engleski jezik 3", "isElective": False, "ects": 3 }
                ],
                "4": [
                    { "id": 18, "name": "Vjerojatnost i statistika", "isElective": False, "ects": 5 },
                    { "id": 19, "name": "Programiranje", "isElective": False, "ects": 6 },
                    { "id": 20, "name": "Teorija sustava", "isElective": False, "ects": 5 },
                    { "id": 21, "name": "Informacije i komunikacije", "isElective": False, "ects": 5 },
                    { "id": 22, "name": "Osnove elektroenergetike", "isElective": False, "ects": 5 },
                    { "id": 23, "name": "Elektrotehnički materijali i tehnologije", "isElective": False, "ects": 4 }
                ],
                "5": [
                    { "id": 64, "name": "Električne mreže", "isElective": False, "ects": 6 },
                    { "id": 65, "name": "Električni strojevi", "isElective": False, "ects": 7 },
                    { "id": 66, "name": "Elementi električnih postrojenja", "isElective": False, "ects": 6 },
                    { "id": 67, "name": "Energetska elektronika", "isElective": False, "ects": 6 },
                    { "id": 68, "name": "Regulacijska tehnika", "isElective": False, "ects": 5 }
                ],
                "6": [
                    { "id": 69, "name": "Elektromotorni pogoni", "isElective": False, "ects": 5 },
                    { "id": 70, "name": "Elementi automatizacije industrijskih procesa", "isElective": False, "ects": 5 },
                    { "id": 71, "name": "Završni rad", "isElective": False, "ects": 12 },
                    { "id": 72, "name": "Električne instalacije i rasvjeta", "isElective": True, "ects": 4 },
                    { "id": 73, "name": "Elektrotehnička sigurnost", "isElective": True, "ects": 4 },
                    { "id": 74, "name": "Distribucija električne energije", "isElective": True, "ects": 4 },
                    { "id": 75, "name": "Upravljanje sustavima energetske elektronike", "isElective": True, "ects": 4 },
                    { "id": 76, "name": "Elektronički pretvarači za napajanje", "isElective": True, "ects": 4 },
                    { "id": 77, "name": "Održavanje i ispitivanje električne opreme", "isElective": True, "ects": 4 },
                    { "id": 78, "name": "Brodska elektrotehnika", "isElective": True, "ects": 4 },
                    { "id": 79, "name": "Instrumentacija i ispitivanje radnog okoliša", "isElective": True, "ects": 4 },
                    { "id": 80, "name": "Instrumentacija za napredne elektroenergetske mreže", "isElective": True, "ects": 4 },
                    { "id": 81, "name": "Dijagnostičke metode u vozilima", "isElective": True, "ects": 5 },
                    { "id": 82, "name": "Stručna praksa", "isElective": True, "ects": 5 }
                ]
                }
                return Response(subjects, status=status.HTTP_200_OK)
            case "114":
                subjects={
                "1": [
                    { "id": 1, "name": "Matematika 1", "isElective": False, "ects": 7 },
                    { "id": 2, "name": "Osnove elektrotehnike 1", "isElective": False, "ects": 7 },
                    { "id": 3, "name": "Računala i programiranje", "isElective": False, "ects": 6 },
                    { "id": 4, "name": "Inženjerska grafika i prezentacija", "isElective": False, "ects": 4 },
                    { "id": 5, "name": "Komunikacijske vještine", "isElective": False, "ects": 3 },
                    { "id": 6, "name": "Engleski jezik 1", "isElective": False, "ects": 3 }
                ],
                "2": [
                    { "id": 7, "name": "Matematika 2", "isElective": False, "ects": 7 },
                    { "id": 8, "name": "Fizika 1", "isElective": False, "ects": 7 },
                    { "id": 9, "name": "Osnove elektrotehnike 2", "isElective": False, "ects": 6 },
                    { "id": 10, "name": "Digitalna elektronika", "isElective": False, "ects": 6 },
                    { "id": 11, "name": "Engleski jezik 2", "isElective": False, "ects": 4 }
                ],
                "3": [
                    { "id": 12, "name": "Matematika 3", "isElective": False, "ects": 5 },
                    { "id": 13, "name": "Fizika 2", "isElective": False, "ects": 7 },
                    { "id": 14, "name": "Elektronički elementi i sklopovi", "isElective": False, "ects": 6 },
                    { "id": 15, "name": "Električna mjerenja", "isElective": False, "ects": 6 },
                    { "id": 16, "name": "Ekonomika i organizacija proizvodnje", "isElective": False, "ects": 3 },
                    { "id": 17, "name": "Engleski jezik 3", "isElective": False, "ects": 3 }
                ],
                "4": [
                    { "id": 18, "name": "Vjerojatnost i statistika", "isElective": False, "ects": 5 },
                    { "id": 19, "name": "Programiranje", "isElective": False, "ects": 6 },
                    { "id": 20, "name": "Teorija sustava", "isElective": False, "ects": 5 },
                    { "id": 21, "name": "Informacije i komunikacije", "isElective": False, "ects": 5 },
                    { "id": 22, "name": "Osnove elektroenergetike", "isElective": False, "ects": 5 },
                    { "id": 23, "name": "Elektrotehnički materijali i tehnologije", "isElective": False, "ects": 4 }
                ],
                "5": [
                    { "id": 83, "name": "Teorija informacija", "isElective": False, "ects": 5 },
                    { "id": 84, "name": "Komunikacijski sustavi i protokoli", "isElective": False, "ects": 5 },
                    { "id": 85, "name": "Objektno orijentirano programiranje", "isElective": False, "ects": 5 },
                    { "id": 86, "name": "Arhitektura računala", "isElective": False, "ects": 5 },
                    { "id": 87, "name": "Analiza mreža", "isElective": False, "ects": 5 },
                    { "id": 88, "name": "Sigurnost računala i sustava", "isElective": True, "ects": 5 },
                    { "id": 89, "name": "Programiranje za Internet", "isElective": True, "ects": 5 },
                    { "id": 90, "name": "Poluvodički elektronički elementi", "isElective": True, "ects": 5 },
                    { "id": 91, "name": "Numeričke metode u elektronici", "isElective": True, "ects": 5 },
                    { "id": 92, "name": "Elektronički sklopovi", "isElective": True, "ects": 5 },
                    { "id": 93, "name": "Simulacijsko modeliranje", "isElective": True, "ects": 5 },
                    { "id": 94, "name": "Automatska regulacija 1", "isElective": True, "ects": 5 }
                ],
                "6": [
                    { "id": 95, "name": "Elektromagnetska polja", "isElective": False, "ects": 5 },
                    { "id": 96, "name": "Digitalna obradba signala", "isElective": False, "ects": 5 },
                    { "id": 97, "name": "Impulsni i digitalni sklopovi", "isElective": False, "ects": 4 },
                    { "id": 98, "name": "Završni rad", "isElective": False, "ects": 12 },
                    { "id": 99, "name": "Bežične senzorske mreže", "isElective": True, "ects": 5 },
                    { "id": 100, "name": "Baze podataka", "isElective": True, "ects": 5 },
                    { "id": 101, "name": "Uvod u bežične komunikacije", "isElective": True, "ects": 5 },
                    { "id": 102, "name": "Analiza mreža i linija primjenom računala", "isElective": True, "ects": 5 },
                    { "id": 103, "name": "Stručna praksa", "isElective": True, "ects": 5 }
                ]
                }
                return Response(subjects, status=status.HTTP_200_OK)
            case "120":
                subjects = {
                "1": [
                    { "id": 104, "name": "Matematika 1", "isElective": False, "ects": 7 },
                    { "id": 105, "name": "Fizika 1", "isElective": False, "ects": 7 },
                    { "id": 106, "name": "Elektrotehnika", "isElective": False, "ects": 7 },
                    { "id": 107, "name": "Uvod u računala i programiranje", "isElective": False, "ects": 7 },
                    { "id": 108, "name": "Engleski jezik 1", "isElective": False, "ects": 2 }
                ],
                "2": [
                    { "id": 109, "name": "Matematika 2", "isElective": False, "ects": 7 },
                    { "id": 110, "name": "Fizika 2", "isElective": False, "ects": 7 },
                    { "id": 111, "name": "Elektronika", "isElective": False, "ects": 7 },
                    { "id": 112, "name": "Programiranje", "isElective": False, "ects": 7 },
                    { "id": 113, "name": "Engleski jezik 2", "isElective": False, "ects": 2 }
                ],
                "3": [
                    { "id": 114, "name": "Diskretna matematika", "isElective": False, "ects": 6 },
                    { "id": 115, "name": "Diskretni sustavi i strukture", "isElective": False, "ects": 7 },
                    { "id": 116, "name": "Objektno orijentirano programiranje", "isElective": False, "ects": 7 },
                    { "id": 117, "name": "Strukture podataka", "isElective": False, "ects": 6 },
                    { "id": 118, "name": "Praktikum", "isElective": False, "ects": 2 },
                    { "id": 119, "name": "Komunikacijske vještine", "isElective": False, "ects": 2 }
                ],
                "4": [
                    { "id": 120, "name": "Vjerojatnost i statistika", "isElective": False, "ects": 5 },
                    { "id": 121, "name": "Arhitektura digitalnih računala", "isElective": False, "ects": 7 },
                    { "id": 122, "name": "Algoritmi", "isElective": False, "ects": 7 },
                    { "id": 123, "name": "Baze podataka", "isElective": False, "ects": 6 },
                    { "id": 124, "name": "Signali i sustavi", "isElective": False, "ects": 5 }
                ],
                "5": [
                    { "id": 125, "name": "Operacijski sustavi", "isElective": False, "ects": 7 },
                    { "id": 126, "name": "Računalne mreže", "isElective": False, "ects": 6 },
                    { "id": 127, "name": "Programsko inženjerstvo", "isElective": False, "ects": 7 },
                    { "id": 128, "name": "Programiranje za Internet", "isElective": False, "ects": 6 },
                    { "id": 129, "name": "Programiranje za Unix", "isElective": True, "ects": 4 },
                    { "id": 130, "name": "Sigurnost računala i podataka", "isElective": True, "ects": 4 },
                    { "id": 131, "name": "Programiranje za Android", "isElective": True, "ects": 4 },
                    { "id": 132, "name": "Programiranje u Pythonu", "isElective": True, "ects": 4 }
                ],
                "6": [
                    { "id": 133, "name": "Projektiranje informacijskih sustava", "isElective": False, "ects": 5 },
                    { "id": 134, "name": "Uvod u distribuirane informacijske sustave", "isElective": False, "ects": 5 },
                    { "id": 135, "name": "Poslovna informatika", "isElective": False, "ects": 4 },
                    { "id": 136, "name": "Završni rad", "isElective": False, "ects": 12 },
                    { "id": 137, "name": "Programiranje za Windows", "isElective": True, "ects": 4 },
                    { "id": 138, "name": "Komunikacijski protokoli i arhitekture", "isElective": True, "ects": 4 },
                    { "id": 139, "name": "Osnove ugradbenih računalnih sustava", "isElective": True, "ects": 4 },
                    { "id": 140, "name": "Obrada signala", "isElective": True, "ects": 4 },
                    { "id": 141, "name": "Inženjerska ekonomika", "isElective": True, "ects": 4 },
                    { "id": 142, "name": "Stručna praksa", "isElective": True, "ects": 5 }
                ]
                }
                return Response(subjects, status=status.HTTP_200_OK)
            case "510":
                subjects = {
                "1": [
                    { "id": 143, "name": "Matematika", "isElective": False, "ects": 7 },
                    { "id": 144, "name": "Fizika", "isElective": False, "ects": 6 },
                    { "id": 145, "name": "Informatika", "isElective": False, "ects": 5 },
                    { "id": 146, "name": "Osnove elektrotehnike 1", "isElective": False, "ects": 7 },
                    {
                        "id": 147,
                        "name": "Elektrotehnički materijali i tehnologije",
                        "isElective": False,
                        "ects": 4
                    },
                    { "id": 148, "name": "Engleski jezik 1", "isElective": False, "ects": 2 }
                ],
                "2": [
                    { "id": 149, "name": "Primijenjena matematika", "isElective": False, "ects": 5 },
                    { "id": 150, "name": "Uvod u programiranje", "isElective": False, "ects": 5 },
                    { "id": 151, "name": "Osnove elektrotehnike 2", "isElective": False, "ects": 6 },
                    { "id": 152, "name": "Elektronički elementi", "isElective": False, "ects": 6 },
                    { "id": 153, "name": "Električna mjerenja", "isElective": False, "ects": 5 },
                    { "id": 154, "name": "Engleski jezik 2", "isElective": False, "ects": 3 }
                ]
                }
                return Response(subjects, status=status.HTTP_200_OK)
            case "511":
                subjects = {
                "1": [
                    { "id": 143, "name": "Matematika", "isElective": False, "ects": 7 },
                    { "id": 144, "name": "Fizika", "isElective": False, "ects": 6 },
                    { "id": 145, "name": "Informatika", "isElective": False, "ects": 5 },
                    { "id": 146, "name": "Osnove elektrotehnike 1", "isElective": False, "ects": 7 },
                    { "id": 147, "name": "Elektrotehnički materijali i tehnologije", "isElective": False, "ects": 4 },
                    { "id": 148, "name": "Engleski jezik 1", "isElective": False, "ects": 2 }
                ],
                "2": [
                    { "id": 149, "name": "Primijenjena matematika", "isElective": False, "ects": 5 },
                    { "id": 150, "name": "Uvod u programiranje", "isElective": False, "ects": 5 },
                    { "id": 151, "name": "Osnove elektrotehnike 2", "isElective": False, "ects": 6 },
                    { "id": 152, "name": "Elektronički elementi", "isElective": False, "ects": 6 },
                    { "id": 153, "name": "Električna mjerenja", "isElective": False, "ects": 5 },
                    { "id": 154, "name": "Engleski jezik 2", "isElective": False, "ects": 3 }
                ],
                "3": [
                    { "id": 155, "name": "Električni strojevi i transformatori", "isElective": False, "ects": 8 },
                    { "id": 156, "name": "Električne mreže", "isElective": False, "ects": 5 },
                    { "id": 157, "name": "Električna postrojenja", "isElective": False, "ects": 6 },
                    { "id": 158, "name": "Energetska elektronika", "isElective": False, "ects": 6 },
                    { "id": 159, "name": "Regulacijska tehnika", "isElective": False, "ects": 5 }
                ],
                "4": [
                    { "id": 160, "name": "Elektromotorni pogoni", "isElective": False, "ects": 5 },
                    { "id": 161, "name": "Električne instalacije", "isElective": False, "ects": 5 },
                    { "id": 162, "name": "Mjerenja u elektroenergetici", "isElective": False, "ects": 5 },
                    { "id": 163, "name": "Distribucija električne energije", "isElective": False, "ects": 5 },
                    { "id": 164, "name": "Primjena procesnih računala", "isElective": False, "ects": 5 },
                    { "id": 165, "name": "Upravljanje i zaštita električnih postrojenja", "isElective": False, "ects": 5 }
                ],
                "5": [
                    { "id": 166, "name": "Elektrotehnička sigurnost", "isElective": False, "ects": 5 },
                    { "id": 167, "name": "Mjerenje procesnih veličina", "isElective": False, "ects": 5 },
                    { "id": 168, "name": "Održavanje i ispitivanje električne opreme", "isElective": False, "ects": 5 },
                    { "id": 169, "name": "Elektronički pretvarači za napajanje", "isElective": False, "ects": 5 },
                    { "id": 170, "name": "Projektiranje niskonaponskih postrojenja", "isElective": True, "ects": 5 },
                    { "id": 171, "name": "Obnovljivi izvori energije", "isElective": True, "ects": 5 },
                    { "id": 172, "name": "Brodska elektrotehnika", "isElective": True, "ects": 5 },
                    { "id": 173, "name": "Zaštita u elektroenergetskom sustavu", "isElective": True, "ects": 5 }
                ],
                "6": [
                    { "id": 174, "name": "Stručna praksa", "isElective": False, "ects": 10 },
                    { "id": 175, "name": "Završni rad", "isElective": False, "ects": 10 },
                    { "id": 176, "name": "Upravljanje elektromotornim pogonima", "isElective": True, "ects": 5 },
                    { "id": 177, "name": "Tehnika visokog napona", "isElective": True, "ects": 5 },
                    { "id": 178, "name": "Elektroenergetski sustav i okoliš", "isElective": True, "ects": 5 },
                    { "id": 179, "name": "Energetski izvori", "isElective": True, "ects": 5 },
                    { "id": 180, "name": "Instrumentacija za napredne elektroenergetske mreže", "isElective": True, "ects": 5 },
                    { "id": 181, "name": "Mikroprocesorski sustavi", "isElective": True, "ects": 5 }
                ]
                }
                return Response(subjects, status=status.HTTP_200_OK)
            case "512":
                subjects = {
                "1": [
                    { "id": 143, "name": "Matematika", "isElective": False, "ects": 7 },
                    { "id": 144, "name": "Fizika", "isElective": False, "ects": 6 },
                    { "id": 145, "name": "Informatika", "isElective": False, "ects": 5 },
                    { "id": 146, "name": "Osnove elektrotehnike 1", "isElective": False, "ects": 7 },
                    { "id": 147, "name": "Elektrotehnički materijali i tehnologije", "isElective": False, "ects": 4 },
                    { "id": 148, "name": "Engleski jezik 1", "isElective": False, "ects": 2 }
                ],
                "2": [
                    { "id": 149, "name": "Primijenjena matematika", "isElective": False, "ects": 5 },
                    { "id": 150, "name": "Uvod u programiranje", "isElective": False, "ects": 5 },
                    { "id": 151, "name": "Osnove elektrotehnike 2", "isElective": False, "ects": 6 },
                    { "id": 152, "name": "Elektronički elementi", "isElective": False, "ects": 6 },
                    { "id": 153, "name": "Električna mjerenja", "isElective": False, "ects": 5 },
                    { "id": 154, "name": "Engleski jezik 2", "isElective": False, "ects": 3 }
                ],
                "3": [
                    { "id": 182, "name": "Elektronički sklopovi", "isElective": False, "ects": 9 },
                    { "id": 183, "name": "Signali i sustavi", "isElective": False, "ects": 6 },
                    { "id": 184, "name": "Automatika", "isElective": False, "ects": 8 },
                    { "id": 185, "name": "Uvod u poduzetništvo", "isElective": False, "ects": 3 },
                    { "id": 186, "name": "Osnove optoelektronike", "isElective": False, "ects": 4 }
                ],
                "4": [
                    { "id": 187, "name": "Komunikacijski sustavi", "isElective": False, "ects": 8 },
                    { "id": 188, "name": "Digitalna tehnika", "isElective": False, "ects": 7 },
                    { "id": 189, "name": "Elektronički CAD", "isElective": False, "ects": 5 },
                    { "id": 190, "name": "Vođenje procesa", "isElective": True, "ects": 5 },
                    { "id": 191, "name": "Elementi robotike", "isElective": True, "ects": 5 },
                    { "id": 192, "name": "Računalne mreže", "isElective": True, "ects": 5 },
                    { "id": 193, "name": "Antene", "isElective": True, "ects": 5 },
                    { "id": 194, "name": "Multimedija", "isElective": True, "ects": 5 }
                ],
                "5": [
                    { "id": 195, "name": "Praktikum iz biomehanike", "isElective": True, "ects": 5 },
                    { "id": 196, "name": "Praktikum iz digitalne obrade slike", "isElective": True, "ects": 5 },
                    { "id": 197, "name": "Praktikum iz mehatronike", "isElective": True, "ects": 5 },
                    { "id": 198, "name": "Praktikum iz elektromagnetskih simulacija", "isElective": True, "ects": 5 },
                    { "id": 199, "name": "Projektiranje elektroničkih sklopova", "isElective": True, "ects": 5 },
                    { "id": 200, "name": "Elektronička instrumentacija", "isElective": True, "ects": 5 },
                    { "id": 201, "name": "Elektromagnetska kompatibilnost", "isElective": True, "ects": 5 },
                    { "id": 202, "name": "Arhitektura računala", "isElective": True, "ects": 5 },
                    { "id": 203, "name": "Modeliranje i simuliranje sustava", "isElective": True, "ects": 5 },
                    { "id": 204, "name": "Sigurnost računala i podataka", "isElective": True, "ects": 5 },
                    { "id": 205, "name": "Projektiranje i korištenje računalnih mreža", "isElective": True, "ects": 5 },
                    { "id": 206, "name": "Projektiranje regulacijskih sustava", "isElective": True, "ects": 5 },
                    { "id": 207, "name": "Radiokomunikacije", "isElective": True, "ects": 5 },
                    { "id": 208, "name": "Analiza zračećih struktura primjenom računala", "isElective": True, "ects": 5 },
                    { "id": 209, "name": "Izloženost ljudi elektromagnetskom polju", "isElective": True, "ects": 5 }
                ],
                "6": [
                    { "id": 210, "name": "Trgovačko pravo", "isElective": False, "ects": 2 },
                    { "id": 211, "name": "Stručna praksa", "isElective": False, "ects": 10 },
                    { "id": 212, "name": "Završni rad", "isElective": False, "ects": 10 },
                    { "id": 213, "name": "Programiranje za Internet", "isElective": True, "ects": 4 },
                    { "id": 214, "name": "Mjerna osjetila i mjerni pretvornici", "isElective": True, "ects": 4 },
                    { "id": 215, "name": "Mobilne komunikacijske mreže", "isElective": True, "ects": 4 },
                    { "id": 216, "name": "Optičke komunikacije", "isElective": True, "ects": 4 },
                    { "id": 217, "name": "Hidraulički i pneumatički uređaji", "isElective": True, "ects": 4 },
                    { "id": 218, "name": "Mikroregulatori i ugradivi mrežni sustavi", "isElective": True, "ects": 4 },
                    { "id": 219, "name": "Radiokomunikacije u pomorstvu", "isElective": True, "ects": 4 },
                    { "id": 220, "name": "Visokofrekvencijska elektronika", "isElective": True, "ects": 4 }
                ]
                }
                return Response(subjects, status=status.HTTP_200_OK)
            case "550":
                subjects = {
                "1": [
                    { "id": 221, "name": "Matematika", "isElective": False, "ects": 7 },
                    { "id": 222, "name": "Elektrotehnika", "isElective": False, "ects": 6 },
                    { "id": 223, "name": "Uvod u organizaciju digitalnih računala", "isElective": False, "ects": 5 },
                    { "id": 224, "name": "Programiranje 1", "isElective": False, "ects": 10 },
                    { "id": 225, "name": "Engleski jezik 1", "isElective": False, "ects": 2 }
                ],
                "2": [
                    { "id": 226, "name": "Primijenjena matematika", "isElective": False, "ects": 5 },
                    { "id": 227, "name": "Osnove elektronike", "isElective": False, "ects": 5 },
                    { "id": 228, "name": "Digitalna tehnika", "isElective": False, "ects": 7 },
                    { "id": 229, "name": "Programiranje 2", "isElective": False, "ects": 10 },
                    { "id": 230, "name": "Engleski jezik 2", "isElective": False, "ects": 3 }
                ],
                "3": [
                    { "id": 231, "name": "Uvod u poduzetništvo", "isElective": False, "ects": 4 },
                    { "id": 232, "name": "Arhitektura digitalnih računala", "isElective": False, "ects": 6 },
                    { "id": 233, "name": "Baze podataka", "isElective": False, "ects": 5 },
                    { "id": 234, "name": "Algoritmi i strukture podataka", "isElective": False, "ects": 5 },
                    { "id": 235, "name": "Programiranje za Unix", "isElective": False, "ects": 5 },
                    { "id": 236, "name": "Programiranje za Internet", "isElective": False, "ects": 5 }
                ],
                "4": [
                    { "id": 237, "name": "Računalne mreže", "isElective": False, "ects": 5 },
                    { "id": 238, "name": "Operacijski sustavi", "isElective": False, "ects": 7 },
                    { "id": 239, "name": "Objektno orijentirano programiranje", "isElective": False, "ects": 7 },
                    { "id": 240, "name": "Programiranje u Javi", "isElective": False, "ects": 6 },
                    { "id": 240, "name": "Multimedijske mreže i sustavi", "isElective": False, "ects": 5 }
                ],
                "5": [
                    { "id": 241, "name": "Programsko inženjerstvo", "isElective": False, "ects": 5 },
                    { "id": 242, "name": "Uvod u distribuirane informacijske sustave", "isElective": False, "ects": 5 },
                    { "id": 243, "name": "Arhitektura osobnih računala", "isElective": True, "ects": 5 },
                    { "id": 244, "name": "Programiranje za Windows", "isElective": True, "ects": 5 },
                    { "id": 245, "name": "Baze podataka 2", "isElective": True, "ects": 5 },
                    { "id": 246, "name": "Sigurnost računala i podataka", "isElective": True, "ects": 5 },
                    { "id": 247, "name": "Projektiranje i korištenje računalnih mreža", "isElective": True, "ects": 5 },
                    { "id": 248, "name": "Napredne web tehnologije", "isElective": True, "ects": 5 },
                    { "id": 249, "name": "Upravljanje poslovnim procesima", "isElective": True, "ects": 5 }
                ],
                "6": [
                    { "id": 250, "name": "Projektiranje informacijskih sustava", "isElective": False, "ects": 5 },
                    { "id": 251, "name": "Stručna praksa", "isElective": False, "ects": 10 },
                    { "id": 252, "name": "Završni rad", "isElective": False, "ects": 10 },
                    { "id": 253, "name": "Mikrokontrolerom upravljani mobilni roboti", "isElective": True, "ects": 5 },
                    { "id": 254, "name": "Mobilne komunikacijske mreže", "isElective": True, "ects": 5 },
                    { "id": 255, "name": "Osnove programiranja 3D računalnih igara", "isElective": True, "ects": 5 },
                    { "id": 256, "name": "Programiranje za android", "isElective": True, "ects": 5 }
                ]
                }
                return Response(subjects, status=status.HTTP_200_OK)
       
        return Response("error", status=status.HTTP_200_OK)
    
class DeletePdfFile(APIView):

    def get(self,request, format=None):
        pdf_folder_path = r'./api/documents'
        delete_all_files(pdf_folder_path)
        return Response("Successfuly deleted the pdf file from temp folder", status=status.HTTP_200_OK)

class CreateStudentView(APIView):
    serializer_class = CreateStudentSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Student.objects.filter(host = host)
            if queryset.exists():
                student = queryset[0]
                student.guest_can_pause = guest_can_pause
                student.votes_to_skip = votes_to_skip
                student.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                return Response(StudentSerializer(student).data, status=status.HTTP_200_OK)
            else:
                student = Student(host=host,guest_can_pause = guest_can_pause, votes_to_skip = votes_to_skip)
                student.save()
                return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)
            
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
    
class Subject:
    subject_name=""
    subject_grade=0

class Student:
    def __init__(self, name, age, gender, id, grades, current_major, future_major):
        self.student_name = name
        self.student_age = age
        self.student_gender = gender
        self.student_id = id
        self.student_grades = grades
        self.student_current_major = current_major
        self.student_future_major = future_major

    def to_dict(self):
        return {
            "student_name": self.student_name,
            "student_age": self.student_age,
            "student_gender": self.student_gender,
            "student_id": self.student_id,
            "student_grades": self.student_grades,
            "student_current_major": self.student_current_major,
            "student_future_major": self.student_future_major
        }

    student_name=""
    student_age=""
    student_gender=""
    student_id=""
    student_grades = []
    student_current_major = {}
    student_future_major = {}

    
def read_png_files(folder_path):
    png_files = []
    for file in os.listdir(folder_path):
        if file.lower().endswith('.png'):
            png_file_path = os.path.join(folder_path, file)
            png_files.append(png_file_path)
    return png_files
    
def delete_all_files(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def process_ocr_result(text):
    lines = [line.strip() for line in text.splitlines()]
    return lines

def student_name(text):
    name_pattern = r'Student(?:ica)?\s+([A-ZČĆŽŠĐ][a-zčćžšđ]+)\s+([A-ZČĆŽŠĐ][a-zčćžšđ]+)'
    name_match = re.search(name_pattern, text)
    name = ""
    if name_match:
        name = name_match.group(1) + " " + name_match.group(2)
    return name

# Extract student date of birth
def student_dob(text):
    dob_pattern = r'rođen(?:a)?\s+(\d+.\s*[A-Za-zžćčšđ]+\s+\d+.)'
    dob_match = re.search(dob_pattern, text)
    dob = ""
    if dob_match:
        dob = dob_match.group(1)
    return dob

# Extract student gender
def student_gender(text):
    gender_pattern = r'Student(?:ica)?'
    gender_match = re.search(gender_pattern, text)
    if gender_match:
        if gender_match.group() == "Student":
            return "m"
        elif gender_match.group() == "Studentica":
            return "ž"

# Extract student ID
def student_id(text):
    id_pattern = r'matični broj\s+(\d+)'
    id_match = re.search(id_pattern, text)
    id = ""
    if id_match:
        id = id_match.group(1)
    return id

def process_table_data(table_data):
    processed_data = []
    for line in table_data:
        # Remove specified symbols
        line = re.sub(r'[.,:;_\/\\|\(\)\[\]\-—=+]', '', line)
        # Remove first encountered numbers
        line = re.sub(r'^\d+\s+', '', line)
        # Remove numbers with more than a single digit
        line = re.sub(r'\b\d{2,}\b', '', line)
        # Add spaces between numbers and digits
        line = re.sub(r'(?<=\d)(?=[a-zA-Z])|(?<=[a-zA-Z])(?=\d)', ' ', line)
        # Remove unnecessary words
        line = re.sub(r'\b(?:dovoljan|dobar|doba|vrlo|vrlodobar|izvrstan|NEE|IH|N|NR)\b', '', line)
        # Remove standalone o and O
        line = re.sub(r'\b[0Oo]\b', '', line)
        # Remove standalone o and O
        line = re.sub(r'(?<!\S)\s{2,}[a-zA-Z]\s{2,}(?!\S)', '', line)
        # Lowercase l into 1
        line = re.sub(r'\bl\b', '1', line)
        # Remove symbol '
        line = re.sub(r"'", '', line)
        # Replace "{standalone letter}{whitespace}{digit}" pattern with digit
        line = re.sub(r'\b[A-Za-z]\s+(\d)', r'\1', line)
        # Replace "{digit}{whitespace}{standalone letter}" pattern with digit
        line = re.sub(r'(\d)\s+\b[A-Za-z]', r'\1', line)
        # Remove all whitespace characters between line end and grade
        line = re.sub(r'\s+\Z', '', re.sub(r'\s+(?!\s*$)', ' ', line))
        # Remove characters between numbers
        matches = re.findall(r'(\b\d+\b).*?(\b\d+\b)', line)
        if len(matches) != 0:
            line = re.sub(r'(\b\d+\b).*?(\b\d+\b)', r'\1 \2', line)
        # Replace "1 1" with "1"
        line = re.sub(r'\b1\s+1\b', '1', line)

        index = len(line) - 1
        for c in reversed(line):
            if index < 0 or index > len(line)-1:
                break

            if ord(c) < 48 or ord(c) > 57:
                line = line.replace(line[index],'')
                index=index-1
            else:
                break

        # Remove all lines that don't end in a number
        line = re.sub(r'^(?![\s\S]*\d\s*$).*?$', '', line)

        if line:
            processed_data.append(line)
        
    return processed_data

def generate_grade_csv_name(id_number):
    return f"{id_number}_grade.csv"

# Create grade.csv file
def create_grade_csv(data_list, output_folder, output_file):
    output_path = os.path.join(output_folder, output_file)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Subject', 'Grade']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for element in data_list:
            subject = ' '.join(element.split()[:-1])
            grade = element.split()[-1]
            writer.writerow({'Subject': subject, 'Grade': grade})
    
class ExtractStudentInfo(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Ensure these parsers are used

    def post(self, request, *args, **kwargs):
        if request.method == "POST" and request.FILES['file']:
            form = UploadFileForm(request.POST, request.FILES)
            file = request.FILES.get("file")
            fs = FileSystemStorage()
            filename = fs.save('./api/documents/' + file.name, file)
            uploaded_file_path = fs.path(filename)

            png_folder_path = r'./api/images'
            pdf_folder_path = r'./api/documents'
            student_data_folder_path = r'./api/student_data'

            table_pattern = r'^(?:\d{1,2}(?:st|nd|rd|th)?(?:\.|\b)|\b(?:[ivxlcdm]+|[IVXLCDM]+)(?:\.|\)))\s.*$'

            name = ""
            dob = ""
            gender = ""
            ID = ""
            student_data = []
            table_data = []
            whole_text = ""

            doc = fitz.open(uploaded_file_path)

            for i, page in enumerate(doc):
                zoom = 1
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix = mat, dpi=300)
                pix.save(f"api/images/page_{i}.png")

            all_png_files = read_png_files(png_folder_path)

            for png_file in all_png_files:
                processed_text = []
                img = cv2.imread(png_file)
                ocr_result = pytesseract.image_to_string(png_file, lang='hrv')
                ocr_result = re.sub(r'[\/\\\-_—|,:;=]', '', ocr_result)
                processed_text = process_ocr_result(ocr_result)
                whole_text += ocr_result


                if ID == "":
                    ID = student_id(ocr_result)
                if name == "":
                    name = student_name(ocr_result)
                    gender = student_gender(ocr_result)
                if dob == "":
                    dob = student_dob(ocr_result)

                for line in processed_text:
                    matches = re.findall(table_pattern, line, re.MULTILINE)
                    table_data.extend(matches)
                table_data = process_table_data(table_data)

            student=Student(name,dob,gender,ID,table_data,{},{})

            delete_all_files(png_folder_path)

            return Response(student.to_dict(), status=status.HTTP_200_OK)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
            