from django import forms

from .models import ContactInquiry


class ContactInquiryForm(forms.ModelForm):
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
                    "placeholder": "Describe your CAD drawings, parcel records, or masterplan, the location, expected outputs, and handover needs...",
                    "rows": 7,
                }
            ),
        }
