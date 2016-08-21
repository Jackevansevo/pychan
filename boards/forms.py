from django import forms

from .models import Thread, Reply


class ThreadCreateForm(forms.ModelForm):
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
    class Meta:
        model = Reply
        fields = ['content', 'image']

    def clean(self):
        # [TODO] Do this check in Javascript, no point sending a get request if
        # no data has been provided
        if self.cleaned_data['content'] == '' and self.cleaned_data['image'] is None:
            raise forms.ValidationError("Please provide some data")
