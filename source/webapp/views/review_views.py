from django.shortcuts import render, get_object_or_404, redirect
from ..models import Product, Category, Review
from ..forms import SimpleSearchForm, ProductForm, ReviewForm
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.db.models import Q
from django.utils.http import urlencode
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ReviewCreate(CreateView):

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




