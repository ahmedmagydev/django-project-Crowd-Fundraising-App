from django import forms
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.Form):
    comment_content = forms.CharField(
        label="add your comment", widget=CKEditorWidget(), min_length=1, max_length=100,
        error_messages={'required': "you can'tsubmit an empty comment"})

    def clean(self):
        cleaned_data = super().clean()
        comment_content = cleaned_data.get("comment_content")
        if not comment_content:
            msg = "comment can't be empty."
            self.add_error('comment_content', msg)
        self.cleaned_data
