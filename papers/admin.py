from papers.models import *
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class PaperStatusAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display=('name', )
admin.site.register(PaperStatus, PaperStatusAdmin)

class ResearchJournalAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display=('name', 'description',)
    search_fields = ['name', 'description',]    
admin.site.register(ResearchJournal, ResearchJournalAdmin)

class PaperAuthorAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display=('last_name', 'first_name', 'mi', 'description','is_local_pi',)
    search_fields = ['last_name', 'first_name',]
    readonly_fields = ['slug', 'id_hash', ]
    list_filter = ('is_local_pi',)
admin.site.register(PaperAuthor, PaperAuthorAdmin)

class ArticleOrderedAuthorListingAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display=('article', 'author', 'sort_order', )
    search_fields = ['author__last_name', 'author__first_name', 'article__title']
admin.site.register(ArticleOrderedAuthorListing, ArticleOrderedAuthorListingAdmin)


class ArticleOrderedAuthorListingInline(admin.TabularInline):
    model = ArticleOrderedAuthorListing
    #form = EmbryoSpermInformationRecordForm
    extra=0

class JournalArticleAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = (ArticleOrderedAuthorListingInline,)
    list_display=('title', 'journal',  'year_of_publication', 'pubmed_link', 'volume', 'issue',  'is_abstract_public', 'is_pdf_public')
    list_filter=['is_abstract_public', 'is_pdf_public','tags', 'journal', 'year_of_publication',  ]
    search_fields = ['title', 'journal__name', 'abstract', 'authors_text', 'notes',]
    filter_horizontal = ('tags',)
    readonly_fields = ('pubmed_link', 'line_listing', 'author_text')
    fieldsets = (
           ('Basic Info', {
               'fields': ('title', 'journal', 'status',  ('year_of_publication','month_of_publication',), ('volume', 'issue', 'page',),  )
           }),
            ('Content', {
                  'fields': ('line_listing', 'abstract', 'pdf',)
              }),
           
           
            # ('Author text (instead of individual author entry)', {
            #    'classes': ('collapse',),             
            #      'fields': ('author_text',)
            #  }),
          
           ('Public Display', {
               'fields': ('is_abstract_public', 'is_pdf_public', )
           }),
           ('Outside Links', {
               'fields': ('pubmed_id', 'url1', 'url2',)
           }),
           
           ('Internal', {
              # 'classes': ('collapse',),
               'fields': ( 'tags', 'notes', 'author_text')
           }),
       )
        
admin.site.register(JournalArticle, JournalArticleAdmin)

