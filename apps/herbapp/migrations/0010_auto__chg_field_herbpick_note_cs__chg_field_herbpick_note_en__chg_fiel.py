# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'HerbPick.note_cs'
        db.alter_column('herbapp_herbpick', 'note_cs', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'HerbPick.note_en'
        db.alter_column('herbapp_herbpick', 'note_en', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'HerbUsage.note_cs'
        db.alter_column('herbapp_herbusage', 'note_cs', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'HerbUsage.note_en'
        db.alter_column('herbapp_herbusage', 'note_en', self.gf('django.db.models.fields.CharField')(max_length=200))
        # Adding field 'Disease.disease_type'
        db.add_column('herbapp_disease', 'disease_type',
                      self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default='1', max_length=4),
                      keep_default=False)

        # Adding field 'Disease.body_parts'
        db.add_column('herbapp_disease', 'body_parts',
                      self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default='', max_length=16),
                      keep_default=False)

        # Adding field 'Disease.head_parts'
        db.add_column('herbapp_disease', 'head_parts',
                      self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default='', max_length=14),
                      keep_default=False)


        # Changing field 'Disease.age_group'
        db.alter_column('herbapp_disease', 'age_group', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10))

    def backwards(self, orm):

        # Changing field 'HerbPick.note_cs'
        db.alter_column('herbapp_herbpick', 'note_cs', self.gf('django.db.models.fields.TextField')())

        # Changing field 'HerbPick.note_en'
        db.alter_column('herbapp_herbpick', 'note_en', self.gf('django.db.models.fields.TextField')())

        # Changing field 'HerbUsage.note_cs'
        db.alter_column('herbapp_herbusage', 'note_cs', self.gf('django.db.models.fields.TextField')())

        # Changing field 'HerbUsage.note_en'
        db.alter_column('herbapp_herbusage', 'note_en', self.gf('django.db.models.fields.TextField')())
        # Deleting field 'Disease.disease_type'
        db.delete_column('herbapp_disease', 'disease_type')

        # Deleting field 'Disease.body_parts'
        db.delete_column('herbapp_disease', 'body_parts')

        # Deleting field 'Disease.head_parts'
        db.delete_column('herbapp_disease', 'head_parts')


        # Changing field 'Disease.age_group'
        db.alter_column('herbapp_disease', 'age_group', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=15))

    models = {
        'herbapp.author': {
            'Meta': {'object_name': 'Author'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'herbapp.disease': {
            'Meta': {'object_name': 'Disease'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'affected_sex': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'age_group': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '10'}),
            'body_parts': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '16'}),
            'disease_type': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "'1'", 'max_length': '4'}),
            'head_parts': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '14'}),
            'name_cs': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'herbapp.herb': {
            'Meta': {'object_name': 'Herb'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'alias_cs': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'alias_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'author_id': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['herbapp.Author']"}),
            'bark_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bark_type_alt': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'blooming_from': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'blooming_to': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'botanical_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'branching': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description_cs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'environment': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '15'}),
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
        'herbapp.herbpick': {
            'Meta': {'object_name': 'HerbPick'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'herb_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['herbapp.Herb']"}),
            'herb_part': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'month_from': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'month_to': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'note_cs': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'note_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'herbapp.herbpicture': {
            'Meta': {'object_name': 'HerbPicture'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'author_id': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['herbapp.Author']"}),
            'herb_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['herbapp.Herb']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '16'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'herbapp.herbusage': {
            'Meta': {'object_name': 'HerbUsage'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'disease_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['herbapp.Disease']"}),
            'herb_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['herbapp.Herb']"}),
            'note_cs': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'note_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'herbapp.purchase': {
            'Meta': {'object_name': 'Purchase'},
            'app_language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '2', 'primary_key': 'True'}),
            'app_platform': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16'}),
            'app_version': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'counter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'last_sync_ts': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'screen_width': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['herbapp']
