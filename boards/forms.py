from django import forms
from captcha.fields import CaptchaField

from .models import Thread, Reply


class ThreadCreateForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Thread
        exclude = ['board', 'bump_count', 'expired']

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image._size > 4*1024*1024:
                raise forms.ValidationError("Image file too large (> 4mb)")
            return image
        else:
            raise forms.ValidationError("Couldn't read uploaded image")


class ReplyForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Reply
        fields = ['content', 'image']


class ThreadDeleteForm(forms.Form):
    OPTIONS = (
        ("O", "Offensive Content"),
        ("S", "Shit Post"),
        ("T", "Off-topic Discussion"),
        ("D", "Duplicate Thread"),
    )
    reason = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=OPTIONS
    )
