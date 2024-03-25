from django.contrib import admin
from .models import Subject, Course, CourseModule

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

class inlineModule(admin.StackedInline):
    model = CourseModule

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['subject', 'title', 'instructor', 'created']
    list_filter = ['created']
    prepopulated_fields= {'slug': ('title',)}
    inlines = [inlineModule]