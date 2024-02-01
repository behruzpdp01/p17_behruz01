from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView

from apps.forms import RegisterForm, EmailForm
from apps.mixins import NotLoginRequiredMixin
from apps.models import Blog, Category


class IndexView(TemplateView):
    template_name = 'apps/index.html'


class BlogListView(ListView):
    template_name = 'apps/blogs/blog-list.html'
    queryset = Blog.objects.order_by('-created_at')
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        if search := self.request.GET.get("search"):
            return queryset.filter(name__icontains=search)
        return queryset


class BlogDetailView(DetailView):
    template_name = 'apps/blogs/blog-details-left-sidebar.html'
    queryset = Blog.objects.all()
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CustomLoginView(NotLoginRequiredMixin, LoginView):
    template_name = 'apps/login-register.html'
    next_page = 'index'


class RegisterFormView(FormView):
    template_name = 'apps/login-register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ShopListView(TemplateView):
    template_name = 'apps/blogs/shop-list.html'


class EmailView(FormView):
    template_name = 'apps/index.html'
    form_class = EmailForm
    success_url = '.'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('.', self.get_context_data(form=form))
