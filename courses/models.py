from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string
from simple_history.models import HistoricalRecords

User = settings.AUTH_USER_MODEL


# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to="courses/preview/", null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    draft = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
        ordering = ['-created']

    def __str__(self):
        return self.title

    def year_month_created(self):
        return self.created.strftime('%Y %B')

    def total_contents(self):
        count = 0
        for module in self.modules.all():
            count += module.contents.all().count()
        return count

    def save(self, *args, **kwargs):
        if not self.preview:
            self.draft = True
        super().save(*args, **kwargs)


class Module(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, editable=False, unique=True, null=True)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


# class Content(models.Model):
#     # module = models.ForeignKey(Module,
#     #                            related_name='contents',
#     #                            on_delete=models.CASCADE)
#     # Creates a link to every model
#     content_type = models.ForeignKey(ContentType,
#                                      on_delete=models.CASCADE,
#                                      limit_choices_to={'model__in': ('text',
#                                                                      'video',
#                                                                      'image',
#                                                                      'file')})
#     # index value
#     object_id = models.PositiveIntegerField()
#     item = GenericForeignKey('content_type', 'object_id')
#     order = OrderField(blank=True, for_fields=['module'])
#
#     class Meta:
#         ordering = ['order']


# Abstract Model
class ItemBase(models.Model):
    # creator = models.ForeignKey(Teacher,
    #                           related_name='%(class)s_related',
    #                           on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords(inherit=True)
    content = models.TextField(null=True)

    class Meta:
        # Abstract don't get saved in database
        abstract = True

    def render(self):
        return render_to_string('courses/content/{}.html'.format(
            self._meta.model_name), {'item': self})

    def __str__(self):
        return self.title

# class Text(ItemBase):
#     content = models.TextField()
#
#
# class File(ItemBase):
#     file = models.FileField(upload_to='files')
#
#
# class Image(ItemBase):
#     file = models.FileField(upload_to='images')
#
#
# class Video(ItemBase):
#     url = models.URLField()
