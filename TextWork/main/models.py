from django.db import models


class TagsModel(models.Model):
    tagName = models.TextField(db_column='tagName', unique=True)
    tagId = models.AutoField(db_column='tagId', primary_key=True)

    class Meta:
        managed = True
        db_table = 'texts_tags'

    def __str__(self):
        return str(self.tagId)


class Articles(models.Model):  # наши новости
    tag = models.CharField('Тег', max_length=10)
    title = models.CharField('Заголовок', max_length=100)
    full_text = models.TextField('Текст статьи')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
