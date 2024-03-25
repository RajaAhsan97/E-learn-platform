from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    path('instruct/', views.CourseListView.as_view(), name='course_list'),
    path('create/', views.createCourse.as_view(), name='create_course'),
    path('<pk>/update/', views.updateCourse.as_view(), name='update_course'),
    path('<pk>/delete/', views.deleteCourse.as_view(), name='delete_course'),
    path('<pk>/module/', views.courseModule.as_view(), name='course_module'),
    path('module/<int:moduleId>/content/<modelName>/create', views.CourseModUpdDelView.as_view(), name="moduleContentCreate"),
    path('module/<int:moduleId>/content/<modelName>/<id>', views.CourseModUpdDelView.as_view(), name="moduleContentUpdate"),
    path('module/<int:moduleId>/', views.CourseModContentsView.as_view(), name="moduleContentList"),
    path('content/<int:id>/delete/', views.ContentDeleteView.as_view(), name='moduleContentDelete'),
]