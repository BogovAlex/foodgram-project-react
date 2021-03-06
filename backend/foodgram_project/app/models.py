from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

from users.models import User


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

    def _get_name(self):
        return f'{self.name[:100]}, {self.measurement_unit[:20]}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name[:100]}, {self.measurement_unit[:20]}'


class Recipe(models.Model):

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        help_text='Выберите подходящие тэги для рецепта',
        through='TagsRecipe'
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
    image = models.ImageField(
        verbose_name='Фотография готового блюда',
        upload_to='recipes/images/',
        blank=False,
        help_text='Загрузите фотографию готового блюда'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (мин)',
        help_text=('Введитe ориентировочное время приготовления'
                   ' по рецепту в минутах'),
        validators=(
            MinValueValidator(
                limit_value=settings.MIN_COOKING_TIME,
                message=('Время приготовления не может быть меньше '
                         f'{settings.MIN_COOKING_TIME} минуты')
            ),
        )
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
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        help_text='Выберите подходящие ингредиенты для рецепта',
        through='RecipeIngredient',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name[:50]


class RecipeIngredient(models.Model):

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='amount'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='Введите количество продукта (не менее 1)',
        validators=(
            MinValueValidator(
                limit_value=settings.MIN_AMOUNT,
                message=f'Не может быть меньше {settings.MIN_AMOUNT}!'),
        )
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient'
    )

    class Meta:
        verbose_name = 'Список ингредиентов в рецепте'
        verbose_name_plural = 'Список ингредиентов в рецепте'
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.ingredient} {self.recipe} {self.amount}'


class TagsRecipe(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тэг',
    )

    class Meta:
        verbose_name = 'Тэг рецепта'
        verbose_name_plural = 'Тэги рецептов'

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        related_name='favorite',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='Пользователь',
        help_text='Укажите кому добавить рецепт в избранное'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorite',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='Рецепт',
        help_text='Рецепт добавленный в избранное'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorite',
            ),
        )
        verbose_name = 'Избранное пользователей'
        verbose_name_plural = 'Избранное пользователей'
        ordering = ('user',)

    def __str__(self):
        return (f'Пользователь {self.user.username} '
                f'добавил {self.recipe.name} в избранное')


class ShoppingCart(models.Model):

    user = models.ForeignKey(
        User,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='Пользователь',
        help_text=('Укажите кому добавить рецепт в корзину покупок')
    )

    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='Рецепт',
        help_text='Рецепт добавленный в корзину покупок'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_recipe_in_cart',
            ),
        )
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ('user',)

    def __str__(self):
        return self.recipe.name
