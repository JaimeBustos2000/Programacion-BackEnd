from django import forms

class UserForm(forms.Form):
    usuario = forms.CharField(label="Usuario",max_length=100,required=True)
    contrasena = forms.CharField(label="Contraseña",widget=forms.PasswordInput(),required=True)
    
class NewUser(forms.Form):
    usuario = forms.CharField(label="Usuario",max_length=100,required=True)
    contrasena = forms.CharField(label="Contraseña",widget=forms.PasswordInput(),required=True)
    email = forms.EmailField(label="Correo",required=True)