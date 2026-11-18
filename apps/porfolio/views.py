from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

from .forms import ContactInquiryForm


def contact(request):
    if request.method == "POST":
        form = ContactInquiryForm(
            request.POST,
            remote_ip=request.META.get("REMOTE_ADDR"),
        )

        if form.is_valid():
            inquiry = form.save()

            notification_email = EmailMessage(
                subject=f"New portfolio inquiry from {inquiry.name}",
                body=(
                    f"Name: {inquiry.name}\n"
                    f"Email: {inquiry.email}\n"
                    f"Industry: {inquiry.get_industry_display()}\n\n"
                    f"Inquiry:\n{inquiry.inquiry}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.DEFAULT_FROM_EMAIL],
                reply_to=[inquiry.email],
            )

            notification_email.send(fail_silently=False)

            confirmation_email = EmailMessage(
                subject="Thanks for reaching out",
                body=(
                    f"Hi {inquiry.name},\n\n"
                    "Thanks for reaching out through my portfolio.\n\n"
                    "I've received your inquiry and will get back to you "
                    "as soon as I can.\n\n"
                    "Best regards,\n"
                    "Joshua De Leon\n"
                    "GIS Software Developer"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[inquiry.email],
            )

            confirmation_email.send(fail_silently=False)

            messages.success(
                request,
                "Thanks for reaching out. I'll get back to you soon.",
            )

            return redirect("contact")

    else:
        form = ContactInquiryForm()

    return render(
        request,
        "porfolio/contact.html",
        {
            "form": form,
            "turnstile_enabled": settings.TURNSTILE_ENABLED,
            "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
        },
    )
