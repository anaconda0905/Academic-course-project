from django.conf import settings
from django.db import models
from django.utils.text import slugify

from accounts.models import Grade, Marketer

User = settings.AUTH_USER_MODEL


class School(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='school_profile')
    name = models.CharField(max_length=50)
    # logo = models.ImageField(upload_to='media/Users/avatar/%Y/%m/%d', null=True, blank=True)
    slug = models.SlugField(max_length=200, editable=False, unique=True, null=True)
    marketer = models.ForeignKey(Marketer,
                                 on_delete=models.CASCADE,
                                 related_name='schools',
                                 null=True)

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name + self.user.username)
        unique_slug = slug
        num = 1
        while School.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Teacher(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='teacher_profile')
    school = models.ForeignKey(School,
                               on_delete=models.CASCADE,
                               related_name='teachers',
                               null=True)
    grade = models.ForeignKey(Grade,
                              on_delete=models.CASCADE,
                              related_name='teacher_class',
                              blank=True,
                              null=True)
    slug = models.SlugField(max_length=200, editable=False, unique=True, null=True)

    # def get_absolute_url(self):
    #     return reverse('schools:student_detail',
    #                    args=[self.school,
    #                          self.user,
    #                          self.id])

    def __str__(self):
        return self.user.first_name

    def _get_unique_slug(self):
        slug = slugify(self.user.get_full_name)
        unique_slug = slug
        num = 1
        while Teacher.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class SchoolStudent(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='school_student_profile')
    school = models.ForeignKey(School,
                               on_delete=models.CASCADE,
                               related_name='students')
    # grade = models.ForeignKey(Grade,
    #                           on_delete=models.CASCADE,
    #                           related_name='student_class',
    #                           null=True,
    #                           blank=True)
    teacher = models.ManyToManyField(Teacher,
                                     related_name='students')
    slug = models.SlugField(max_length=200, editable=False, unique=True, null=True)

    # def get_absolute_url(self):
    #     return reverse('schools:student_detail',
    #                    args=[self.school,
    #                          self.user,
    #                          self.id])

    def __str__(self):
        return self.user.first_name

    def _get_unique_slug(self):
        slug = slugify(self.user.first_name + self.user.last_name)
        unique_slug = slug
        num = 1
        while SchoolStudent.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
