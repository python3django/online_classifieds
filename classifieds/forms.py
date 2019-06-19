from django import forms
from classifieds.models import Note, Image
from django.forms import inlineformset_factory


class CreateNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('name', 'description', 'price', 'phone', 'email', 'messenger')
        widgets = {'description': forms.Textarea(attrs={'rows':10, 'cols':80}),}
        labels = {
                'name': 'Название сообщения',
                'description': 'Описание',
                'price': 'Цена',
                'phone': 'Телефон',
                'email': 'E-mail',
                'messenger': 'Месседжер'
        }


ImageFormSet = inlineformset_factory(
                            Note, 
                            Image, 
                            fields=('image',), 
                            labels={'image': 'Картинка'}
)

