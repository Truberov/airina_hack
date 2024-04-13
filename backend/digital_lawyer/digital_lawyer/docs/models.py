import uuid

from shortuuid import ShortUUID

from storages.backends.s3boto3 import S3Boto3Storage

from django.utils import timezone
from django.db import models


def get_short_uuid():
    return ShortUUID().random(length=5)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class DocumentsArchive(BaseModel):
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование архива',
        default=get_short_uuid,
    )

    def __str__(self):
        return str(self.name)


def image_directory_path(instance, filename):
    if instance.docs_group:
        return "archive_{0}/{1}".format(instance.docs_group.id, str(get_short_uuid()))


class Document(BaseModel):
    docs_group = models.ForeignKey(
        DocumentsArchive,
        on_delete=models.CASCADE,
        verbose_name='Архив документов',
        related_name='docs',
    )
    predicted_class = models.CharField(
        max_length=50,
        verbose_name='Предсказаный класс',
        null=True,
        blank=True,
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to=image_directory_path,
        storage=S3Boto3Storage(),
        null=True,
    )

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return str(self.file.name)
