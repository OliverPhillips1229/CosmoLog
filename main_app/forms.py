from django import forms
from .models import Mission, Experiment

CAMERA_CHOICES = [
    ("", "All Cameras"),
    ("fhaz", "FHAZ – Front Hazard"),
    ("rhaz", "RHAZ – Rear Hazard"),
    ("mast", "MAST – Mast Camera"),
    ("chemcam", "CHEMCAM – Chem & Camera"),
    ("mahli", "MAHLI – Hand Lens"),
    ("mardi", "MARDI – Descent Imager"),
    ("navcam", "NAVCAM – Navigation"),
    ("pancam", "PANCAM – Panoramic (Opp/Spirit)"),
    ("minites", "MINITES – Mini-TES (Opp/Spirit)"),
]

ROVER_CHOICES = [
    ("curiosity", "Curiosity"),
    ("opportunity", "Opportunity"),
    ("spirit", "Spirit")
]

class RoverPhotoFilter(forms.Form):
    rover = forms.ChoiceField(choices=ROVER_CHOICES, initial="curiosity")
    # allow either sol or earth_date; validate in the view
    sol = forms.IntegerField(required=False, min_value=0, label="Sol")
    earth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    camera = forms.ChoiceField(choices=CAMERA_CHOICES, required=False)
    page = forms.IntegerField(required=False, min_value=1, initial=1)

class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ['name', 'agency', 'launch_date', 'outcome', 'crewed', 'experiments']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Apollo 11'}),
            'agency': forms.TextInput(attrs={'placeholder': 'e.g. NASA'}),
            'launch_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'e.g. 1969-07-16'}),
            'outcome': forms.TextInput(attrs={'placeholder': 'e.g. Successful lunar landing'}),
        }

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['title', 'category', 'result_summary', 'success_status', 'mission']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Lunar Surface Sample Collection'}),
            'category': forms.TextInput(attrs={'placeholder': 'e.g. Geology'}),
            'result_summary': forms.Textarea(attrs={'placeholder': 'e.g. Collected 2kg of lunar regolith'}),
        }
