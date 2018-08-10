import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class UUIDasPKModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class AbstractNameSlugModel(models.Model):
    """
    Base abstract Model with name and slug property. Updates
    the slug based on the get_slug method
    """
    name = models.CharField(_('Name'), max_length=1000, db_index=True,
                            null=True, blank=True)
    slug = models.SlugField(_('Slug'), max_length=1008, db_index=True,
                            null=True, blank=True)

    slug_unique = True  # default
    auto_slugs = True

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_name()

    def get_name(self):
        return self.name or '%s %s' % (self.__class__.__name__, self.pk)

    def get_slug(self):
        return slugify(str(self))

    def save(self, *args, **kwargs):
        """
        Sets the slug of the instance based on the instance-method get_slug
        if the slugified name and the slug in the database aren't equal
        """
        if not self.name:
            self.name = str(self)
        if self.auto_slugs and (not self.get_slug() == self.slug or not self.slug):
            self.slug = self.get_slug()
        elif not self.slug:
            self.slug = self.get_slug()

        if self.slug_unique:
            # slug uniqueness is set on per model basis
            if self.__class__.objects.exclude(pk=self.pk).filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(self.slug, str(self.id)[-8:])

        super().save(*args, **kwargs)


class AbstractTimeStampModel(models.Model):
    """
    Base abstract Model that automatically stores created and updated timestamps.
    """
    created_ts = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)
    last_changed_ts = models.DateTimeField(_('Last changed at'), auto_now=True, editable=False)

    class Meta:
        abstract = True
        ordering = ('-last_changed_ts',)
        get_latest_by = 'last_changed_ts'


class AbstractOwnedModel(models.Model):
    """
    adds user ownership fields to model, based on settings.AUTH_USER_MODEL
    created_by and last_changed_by are set automatically on creation and save
    owner defaults to created_by at first save but can be assigned to any other user
    """
    user_required = False

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name=_('Owner'),
                              related_name='owned_%(app_label)s_%(class)s',
                              on_delete=models.SET_NULL,
                              blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name=_('Created by'),
                                   related_name='created_%(app_label)s_%(class)s',
                                   on_delete=models.SET_NULL,
                                   editable=False,
                                   blank=True, null=True)
    last_changed_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        verbose_name=_('Last changed by'),
                                        related_name='changed_%(app_label)s_%(class)s',
                                        on_delete=models.SET_NULL,
                                        editable=False,
                                        blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        models subclassing this must have an override of
        the save-method on view level to set owner, created_by and last_changed_by
        based on request.user
        or have to set request into kwargs
        """
        user = kwargs.pop('user', None)

        if self.user_required and (not user or not user.is_authenticated()):
            raise NotImplementedError(
                '`user_required` is `True` for this model, '
                'so set user data on view level or give user kwarg to save()'
            )

        if user and user.is_authenticated():
            if not self.__class__.objects.filter(pk=self.pk).exists():  # new entry
                # FIXME
                # we can't check for `self.pk` because uuids are already assigned
                # even if the instance doesn't exist yet
                self.owner = user
                self.created_by = user
            self.last_changed_by = user

        super().save(*args, **kwargs)


class AbstractBaseModel(UUIDasPKModel, AbstractNameSlugModel, AbstractTimeStampModel, AbstractOwnedModel):
    class Meta(AbstractTimeStampModel.Meta):
        abstract = True


class AbstractVisibleModel(AbstractBaseModel):
    visible = models.BooleanField(_('Is visible?'), default=True)

    def get_absolute_url(self):
        return reverse('%s-detail' % slugify(self.__class__.__name__),
                       kwargs={'slug': self.slug})

    class Meta(AbstractBaseModel.Meta):
        abstract = True
