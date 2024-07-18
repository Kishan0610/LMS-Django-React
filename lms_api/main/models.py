from django.db import models
from django.core import serializers

# Teacher Model
class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)
    qualification = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    profile_img = models.ImageField(upload_to='teacher_profile_imgs/', null=True)
    skills = models.TextField()

    def skill_list(self):
        skill_list=self.skills.split(',')
        return skill_list
    
    # Total Teacher Courses
    def total_teacher_courses(self):
        total_courses = Course.objects.filter(teacher=self).count()
        return total_courses
    
    # Total Teacher Chapters
    def total_teacher_chapters(self):
        total_chapters = Chapter.objects.filter(course__teacher=self).count()
        return total_chapters
    
    # Total Teacher Students
    def total_teacher_students(self):
        total_students = StudentCourseEnrollment.objects.filter(course__teacher=self).count()
        return total_students

    class Meta:
        verbose_name_plural = "1. Teacher"

    def __str__(self):
        return self.full_name

# Course Category Model
class CourseCategory(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "2. Course Categories"

    def __str__(self):
        return self.title

# Course Model
class Course(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_courses')
    title = models.CharField(max_length=150)
    description = models.TextField()
    featured_img = models.ImageField(upload_to='course_imgs/', null=True)
    techs = models.TextField(null=True)

    def related_videos(self):
        related_videos=Course.objects.filter(techs__icontains=self.techs)
        return serializers.serialize('json',related_videos)
    
    def tech_list(self):
        tech_list=self.techs.split(',')
        return tech_list
    
    def total_enrolled_students(self):
        total_enrolled_students=StudentCourseEnrollment.objects.filter(course=self).count()
        return total_enrolled_students

    def course_rating(self):
        course_rating=CourseRating.objects.filter(course=self).aggregate(avg_rating=models.Avg('rating'))
        return course_rating['avg_rating']

    class Meta:
        verbose_name_plural = "3. Course"

    def __str__(self):
        return self.title
    

# Chapter Model
class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_chapters')
    title = models.CharField(max_length=150)
    description = models.TextField()
    video = models.FileField(upload_to='chapter_videos/', null=True)
    remarks = models.TextField(null=True)

    def chapter_duration(self):
        second=0
        import cv2
        cap = cv2.VideoCapture(self.video.path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if frame_count:
            duration = frame_count/fps
            print('fps = ' + str(fps))
            print('number of frames = ' + str(frame_count))
            print('duration (S) = ' + str(duration))
            minutes = int(duration/60)
            seconds = duration%60
            print('duration (M:S) = ' + str(minutes) + ' : ' + str(seconds))
        return seconds

    class Meta:
        verbose_name_plural = "4. Chapters"

    def __str__(self):
        return self.title


# Student Model
class Student(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100,blank=True, null=True)
    username = models.CharField(max_length=200)
    interested_categories = models.TextField()
    profile_img = models.ImageField(upload_to='student_profile_imgs/', null=True)

    # Total Enrolled Courses
    def enrolled_courses(self):
        enrolled_courses = StudentCourseEnrollment.objects.filter(student=self).count()
        return enrolled_courses
    
    # Total Favourite Courses
    def favourite_courses(self):
        favourite_courses = StudentFavouriteCourse.objects.filter(student=self).count()
        return favourite_courses
    
    # Completed Assignments 
    def complete_assignments(self):
        complete_assignments = StudentAssignment.objects.filter(student=self, student_status=True).count()
        return complete_assignments
    
    # Pending Assignments 
    def pending_assignments(self):
        pending_assignments = StudentAssignment.objects.filter(student=self, student_status=False).count()
        return pending_assignments

    class Meta:
        verbose_name_plural = "5. Students"

    def __str__(self):
        return self.full_name

# Student Course Enrollment
class StudentCourseEnrollment(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE, related_name='enrolled_courses')
    student=models.ForeignKey(Student,on_delete=models.CASCADE, related_name='enrolled_student')
    enrolled_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course} - {self.student}"

    class Meta:
        verbose_name_plural = "6. Enrolled Courses"

# Student Favourite Course
class StudentFavouriteCourse(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    status=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course} - {self.student}"

    class Meta:
        verbose_name_plural = "7. Student Favourite Courses"


# Course Rating & Reviews
class CourseRating(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE, null=True)
    student=models.ForeignKey(Student,on_delete=models.CASCADE, null=True)
    rating=models.PositiveBigIntegerField(default=0)
    reviews=models.TextField(null=True)
    review_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"\"{self.course}\" - {self.student} - {self.rating}"

    class Meta:
        verbose_name_plural = "8. Course Ratings"

# Student Assignment
class StudentAssignment(models.Model):
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE, null=True)
    student=models.ForeignKey(Student,on_delete=models.CASCADE, null=True)
    title=models.CharField(max_length=200)
    detail=models.TextField(null=True)
    student_status = models.BooleanField(default=False, null=True)
    add_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"\"{self.title}\" to {self.student}"

    class Meta:
        verbose_name_plural = "9. Student Assignments"

# Notifivation Model
class Notification(models.Model):
    teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    student=models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    notif_subject=models.CharField(max_length=200, verbose_name='Notification Subject', null=True)
    notif_for=models.CharField(max_length=200, verbose_name='Notification For')
    notif_created_time=models.DateTimeField(auto_now_add=True, verbose_name='Notification Created Time')
    notifread_status=models.BooleanField(default=False , verbose_name='Notification Status')

    class Meta:
        verbose_name_plural = "9.1. Notifications"

# Quiz Model
class Quiz(models.Model):
    teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    title=models.CharField(max_length=200)
    detail=models.TextField()
    add_time=models.DateTimeField(auto_now_add=True)

    def assign_status(self):
        return CourseQuiz.objects.filter(quiz=self).count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "9.2. Quiz"

# Quiz Questions Model
class QuizQuestions(models.Model):
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    questions=models.CharField(max_length=200)
    ans1=models.CharField(max_length=200)
    ans2=models.CharField(max_length=200)
    ans3=models.CharField(max_length=200)
    ans4=models.CharField(max_length=200)
    right_ans=models.CharField(max_length=200)
    add_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.questions

    class Meta:
        verbose_name_plural = "9.3. Quiz Questions"

# Add Quiz to Course
class CourseQuiz(models.Model):
    teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    course=models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    add_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"\"{self.quiz}\" to {self.course}"

    class Meta:
        verbose_name_plural = "9.4. Course Quiz"

# Attempt Quiz Question by student
class AttemptQuiz(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    question=models.ForeignKey(QuizQuestions, on_delete=models.CASCADE, null=True)
    right_ans=models.CharField(max_length=200, null=True)
    add_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student

    class Meta:
        verbose_name_plural = "9.5. Attempted Questions"

# Study Materials Model
class StudyMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    upload = models.FileField(upload_to='study_materials/', null=True)
    remarks = models.TextField(null=True)

    class Meta:
        verbose_name_plural = "9.6. Study Materials"