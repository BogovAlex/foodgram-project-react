from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название для тэга'
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет в HEX',
        help_text='Цвет вводится в формате HEX вида #000000'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name[:40]


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        blank=False,
        null=False,
        help_text='Введите название продукта'
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
        blank=False,
        null=False,
        help_text='Введите единицу измерения продукта вида - кг/г/мг'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name[:100] + ', ' + self.measurement_unit[:20]


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        help_text='Выберите подходящие тэги для рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта'
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Описание рецепта'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (мин)',
        help_text=('Введитe ориентировочное время приготовления'
                   ' по рецепту в минутах'),
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Время приготовления не может быть меньше 1 минуты')
        ]
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор',
        help_text='Выберите автора рецепта'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации рецепта',
        auto_now_add=True,
        help_text='Введите дату публикации рецепта',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name[:50]


class RecipeIngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='amount'
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        help_text='Введите количество продукта (не менее 1)',
        validators=(MinValueValidator(1, message='Не может быть меньше 1!'),)
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список ингредиентов в рецепте'
        verbose_name_plural = 'Список ингредиентов в рецепте'
        ordering = ['recipe']

    def __str__(self):
        return (f'{self.ingredient.name[:50]} {self.amount}'
                f' {self.ingredient.measurement_unit[:20]}')