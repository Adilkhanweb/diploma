from django import forms

from discussions.models import Reply, Discussion


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('description',)


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ('title', 'description',)
