from django.urls import path
from . import views


app_name = 'classifieds'

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('create-note/', views.create_note, name='create_note'),
    path('update-note/<int:id>/', views.update_note, name='update_note'),
    path('delete-note/<int:id>/', views.delete_note, name='delete_note'),
    path('<slug:category_slug>/', views.note_list_by_category, name='note_list_by_category'),
    path('<int:id>/<slug:slug>/', views.note_detail, name='note_detail'),
    path('<slug:category_slug>/<slug:subcategory_slug>/', views.note_list_by_subcategory, name='note_list_by_subcategory'),
]

