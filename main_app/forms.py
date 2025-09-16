from django import forms

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
