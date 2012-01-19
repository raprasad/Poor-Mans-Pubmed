from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response

from django.core.urlresolvers import reverse
from papers.models import *

from pubmed.forms import PubMedImportForm
from pubmed.pubrun import pubmed_efetch

from django.conf import settings

ALLOWED_GROUP = 'SCD_RESEARCH_GROUP'

def is_user_in_group(request, group_name):
    if request is None or request.user is None:
        return False
    try:    
        for grp in request.user.groups.all():
            if grp.name == group_name:
                return True
    except:
        pass
        
    return False

def import_pubmed_article(pubmed_form):
    if pubmed_form is None:
        return None
            
    pid = pubmed_form.cleaned_data.get('pubmed_id')
    
    articles = pubmed_efetch([pid])
    if articles is None or len(articles) == 0:
        return None
    
    return articles[0]
    
def view_pubmed_import_form(request):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return HttpResponse('no access')

    #if not is_user_in_group(request, ALLOWED_GROUP):
    #    return HttpResponse('no access')
    # reverse("admin:papers_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    lu = {}
    if request.method == 'POST':
        f = PubMedImportForm(request.POST)
        if f.is_valid():
            article = import_pubmed_article(f)
            if article is None:
                lu.update({'ERR_IMPORT' : True,
               })                
            else:
                lu.update({'MSG_IMPORT_SUCCESS' : True,
                    'article': article })
    else:
        f = PubMedImportForm()
    
    lu.update({ 'pubmed_form' : f })
    
    return render_to_response('admin/papers/view_pubmed_import.html', lu, context_instance=RequestContext(request))
    