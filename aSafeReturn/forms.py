from django import forms
from .models import FromTo

class FromToForm(forms.ModelForm):
    class Meta:
        model = FromTo
        fields = ('start_point', 'end_point') #내가 뭘 쓴걸꺄?