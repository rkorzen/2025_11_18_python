from django.http import HttpResponse
from django.shortcuts import render

from posts.adapters import FakeDatabaseAdapter, DjangoAdapter
from posts.service import PostService

from .models import Post
# Create your views here.

def post_list(request):
    # return HttpResponse("Lista Postow")
    return render(
        request,
        "posts/list.html",
        {"x": 1, "y": [1, 2, 3], "posts": PostService().get_posts(db=DjangoAdapter())}
    )

def post_detail(request, id):
    p = Post.objects.get(id=id)
    context= {"post": p}
    return render(
        request,
        "posts/detail.html",
        context

    )