from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """Formulaire pour créer/modifier un post"""

    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Partagez quelque chose avec votre réseau...',
                'style': 'resize: none; border: none; outline: none; background-color: #f3f2ef;'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'style': 'display: none;'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = True
        self.fields['image'].required = False

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError('Le contenu ne peut pas être vide.')
        return content.strip()

class CommentForm(forms.ModelForm):
    """Formulaire pour ajouter un commentaire"""

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ajouter un commentaire...',
                'style': 'border: none; outline: none; background-color: #f3f2ef;'
            })
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError('Le commentaire ne peut pas être vide.')
        return content.strip()
