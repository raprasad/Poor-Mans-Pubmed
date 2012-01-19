from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from papers.models import JournalArticle, PaperAuthor

def view_article_as_listing(journal_article):
    if journal_article is None:
        return None
        
    lu = { 'journal_article' : journal_article }
    return render_to_string('papers/view_article_as_listing.html', lu)
    
def view_papers_by_author(request, author_slug, id_hash):

    if id_hash is None:
        return Http404('view_papers_by_author')
    
    lu = {}
    try:
        author = PaperAuthor.objects.get(id_hash=id_hash)
    except PaperAuthor.DoesNotExist:
        lu.update({ 'ERR_author_not_found' : True})
        return render_to_response('papers/view_papers_by_author.html', lu, context_instance=RequestContext(request))
      
    ordered_author_papers = author.articleorderedauthorlisting_set.all().order_by('-article__year_of_publication', '-article__month_of_publication')
    
    lu.update({ 'author':author, 'papers' : ordered_author_papers})

    return render_to_response('papers/view_papers_by_author.html', lu, context_instance=RequestContext(request))
    