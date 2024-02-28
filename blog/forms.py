from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Form for adding comments.
    """
    class Meta:
        """
        Meta class for defining form properties.
        """
        model = Comment
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Share your thoughts in the comments...',
                                          'class': 'form-control',
                                          'rows': 4})
        }

        labels = {
            'body': 'Add your comment'
        }
