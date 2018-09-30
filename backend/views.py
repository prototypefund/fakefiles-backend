from parler.views import TranslatableSlugMixin

from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import Item, Tag


class ItemDetailView(TranslatableSlugMixin, DetailView):
    template_name = 'views/item-detail/item_detail.html'
    model = Item

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['share_title'] = self.object.name
        return context


class ItemListView(ListView):
    template_name = 'views/index/index.html'
    model = Item

    def post(self, request):
        image_url = request.POST.get('image_url')
        if image_url:
            # do the search
            setattr(self, 'results', [])
        return self.get(request)

    def get_queryset(self):
        if hasattr(self, 'results'):
            return super().get_queryset().filter(id__in=self.results)
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        tag = self.request.GET.get('tag')
        cat = self.request.GET.get('cat')
        if q:
            ids = qs.filter(
                Q(translations__name__icontains=q) |
                Q(tags__name__icontains=q) |
                Q(category__name__icontains=q) |
                Q(translations__description__icontains=q)
            ).values_list('id', flat=True)
            return qs.filter(id__in=ids)
        elif tag:
            return qs.filter(tags__translations__name=tag)
        elif cat:
            return qs.filter(category__translations__name=cat)
        return qs.order_by('?')[:10]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        objects = context.get('object_list')
        if not objects:
            context['object_list'] = Item.objects.order_by('?')[:10]
            context['no_results'] = True
        context['helper_text_tags'] = Tag.objects.order_by('?')[:5]
        context['count'] = Item.objects.count()
        context['q'] = self.request.GET.get('q') or self.request.GET.get('tag') or self.request.GET.get('cat')
        context['share_title'] = 'Fakefiles.org – %s' % (context['q'] or 'Home')
        return context
