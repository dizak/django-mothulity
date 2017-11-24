from django import forms


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}))


class OptionsForm(forms.Form):
    job_name = forms.CharField(label="job-name",
                               max_length=20)
    notify_email = forms.CharField(label="notify-email",
                                   max_length=40)
