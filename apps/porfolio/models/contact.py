from django.db import models


class ContactInquiry(models.Model):
    INDUSTRY_CHOICES = [
        ("government", "Government / LGU"),
        ("utilities", "Utilities"),
        ("real_estate", "Real Estate"),
        ("engineering", "Engineering / Construction"),
        ("agriculture", "Agriculture"),
        ("technology", "Technology"),
        ("research", "Research / Academia"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    industry = models.CharField(
        max_length=50,
        choices=INDUSTRY_CHOICES,
    )
    inquiry = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.name} — {self.industry}"