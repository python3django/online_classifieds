from django.contrib import admin
from .models import Category, Subcategory, Note, Image


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ImageInline(admin.TabularInline):
    model = Image
    raw_id_fields = ['note']
    readonly_fields = ("image_img",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'price', 'is_active', 'created', 'updated']
    list_display_links = ['name']
    list_filter = ['is_active', 'created', 'updated']
    list_editable = ['price', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ImageInline]


