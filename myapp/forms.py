from django import forms
from django.forms import ModelForm
from .models import Task, Project

class CreateNewTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important','project']
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control'}),
            'important' : forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }
    #title = forms.CharField(label= "titulo de tarea",max_length=20, widget=forms.TextInput(attrs={'class': 'input'}))
    #description = forms.CharField(widget=forms.Textarea(attrs={'class': 'input'}))
    #important=forms.BooleanField(label= "importante")

class CreateNewProject(ModelForm):
    class Meta:
        model = Project
        fields =['name']
    
    #name = forms.CharField(label= "Nombre del proyecto",max_length=200,widget=forms.TextInput(attrs={'class': 'input'}))

