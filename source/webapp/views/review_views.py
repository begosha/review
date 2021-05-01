from django.shortcuts import render, get_object_or_404, redirect
from ..models import Product, Category, Review
from ..forms import SimpleSearchForm, ProductForm, ReviewForm
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.db.models import Q
from django.utils.http import urlencode
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ReviewCreate(LoginRequiredMixin, CreateView):

    form_class = ReviewForm
    model = Review

    def get_success_url(self):
        return reverse(
            'product',
            kwargs={'pk': self.kwargs.get('pk')}
        )

    def form_valid(self, form):
        product = get_object_or_404(Product, id=self.kwargs.get('pk'))
        review = form.instance
        review.product = product
        review.author = self.request.user
        return super().form_valid(form)

class ReviewUpdateView(PermissionRequiredMixin, UpdateView):
    model = Review
    template_name = 'review/review_update.html'
    form_class = ReviewForm
    context_object_name = 'review'
    permission_required = 'webapp.change_review'

    def has_permission(self):
        return self.get_object().author == self.request.user or super().has_permission()

    def get_success_url(self):
        return reverse('product', kwargs={'pk': self.object.product.pk})

class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    model = Review
    permission_required = 'webapp.delete_review'

    def has_permission(self):
        return self.get_object().author == self.request.user or super().has_permission()

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('product', kwargs={'pk': self.object.product.pk})




