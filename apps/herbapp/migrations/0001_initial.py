# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table('herbapp_author', (
            ('_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('herbapp', ['Author'])

        # Adding model 'Herb'
        db.create_table('herbapp_herb', (
            ('_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['herbapp.Author'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('botanical_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('alias_en', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('family_en', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name_cs', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('alias_cs', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('family_cs', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('description_cs', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_healing', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_toxic', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('plant_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('height_min', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('height_max', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('flower_color', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('flower_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('blooming_from', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('blooming_to', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('petal_mincount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('petal_maxcount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('leaf_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('leaf_shape', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('leaf_shape_alt', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('leaf_edge', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('leaf_edge_alt', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('leaf_arrangement', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('leaf_arrangement_alt', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('needle_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('branching', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bark_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bark_type_alt', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fruit_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fruit_from', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fruit_to', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('herbapp', ['Herb'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table('herbapp_author')

        # Deleting model 'Herb'
        db.delete_table('herbapp_herb')


    models = {
        'herbapp.author': {
            'Meta': {'object_name': 'Author'},
            '_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
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
        }
    }

    complete_apps = ['herbapp']