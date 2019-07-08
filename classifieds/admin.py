from django.contrib import admin
from .models import Rubric, Category, Subcategory, Note, Image


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'rubric']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('rubric',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('category',)


class ImageInline(admin.TabularInline):
    model = Image
    raw_id_fields = ['note']
    readonly_fields = ("image_img",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'subcategory', 'price', 'is_active', 'created']
    list_display_links = ['name']
    list_filter = ['is_active', 'created', 'updated']
    list_editable = ['price', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('subcategory',)
    inlines = [ImageInline]


