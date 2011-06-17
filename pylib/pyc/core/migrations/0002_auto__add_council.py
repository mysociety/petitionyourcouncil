# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Council'
        db.create_table('core_council', (
            ('petition_rss', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('petition_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200, db_index=True)),
        ))
        db.send_create_signal('core', ['Council'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Council'
        db.delete_table('core_council')
    
    
    models = {
        'core.council': {
            'Meta': {'object_name': 'Council'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'petition_rss': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'petition_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'})
        }
    }
    
    complete_apps = ['core']
