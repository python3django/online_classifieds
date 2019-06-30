from django import forms
from classifieds.models import Note, Image
from django.forms import inlineformset_factory


class SearchForm(forms.Form):
    query = forms.CharField(label='Введите Ваш запрос', widget=forms.TextInput(attrs={'size':'50'}))


class CreateNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('name', 'description', 'price', 'phone', 'email', 'messenger')
        widgets = {
                    'name': forms.TextInput(attrs={'size':80}),
                    'description': forms.Textarea(attrs={'rows':10, 'cols':80}),
        }
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
                                        fields=('image', 'main'), 
                                        labels={'image': 'Картинка', 'main': 'Сделать основным изображением'},
                                        extra=5,
                                        max_num=5
                                     )

