from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(db_index=True, max_length=50)
    year = models.IntegerField(blank=True)
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre, related_name='titles', verbose_name=("Жанр"))
    category = models.ForeignKey(
        Category,
        verbose_name=("Категория"),
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-id', ]


class Comment(models.Model):
    rewiew = models.ForeignKey('Review', on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='rewiews'
    )
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
