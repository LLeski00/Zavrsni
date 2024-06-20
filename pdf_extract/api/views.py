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
            