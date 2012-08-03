# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Article.topic'
        db.delete_column('visualization_article', 'topic')

        # Adding field 'Cluster.topic'
        db.add_column('visualization_cluster', 'topic',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Article.topic'
        db.add_column('visualization_article', 'topic',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Deleting field 'Cluster.topic'
        db.delete_column('visualization_cluster', 'topic')


    models = {
        'visualization.article': {
            'Meta': {'object_name': 'Article'},
            'added_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['visualization.Cluster']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        },
        'visualization.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'added_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'continent_location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'is_local': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'relevancy': ('django.db.models.fields.IntegerField', [], {}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['visualization']