from django import forms
from turnero.models import Usuarios

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['profile_picture']
        
    profile_picture = forms.ImageField(label="Avatar", required=False, widget=forms.FileInput(attrs={'class':'form-control'}))