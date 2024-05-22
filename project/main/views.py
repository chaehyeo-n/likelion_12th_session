from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone #Django에서 제공하는 시간 관련 유틸리티 모듈

from .models import Blog, Comment, Tag

# Create your views here.
def mainpage(request):
    context = {
        'generation': 12,
        'members': ['현아', '영심이', '티준'],
        'info':{'weather': '좋음', 'feeling': '배고픔(?)', 'note': '아기사자 화이팅!'}
    }
    return render(request, 'main/mainpage.html', context)
def secondpage(request):
    blogs = Blog.objects.all()
    return render(request, 'main/secondpage.html', {'blogs': blogs})
def new_blog(request):
    return render(request, 'main/new-blog.html')

def detail(request, id):
    blog = get_object_or_404(Blog, pk = id)
    if request.method == 'GET':
        comments = Comment.objects.filter(blog=blog)
        return render(request, 'main/detail.html', {'blog':blog, 'comments': comments})
    elif request.method == 'POST':
        new_comment = Comment()

        new_comment.blog = blog
        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        new_comment.pub_date = timezone.now()

        new_comment.save()

        words = new_comment.content.split(' ')
        tag_list = []

        for w in words: 
            if len(w)>0:
                if w[0] == '#':
                    tag_list.append(w[1:])

        for t in tag_list:
            tag, boolean = Tag.objects.get_or_create(name=t)
            new_comment.tags.add(tag.id)

        return redirect('main:detail', id)

def edit(request, id):
    edit_blog = Blog.objects.get(pk=id)
    return render(request, 'main/edit.html', {'blog' : edit_blog})

# 데이터베이스에 저장하는 함수
def create(request):
    if request.user.is_authenticated:
        new_blog = Blog()
    
        # POST로 들어오는 데이터를 new_blog 객체에 저장
        new_blog.title = request.POST['title']
        new_blog.writer = request.user
        new_blog.body = request.POST['body']
        new_blog.pub_date = timezone.now()
        new_blog.image = request.FILES.get('image')

        # new_blog 객체를 저장
        new_blog.save()

        words = new_blog.body.split(' ')
        tag_list = []

        for w in words:
            if len(w)>0:
                if w[0] == '#':
                    tag_list.append(w[1:])

        for t in tag_list:
            tag, boolean = Tag.objects.get_or_create(name=t)
            new_blog.tags.add(tag.id)

        return redirect('main:detail', new_blog.id)
    
    else:
        return redirect('accounts:login')

def update(request, id):
    update_blog = Blog.objects.get(pk=id)
    if request.user.is_authenticated and request.user == update_blog.writer:
        update_blog.title = request.POST['title']
        update_blog.body = request.POST['body']
        update_blog.pub_date = timezone.now()

        if request.FILES.get('image'):
            update_blog.image = request.FILES['image']

        update_blog.save()

        words = update_blog.body.split(' ')
        tag_list = []

        for w in words:
            if len(w)>0:
                if w[0] == '#':
                    tag_list.append(w[1:])

        for t in tag_list:
            tag, boolean = Tag.objects.get_or_create(name=t)
            update_blog.tags.add(tag.id)

        return redirect('main:detail', update_blog.id)
    return redirect('accounts:login', update_blog.id)

def delete(request, id):
    delete_blog = Blog.objects.get(pk=id)
    delete_blog.delete()
    return redirect('main:secondpage')

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'main/tag-list.html', { 'tags' : tags })

def tag_blogs(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    blogs = tag.blogs.all()
    comments = tag.comments.all()
    return render(request, 'main/tag-blog.html', {
        'tag': tag,
        'blogs' : blogs,
        'comments' : comments
    })