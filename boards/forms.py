from .models import Thread, Reply
from django.core.exceptions import ValidationError
from django.forms import ModelForm


class ThreadCreateForm(ModelForm):
    class Meta:
        model = Thread
        exclude = ['board', 'bump_count', 'expired']

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image._size > 4*1024*1024:
                raise ValidationError("Image file too large (> 4mb)")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['content', 'image']
