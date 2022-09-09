from django.urls import reverse
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

class NewTaskForm(forms.Form):
  task = forms.CharField(label='New Task')
  # priority = forms.IntegerField(label='Priority', min_value=1, max_value=10, )

TASKS_LABEL = 'tasks'

def index(request):
  if 'tasks' not in request.session:
    request.session[TASKS_LABEL] = []

  return render(request, 'tasks/index.html', { 'tasks': request.session[TASKS_LABEL], 'hasTasks': len(request.session[TASKS_LABEL]) })

def add(request):
  if request.method == 'POST':
    form = NewTaskForm(request.POST)

    if form.is_valid():
      request.session[TASKS_LABEL] += [form.cleaned_data['task']]
      return HttpResponseRedirect(reverse('tasks:index'))
    else:
      return render(request, 'tasks/add.html', { 'form': form })

  return render(request, 'tasks/add.html', {
    'form': NewTaskForm()
  })