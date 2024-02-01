import time
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, CASCADE, DateTimeField, ForeignKey, \
    ManyToManyField, ImageField
from django_resized import ResizedImageField

from apps.task import task_send_email


class User(AbstractUser):
    image = ResizedImageField(size=[90, 90], crop=['middle', 'center'], upload_to='users/images',
                              default='users/default.jpg')


class Category(Model):
    name = CharField(max_length=255)

    def count_bloga(self) -> int:
        return self.blog_set.count()


class Tag(Model):
    name = CharField(max_length=255)

    def str(self):
        return self.name


class Blog(Model):
    name = CharField(max_length=255)
    author = ForeignKey('apps.User', CASCADE, 'blogs')
    category = ForeignKey('apps.Category', on_delete=CASCADE)
    image = ImageField(upload_to='products/images/', default='products/default.jpg')
    tags = ManyToManyField('apps.Tag')
    text = CKEditor5Field(blank=True, null=True, config_name='extends')
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        emails: list = Emails.objects.values_list('email', flat=True)
        print(emails)
        start = time.time()
        task_send_email.delay("New blog", self.name, list(emails))
        end = time.time()
        print(f"Time taken: {end - start}")

    def count_comment(self):
        return self.comment_set.count()


class Comment(Model):
    text = CKEditor5Field()
    blog = ForeignKey('apps.Blog', CASCADE)
    author = ForeignKey('apps.User', CASCADE, 'comments')
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)


class Emails(Model):
    email = CharField(max_length=255)
