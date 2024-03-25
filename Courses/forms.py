from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, CourseModule

CourseModuleFormset = inlineformset_factory(Course, CourseModule, 
                                            fields=['title', 'description'], extra=2, can_delete=True)
