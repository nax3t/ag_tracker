from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        help_texts = {
            'username': 'Letters, digits and @/./+/-/_ only.',
            'email': 'A valid email address is required.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize password help texts to be more concise
        self.fields['password1'].help_text = "At least 8 characters. Mix letters and numbers."
        self.fields['password2'].help_text = "Enter the same password again."

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user 