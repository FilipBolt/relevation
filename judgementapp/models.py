from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import xml.etree.ElementTree as ET

# Create your models here.


class Document(models.Model):
    docId = models.CharField(max_length=250)
    text = models.TextField()

    def __unicode__(self):
        return self.docId

    def document_absolute_path(self):
        return settings.DATA_DIR + "/" + self.docId

    def get_content(self):
        content = ""

        try:
            with open(self.document_absolute_path()) as f:
                content = f.read()
        except Exception:
            content = "Could not read file %s" % self.document_absolute_path()
        return content

    def get_title(self):
        title = ""
        tree = ET.parse(self.document_absolute_path())
        root = tree.getroot()
        title = root.find('HEAD').find('TITLE').text
        return title


class Query(models.Model):
    qId = models.IntegerField()

    text = models.CharField(max_length=250)
    difficulty = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    annotator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    instructions = models.TextField(blank=True, null=True)
    criteria = models.TextField(blank=True, null=True)
    example = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return '%s: %s' % (self.qId, self.text)

    def num_unjudged_docs(self):
        unjugded = [judgement for judgement in self.judgements()
                    if judgement.relevance < 0]
        return len(unjugded)

    def num_judgements(self):
        return len(self.judgements())

    def judgements(self):
        return Judgement.objects.filter(query=self.id, annotator=self.annotator)

    class Meta:
        # primary key
        unique_together = (('qId', 'annotator'),)


class Judgement(models.Model):
    labels = {-1: 'Unjudged', 0: 'Not relevant',
              1: 'Somewhat relevant', 2: 'Highly relevant'}

    query = models.ForeignKey(Query)
    document = models.ForeignKey(Document)

    annotator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)

    relevance = models.IntegerField()

    def __unicode__(self):
        return '%s\t0%s\t%s\t%s\n' % (
            self.query.qId, self.document.docId,
            self.relevance, self.annotator
        )

    def label(self):
        return self.labels[self.relevance]
