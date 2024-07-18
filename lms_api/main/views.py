from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from .serializers import TeacherSerializer, CategorySerializer, CourseSerializer, ChapterSerializer, StudentSerializer, StudentCourseEnrollSerializer, CourseRatingSerializer, TeacherDashboardSerializer, StudentFavouriteCourseSerializer, StudnetAssignmentSerializer, StudentDashboardSerializer, NotificationSerializer, QuizSerializer, QuestionSerializer, CourseQuizSerializer, AttemptQuizSerializer
from . import models

class TeacherList(generics.ListCreateAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes = [permissions.IsAuthenticated]

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes = [permissions.IsAuthenticated]

class TeacherDashboard(generics.RetrieveAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherDashboardSerializer

@csrf_exempt
def teacher_login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        teacherData = models.Teacher.objects.get(email=email, password=password)
    except models.Teacher.DoesNotExist:
        teacherData=None
    if teacherData:
        return JsonResponse({'bool':True, 'teacher_id':teacherData.id})
    else:
        return JsonResponse({'bool':False})
    
# Category
class CategoryList(generics.ListCreateAPIView):
    queryset = models.CourseCategory.objects.all()
    serializer_class = CategorySerializer

# Course
class CourseList(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        if 'result' in self.request.GET:
            limit=int(self.request.GET['result'])
            qs=models.Course.objects.all().order_by('-id')[:limit]

        if 'category' in self.request.GET:
            category=self.request.GET['category']
            qs=models.Course.objects.filter(techs__icontains=category)

        if 'skill_name' in self.request.GET and 'teacher' in self.request.GET:
            skill_name=self.request.GET['skill_name']
            teacher=self.request.GET['teacher']
            teacher=models.Teacher.objects.filter(id=skill_name).first()
            qs=models.Course.objects.filter(techs__icontains=skill_name, teacher=teacher)

        if 'searchstring' in self.kwargs:
            search=self.kwargs['searchstring']
            if search:
                qs=models.Course.objects.filter(Q(title__icontains=search) | Q(techs__icontains=search))


        elif 'studentId' in self.kwargs:
            student_id=self.kwargs['studentId']
            student = models.Student.objects.get(pk=student_id)
            queries = [Q(techs__iendswith=value) for value in student.interested_categories]
            query = queries.pop()
            for item in queries:
                query |= item 
            qs = models.Course.objects.filter(query)
            return qs

        return qs
    
class CourseDetailView(generics.RetrieveAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer

# Specific Teacher Course
class TeacherCourseList(generics.ListCreateAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        teacher_id=self.kwargs['teacher_id']
        teacher=models.Teacher.objects.get(pk=teacher_id)
        return models.Course.objects.filter(teacher=teacher)
    
# Course Detail
class TeacherCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer
    
# Chapter
class ChapterList(generics.ListCreateAPIView):
    queryset = models.Chapter.objects.all()
    serializer_class = ChapterSerializer

# Course Chapter List
class CourseChapterList(generics.ListCreateAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        course_id=self.kwargs['course_id']
        course = models.Course.objects.get(pk=course_id)
        return models.Chapter.objects.filter(course=course)

class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Chapter.objects.all()
    serializer_class = ChapterSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['chapter_duration']=self.chapter_duration
        print(context)
        return context









# Student Data
class StudentList(generics.ListCreateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes = [permissions.IsAuthenticated]

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes = [permissions.IsAuthenticated]

@csrf_exempt
def student_login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        studentData = models.Student.objects.get(email=email, password=password)
    except models.Student.DoesNotExist:
        studentData=None
    if studentData:
        return JsonResponse({'bool':True, 'student_id':studentData.id})
    else:
        return JsonResponse({'bool':False})
    
class StudentDashboard(generics.RetrieveAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentDashboardSerializer
    
class StudentEnrollCourseList(generics.ListCreateAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = StudentCourseEnrollSerializer

class StudentFavouriteCourseList(generics.ListCreateAPIView):
    queryset = models.StudentFavouriteCourse.objects.all()
    serializer_class = StudentFavouriteCourseSerializer

    def get_queryset(self):
        if 'student_id' in self.kwargs:
            student_id=self.kwargs['student_id']
            student = models.Student.objects.get(pk=student_id)
            return models.StudentFavouriteCourse.objects.filter(student=student).distinct()

def fetch_enroll_status(request, student_id, course_id):
    student = models.Student.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    enrollStatus=models.StudentCourseEnrollment.objects.filter(course=course, student=student).count()
    if enrollStatus:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})
    
def fetch_favourite_status(request, course_id, student_id):
    student = models.Student.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    favouriteStatus=models.StudentFavouriteCourse.objects.filter(course=course, student=student).first()
    if favouriteStatus:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})
    
def remove_favourite_course(request, course_id, student_id):
    student = models.Student.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    favouriteStatus=models.StudentFavouriteCourse.objects.filter(course=course, student=student).delete()
    if favouriteStatus:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})

class EnrolledStudentList(generics.ListAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = StudentCourseEnrollSerializer

    def get_queryset(self):
        if 'course_id' in self.kwargs:
            course_id=self.kwargs['course_id']
            course = models.Course.objects.get(pk=course_id)
            return models.StudentCourseEnrollment.objects.filter(course=course)
        elif 'teacher_id' in self.kwargs:
            teacher_id=self.kwargs['teacher_id']
            teacher = models.Teacher.objects.get(pk=teacher_id)
            return models.StudentCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
        elif 'student_id' in self.kwargs:
            student_id=self.kwargs['student_id']
            student = models.Student.objects.get(pk=student_id)
            return models.StudentCourseEnrollment.objects.filter(student=student).distinct()
        

class CourseRatingList(generics.ListCreateAPIView):
    queryset = models.CourseRating.objects.all()
    serializer_class = CourseRatingSerializer

def fetch_rating_status(request, student_id, course_id):
    student = models.Student.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    ratingStatus=models.CourseRating.objects.filter(course=course, student=student).count()
    if ratingStatus:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})

@csrf_exempt
def teacher_change_password(request, teacher_id):
    password = request.POST['password']
    try:
        teacherData = models.Teacher.objects.get(id=teacher_id)
    except models.Teacher.DoesNotExist:
        teacherData=None
    if teacherData:
        models.Teacher.objects.filter(id=teacher_id).update(password=password)
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})
    
# Assignment List
class AssignmentList(generics.ListCreateAPIView):
    queryset = models.StudentAssignment.objects.all()
    serializer_class = StudnetAssignmentSerializer

    def get_queryset(self):
        student_id=self.kwargs['student_id']
        teacher_id=self.kwargs['teacher_id']
        student = models.Student.objects.get(pk=student_id)
        teacher = models.Teacher.objects.get(pk=teacher_id)
        return models.StudentAssignment.objects.filter(student=student, teacher=teacher)
    
# MyAssignment List
class MyAssignmentList(generics.ListCreateAPIView):
    queryset = models.StudentAssignment.objects.all()
    serializer_class = StudnetAssignmentSerializer

    def get_queryset(self):
        student_id=self.kwargs['student_id']
        student = models.Student.objects.get(pk=student_id)
        models.Notification.objects.filter(student=student, notif_for='student', notif_subject='assignment').update(notifread_status=True)
        return models.StudentAssignment.objects.filter(student=student)
    
# MyAssignment List
class UpdateAssignment(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.StudentAssignment.objects.all()
    serializer_class = StudnetAssignmentSerializer

# Student Change Password
@csrf_exempt
def student_change_password(request, student_id):
    password = request.POST['password']
    try:
        studentData = models.Student.objects.get(id=student_id)
    except models.Student.DoesNotExist:
        studentData=None
    if studentData:
        models.Student.objects.filter(id=student_id).update(password=password)
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})
    
# Notification List
class NotificationList(generics.ListCreateAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        student_id=self.kwargs['student_id']
        student = models.Student.objects.get(pk=student_id)
        return models.Notification.objects.filter(student=student, notif_for='student', notif_subject='assignment', notifread_status=False)
    


# Quiz

class QuizList(generics.ListCreateAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = QuizSerializer

# Specific Teacher Quiz
class TeacherQuizList(generics.ListCreateAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        teacher_id=self.kwargs['teacher_id']
        teacher=models.Teacher.objects.get(pk=teacher_id)
        return models.Quiz.objects.filter(teacher=teacher)

# Quiz Detail
class TeacherQuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizQuestionList(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        quiz_id=self.kwargs['quiz_id']
        quiz = models.Quiz.objects.get(pk=quiz_id)
        if 'limit' in self.kwargs:
            return models.QuizQuestions.objects.filter(quiz=quiz).order_by('id')[:1]
        elif 'question_id' in self.kwargs:
            current_question=self.kwargs['question_id']
            return models.QuizQuestions.objects.filter(quiz=quiz, id_gt=current_question).order_by('id')[:1]
        else:
            return models.QuizQuestions.objects.filter(quiz=quiz)
    
class CourseQuizList(generics.ListCreateAPIView):
    queryset = models.CourseQuiz.objects.all()
    serializer_class = CourseQuizSerializer

    def get_queryset(self):
        if 'course_id' in self.kwargs:
            course_id=self.kwargs['course_id']
            course = models.Course.objects.get(pk=course_id)
            return models.CourseQuiz.objects.filter(course=course)

def fetch_quiz_assign_status(request, quiz_id, course_id):
    quiz=models.Quiz.objects.filter(id=quiz_id).first()
    course=models.Course.objects.filter(id=course_id).first()
    assignStatus=models.CourseQuiz.objects.filter(course=course, quiz=quiz).count()
    if assignStatus:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})

class AttemptQuizList(generics.ListCreateAPIView):
    queryset = models.AttemptQuiz.objects.all()
    serializer_class = AttemptQuizSerializer

def fetch_quiz_attempt_status(request, quiz_id, student_id):
    quiz=models.Quiz.objects.filter(id=quiz_id).first()
    student=models.Student.objects.filter(id=student_id).first()
    attemptStatus=models.AttemptQuiz.objects.filter(student=student, question__quiz=quiz).count()
    if attemptStatus > 0:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})