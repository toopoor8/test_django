from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError


class MenuItem(models.Model):
    title = models.CharField(max_length=200, verbose_name="название пункта")
    url = models.CharField(max_length=200, blank=True, verbose_name="URL")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children", verbose_name="родительский пункт")
    order = models.IntegerField(default=0, verbose_name="порядок сортировки")

    class Meta:
        verbose_name = "пункт меню"
        verbose_name_plural = "пункты меню"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def get_url(self):
        if not self.url:
            return "#"
        try:
            return reverse(self.url)
        except:
            return self.url

    def clean(self):
        if self.parent and self.parent.id == self.id:
            raise ValidationError("пункт меню не может быть своим собственным родителем")
        if self.parent:
            p = self.parent
            seen = {self.id}
            while p:
                if p.id in seen:
                    raise ValidationError("обнаружена циклическая зависимость в меню")
                seen.add(p.id)
                p = p.parent
