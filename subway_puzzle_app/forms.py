from django import forms

class TrainForm(forms.Form):
    train_1 = forms.CharField(label='', max_length=20, required=True)
    train_2 = forms.CharField(label='', max_length=20, required=False)
    train_3 = forms.CharField(label='', max_length=20, required=False)
    solution = forms.CharField(label='', max_length=1000, required=False)