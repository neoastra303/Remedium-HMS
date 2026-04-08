from django import forms
from django.contrib.auth.models import User
from .models import Staff

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['staff_id', 'first_name', 'last_name', 'role', 'department', 'phone', 'email', 'schedule']

class StaffWithUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    is_superuser = forms.BooleanField(required=False, label="Grant Admin Access (Superuser)")

    class Meta:
        model = Staff
        fields = ['staff_id', 'first_name', 'last_name', 'role', 'department', 'phone', 'email', 'schedule']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("username")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
            
        return cleaned_data

    def save(self, commit=True):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        is_superuser = self.cleaned_data.get('is_superuser')

        user = User.objects.create_user(username=username, email=email, password=password)
        if is_superuser:
            user.is_superuser = True
            user.is_staff = True
        user.save()

        staff = super().save(commit=False)
        staff.user = user
        if commit:
            staff.save()
        return staff
