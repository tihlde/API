import uuid

from django.db import models
from django.utils.text import slugify

from app.util.models import OptionalImage, BaseModel
from mptt.models import MPTTModel, TreeForeignKey


class WikiPost(MPTTModel, OptionalImage, BaseModel):
    parent = TreeForeignKey('self',null=True,blank=True, on_delete=models.CASCADE, related_name='children')
    wikipost_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150, unique=False)
    slug = models.SlugField(max_length=50, unique=False, null=True) 
    content = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("parent", "slug")
        verbose_name = "Wiki Post"
        verbose_name_plural = "Wiki Posts"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @staticmethod
    def get_by_path(path):
        path = path.split('/')
        node = WikiPost.objects.get(parent = None)
        for i in range(0,len(path)):
            for child in node.get_children():
                if(child.slug == path[i]):
                    node = child
        return node


    def __str__(self):
        return f"{self.wikipost_id} {self.title}"
