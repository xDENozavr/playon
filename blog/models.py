from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='title')
    text_content = models.TextField(verbose_name='news text')
    image = models.ImageField(upload_to='news/%Y/%m/', null=True, blank=True, verbose_name='cover image')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')
    is_published = models.BooleanField(default=True, verbose_name='published')

    class Meta:
        verbose_name = 'News item'
        verbose_name_plural = 'News'
        ordering = ['-created_at']

    def __str__(self):
        return self.title