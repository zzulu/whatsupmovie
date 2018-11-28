from django import forms
from .models import Rating


class RatingForm(forms.ModelForm):
    SCORES = (
        (5.0,'5.0'),
        (4.5,'4.5'),
        (4.0,'4.0'),
        (3.5,'3.5'),
        (3.0,'3.0'),
        (2.5,'2.5'),
        (2.0,'2.0'),
        (1.5,'1.5'),
        (1.0,'1.0'),
    )
    score = forms.ChoiceField(label='Score', choices=SCORES)

    class Meta:
        model = Rating
        fields = ['score','content',]
