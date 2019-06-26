from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Subcategory, Note
from django.contrib.auth.decorators import login_required
from classifieds.forms import CreateNote, ImageFormSet
from django.utils import timezone
from django.contrib import messages
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def note_list(request):
    categories = Category.objects.all()
    notes = Note.objects.filter(is_active=True)

    paginator = Paginator(notes, 6) # 3 сообщения на каждой странице 
    page = request.GET.get('page') 
    try: 
        notes = paginator.page(page) 
    except PageNotAnInteger: 
        # Если страница не является целым числом, перемещаемся на первую страницу 
        notes = paginator.page(1) 
    except EmptyPage: 
        # Если страница за пределами допустимого диапазона перемещаемся на последнюю страницу 
        notes = paginator.page(paginator.num_pages) 

    return render(
                request,
                'classifieds/note/list.html',
                {'categories': categories, 'notes': notes}
    )


def note_list_by_category(request, category_slug):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = Subcategory.objects.filter(category=category)
        notes = Note.objects.filter(subcategory__in=subcategories).filter(is_active=True)

        paginator = Paginator(notes, 2) # 3 сообщения на каждой странице 
        page = request.GET.get('page') 
        try: 
            notes = paginator.page(page) 
        except PageNotAnInteger: 
            # Если страница не является целым числом, перемещаемся на первую страницу 
            notes = paginator.page(1) 
        except EmptyPage: 
            # Если страница за пределами допустимого диапазона перемещаемся на последнюю страницу 
            notes = paginator.page(paginator.num_pages)

    return render(
                request,
                'classifieds/note/list.html',
                {'category': category, 'subcategories': subcategories, 'notes': notes}
    )


def note_list_by_subcategory(request, category_slug=None, subcategory_slug=None):  
    if subcategory_slug:
        category = get_object_or_404(Category, slug=category_slug)
        subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
        notes = Note.objects.filter(subcategory=subcategory).filter(is_active=True)

        paginator = Paginator(notes, 2) # 3 сообщения на каждой странице 
        page = request.GET.get('page') 
        try: 
            notes = paginator.page(page) 
        except PageNotAnInteger: 
            # Если страница не является целым числом, перемещаемся на первую страницу 
            notes = paginator.page(1) 
        except EmptyPage: 
            # Если страница за пределами допустимого диапазона перемещаемся на последнюю страницу 
            notes = paginator.page(paginator.num_pages)

    return render(
                request,
                'classifieds/note/list.html',
                {'category': category, 'subcategory': subcategory, 'notes': notes}
    )


def note_detail(request, id, slug):
    note = get_object_or_404(Note, id=id, slug=slug, is_active=True)
    images = note.images.all()
    main_image = None
    if images:
        for i, im in enumerate(images):           
            if im.main or i == 0:
                main_image = im
    return render(
                request, 
                'classifieds/note/detail.html',
                {'note': note, 'images': images, 'main_image': main_image}
    )


@login_required
def create_note(request):
    if request.method == 'POST':
        form_note = CreateNote(request.POST)
        data_form = form_note.data.dict()
        if form_note.is_valid():
            new_note = form_note.save(commit=False)
            new_note.user = request.user
            new_note.subcategory = get_object_or_404(Subcategory, id=int(data_form['selectSubcategory']))
            new_note.save()
            formset = ImageFormSet(request.POST, request.FILES, instance=new_note)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Ваше объявление успешно создано!")
                return redirect('classifieds:note_detail', id=new_note.id, slug=new_note.slug)
    else:
        form_note = CreateNote()
        formset = ImageFormSet()
    categorys = Category.objects.all()
    subcategorys_js = {};
    for category in categorys:
        for subcategory in category.subcategory.all():           
            if subcategorys_js.get(category.id):
                subcategorys_js[category.id].update({subcategory.id: subcategory.name})
            else:
                subcategorys_js[category.id] = {subcategory.id: subcategory.name}
    subcategorys_js = json.dumps(subcategorys_js, ensure_ascii=False)
    subcategory_js = "false"
    category_js = "false"
    context = {
                'form_note': form_note,
                'formset': formset, 
                'categorys': categorys, 
                'subcategorys_js': subcategorys_js,
                'subcategory_js': subcategory_js,
                'category_js': category_js
    }
    return render(request, 'classifieds/note/create_update_note.html', context)


@login_required
def update_note(request, id=id):
    note = get_object_or_404(Note, id=id)
    subcategory_js = note.subcategory.id
    category_js = note.subcategory.category.id
    if request.method == 'POST' and note.user == request.user:
        form_note = CreateNote(request.POST, instance=note)
        data_form = form_note.data.dict()
        if form_note.is_valid():
            cd = form_note.cleaned_data
            edit_note = form_note.save(commit=False)
            edit_note.user = request.user
            edit_note.updated = timezone.now()
            if data_form.get('selectSubcategory'):
                edit_note.subcategory = get_object_or_404(Subcategory, id=int(data_form['selectSubcategory']))
            edit_note.save()
            formset = ImageFormSet(request.POST, request.FILES, instance=edit_note)
            if formset.is_valid():
                formset.save()
            messages.success(request, "Ваше сообщение успешно обновленно!")
            return redirect('classifieds:note_detail', id=edit_note.id, slug=edit_note.slug)
    elif request.method == 'GET' and note.user == request.user:        
        form_note = CreateNote(instance=note)
        formset = ImageFormSet(instance=note)
    elif note.user is not request.user:
        form_note = None
        formset = None        
        messages.error(request, "У Вас недостаточно прав чтобы редактировать это сообщение.")
    categorys = Category.objects.all()
    subcategorys_js = {};
    for category in categorys:
        for subcategory in category.subcategory.all():           
            if subcategorys_js.get(category.id):
                subcategorys_js[category.id].update({subcategory.id: subcategory.name})
            else:
                subcategorys_js[category.id] = {subcategory.id: subcategory.name}
    subcategorys_js = json.dumps(subcategorys_js, ensure_ascii=False)
    context = {
                'form_note': form_note, 
                'formset': formset, 
                'categorys': categorys, 
                'subcategorys_js': subcategorys_js,
                'subcategory_js': subcategory_js,
                'category_js': category_js,
                'note': note
    }
    print('note: ', note.user)
    return render(request, 'classifieds/note/create_update_note.html', context)


@login_required
def delete_note(request, id=id):
    note = get_object_or_404(Note, id=id)
    if note.user == request.user:
        note.delete()
        messages.success(request, "Ваше сообщение успешно удаленно!")
    else:
        messages.error(request, "У Вас недостаточно прав чтобы удалить это сообщение.")
    notes = Note.objects.filter(user=request.user)
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'notes': notes})
 
