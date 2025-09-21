# detection/models.py
from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

class NewsCheck(models.Model):
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    text_en = models.TextField()
    prediction_label = models.CharField(max_length=50)
    confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("text", "state")  # prevent duplicates
