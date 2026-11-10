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
                    "placeholder": "Tell me about the role or project — your spatial data, goals, tools (QGIS, ArcGIS, WebGIS...), timeline, and how you'd like to work together...",
                    "rows": 7,
                }
            ),
        }
