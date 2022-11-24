#FORMS USED IN HTML
from django import forms

## input of form to test existing password's strength
class passwordInput(forms.Form):
    # hidden value that will let us know whether it was this form or the other that was filled
    password_input = forms.CharField(max_length=64,)

# Form to get a new password randomly
class RandomGeneratorInput(forms.Form):
    # generator = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    ## min length of password has to be 8, max is 64
    size = forms.IntegerField(max_value=64,min_value=8)
    ## if use special chars
    use_special = forms.BooleanField(initial=True,required=False)
    use_uppercase = forms.BooleanField(initial=True,required=False)
    use_lowercase = forms.BooleanField(initial=True,required=False)
    use_numbers = forms.BooleanField(initial=True,required=False)

class PersonalizedGeneratorInput(forms.Form):
    word_or_phrase = forms.CharField(label="Words or phrases you will remember",min_length=3,max_length=40,initial='apple,cake')
    numbers = forms.CharField(label="Numbers ",max_length=40)
    special_e = forms.CharField(label="Special element (these will be taken as words) ",max_length=40)
    symbols = forms.CharField(label="Symbols ",max_length=21)
   

