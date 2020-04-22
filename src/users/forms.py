from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm as AccountSignup
from allauth.socialaccount.forms import SignupForm as SocialSignup
from django import forms
# from django.contrib.auth.models import User
from .models import User

# account/login.html
class MyCustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'type': 'email', 'class': 'account-input','placeholder':'Email Adreess'})
        self.fields['login'].label = ''
        
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'account-input', 'placeholder':'Password'})
        self.fields['password'].label = ''
        
        self.fields['remember'].label = "이메일 저장"
        
    def login(self, *args, **kwargs):
        # custom override
        return super(MyCustomLoginForm,self).login(*args, **kwargs)


# account/signup.html
class MyCustomSignupForm(AccountSignup):
    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'account-input','placeholder':'Email Adreess'})
        self.fields['email'].label = ''

        self.fields['username'].widget = forms.TextInput(attrs={'class': 'account-input','placeholder':'username'})
        self.fields['username'].label = ''

        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'account-input','placeholder':'Password1'})
        self.fields['password1'].label = ''

        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'account-input','placeholder':'Password2'})
        self.fields['password2'].label = ''

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user

# socialaccount/signup.html
class MyCustomSocialSignupForm(SocialSignup):
    def __init__(self, *args, **kwargs):
        super(MyCustomSocialSignupForm, self).__init__(*args, **kwargs)
        # self.fields['email'].widget = forms.TextInput(attrs={'class': 'input-socialsignup','placeholder':'Email Adreess', 'readonly':'readonly'})

    def save(self):    
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSocialSignupForm, self).save()
        
        
        # Add your own processing here.

        # You must return the original result.
        return user
