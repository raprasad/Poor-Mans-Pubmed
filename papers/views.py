#from papers.models import JournalArticle
from django.template.loader import render_to_string

def view_article_as_listing(journal_article):
    if journal_article is None:
        return None
        
    lu = { 'journal_article' : journal_article }
    return render_to_string('papers/view_article_as_listing.html', lu)
    
def view_by_author(request)