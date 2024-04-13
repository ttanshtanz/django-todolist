from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin #to give restricted access

from .models import Task

from django.shortcuts import redirect
from django.views.decorators.http import require_POST

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks') #loads url tasks if all goes right
    
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form): #to redirect the user to login after successful creation of account
        user = form.save() #save the details
        if user is not None: #if the user has sucessfully created an account
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
        
    def get(self, *args, **kwargs): #if logged cant access register - redirected to tasks
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    model = Task #gets all the task from task db irrespective of user
    context_object_name = 'tasks' 

    def get_context_data(self, **kwargs): #to filter data based on user
        context = super().get_context_data(**kwargs)
        context ['tasks'] = context ['tasks'].filter(user=self.request.user)
        context ['count'] = context ['tasks'].filter(complete=False).count() #count of incomplete items

        search_input = self.request.GET.get('search-area') or ''
        if search_input: #if theres ant search value given
            context ['tasks'] = context ['tasks'].filter(title__startswith=search_input) #title__icontains to search for anywhere, startswith jz chks fr the items that starts with the given input

        context ['search_input'] = search_input #to keep the search value until refreshed

        return context
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'complete']
        widgets = {
            'complete': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        }

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm  # Use the custom form class
    success_url = reverse_lazy('tasks')
    template_name = 'base/task-form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm  # Use the custom form class
    success_url = reverse_lazy('tasks')
    template_name = 'base/task-form.html'
    

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    # template_name = looks for task_confirm_delete.html

@require_POST
def toggle_task_status(request, pk):
    task = Task.objects.get(pk=pk)
    task.complete = not task.complete
    task.save()
    return redirect('tasks')  # Redirect back to the task list page