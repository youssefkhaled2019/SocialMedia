from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,UpdateView,DeleteView)
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
    context={"posts":Post.objects.all()}
    return render(request,"blog/home.html",context)


class PostListView(LoginRequiredMixin,ListView):
    model=Post
    template_name ="blog/home.html" #<app>/<model>_<viewtype>.html
    context_object_name="posts"
    ordering=["-date_posted"]

class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post  
    fields=['title','content']
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author=self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post  
    fields=['title','content']
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author=self.request.user
        return super().form_valid(form)    
    
    def test_func(self) -> bool | None:
        post =self.get_object()
        if (self.request.user==post.author):
            return True
        return False
        


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model=Post
    success_url="/"
    def test_func(self) -> bool | None:
        post =self.get_object()
        if (self.request.user==post.author):
            return True
        return False

def about(request):
    return render(request,"blog/about.html",{"title":"about"})
