# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Purchase.app_version'
        db.alter_column(u'herbapp_purchase', 'app_version', self.gf('django.db.models.fields.CharField')(max_length=16))

    def backwards(self, orm):

        # Changing field 'Purchase.app_version'
        db.alter_column(u'herbapp_purchase', 'app_version', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'herbapp.author': {
            'Meta': {'object_name': 'Author'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'herbapp.disease': {
            'Meta': {'object_name': 'Disease'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'affected_sex': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'age_group': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '10'}),
            'body_parts': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'disease_type': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "'1'", 'max_length': '4'}),
            'head_parts': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'name_cs': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'herbapp.herb': {
            'Meta': {'object_name': 'Herb'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'alias_cs': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'alias_de': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'alias_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'author_id': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['herbapp.Author']"}),
            'bark_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bark_type_alt': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'blooming_from': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'blooming_to': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'botanical_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'branching': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description_cs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_de': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'environment': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '15'}),
            'family_cs': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'family_de': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
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
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'needle_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'petal_maxcount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'petal_mincount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'plant_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'herbapp.herbpick': {
            'Meta': {'object_name': 'HerbPick'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'herb_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbapp.Herb']"}),
            'herb_part': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'month_from': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'month_to': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'note_cs': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'note_de': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'note_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'herbapp.herbpicture': {
            'Meta': {'object_name': 'HerbPicture'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'author_id': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['herbapp.Author']"}),
            'herb_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbapp.Herb']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '16'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'herbapp.herbusage': {
            'Meta': {'object_name': 'HerbUsage'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'disease_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbapp.Disease']"}),
            'herb_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbapp.Herb']"}),
            'note_cs': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'note_de': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'note_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'herbapp.purchase': {
            'Meta': {'object_name': 'Purchase'},
            'app_language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2'}),
            'app_platform': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16'}),
            'app_region': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'app_version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16'}),
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '48', 'primary_key': 'True'}),
            'counter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'last_sync_ts': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'screen_height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'screen_width': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['herbapp']
