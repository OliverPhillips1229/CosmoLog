from django.db import models
from django.urls import reverse

class Experiment(models.Model):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=80)  # Biology, Physics, Materials
    result_summary = models.TextField(blank=True)
    success_status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('experiment-detail', kwargs={'pk': self.id})


class Mission(models.Model):
    name = models.CharField(max_length=120)
    agency = models.CharField(max_length=80)  # NASA, ESA, JAXA, SpaceX
    launch_date = models.DateField()
    outcome = models.CharField(max_length=80, blank=True)  # Success, Partial, Failure
    crewed = models.BooleanField(default=False)
    # M:M with Experiment
    experiments = models.ManyToManyField(Experiment, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mission-detail', kwargs={'pk': self.id})