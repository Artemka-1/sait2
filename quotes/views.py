from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Quote, Author, Tag
from .forms import AuthorForm, QuoteForm


def quote_list(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 5)
    page = request.GET.get('page')
    quotes = paginator.get_page(page)

    top_tags = Tag.objects.annotate(num=Count('quote')).order_by('-num')[:10]

    return render(request, 'quotes.html', {
        'quotes': quotes,
        'top_tags': top_tags
    })


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, 'author.html', {'author': author})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.created_by = request.user
            quote.save()

            tags = request.POST['tags'].split(',')
            for tag in tags:
                tag_obj, _ = Tag.objects.get_or_create(name=tag.strip())
                quote.tags.add(tag_obj)

            return redirect('home')
    else:
        form = QuoteForm()

    return render(request, 'add_quote.html', {'form': form})


def quotes_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    quotes = Quote.objects.filter(tags=tag)
    return render(request, 'quotes.html', {'quotes': quotes})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
