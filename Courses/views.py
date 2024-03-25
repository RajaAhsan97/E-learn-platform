from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.shortcuts import get_object_or_404, redirect
from django.apps import apps
from django.forms.models import modelform_factory
from .models import Course, Content, CourseModule
from .forms import CourseModuleFormset

# get current instructor 
class Instructor:
    def get_queryset(self):
        inst_Queries = super().get_queryset()
        return inst_Queries.filter(instructor=self.request.user)                  

class EditForm:
    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)

# get model and fields to be used in the list and edit views
class InstructorCourse(Instructor, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'course_description']
    success_url = reverse_lazy('courses:course_list')

# list view
class CourseListView(InstructorCourse, ListView):
    template_name = "courses/manage/course_list.html"
    permission_required = 'courses.view_course'

# course create view
class createCourse(InstructorCourse, EditForm, CreateView):
    template_name = "courses/manage/form.html"
    permission_required = 'courses.add_course'

    
# course update view
class updateCourse(InstructorCourse, EditForm, UpdateView):
    template_name = "courses/manage/form.html"
    permission_required = 'courses.change_course'


# course delete view
class deleteCourse(InstructorCourse, DeleteView):
    template_name = "courses/manage/course_delete.html"
    permission_required = 'courses.delete_courses'

# Add modules to course
class courseModule(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None 

    def get_formset(self, data=None):
        return CourseModuleFormset(instance=self.course, data=data)
    
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, instructor=request.user)
        return super().dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})
    
class CourseModUpdDelView(TemplateResponseMixin, View):
    template_name = "courses/manage/content/form.html"
    model = None
    module= None
    obj = None

    def get_model(self, modelName):
        if modelName in ['text', 'image', 'video', 'file']:
            return apps.get_model(app_label='Courses', model_name=modelName)
        else:
            return None
        
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['instructor', 'created', 'updated'])

        return Form(*args, **kwargs)
    
    def dispatch(self, request, moduleId, modelName, id=None):
        self.module =get_object_or_404(CourseModule, id=moduleId, course__instructor=request.user)
        self.model = self.get_model(modelName)

        if id:
            self.obj = get_object_or_404(self.model, id=id, instructor=request.user)
        
        return super().dispatch(request, moduleId, modelName, id)
    
    def get(self, request, moduleId, modelName, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})
    
    def post(self, request, moduleId, modelName, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.instructor =request.user
            obj.save()
            if not id:
                Content.objects.create(courseModule=self.module, item=obj)

            return redirect('courses:moduleContentList', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})
    
class CourseModContentsView(TemplateResponseMixin, View):
    template_name = "courses/manage/content/contentlist.html"

    def get(self, request, moduleId):
        module = get_object_or_404(CourseModule, id=moduleId, course__instructor=request.user)
        return self.render_to_response({'module': module})
    
class ContentDeleteView(View):
    def post(self, request, id):
        content= get_object_or_404(Content, id=id, courseModule__course__instructor=request.user)
        module = content.courseModule
        content.item.delete()
        content.delete()
        return redirect("courses:moduleContentList", module.id)