from django.urls import path
from .views import *

app_name = "main"
urlpatterns = [
    path('', mainpage, name="mainpage"),
    path('second', secondpage, name="secondpage"),
    path('new-blog', new_blog, name="new-blog"),
    path('create', create, name="create"),
    path('<int:id>', detail, name="detail"),
    path('edit/<int:id>', edit, name="edit"),
    path('update/<int:id>', update, name="update"),
    path('delete/<int:id>', delete, name="delete"),
    path('tag-list', tag_list, name="tag-list"),
    path('tag-blogs/<int:tag_id>', tag_blogs, name="tag-blogs"),
]