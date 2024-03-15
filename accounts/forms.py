from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.core.exceptions import ValidationError

from .models import Profile
from .validators import validate_birth_date

User = get_user_model()


class CustomDateInput(forms.DateInput):
    """
    Custom date input widget with specific attributes.

    Attributes:
    - input_type (str): The type of input, set to 'date'.
    """

    input_type = 'date'

    def __init__(self, attrs=None, options=None):
        """
        Initialize the CustomDateInput widget.

        Parameters:
        - attrs (dict): Additional attributes for the widget.
        - options (dict): Additional options for the widget.
        """
        if attrs is None:
            attrs = {}
        if options is None:
            options = {}
        attrs.update({'class': 'form-control mb-3', 'data-date-format': 'yyyy-mm-dd'})
        attrs.update(options)
        super().__init__(attrs=attrs)


class RegisterForm(UserCreationForm):
    """
    Form for user registration.

    Inherits from UserCreationForm.

    Attributes:
    - Meta: Inner class defining the metadata for the form.
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the RegisterForm.

        Sets additional attributes for form fields.

        Parameters:
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.
        """
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control mt-2 mb-2'})


class LoginForm(forms.Form):
    """
    Form for user login.

    Inherits from forms.Form.

    Attributes:
    - email: Email field for the form.
    - password: Password field for the form.
    - remember_me: Checkbox field for remembering user login.
    """

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput({'class': 'form-check-input'})
    )


class BaseReactivationForm(forms.Form):
    """
    Base form for reactivating user account.

    Inherits from forms.Form.

    Attributes:
    - email: Email field for reactivation.
    """

    email = forms.EmailField(label='Your email',
                             required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        """
        Clean email field.

        Check if the user with provided email exists.

        Returns:
        - email (str): The cleaned email.

        Raises:
        - ValidationError: If the user with provided email doesn't exist.
        """
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise forms.ValidationError("User with this email doesn't exist")
        return email


class ReactivationForm(BaseReactivationForm):
    """
    Form for reactivating user account.

    Inherits from BaseReactivationForm.
    """

    pass


class PasswordSetForm(SetPasswordForm):
    """
    Form for setting user password.

    Inherits from SetPasswordForm.

    Attributes:
    - Meta: Inner class defining metadata for the form.
    """

    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]
        widgets = {
            'new_password1': forms.PasswordInput(),
            'new_password2': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the PasswordSetForm.

        Sets additional attributes for form fields.

        Parameters:
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.
        """
        super(PasswordSetForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control mt-2 mb-2'})


class ProfileForm(forms.ModelForm):
    """
    Form for user profile.

    Inherits from forms.ModelForm.

    Attributes:
    - Meta: Inner class defining metadata for the form.
    """

    class Meta:
        model = Profile
        fields = ('gender', 'date_of_birth', 'avatar', 'bio', 'info')

        labels = {
            'date_of_birth': 'Date of your Birth',
            'avatar': 'Avatar URL'
        }

        placeholders = {
            'avatar': 'Left empty to use gravatar',
            'bio': 'Write short biography',
            'info': 'Enter some additional information'
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the ProfileForm.

        Sets additional attributes for form fields.

        Parameters:
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.
        """
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control border border-4 mb-3',
                                       'placeholder': self.Meta.placeholders.get(field_name)})
        self.fields['date_of_birth'].widget = CustomDateInput()

    def clean_date_of_birth(self):
        """
        Clean date of birth field.

        Validate the date of birth.

        Returns:
        - data: Cleaned date of birth.

        Raises:
        - ValidationError: If date of birth is invalid.
        """
        data = self.cleaned_data['date_of_birth']
        try:
            validate_birth_date(data)
        except ValidationError as error:
            self.add_error('date_of_birth', str(error))
        return data