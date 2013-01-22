# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Download'
        db.delete_table('herbapp_download')

        # Adding model 'Purchase'
        db.create_table('herbapp_purchase', (
            ('order', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('herbapp', ['Purchase'])


    def backwards(self, orm):
        # Adding model 'Download'
        db.create_table('herbapp_download', (
            ('_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('client', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('app_version', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('herbapp', ['Download'])

        # Deleting model 'Purchase'
        db.delete_table('herbapp_purchase')


    models = {
        'herbapp.author': {
            'Meta': {'object_name': 'Author'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'herbapp.disease': {
            'Meta': {'object_name': 'Disease'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cs': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'herbapp.herb': {
            'Meta': {'object_name': 'Herb'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'alias_cs': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'alias_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['herbapp.Author']"}),
            'bark_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bark_type_alt': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'blooming_from': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'blooming_to': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'botanical_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'branching': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description_cs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'family_cs': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'family_en': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'flower_color': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'flower_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fruit_from': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fruit_to': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fruit_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'height_max': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'height_min': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_healing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_toxic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'leaf_arrangement': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'leaf_arrangement_alt': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'leaf_edge': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'leaf_edge_alt': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'leaf_shape': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'leaf_shape_alt': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'leaf_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name_cs': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'needle_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'petal_maxcount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'petal_mincount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'plant_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'herbapp.herbenvironment': {
            'Meta': {'object_name': 'HerbEnvironment'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'environment': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'herb_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['herbapp.Herb']"})
        },
        'herbapp.herbpick': {
            'Meta': {'object_name': 'HerbPick'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'herb_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['herbapp.Herb']"}),
            'herb_part': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'month_from': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'month_to': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'herbapp.herbpicture': {
            'Meta': {'object_name': 'HerbPicture'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'author_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['herbapp.Author']"}),
            'filename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'herb_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['herbapp.Herb']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'herbapp.herbusage': {
            'Meta': {'object_name': 'HerbUsage'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'disease_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['herbapp.Disease']"}),
            'herb_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['herbapp.Herb']"}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'herbapp.purchase': {
            'Meta': {'object_name': 'Purchase'},
            'order': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['herbapp']