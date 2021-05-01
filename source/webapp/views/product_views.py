    from django.shortcuts import render, get_object_or_404, redirect
    from ..models import Product, Category, Review
    from ..forms import SimpleSearchForm, ProductForm, ReviewForm
    from django.urls import reverse, reverse_lazy
    from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
    from django.db.models import Q
    from django.utils.http import urlencode
    from django.views.generic.edit import FormMixin
    from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class IndexView(ListView):
    template_name = 'product/index.html'
    context_object_name = 'products'
    model = Product
    ordering = ['-name', '-category']
    paginate_by = 5
    paginate_orphans = 2

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

class ProductView(FormMixin, DetailView):
    model = Product
    template_name = 'product/product_view.html'
    form_class = ReviewForm

class ProductCreateView(CreateView):
    template_name = 'product/product_add_view.html'
    form_class = ProductForm
    model = Product

    def form_valid(self, form):
        product = Product()
        for key, value in form.cleaned_data.items():
            setattr(product, key, value)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')

class ProductUpdateView(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'product/product_update_view.html'
    context_object_name = 'product'


    def get_success_url(self):
        return reverse('product', kwargs={'pk': self.kwargs.get('pk')})

class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
