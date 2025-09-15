from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    from django.shortcuts import render
    logout(request)
    return render(request, 'registration/logged_out.html')
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Mission, Experiment
from django import forms

# --- Mission CBVs ---
class MissionList(ListView):
    model = Mission
    ordering = ['-launch_date']  # newest first

class MissionDetail(DetailView):
    model = Mission

class MissionCreate(CreateView):
    model = Mission
    fields = ['name', 'agency', 'launch_date', 'outcome', 'crewed', 'experiments']

class MissionUpdate(UpdateView):
    model = Mission
    fields = ['name', 'agency', 'launch_date', 'outcome', 'crewed', 'experiments']

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

    def form_valid(self, form):
        mission_id = self.kwargs.get('mission_id')
        if mission_id:
            form.instance.mission_id = mission_id
        return super().form_valid(form)

class ExperimentUpdate(UpdateView):
    model = Experiment
    fields = ['title', 'category', 'result_summary', 'success_status']

class ExperimentDelete(DeleteView):
    model = Experiment
    success_url = reverse_lazy('experiment-index')

# --- Add Existing Experiment to Mission ---
class AddExperimentForm(forms.Form):
    experiment = forms.ModelChoiceField(queryset=Experiment.objects.none(), label="Select Experiment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['experiment'].queryset = Experiment.objects.all()

def add_existing_experiment(request, mission_id):
    mission = Mission.objects.get(pk=mission_id)
    if request.method == 'POST':
        form = AddExperimentForm(request.POST)
        if form.is_valid():
            experiment = form.cleaned_data['experiment']
            experiment.mission = mission
            experiment.save()
            return redirect('mission-detail', pk=mission_id)
    else:
        form = AddExperimentForm()
    return render(request, 'main_app/add_existing_experiment.html', {'form': form, 'mission': mission})

# --- Simple pages ---
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# --- User Registration ---
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})