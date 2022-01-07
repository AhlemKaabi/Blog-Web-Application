from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from .models import Post
# class views!
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.models import User

# def home(request):
    # render all the posts
    # context = {
    #     'posts': Post.objects.all()
    # }
    # return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class PostListView(ListView):
    model = Post # what model to query
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts' # changing the default object list name!
    ordering = ['-date_posted'] # '-' => reverse
    paginate_by = 5 # simply calling the paginator object


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        """
            List posts for a user, change the QuerySet
        """
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # get_object_or_404 = a query to the db
        # get the user object from the User Model
        # with username= from the url ==>
        # kwargs: the query parameters
        # get() get the username string from the url
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # This create view contain a form => we specify the fields.
    fields = ['title', 'content']

    def form_valid(self, form):
        """
            for each Post => an author
            link the post (instance)created to the current user
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
            With the help of UserPassesTestMixin
            This function prevent any user from trying to update
            someone's else post!
        """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # success_url: telling django where to redirect after
    # deleting the post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False