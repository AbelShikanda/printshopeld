from django import forms
from django.forms import TextInput
from django_countries.fields import CountryField
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)
from .models import UserBase

class UserLoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
                                                                'class': 'form-control', 
                                                                'placeholder': 'Email', 
                                                                'id': 'login-username',
                                                            }
                                                        )
                                )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                    'class': 'form-control',
                                                                    'placeholder': 'Password',
                                                                    'id': 'login-pwd',
                                                                }
                                                            )
                                )


class RegistrationForm(forms.ModelForm):
    
    user_name = forms.CharField(
        min_length=3,
        max_length=200,
		required = True,
		help_text='Enter Username',
		widget=forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Username'
                                    }),
                                )
    email = forms.EmailField(
        max_length=100,
		required = True,
		help_text='Enter Email Address',
        error_messages={'required': 'You will need an email'},
		widget=forms.TextInput(attrs={
                                        'class': 'form-control', 
                                        'placeholder': 'Email',
                                        'name': 'email', 
                                        'id': 'id_email'
                                    }),
                            )
    password = forms.CharField(
        help_text='Enter Password',
		required = True,
		widget=forms.PasswordInput(attrs={
                                            'class': 'form-control', 
                                            'placeholder': 'Password'
                                        }),
                                )
    password2 = forms.CharField(
        help_text='Enter Password',
		required = True,
		widget=forms.PasswordInput(attrs={
                                            'class': 'form-control', 
                                            'placeholder': 'Confirm Password'
                                        }),
                                )
    
    class Meta:
        model = UserBase
        fields = ('email','user_name')
        
    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError( 'Please use another Email, that one is already taken')
        return email

class PwdResetForm(PasswordResetForm):
    
    email = forms.EmailField(max_length=254, 
                            help_text='Enter Email Address',
                            widget=forms.TextInput(
                                                                    attrs={
                                                                            'class': 'form-control', 
                                                                            'placeholder': 'Email', 
                                                                            'id': 'form-email'
                                                                            }
                                                                    )
                            )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
                                    label='New password', 
                                    widget=forms.PasswordInput(attrs={
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'New Password', 
                                                                        'id': 'form-newpass'
                                                                        }
                                                                )
                                    )
    new_password2 = forms.CharField(
                                    label='Confirm password', 
                                    widget=forms.PasswordInput(attrs={
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'New Password', 
                                                                        'id': 'form-new-pass2'
                                                                        }
                                                                )
                                    )

class UserEditForm(forms.ModelForm):
    
    email = forms.EmailField(
                            label='Email can not be changed', 
                            max_length=200, 
                            widget=forms.TextInput(
                                                    attrs={
                                                            'class': 'form-control', 
                                                            'placeholder': 'email', 
                                                            'id': 'form-email', 
                                                            'readonly': 'readonly'
                                                            }
                                                    )
                            )
    user_name = forms.CharField(
                                label='Username', 
                                min_length=4, 
                                max_length=50,
                                required = False, 
                                widget=forms.TextInput(
                                                        attrs={
                                                                'class': 'form-control', 
                                                                'placeholder': 'Username', 
                                                                'id': 'form-username', 
                                                                }
                                                        )
                                )
    first_name = forms.CharField(
                                label='Firstname', 
                                min_length=4, 
                                max_length=50, 
                                required = True,
                                widget=forms.TextInput(
                                                        attrs={
                                                                'class': 'form-control', 
                                                                'placeholder': 'Firstname', 
                                                                'id': 'form-firstname',
                                                                }
                                                        )
                                )
    last_name       = forms.CharField(
                                label='Lastname', 
                                min_length=4, 
                                max_length=50, 
                                required = True,
                                widget=forms.TextInput(
                                                        attrs={
                                                                'class': 'form-control', 
                                                                'placeholder': 'lastname', 
                                                                'id': 'form-lastname',
                                                                }
                                                        )
                                )
    country         = CountryField(
                                    blank_label='(select country)', 
                                    # required = False,
                                    )
    phone           = forms.CharField(
                                        max_length=100, 
                                required = False,
                                        widget=forms.TextInput(
                                                                attrs={
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'phone number', 
                                                                        'id': 'form-phone',
                                                                        }
                                                                )
                                    )
    landmark          = forms.CharField(
                                        max_length=200, 
                                required = False,
                                        widget=forms.TextInput(
                                                                attrs={
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'closest known location', 
                                                                        'id': 'form-lamdmark',
                                                                        }
                                                                )
                                    )
    town            = forms.CharField(
                                        max_length=200, 
                                required = False,
                                        widget=forms.TextInput(
                                                                attrs={
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'town', 
                                                                        'id': 'form-town',
                                                                        }
                                                                )
                                    )
    estate          = forms.CharField(
                                        max_length=200, 
                                required = False,
                                        widget=forms.TextInput(
                                                                attrs={
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'estate', 
                                                                        'id': 'form-estate',
                                                                        }
                                                                )
                                    )
    house_no        = forms.CharField(
                                        max_length=200, 
                                required = False,
                                        widget=forms.TextInput(
                                                                attrs={
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'house', 
                                                                        'id': 'form-house',
                                                                        }
                                                                )
                                    )
    class Meta:
        model = UserBase
        fields = ('email', 'user_name','first_name', 'last_name','gender', 'country','phone', 'landmark','town', 'estate', 'house_no')

class UserOrderForm(forms.ModelForm):
    
    
    first_name = forms.CharField(
                                label='Firstname', 
                                min_length=4, 
                                max_length=50, 
                                required = True,
                                widget=forms.TextInput(
                                                        attrs={
                                                                'class': 'form-control', 
                                                                'placeholder': 'Firstname', 
                                                                'id': 'form_firstname',
                                                                'readonly': 'readonly',
                                                                'type' : 'hidden'
                                                                }
                                                        )
                                )
    last_name       = forms.CharField(
                                label='Lastname', 
                                min_length=4, 
                                max_length=50, 
                                required = True,
                                widget=forms.TextInput(
                                                        attrs={
                                                                'class': 'form-control', 
                                                                'placeholder': 'lastname', 
                                                                'id': 'form_lastname',
                                                                'readonly': 'readonly',
                                                                'type' : 'hidden'
                                                                }
                                                        )
                                )
    phone           = forms.CharField(
                                        max_length=100, 
                                required = False,
                                        widget=forms.TextInput(
                                                                attrs={
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'phone number', 
                                                                        'id': 'form_phone',
                                                                        'readonly': 'readonly',
                                                                        'type' : 'hidden'
                                                                        }
                                                                )
                                    )
    landmark          = forms.CharField(
                                        max_length=200, 
                                required = False,
                                        widget=forms.TextInput(
                                                                attrs={
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'closest known location', 
                                                                        'id': 'form_lamdmark',
                                                                        'readonly': 'readonly',
                                                                        'type' : 'hidden'
                                                                        }
                                                                )
                                    )
    town            = forms.CharField(
                                        max_length=200, 
                                required = False,
                                        widget=forms.TextInput(
                                                                attrs={
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'town', 
                                                                        'id': 'form_town',
                                                                        'readonly': 'readonly',
                                                                        'type' : 'hidden'
                                                                        }
                                                                )
                                    )
    estate          = forms.CharField(
                                        max_length=200, 
                                required = False,
                                        widget=forms.TextInput(
                                                                attrs={
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'estate', 
                                                                        'id': 'form_estate',
                                                                        'readonly': 'readonly',
                                                                        'type' : 'hidden'
                                                                        }
                                                                )
                                    )
    house_no        = forms.CharField(
                                        max_length=200, 
                                required = False,
                                        widget=forms.TextInput(
                                                                attrs={
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'house', 
                                                                        'id': 'form_house',
                                                                        'readonly': 'readonly',
                                                                        'type' : 'hidden'
                                                                        }
                                                                )
                                    )
    class Meta:
        model = UserBase
        fields = ('first_name','last_name','phone', 'landmark','town', 'estate', 'house_no')
