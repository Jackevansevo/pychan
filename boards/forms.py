from django import forms
from captcha.fields import ReCaptchaField

from .models import Thread, Reply


class CaptchaFormMixin(forms.Form):
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(CaptchaFormMixin, self).__init__(*args, **kwargs)
        self.fields['captcha'].error_messages = {
            'required': "Oops, please proove you're not a robot"
        }


class ThreadCreateForm(CaptchaFormMixin, forms.ModelForm):

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


class ReplyForm(CaptchaFormMixin, forms.ModelForm):

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
