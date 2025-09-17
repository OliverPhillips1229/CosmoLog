from django.http import HttpResponseRedirect

def accounts_logout_redirect(request):
    return HttpResponseRedirect('/logout/')
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

# --- Custom Login View ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
from django.contrib import messages
from .forms import RoverPhotoFilter
from .services import nasa

def mars_manifest(request, rover):
    try:
        manifest = nasa.get_manifest(rover)
    except Exception as e:
        messages.error(request, f"NASA API error: {e}")
        manifest = {}
    return render(request, "mars/manifest.html", {"manifest": manifest, "rover": rover})

def mars_gallery(request):
    from main_app.services.nasa_images import get_mars_images
    photos = get_mars_images(count=24)
    meta = {"count": 24, "interval": 4}
    return render(request, "mars/gallery.html", {"photos": photos, "meta": meta})
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
    ordering = ['launch_date']  # earliest first

class MissionDetail(DetailView):
    model = Mission

class MissionCreate(CreateView):
    model = Mission
    fields = ['name', 'agency', 'launch_date', 'outcome', 'crewed', 'experiments']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MissionUpdate(UpdateView):
    model = Mission
    fields = ['name', 'agency', 'launch_date', 'outcome', 'crewed', 'experiments']

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            return redirect('mission-detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

class MissionDelete(DeleteView):
    model = Mission
    success_url = reverse_lazy('mission-index')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            return redirect('mission-detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

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
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExperimentUpdate(UpdateView):
    model = Experiment
    fields = ['title', 'category', 'result_summary', 'success_status']

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Only allow edit if user owns the experiment
        if obj.user != request.user:
            return redirect('experiment-detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

class ExperimentDelete(DeleteView):
    model = Experiment

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Only allow delete if user owns the experiment
        if obj.user != request.user:
            return redirect('experiment-detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)
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
            mission.experiments.add(experiment)
            return redirect('mission-detail', pk=mission_id)
    else:
        form = AddExperimentForm()
    return render(request, 'main_app/add_existing_experiment.html', {'form': form, 'mission': mission})

# --- Simple pages ---
def home(request):
    from django.core.cache import cache
    from main_app.services import nasa
    rover = "curiosity"
    sol = 1000
    cache_key = f"nasa_photos_{rover}_{sol}"
    photos = cache.get(cache_key)
    if photos is None:
        try:
            photos = nasa.get_photos(rover, sol=sol)
        except Exception as e:
            photos = []
        cache.set(cache_key, photos, 60 * 10)  # cache for 10 minutes
    return render(request, 'home.html', {"mars_photos": photos})

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