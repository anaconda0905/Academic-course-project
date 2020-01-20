from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from simple_history.models import HistoricalRecords

from accounts.models import Curator, Student, Grade, SuperAdmin
from courses.fields import OrderField
from courses.models import Subject, Course, Module, ItemBase
from schools.models import SchoolStudent


# Create your models here.


class OpenSubject(Subject):
    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while OpenSubject.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class OpenCourse(Course):
    creator = models.ForeignKey(Curator,
                                on_delete=models.CASCADE)
    subject = models.ForeignKey(OpenSubject,
                                related_name='courses',
                                on_delete=models.CASCADE,
                                null=True)
    admin = models.ForeignKey(SuperAdmin,
                              related_name='courses',
                              on_delete=models.CASCADE,
                              null=True)
    students = models.ManyToManyField(Student,
                                      related_name='courses_joined', blank=True)
    school_students = models.ManyToManyField(SchoolStudent,
                                             related_name='courses_enrolled', blank=True)
    grade = models.ForeignKey(Grade,
                              on_delete=models.CASCADE,
                              null=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while OpenCourse.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def total_students(self):
        return self.school_students.count() + self.students.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class OpenModule(Module):
    course = models.ForeignKey(OpenCourse,
                               related_name='modules',
                               on_delete=models.CASCADE)
    order = OrderField(blank=True, for_fields=['opencourse'])

    class Meta:
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while OpenModule.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class OpenContent(models.Model):
    module = models.ForeignKey(OpenModule,
                               related_name='contents',
                               on_delete=models.CASCADE)
    # Creates a link to every model
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': ('atext',
                                                                     'avideo',
                                                                     'aimage',
                                                                     'afile')})
    # index value
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])
    history = HistoricalRecords()

    def __str__(self):
        return self.item.title

    class Meta:
        ordering = ['order']
        verbose_name = 'Content'
        verbose_name_plural = 'Contents'


class OpenItemBase(ItemBase):
    creator = models.ForeignKey(Curator,
                                related_name='%(class)s_related',
                                on_delete=models.CASCADE)

    class Meta:
        abstract = True


class AText(OpenItemBase):
    video = models.FileField(upload_to='videos', null=True, blank=True)
    file = models.FileField(upload_to='videos', null=True, blank=True)
    image = models.FileField(upload_to='videos', null=True, blank=True)

    class Meta:
        verbose_name = 'AText'
        verbose_name_plural = 'ATexts'

    def __str__(self):
        return self.title


class AFile(OpenItemBase):
    file = models.FileField(upload_to='files')

    class Meta:
        verbose_name = 'AFile'
        verbose_name_plural = 'AFiles'

    def __str__(self):
        return self.title


class AImage(OpenItemBase):
    file = models.FileField(upload_to='images')

    class Meta:
        verbose_name = 'AImage'
        verbose_name_plural = 'AImages'

    def __str__(self):
        return self.title


class AVideo(OpenItemBase):
    file = models.FileField(upload_to='videos')

    class Meta:
        verbose_name = 'AVideo'
        verbose_name_plural = 'AVideos'

    def __str__(self):
        return self.title
