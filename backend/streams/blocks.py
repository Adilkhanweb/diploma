"""StreamFields"""
from django.utils.translation import gettext_lazy as _
from wagtail import blocks


class TitleAndTextBlock(blocks.StructBlock):
    """Title and Text block"""
    title = blocks.CharBlock(max_length=128, required=True, help_text=_("Add your Title"))
    text = blocks.TextBlock(required=True, help_text=_("Add additional text"))

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"