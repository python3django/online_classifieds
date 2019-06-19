from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
#from django.utils.text import slugify
from uuslug import slugify # slugify из библеотеки django-uuslug делает транслитерацию кирилици в латиницу
from django.utils.safestring import mark_safe


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('classifieds:note_list_by_category', args=[self.slug])


class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('classifieds:note_list_by_subcategory', args=[self.category.slug, self.slug])


class Note(models.Model):
    subcategory = models.ForeignKey(Subcategory, related_name='note', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='E-mail')
    messenger = models.CharField(max_length=200, db_index=True, verbose_name='Мессенджер', blank=True)

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('classifieds:note_detail', args=[self.id, self.slug])

    # создаем slug из name, в случае если сообщеие создано через интерфейс сайта (а не через админку)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Note, self).save(*args, **kwargs)


class Image(models.Model):
    note = models.ForeignKey(Note, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='note/%Y/%m/%d', verbose_name='Изображение')

    def get_absolute_url(self):
        return "{0}".format(self.image.url)

    def image_img(self):
        return mark_safe(u'<a href="{0}"><img src="{0}" style="height: 50px; width: 50px;"></a>'.format(self.image.url))
