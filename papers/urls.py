from django.conf.urls.defaults import *


#
#   Urls for recommendations
#
urlpatterns = patterns(
    'papers.views',

    url(r'papers-by-author/(?P<author_slug>\w([\w|\.\-])*)/(?P<id_hash>\w{40})/$', 'view_papers_by_author', name='view_papers_by_author'),

)
