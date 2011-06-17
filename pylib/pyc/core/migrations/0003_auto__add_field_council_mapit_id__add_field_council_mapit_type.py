# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Council.mapit_id'
        db.add_column('core_council', 'mapit_id', self.gf('django.db.models.fields.IntegerField')(default=0, unique=True), keep_default=False)

        # Adding field 'Council.mapit_type'
        db.add_column('core_council', 'mapit_type', self.gf('django.db.models.fields.CharField')(default='', max_length=3), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Council.mapit_id'
        db.delete_column('core_council', 'mapit_id')

        # Deleting field 'Council.mapit_type'
        db.delete_column('core_council', 'mapit_type')
    
    
    models = {
        'core.council': {
            'Meta': {'object_name': 'Council'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapit_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'mapit_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'petition_rss': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'petition_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'})
        }
    }
    
    complete_apps = ['core']
