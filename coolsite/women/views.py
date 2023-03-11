from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404, request
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView, CreateView
from .forms import AddPostForm, RegisterUserForm, LoginUserForm
from .models import *
from .utils import DataMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
            {'title': "Добавить статью", 'url_name': 'add_page'},
            {'title': "Обратная связь", 'url_name': 'contact'}

            ]

class WomenHome(DataMixin, ListView):
    paginate_by = 3
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published = True).select_related('cat')


def about(request):
    return render(request, 'women/about.html', {'title' : 'O saite'})

def categories(request,catid):
    print(request.GET)
    return HttpResponse(f'<h1> Sttai po kategorijam </h1><p>{catid}</p>')

class AddPAge(CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

class ShowPost(DataMixin,DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))
# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         # 'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'women/post.html', context=context)

class ShowCategory(DataMixin, ListView):
    posts = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c=Category.objects.get(slug = self.kwargs['cat_slug'])
        c_def = self.get_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(cat__slug = self.kwargs['cat_slug'], is_published= True).select_related('cat')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

# def pageNotFound(request,exception):
#     return HttpResponseNotFound('<h1>Not correct path</h1>')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    # def get_success_url(self):
    #     return reverse_lazy('home')

def Logout_user(request):
    logout(request)
    return redirect('login')