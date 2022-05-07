from django.db import models


class Ingredient(models.Model):
    name = models.TextField(
        verbose_name='Название',
        max_length=200,
        blank=False,
        null=False
    )
    measurement_unit = models.TextField(
        verbose_name='Единица измерения',
        max_length=200,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name[:20] + ', ' + self.measurement_unit[:10]
