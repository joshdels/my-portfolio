from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from .models import ContactInquiry


class ContactInquiryForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = ContactInquiry
        fields = ["name", "email", "industry", "inquiry"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Your name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                }
            ),
            "industry": forms.Select(
                attrs={
                    "placeholder": "Select your industry",
                }
            ),
            "inquiry": forms.Textarea(
                attrs={
                    "placeholder": "Tell me about the role, project, or GIS problem you'd like to discuss...",
                    "rows": 7,
                }
            ),
        }
