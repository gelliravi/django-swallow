from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class ArticleToSection(models.Model):
    article = models.ForeignKey('Article')
    section = models.ForeignKey(Section)
    weight = models.IntegerField()


class Article(models.Model):
    title = models.CharField(max_length=255)
    sections = models.ManyToManyField(Section, through=ArticleToSection)
    primary_sections = models.ManyToManyField(
        Section,
        related_name='highlight_set'
    )
    kind = models.CharField(max_length=255)

    publication_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


from models import *
from integration import *
