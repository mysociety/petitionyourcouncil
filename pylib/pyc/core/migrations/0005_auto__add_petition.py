# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Petition'
        db.create_table('core_petition', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('council', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Council'])),
            ('first_seen', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['Petition'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Petition'
        db.delete_table('core_petition')
    
    
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
        },
        'core.petition': {
            'Meta': {'object_name': 'Petition'},
            'council': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Council']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'first_seen': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }
    
    complete_apps = ['core']
