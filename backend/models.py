import reversion

from easy_thumbnails.fields import ThumbnailerImageField

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone, formats
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from parler.models import TranslatedFields

# from .elastic import add_image
from .mixins.models import AbstractVisibleModel, AbstractBaseModel


class Category(AbstractVisibleModel):
    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=1000, db_index=True),
        slug=models.SlugField(_('Slug'), max_length=1008, db_index=True, null=True, blank=True)
    )
    parent = models.ManyToManyField('self', verbose_name=_('Parent'), blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        # ordering = ('name',)

    def get_absolute_url(self):
        return '%s?cat=%s' % (reverse('index'), self.name)


class Tag(AbstractVisibleModel):
    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=1000, db_index=True),
        slug=models.SlugField(_('Slug'), max_length=1008, db_index=True, null=True, blank=True)
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name=_('Category'),
                                 related_name='tags', blank=True, null=True)
    parent = models.ManyToManyField('self', verbose_name=_('Parent'), blank=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        # ordering = ('name',)

    def get_absolute_url(self):
        return '%s?tag=%s' % (reverse('index'), self.name)


class Source(AbstractVisibleModel):
    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=1000, db_index=True),
        slug=models.SlugField(_('Slug'), max_length=1008, db_index=True, null=True, blank=True)
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name=_('Category'),
                                 limit_choices_to={'parent__translations__name': settings.TAXONOMY['SOURCE']},
                                 blank=True, null=True, related_name='sources')
    url = models.URLField()

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')


@reversion.register()
class Item(AbstractVisibleModel):
    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=1000, db_index=True),
        slug=models.SlugField(_('Slug'), max_length=1008, db_index=True, null=True, blank=True),
        description=models.TextField(_('Description'))
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 limit_choices_to={'parent__translations__name': settings.TAXONOMY['CONTEXT']},
                                 verbose_name=_('Context'), related_name='items')
    tags = models.ManyToManyField(Tag, related_name='items',
                                  limit_choices_to={'category__translations__name': settings.TAXONOMY['DESCRIPTIVE']})

    @cached_property
    def original(self):
        return self.image_assets.filter(kind='o').first().image

    @cached_property
    def thumbnail(self):
        thumbnail = self.image_assets.filter(kind='t').first()
        if thumbnail:
            return thumbnail.image
        return self.cover

    @cached_property
    def cover(self):
        cover = self.image_assets.filter(kind='d').first()
        if cover:
            return cover.image
        thumbnail = self.image_assets.filter(kind='t').first()
        if thumbnail:
            return thumbnail.image
        return self.original

    @cached_property
    def right_claims(self):
        return self.claims.filter(is_true=True)

    @cached_property
    def wrong_claims(self):
        return self.claims.filter(is_true=False)

    def sync_elasticsearch(self):
        for img in self.image_assets.all():
            img.sync_elasticsearch()


def get_upload_to(instance, filename):
    now = timezone.now()
    return '%s/%s/%s/%s.%s' % (
        now.year,
        now.month,
        instance.item.pk,
        instance.pk,
        filename.split('.')[-1]
    )


class Media(AbstractBaseModel):
    ORIGINAL = 'o'
    VARIANT = 'v'
    THUMBNAIL = 't'
    DISPLAY = 'd'
    SOCIAL_MEDIA = 's'
    KIND_CHOICES = (
        (ORIGINAL, _('Original')),
        (VARIANT, _('Variant')),
        (THUMBNAIL, _('Thumbnail')),
        (DISPLAY, _('Display')),
        (SOCIAL_MEDIA, _('Social Media'))
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='%(class)s_assets')
    kind = models.CharField(_('Type'), max_length=1, choices=KIND_CHOICES, default=ORIGINAL)
    credits = models.TextField(_('Credits'), blank=True, null=True)

    class Meta:
        abstract = True


class Image(Media):
    image = ThumbnailerImageField(_('Image'), upload_to=get_upload_to)

    def __str__(self):
        return '%s %s' % (_('Image for'), self.item)

    def serialize(self):
        return {
            'item': str(self.item.pk),
            'kind': self.kind
        }

    # def sync_elasticsearch(self):
    #     add_image(self.image.path, self.serialize())


class Video(Media):
    video = models.FileField(_('Video File'), upload_to=get_upload_to, blank=True, null=True)
    video_url = models.URLField(_('Video URL'), blank=True, null=True)

    def __str__(self):
        return '%s %s' % (_('Video for'), self.item)


class Reference(AbstractVisibleModel):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='%(class)ss')
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='%(class)ss')
    pub_date = models.DateTimeField(_('Publication Date'))
    pub_date_show_month = models.BooleanField(_('Show month?'), default=True)
    pub_date_show_day = models.BooleanField(_('Show day?'), default=True)
    pub_date_show_time = models.BooleanField(_('Show time?'), default=True)
    url = models.URLField(_('URL'), blank=True, null=True)
    archive_url = models.URLField(_('Archive URL'), blank=True, null=True)
    screenshot = ThumbnailerImageField(_('Screenshot'), upload_to=get_upload_to, blank=True, null=True)
    lang = models.ForeignKey(Tag, on_delete=models.SET_NULL, verbose_name=_('Language'), null=True,
                             limit_choices_to={'category__translations__name': settings.TAXONOMY['LANGUAGE']})

    def get_absolute_url(self):
        return self.url or self.archive_url or self.screenshot.url

    class Meta:
        abstract = True

    @cached_property
    def date(self):
        if not self.pub_date_show_time:
            return self.short_date
        return formats.date_format(self.pub_date)

    @cached_property
    def short_date(self):
        if not self.pub_date_show_month:
            return self.pub_date.year
        if not self.pub_date_show_day:
            return formats.date_format(self.pub_date, 'm Y')
        return formats.date_format(self.pub_date, 'd.m.Y')


class FactCheck(Reference):
    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=1000, db_index=True),
        slug=models.SlugField(_('Slug'), max_length=1008, db_index=True, null=True, blank=True)
    )
    icon = 'verified_user'

    def get_name(self):
        # FIXME translations
        return self.name or 'Factcheck by %s about %s' % (self.source, self.item)

    class Meta:
        ordering = ('-pub_date',)


class Occurence(Reference):
    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=1000, db_index=True),
        slug=models.SlugField(_('Slug'), max_length=1008, db_index=True, null=True, blank=True),
        description=models.TextField(_('Description'), blank=True, null=True)
    )
    icon = 'error'

    def get_name(self):
        # FIXME translations
        return self.name or 'Occurence by %s of %s' % (self.source, self.item)

    class Meta:
        ordering = ('-pub_date',)


class Claim(AbstractVisibleModel):
    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=1000, db_index=True),
        slug=models.SlugField(_('Slug'), max_length=1008, db_index=True, null=True, blank=True),
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims', verbose_name=_('Item'))
    is_true = models.BooleanField(verbose_name=_('True?'), default=False)

    @cached_property
    def icon(self):
        return 'check' if self.is_true else 'close'

    class Meta:
        ordering = ('-is_true', '-last_changed_ts')
