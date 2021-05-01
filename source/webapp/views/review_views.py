from django.shortcuts import  get_object_or_404
from ..models import Product, Review
from ..forms import ReviewForm, ModerateForm
from django.urls import reverse
from django.views.generic import DeleteView, UpdateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class ReviewListView(PermissionRequiredMixin, ListView):
    template_name = 'review/reviews_list.html'
    context_object_name = 'reviews'
    model = Review
    ordering = ['-updated_at']
    paginate_by = 5
    paginate_orphans = 2
    permission_required = 'webapp.moderate'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(is_moderated=True)
        return queryset

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

    def get_context_data(self, **kwargs):
        if 'moderate_form' not in kwargs:
            kwargs['moderate_form'] = self.get_moderate_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        moderate_form = self.get_moderate_form()
        if form.is_valid() and moderate_form.is_valid():
            user = self.request.user
            if not user.groups.filter(name='Moderators').exists():
                self.object.is_moderated=False
            return self.form_valid(form, moderate_form)
        else:
            return self.form_invalid(form, moderate_form)

    def has_permission(self):
        return self.get_object().author == self.request.user or super().has_permission()

    def form_valid(self, form, moderate_form):
        response = super().form_valid(form)
        moderate_form.save()
        return response

    def form_invalid(self, form, moderate_form):
        context = self.get_context_data(form=form, moderate_form=moderate_form)
        return self.render_to_response(context)

    def get_moderate_form(self):
        form_kwargs = {'instance': self.object}
        print(form_kwargs)
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            print(form_kwargs['data'])
        return ModerateForm(**form_kwargs)


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




