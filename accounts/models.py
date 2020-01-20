from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField

# Create your models here.
from simple_history.models import HistoricalRecords


class User(AbstractUser):
    TYPES = (
        ('student', 'SchoolStudent'),
        ("aonestudent", 'AoneStudent'),
        ('teacher', 'Teacher'),
        ('school', 'School'),
        ('curator', 'Curator'),
        ('editor', 'Editor'),
        ('super admin', 'Super Admin'),
        ('marketer', 'Marketer'),
        ('admin', 'Admin')
    )
    avatar = models.ImageField(upload_to='media/Users/avatar/%Y/%m/%d', null=True, blank=True,
                               default='avatar/default_avatar.png')
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=150, null=True)
    country = CountryField()
    city = models.CharField(max_length=50, null=True)
    phone = models.IntegerField(null=True)
    mobile = models.IntegerField(null=True)
    is_active = models.BooleanField('active status', default=True)
    account_type = models.CharField(max_length=11, choices=TYPES, verbose_name='Account Type')
    history = HistoricalRecords()

    def __str__(self):
        return "{}({})".format(self.username, self.get_full_name())


class Grade(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    history = HistoricalRecords()

    class Meta:
        ordering = ['title']
        verbose_name = 'class'
        verbose_name_plural = 'classes'

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Grade.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class SuperAdmin(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='super_admin_profile')
    slug = models.SlugField(max_length=200, unique=True, editable=False, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.user.first_name

    def _get_unique_slug(self):
        slug = slugify(self.user.first_name + self.user.last_name)
        unique_slug = slug
        num = 1
        while SuperAdmin.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Curator(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='curator')
    admin = models.ForeignKey(SuperAdmin,
                              null=True,
                              on_delete=models.CASCADE,
                              related_name='curator')
    slug = models.SlugField(max_length=200, unique=True, editable=False, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.user.first_name

    def _get_unique_slug(self):
        slug = slugify(self.user.first_name + self.user.last_name)
        unique_slug = slug
        num = 1
        while Curator.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Editor(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='editor')
    admin = models.ForeignKey(SuperAdmin,
                              null=True,
                              on_delete=models.CASCADE,
                              related_name='editor')
    slug = models.SlugField(max_length=200, unique=True, editable=False, null=True)

    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True)
    )

    def __str__(self):
        return self.user.first_name

    def _get_unique_slug(self):
        slug = slugify(self.user.first_name + self.user.last_name)
        unique_slug = slug
        num = 1
        while Editor.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Marketer(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='marketer_profile')
    slug = models.SlugField(max_length=200, unique=True, editable=True, null=True)
    admin = models.ForeignKey(SuperAdmin,
                              on_delete=models.CASCADE,
                              related_name='marketer')
    history = HistoricalRecords()

    def __str__(self):
        return self.user.first_name

    def _get_unique_slug(self):
        slug = slugify(self.user.first_name + self.user.last_name)
        unique_slug = slug
        num = 1
        while Marketer.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='open_student_profile')
    slug = models.SlugField(max_length=200, unique=True, editable=False, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.user.first_name

    def _get_unique_slug(self):
        slug = slugify(self.user.first_name + self.user.last_name)
        unique_slug = slug
        num = 1
        while Student.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
