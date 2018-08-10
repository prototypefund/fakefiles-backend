from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from reversion.admin import VersionAdmin

from .mixins.admin import AbstractVisibleModelAdmin
from .models import Category, Tag, Image, Item, FactCheck, Occurence, Source, Claim


class ReferenceForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get('url')
                or cleaned_data.get('archive_url')
                or cleaned_data.get('screenshot')):
            raise forms.ValidationError(
                _('Set at least one of "Url", "Archive Url" or "Screenshot"')
            )


@admin.register(Category)
class CategoryAdmin(AbstractVisibleModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(AbstractVisibleModelAdmin):
    pass


@admin.register(Source)
class SourceAdmin(AbstractVisibleModelAdmin):
    pass


class FactCheckInline(admin.StackedInline):
    model = FactCheck
    form = ReferenceForm
    fields = ('name', 'source', 'pub_date', 'url', 'archive_url', 'screenshot')


class OccurenceInline(FactCheckInline):
    model = Occurence


class ClaimInline(admin.TabularInline):
    model = Claim
    fields = ('name', 'is_true')


class ImageInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if not count:
            raise forms.ValidationError(
                _('Please add at least one image')
            )


class ImageInline(admin.TabularInline):
    model = Image
    formset = ImageInlineFormset
    fields = ('kind', 'image')


@admin.register(Item)
class ItemAdmin(AbstractVisibleModelAdmin, VersionAdmin):
    inlines = [ImageInline, ClaimInline, FactCheckInline, OccurenceInline]
    filter_horizontal = ('tags',)
