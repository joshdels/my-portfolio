import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import ContactInquiry


TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


def verify_turnstile(token, remote_ip=None):
    """Validate a single-use Turnstile token with Cloudflare."""
    if getattr(settings, "TURNSTILE_TESTING", False):
        return token == "PASSED"

    payload = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": token,
    }
    if remote_ip:
        payload["remoteip"] = remote_ip
    request = Request(
        TURNSTILE_VERIFY_URL,
        data=urlencode(payload).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urlopen(request, timeout=settings.TURNSTILE_VERIFY_TIMEOUT) as response:
            result = json.load(response)
    except (OSError, URLError, ValueError, json.JSONDecodeError):
        return False
    return result.get("success") is True


class ContactInquiryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.remote_ip = kwargs.pop("remote_ip", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not getattr(settings, "TURNSTILE_ENABLED", False):
            return cleaned_data
        token = self.data.get("cf-turnstile-response", "")
        if not token or not verify_turnstile(token, self.remote_ip):
            raise ValidationError(
                "Please complete the security check and try again.",
                code="turnstile_invalid",
            )
        return cleaned_data

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
