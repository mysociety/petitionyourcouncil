# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Petition.url'
        db.alter_column('core_petition', 'url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=1000))


    def backwards(self, orm):
        
        # Changing field 'Petition.url'
        db.alter_column('core_petition', 'url', self.gf('django.db.models.fields.URLField')(max_length=200, unique=True))


    models = {
        'core.council': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Council'},
            'centre': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'blank': 'True'}),
            'defer_check_until': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'mapit_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'mapit_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'north_east': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'petition_rss': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'petition_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'south_west': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'})
        },
        'core.petition': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Petition'},
            'council': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Council']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'first_seen': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '1000'})
        }
    }

    complete_apps = ['core']
