from urllib.error import URLError

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from .models import ContactInquiry


class ResilientReCaptchaField(ReCaptchaField):
    """Fail closed without turning a CAPTCHA network outage into a 500."""

    def validate(self, value):
        if getattr(settings, "RECAPTCHA_TESTING", False):
            if value != "PASSED":
                raise ValidationError(
                    self.error_messages["captcha_invalid"],
                    code="captcha_invalid",
                )
            return

        try:
            return super().validate(value)
        except URLError as error:
            raise ValidationError(
                self.error_messages["captcha_error"],
                code="captcha_error",
            ) from error


class ContactInquiryForm(forms.ModelForm):
    captcha = ResilientReCaptchaField(widget=ReCaptchaV2Checkbox())

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
