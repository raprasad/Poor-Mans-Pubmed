import hashlib

from django.db import models
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save     
from django.conf import settings

from papers.author_helper import update_author_text_from_article
#from papers.author_helper import update_author_text_from_artice

from tags.models import Tag

class PaperStatus(models.Model):
    """ e.g. Submitted, In Press, etc"""
    name = models.CharField(max_length=255, unique=True)
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Paper status'

class ResearchJournal(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    slug = models.SlugField('automatically filled in)', max_length=250, blank=True,  db_index=True,)
    
    def __unicode__(self):
        return self.name

    def save(self):
        self.slug = slugify(self.name)
        super(ResearchJournal, self).save()      

    class Meta:
        ordering = ('name',)
    
class PaperAuthor(models.Model):
    first_name = models.CharField('First Name', max_length=70)
    mi = models.CharField('Middle Initial', blank=True, max_length=5)
    last_name = models.CharField('Last Name', max_length=70)
    slug = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    
    is_local_pi = models.BooleanField('is local principal investigator?', default=False)
    id_hash = models.CharField(max_length=40, blank=True)
    
    def get_absolute_url(self):
        if self.id is None:
            return ''
        return reverse('view_papers_by_author'\
                        , kwargs={ 'author_slug':self.slug, 'id_hash':self.id_hash}\
                      ) 
            
        return 
    
    def fmt_fullname_lname_first(self):
        if self.mi:
            return '%s, %s %s' %  (self.last_name, self.first_name, self.mi)
        return '%s, %s' % (self.last_name, self.first_name)

    def fmt_for_listing(self):
        if self.mi:
            return '%s, %s. %s.' %  (self.last_name, self.first_name[0], self.mi[0])
        return '%s, %s.' % (self.last_name, self.first_name[0])

    def save(self):
        if not self.id:
            super(PaperAuthor, self).save()

        self.id_hash =  hashlib.sha1('%s%s' % (self.id, self.last_name)).hexdigest()
        self.slug = slugify(self.fmt_fullname_lname_first())
        
        super(PaperAuthor, self).save()
        
    def __unicode__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    class Meta:
        ordering = ('last_name', 'first_name',)
            
class JournalArticle(models.Model):

    title = models.CharField(max_length=255, unique=True)
    status = models.ForeignKey(PaperStatus)

    year_of_publication = models.IntegerField(db_index=True)
    month_of_publication = models.CharField(max_length=30, blank=True, null=True)
    pub_month = models.DateField(help_text='select 1st day of month', blank=True, null=True)
    
    journal = models.ForeignKey(ResearchJournal)
    volume = models.CharField(max_length=100,  blank=True, null=True)
    issue = models.CharField(max_length=100,  blank=True, null=True)
    page = models.CharField(max_length=100,  blank=True, null=True)

    author_text = models.TextField(blank=True)
    
    pubmed_id = models.CharField(max_length=100, blank=True)
    pmc_id = models.CharField(max_length=100, blank=True, null=True)

    abstract = models.TextField(blank=True, null=True)
    
    url1 = models.URLField(blank=True)
    url2 = models.URLField(blank=True)
    
    is_abstract_public = models.BooleanField(default=False)
    is_pdf_public = models.BooleanField(default=False)
    
    pdf = models.FileField(upload_to=settings.PAPERS_UPLOAD, blank=True, null=True) #upload_to)
    

    notes = models.TextField(blank=True)

    tags = models.ManyToManyField(Tag, blank=True, null=True)    

    def pubmed_link(self):
        if self.pubmed_id is None:
            return None
        return '<a href="http://www.ncbi.nlm.nih.gov/pubmed?term=%s" target="_blank">pubmed</a>' % self.pubmed_id
    pubmed_link.allow_tags = True

    
    def get_updated_author_text(self):
        if self.id is None:
            return
        authors_listing_for_text = []
        for a in self.get_author_listing():
            authors_listing_for_text.append(a.author.fmt_fullname_lname_first())
        return '; '.join(authors_listing_for_text)
        
    def get_author_listing(self):
        return self.articleorderedauthorlisting_set.all()
        
    def line_listing(self):
        lu = { 'ja' : self }
        return render_to_string('papers/view_article_as_listing.html', lu)
    line_listing.allow_tags = True
    
    def __unicode__(self):
        return '%s - %s '  % (self.title, self.journal)
    
    class Meta:
        ordering = ('title', )
        
class ArticleOrderedAuthorListing(models.Model):
    article = models.ForeignKey(JournalArticle)
    author = models.ForeignKey(PaperAuthor)
    sort_order = models.IntegerField(default=1)

    def __unicode__(self):
        return '%s - %s '  % (self.author, self.article)
    
    class Meta:
        ordering = ('article', 'sort_order' )


post_save.connect(update_author_text_from_article, sender=JournalArticle)

