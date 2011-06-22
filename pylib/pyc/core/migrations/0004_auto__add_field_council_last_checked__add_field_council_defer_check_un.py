# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Council.last_checked'
        db.add_column('core_council', 'last_checked', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Council.defer_check_until'
        db.add_column('core_council', 'defer_check_until', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Changing field 'Council.petition_rss'
        db.alter_column('core_council', 'petition_rss', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True))

        # Changing field 'Council.petition_url'
        db.alter_column('core_council', 'petition_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True))
    
    
    def backwards(self, orm):
        
        # Deleting field 'Council.last_checked'
        db.delete_column('core_council', 'last_checked')

        # Deleting field 'Council.defer_check_until'
        db.delete_column('core_council', 'defer_check_until')

        # Changing field 'Council.petition_rss'
        db.alter_column('core_council', 'petition_rss', self.gf('django.db.models.fields.URLField')(max_length=200))

        # Changing field 'Council.petition_url'
        db.alter_column('core_council', 'petition_url', self.gf('django.db.models.fields.URLField')(max_length=200))
    
    
    models = {
        'core.council': {
            'Meta': {'object_name': 'Council'},
            'defer_check_until': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'mapit_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'mapit_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'petition_rss': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'petition_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'})
        }
    }
    
    complete_apps = ['core']
