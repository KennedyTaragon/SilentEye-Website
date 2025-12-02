from django.db import models
from django.utils.text import slugify


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon_class = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            counter = 1
            while ProductCategory.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    specifications = models.JSONField(default=list, blank=True, null=True)
    description = models.TextField()
    price_range = models.CharField(max_length=100, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'