from django import forms

class calculateForm(forms.ModelForm):
    equation = forms.CharField(label='equation', widget=forms.Textarea)
