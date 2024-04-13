from django.contrib import admin

from .models import DocumentsArchive, Document

admin.site.register(Document)

class DocumentInline(admin.StackedInline):
    model = Document


class DocumentsArchiveAdmin(admin.ModelAdmin):
    inlines = (DocumentInline,)
    search_fields = ('name',)
    list_per_page = 20


admin.site.register(DocumentsArchive, DocumentsArchiveAdmin)
