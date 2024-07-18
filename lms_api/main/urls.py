from django.urls import path
from . import views

urlpatterns = [
    # Teacher
    path('teacher/', views.TeacherList.as_view()),
    path('teacher/dashboard/<int:pk>/', views.TeacherDashboard.as_view()),
    path('teacher/<int:pk>/', views.TeacherDetail.as_view()),
    path('teacher-change-password/<int:teacher_id>/', views.teacher_change_password),
    path('teacher-login', views.teacher_login),

    # Category
    path('category/', views.CategoryList.as_view()),

    # Course
    path('course/', views.CourseList.as_view()),

    # Search Courses
    path('search-courses/<str:searchstring>', views.CourseList.as_view()),

    # Course Detail
    path('course/<int:pk>', views.CourseDetailView.as_view()),

    # Chapter
    path('chapter/', views.ChapterList.as_view()),

    # Specific Course Chapter
    path('course-chapters/<int:course_id>/', views.CourseChapterList.as_view()),

    # Specific Chapter
    path('chapter/<int:pk>/', views.ChapterDetailView.as_view()),

    # Teacher Courses
    path('teacher-courses/<int:teacher_id>', views.TeacherCourseList.as_view()),

    # Course Detail
    path('teacher-course-detail/<int:pk>', views.TeacherCourseDetail.as_view()),



    # Student
    path('student/', views.StudentList.as_view()),
    path('student/<int:pk>/', views.StudentDetail.as_view()),
    path('student/dashboard/<int:pk>/', views.StudentDashboard.as_view()),
    path('student-change-password/<int:student_id>/', views.student_change_password),
    path('student-login', views.student_login),
    path('student-enroll-course/', views.StudentEnrollCourseList.as_view()),
    path('fetch-enroll-status/<int:student_id>/<int:course_id>', views.fetch_enroll_status),
    path('fetch-all-enrolled-students/<int:teacher_id>', views.EnrolledStudentList.as_view()),
    path('fetch-enrolled-students/<int:course_id>', views.EnrolledStudentList.as_view()),
    path('fetch-enrolled-courses/<int:student_id>', views.EnrolledStudentList.as_view()),
    path('fetch-recommended-courses/<int:studentId>', views.CourseList.as_view()),
    path('course-rating/', views.CourseRatingList.as_view()),
    path('fetch-rating-status/<int:student_id>/<int:course_id>', views.fetch_rating_status),
    path('student-add-favourite-course/', views.StudentFavouriteCourseList.as_view()),
    path('student-remove-favourite-course/<int:course_id>/<int:student_id>', views.remove_favourite_course),
    path('fetch-favourite-status/<int:student_id>/<int:course_id>', views.fetch_favourite_status),
    path('fetch-favourite-courses/<int:student_id>', views.StudentFavouriteCourseList.as_view()),
    path('student-assignment/<int:teacher_id>/<int:student_id>', views.AssignmentList.as_view()),
    path('my-assignments/<int:student_id>', views.MyAssignmentList.as_view()),
    path('update-assignment/<int:pk>', views.UpdateAssignment.as_view()),
    path('student/fetch-all-notifications/<int:student_id>/', views.NotificationList.as_view()),
    path('save-notification/', views.NotificationList.as_view()),


    # Quiz Start-
    path('quiz/', views.QuizList.as_view()),
    path('teacher-quiz/<int:teacher_id>', views.TeacherQuizList.as_view()),
    path('teacher-quiz-detail/<int:pk>', views.TeacherQuizDetail.as_view()),
    path('quiz/<int:pk>/', views.QuizDetailView.as_view()),
    path('quiz-questions/<int:quiz_id>', views.QuizQuestionList.as_view()),
    path('quiz-questions/<int:quiz_id>/<int:limit>', views.QuizQuestionList.as_view()),
    path('fetch-quiz-assign-status/<int:quiz_id>/<int:course_id>', views.fetch_quiz_assign_status),
    path('quiz-assign-course/', views.CourseQuizList.as_view()),
    path('fetch-assigned-quiz/<int:course_id>', views.CourseQuizList.as_view()),
    path('attempt-quiz/', views.AttemptQuizList.as_view()),
    path('quiz-questions/<int:quiz_id>/next-question/<int:question_id>', views.QuizQuestionList.as_view()),
    path('fetch-quiz-attempt-status/<int:quiz_id>/<int:student_id>', views.fetch_quiz_attempt_status),
]
