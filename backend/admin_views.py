# bc of a bug somehow related to parler and admin inline:

# IntegrityError at /admin/backend/item/add/
# insert or update on table "backend_item_translation" violates foreign key constraint "backend_item_translation_master_id_fa0d05e0_fk_backend_item_id"  # noqa
# DETAIL:  Key (master_id)=(cae9455b-016e-4434-b464-31282698838f) is not present in table "backend_item".

# this view is for the purpose to first create an item w/o inline formsets,
# to edit it later then in the admin w/ additional inline formsets

from parler.views import TranslatableCreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Item


class ItemCreateView(LoginRequiredMixin, TranslatableCreateView):
    template_name = 'views/item-create/item_form.html'
    model = Item
    fields = ('name', 'category', 'tags', 'description')

    def get_success_url(self):
        return reverse('admin:backend_item_change', kwargs={'object_id': self.object.pk})
