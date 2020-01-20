from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify

from courses.fields import OrderField
from courses.models import Subject, Course, Module, ItemBase
from schools.models import Teacher, SchoolStudent, School, Grade


# Create your models here.


class SchoolSubject(Subject):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="subjects", null=True)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while SchoolSubject.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class SchoolCourse(Course):
    creator = models.ForeignKey(Teacher,
                                related_name='courses_created',
                                on_delete=models.CASCADE)
    school = models.ForeignKey(School,
                               related_name='courses',
                               on_delete=models.CASCADE)
    subject = models.ForeignKey(SchoolSubject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    students = models.ManyToManyField(SchoolStudent,
                                      related_name='courses_joined',
                                      blank=True)
    grade = models.ForeignKey(Grade,
                              related_name='grade',
                              on_delete=models.CASCADE,
                              null=True, blank=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def total_students(self):
        return self.students.count()

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while SchoolCourse.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class SchoolModule(Module):
    course = models.ForeignKey(SchoolCourse,
                               related_name='modules',
                               on_delete=models.CASCADE)
    order = OrderField(blank=True, for_fields=['schoolcourse'])

    class Meta:
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while SchoolModule.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class SchoolContent(models.Model):
    module = models.ForeignKey(SchoolModule,
                               related_name='contents',
                               on_delete=models.CASCADE)
    # Creates a link to every model
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': ('stext',
                                                                     'svideo',
                                                                     'simage',
                                                                     'sfile')})
    # index value
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']
        verbose_name = 'Content'
        verbose_name_plural = 'Contents'


class SchoolItemBase(ItemBase):
    creator = models.ForeignKey(Teacher,
                                related_name='%(class)s_related',
                                on_delete=models.CASCADE)

    class Meta:
        abstract = True


class SText(SchoolItemBase):
    content = models.TextField()

    class Meta:
        verbose_name = 'SText'
        verbose_name_plural = 'STexts'

    def __str__(self):
        return self.title


class SFile(SchoolItemBase):
    file = models.FileField(upload_to='school/files')

    class Meta:
        verbose_name = 'SFile'
        verbose_name_plural = 'SFiles'

    def __str__(self):
        return self.title


class SImage(SchoolItemBase):
    file = models.FileField(upload_to='school/images')

    class Meta:
        verbose_name = 'SImage'
        verbose_name_plural = 'SImages'

    def __str__(self):
        return self.title


class SVideo(SchoolItemBase):
    file = models.FileField(upload_to='school/videos', null=True)

    class Meta:
        verbose_name = 'SVideo'
        verbose_name_plural = 'SVideos'

    def __str__(self):
        return self.title
