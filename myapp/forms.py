from django import forms
from myapp.models import Order, Student


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courses', 'student', 'levels', 'order_date']
        widgets = {
            'student': forms.RadioSelect(),
            'order_date': forms.SelectDateWidget()
        }

    def clean(self):
        for cors in self.cleaned_data['courses']:
            if cors.stages < self.cleaned_data['levels']:
                print("success")
                raise forms.ValidationError('You exceeded the number of levels for this course.')


class InterestForm(forms.Form):
    CHOICES = [('1', 'Yes'), ('2', 'No')]
    interested = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect)
    levels = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(widget=forms.Textarea, required=False, label="Additional Comments")


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Student
        fields = ('username', 'password')


class RegisterForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('username', 'password', 'first_name', 'last_name', 'city', 'interested_in')
