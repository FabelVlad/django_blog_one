# from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
# from django.urls import reverse
from django.views.generic import View
from django.db.models import Q

from .forms import TagForm, PostForm
from .models import Tag, Post
from .uttils import ObjectDetaiMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin


class PostDetail(ObjectDetaiMixin, View):
    model = Post
    template = 'st_case/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'st_case/post_create_form.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'st_case/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'st_case/post_delete_form.html'
    redirect_url = 'post_list_url'
    raise_exception = True


class TagDetail(ObjectDetaiMixin, View):
    model = Tag
    template = 'st_case/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'st_case/tag_create.html'
    raise_exception = True
    # def get(self, request):
    #     form = TagForm()
    #     return render(request, 'st_case/tag_create.html', context={'form': form})
    #
    # def post(self, request):
    #     bound_form = TagForm(request.POST)
    #     if bound_form.is_valid():
    #         new_tag = bound_form.save()
    #         return redirect(new_tag)
    #     return render(request, 'st_case/tag_create.html', context={'form': bound_form})


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'st_case/tag_update_form.html'
    raise_exception = True
    # def get(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     bound_form = TagForm(instance=tag)
    #     return render(request, 'st_case/tag_update_form.html', context={'form': bound_form, 'tag': tag})
    #
    # def post(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     bound_form = TagForm(request.POST, instance=tag)
    #     if bound_form.is_valid():
    #         new_tag = bound_form.save()
    #         return redirect(new_tag)
    #     return render(request, 'st_case/tag_update_form.html', context={'form': bound_form, 'tag': tag})


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'st_case/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True
    # def get(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     return render(request, 'st_case/tag_delete_form.html', context={'tag': tag})
    #
    # def post(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     tag.delete()
    #     return redirect(reverse('tags_list_url'))


def index(request):
    search_query = request.GET.get('search_query', '')
    if search_query:
        posts = Post.objects.filter(Q(title__contains=search_query) | Q(body__contains=search_query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 2)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        previous_page_url = f'?page={page.previous_page_number()}'
    else:
        previous_page_url = ''

    if page.has_next():
        next_page_url = f'?page={page.next_page_number()}'
    else:
        next_page_url = ''

    context = {
        'page': page,
        'is_paginated': is_paginated,
        'next_page_url': next_page_url,
        'previous_page_url': previous_page_url
    }
    return render(request, 'st_case/index.html', context=context)


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'st_case/tags_list.html', context={'tags': tags})
