from django import forms

class ProductCreateForm(forms.Form):
    image = forms.FileField(required=False)
    title = forms.CharField(max_length=36, min_length=5)
    description = forms.CharField(widget=forms.Textarea())

