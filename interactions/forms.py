from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control', 'required': True,
                       'placeholder': 'Add a Comment'}),
        }
        labels = {
            'content': 'Do you have any constructive feedback? Add a Comment',
        }
