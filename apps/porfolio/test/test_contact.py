from unittest.mock import patch

from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse

from apps.porfolio.forms import ContactInquiryForm
from apps.porfolio.models import ContactInquiry


class ContactInquiryFormTests(TestCase):

    def test_valid_contact_form(self):
        form = ContactInquiryForm(
            {
                "name": "Test User",
                "email": "test@example.com",
                "industry": "other",
                "inquiry": "Testing the contact form.",
            }
        )

        self.assertTrue(form.is_valid())

    def test_contact_form_saves(self):
        form = ContactInquiryForm(
            {
                "name": "Test User",
                "email": "test@example.com",
                "industry": "other",
                "inquiry": "Testing the contact form.",
            }
        )

        self.assertTrue(form.is_valid())

        inquiry = form.save()

        self.assertIsNotNone(inquiry.pk)
        self.assertEqual(inquiry.name, "Test User")
        self.assertEqual(inquiry.email, "test@example.com")
        self.assertEqual(inquiry.industry, "other")


class ContactViewTests(TestCase):

    def test_contact_page_loads(self):
        response = self.client.get(reverse("contact"))

        self.assertEqual(response.status_code, 200)

        self.assertIsInstance(
            response.context["form"],
            ContactInquiryForm,
        )

    @patch("apps.porfolio.views.EmailMessage.send")
    def test_contact_form_submission(self, mock_send):
        mock_send.return_value = 1

        response = self.client.post(
            reverse("contact"),
            {
                "name": "Test User",
                "email": "test@example.com",
                "industry": "other",
                "inquiry": "Testing the production contact form.",
            },
        )

        # Redirect after successful submission
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("contact"))

        # Inquiry is saved
        self.assertEqual(
            ContactInquiry.objects.count(),
            1,
        )

        inquiry = ContactInquiry.objects.first()

        self.assertEqual(inquiry.name, "Test User")
        self.assertEqual(inquiry.email, "test@example.com")
        self.assertEqual(inquiry.industry, "other")

        # Two emails should be sent:
        # 1. Notification to Joshua
        # 2. Confirmation to the visitor
        self.assertEqual(mock_send.call_count, 2)

        notification_email = mock_send.call_args_list[0][0]
        confirmation_email = mock_send.call_args_list[1][0]

        self.assertEqual(
            notification_email,
            (),
        )

        self.assertEqual(
            confirmation_email,
            (),
        )

    def test_invalid_submission_preserves_input_without_saving_or_emailing(self):
        payload = {
            "name": "Parcel mapping client", "email": "invalid-address",
            "industry": "real_estate", "inquiry": "Convert our masterplan drawings to GIS.",
        }
        response = self.client.post(reverse("contact"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.context["form"].errors)
        self.assertContains(response, payload["inquiry"])
        self.assertFalse(ContactInquiry.objects.exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_submission_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse("contact"), {
            "name": "Parcel mapping client", "email": "client@example.com",
            "industry": "real_estate", "inquiry": "Convert a masterplan to WebGIS.",
        })
        self.assertEqual(response.status_code, 403)
        self.assertFalse(ContactInquiry.objects.exists())
        self.assertEqual(len(mail.outbox), 0)
