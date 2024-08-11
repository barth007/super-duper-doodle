from django import forms

class SubscriberForm (forms.Form):
    email = forms.EmailField(
        label="Enter your Email",
        max_length=100,
        widget=forms.EmailInput(attrs={'class':'form-controls'})


    )