from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Subject(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Course(models.Model):
    subject = models.ForeignKey(Subject, related_name = "subject", on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, related_name='instructor', on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    course_description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title

class CourseModule(models.Model):
    course = models.ForeignKey(Course, related_name='course_module', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title   
    
class Content(models.Model):
    courseModule = models.ForeignKey(CourseModule, related_name='content', on_delete=models.CASCADE)
    contentTypes = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':(
        'text', 'video', 'image', 'file'
    )})
    objectId = models.PositiveIntegerField()
    item = GenericForeignKey('contentTypes', 'objectId')

class contentType(models.Model):
    instructor = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
    
class Text(contentType):
    content = models.TextField()

class Image(contentType):
    file_nm = models.FileField(upload_to='images')

class File(contentType):
    file_nm = models.FileField(upload_to='files')

class Video(contentType):
    url = models.URLField()