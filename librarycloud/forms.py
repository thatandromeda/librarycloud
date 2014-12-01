from django import forms

class SubjectsForm(forms.Form):
	querystring = forms.CharField()
