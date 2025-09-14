from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Mission, Experiment

# Simple pages
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# --- Mission CBVs ---
class MissionList(ListView):
    model = Mission
    ordering = ['-launch_date']  # newest first

class MissionDetail(DetailView):
    model = Mission

class MissionCreate(CreateView):
    model = Mission
    fields = ['name', 'agency', 'launch_date', 'outcome', 'crewed']  # exclude M2M here

class MissionUpdate(UpdateView):
    model = Mission
    fields = ['name', 'agency', 'launch_date', 'outcome', 'crewed']

class MissionDelete(DeleteView):
    model = Mission
    success_url = reverse_lazy('mission-index')

# --- Experiment CBVs ---
class ExperimentList(ListView):
    model = Experiment
    ordering = ['title']

class ExperimentDetail(DetailView):
    model = Experiment

class ExperimentCreate(CreateView):
    model = Experiment
    fields = ['title', 'category', 'result_summary', 'success_status']

class ExperimentUpdate(UpdateView):
    model = Experiment
    fields = ['title', 'category', 'result_summary', 'success_status']

class ExperimentDelete(DeleteView):
    model = Experiment
    success_url = reverse_lazy('experiment-index')