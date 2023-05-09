from django.forms import ModelForm, DateInput
from calendarapp.models import Event, EventMember
from django import forms


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["description", "assignment", "quiz"]
        # datetime-local is a HTML5 input type
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                }
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["user"]
