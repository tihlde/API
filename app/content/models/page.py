import uuid

from django.db import models
from django.utils.text import slugify

from mptt.models import MPTTModel, TreeForeignKey

from app.util.models import BaseModel, OptionalImage


class Page(MPTTModel, OptionalImage, BaseModel):
    parent = TreeForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    page_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150, unique=False)
    slug = models.SlugField(max_length=50, unique=False, null=True)
    content = models.TextField(blank=True)

    class Meta:
        unique_together = ("parent", "slug")
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @staticmethod
    def get_by_path(path):
        page_list = path.split("/")
        node = Page.objects.get(parent=None)
        if path == "":
            return node
        for i in range(0, len(page_list)):
            for child in node.get_children():
                if child.slug == path[i]:
                    node = child
        if node.slug != page_list[len(page_list) - 1]:
            raise Page.DoesNotExist
        return node

    def get_path(self):
        family = self.get_ancestors(include_self=True)
        path = ""
        for i in range(1, len(family)):
            path += family[i].slug + "/"
        return path

    def __str__(self):
        return f"{self.page_id} {self.title}"
