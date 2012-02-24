# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PageTranslation'
        db.create_table('fiber_pagetranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['fiber.Page'])),
        ))
        db.send_create_signal('fiber', ['PageTranslation'])

        # Adding unique constraint on 'PageTranslation', fields ['language_code', 'master']
        db.create_unique('fiber_pagetranslation', ['language_code', 'master_id'])

        # copy Page.title to translation table
        Page = orm['fiber.page']
        PageTranslation = orm['fiber.pagetranslation']

        if not db.dry_run:
            for page in Page.objects.all():
                PageTranslation.objects.create(
                    title=page.title,
                    master=page,
                    language_code='en'
                )

        # Deleting field 'Page.title'
        db.delete_column('fiber_page', 'title')

        # Adding model 'ContentItemTranslation'
        db.create_table('fiber_contentitemtranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('content_markup', self.gf('fiber.utils.fields.FiberMarkupField')()),
            ('content_html', self.gf('fiber.utils.fields.FiberHTMLField')()),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['fiber.ContentItem'])),
        ))
        db.send_create_signal('fiber', ['ContentItemTranslation'])

        # Adding unique constraint on 'ContentItemTranslation', fields ['language_code', 'master']
        db.create_unique('fiber_contentitemtranslation', ['language_code', 'master_id'])

        # copy ContentItem fields to translation table
        ContentItem = orm['fiber.contentitem']
        ContentItemTranslation = orm['fiber.contentitemtranslation']

        if not db.dry_run:
            for content_item in ContentItem.objects.all():
                ContentItemTranslation.objects.create(
                    content_html=content_item.content_html,
                    content_markup=content_item.content_markup,
                    master=content_item,
                    language_code='en'
                )

        # Deleting field 'ContentItem.content_markup'
        db.delete_column('fiber_contentitem', 'content_markup')

        # Deleting field 'ContentItem.content_html'
        db.delete_column('fiber_contentitem', 'content_html')

    def backwards(self, orm):
        raise Exception('Cannot migrate backwards')

    models = {
        'fiber.contentitem': {
            'Meta': {'object_name': 'ContentItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('fiber.utils.json.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'used_on_pages_data': ('fiber.utils.json.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'content_html': ('fiber.utils.fields.FiberHTMLField', [], {}),  # before migration
            'content_markup': ('fiber.utils.fields.FiberMarkupField', [], {}),  # before migration
        },
        'fiber.contentitemtranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'ContentItemTranslation'},
            'content_html': ('fiber.utils.fields.FiberHTMLField', [], {}),
            'content_markup': ('fiber.utils.fields.FiberMarkupField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': "orm['fiber.ContentItem']"})
        },
        'fiber.file': {
            'Meta': {'ordering': "('file',)", 'object_name': 'File'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'fiber.image': {
            'Meta': {'ordering': "('image',)", 'object_name': 'Image'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'fiber.page': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'object_name': 'Page'},
            'content_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fiber.ContentItem']", 'through': "orm['fiber.PageContentItem']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mark_current_regexes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'metadata': ('fiber.utils.json.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subpages'", 'null': 'True', 'to': "orm['fiber.Page']"}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'redirect_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'redirected_pages'", 'null': 'True', 'to': "orm['fiber.Page']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'show_in_menu': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('fiber.utils.fields.FiberURLField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})  # before migration
        },
        'fiber.pagecontentitem': {
            'Meta': {'object_name': 'PageContentItem'},
            'block_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'content_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'page_content_items'", 'to': "orm['fiber.ContentItem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'page_content_items'", 'to': "orm['fiber.Page']"}),
            'sort': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'fiber.pagetranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'PageTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': "orm['fiber.Page']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['fiber']
