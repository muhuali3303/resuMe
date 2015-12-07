from django import forms
from resuMe.models import *


# form for register
class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=20, label='Password')
    password2 = forms.CharField(max_length=20, label='Confirm Password')
    email = forms.EmailField(max_length=40, label='Email')

    # customize form validation
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        # return cleanned data
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # username not include in database
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        # return cleanned data
        return username


# Form for sign in
class SignInForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username or not len(username):
            raise forms.ValidationError("user name is required")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password or not len(password):
            raise forms.ValidationError("password is required")
        return password


# Form for change First name, Last name and Summary
class FLSForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = UserInfo
        fields = ['summary', 'photo']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name or not len(first_name):
            raise forms.ValidationError("first name is required")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name or not len(last_name):
            raise forms.ValidationError("last name is required")
        return last_name


# Form for edit about
class AboutForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['about']


# Form for edit Address, Phone, and Email
class APEForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = UserInfo
        fields = ['address', 'phone']


# Form for Block Content
class BlockContentForm(forms.ModelForm):
    class Meta:
        model = BlockContent
        exclude = ('block', 'index')
        widgets = {'sub_title': forms.TextInput(),
                   'content': forms.TextInput(),
                   'url': forms.TextInput(),
                   }

    def clean_sub_title(self):
        sub_title = self.cleaned_data.get('sub_title')
        if not sub_title or not len(sub_title):
            raise forms.ValidationError("sub title is required")
        return sub_title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or not len(content):
            raise forms.ValidationError("content is required")
        return content


# Form for pictures in Block Content
class BlockContentPicForm(forms.ModelForm):
    class Meta:
        model = Picture
        exclude = ('blockcontent', 'description',)


# Form for send email
class EmailForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    message = forms.CharField(max_length=400)

    def clean_name(self):
        toClean = self.cleaned_data.get('name')
        if not toClean or not len(toClean):
            raise forms.ValidationError("name is required")
        return toClean

    def clean_email(self):
        toClean = self.cleaned_data.get('email')
        if not toClean or not len(toClean):
            raise forms.ValidationError("email is required")
        return toClean

    def clean_message(self):
        toClean = self.cleaned_data.get('message')
        if not toClean or not len(toClean):
            raise forms.ValidationError("message is required")
        return toClean