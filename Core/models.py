from django.db import models
from django.contrib.sites.models import Site

class SiteInformation(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)

    site_name = models.CharField(max_length=225, null=True, blank=True)
    
    logo = models.ImageField(upload_to='site-logo/', blank=True, null=True, help_text="Image should be 588 x 137 pixels or will get resized on upload")
    favicon = models.ImageField(upload_to='site-favicon/', blank=True, null=True, help_text="Image should be 128 x 128 pixels or will get resized on upload")

    facebook_link = models.URLField(blank=True, null=True, help_text="Link to the Facebook page")
    twitter_link = models.URLField(blank=True, null=True, help_text="Link to the Twitter profile")
    instagram_link = models.URLField(blank=True, null=True, help_text="Link to the Instagram profile")
    tiktok_link = models.URLField(blank=True, null=True, help_text="Link to the Tiktok profile")

    address = models.TextField(blank=True, null=True, help_text="Physical address of the site")
    contact_email = models.EmailField(blank=True, null=True, help_text="Contact email address for inquiries")
    contact_number = models.CharField(max_length=20, blank=True, null=True, help_text="Contact phone number")

class Testimonial(models.Model):

    name = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.name

class FlashMessage(models.Model):
    highlighted_text = models.CharField(max_length=255, null=True, blank=True, help_text="Text to highlight in the flash message")
    message = models.TextField(help_text="The content of the flash message")
    published = models.BooleanField(default=False, help_text="Indicates whether the flash message is currently active")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the flash message was created")

    def __str__(self):
        return self.message[:50]  # Return first 50 characters of the message

    class Meta:
        verbose_name = 'Flash Message'
        verbose_name_plural = 'Flash Messages'