from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)


@register_setting
class WebsiteSettings(BaseSiteSetting):
    website_name = models.CharField(max_length=128, null=True)
    website_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    slogan = models.CharField(max_length=255, null=True)

    panels = [
        FieldPanel('website_name'),
        FieldPanel('website_logo'),
        FieldPanel('slogan'),
    ]

@register_setting
class SocialMediaSettings(BaseGenericSetting):
    instagram = models.URLField(null=True)
    tiktok = models.URLField(null=True)
    telegram = models.URLField(null=True)
    youtube = models.URLField(null=True)
    whatsapp = models.URLField(null=True)

    panels = [
        FieldPanel('instagram'),
        FieldPanel('tiktok'),
        FieldPanel('telegram'),
        FieldPanel('youtube'),
        FieldPanel('whatsapp'),
    ]


@register_setting
class MobileApplicationSettings(BaseGenericSetting):
    google_play = models.URLField(null=True)
    app_store = models.URLField(null=True)
    app_gallery = models.URLField(null=True)

    panels = [
        FieldPanel('google_play'),
        FieldPanel('app_store'),
        FieldPanel('app_gallery'),
    ]
