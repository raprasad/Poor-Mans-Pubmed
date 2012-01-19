from django.conf.urls.defaults import *


#
#   Urls for recommendations
#
urlpatterns = patterns(
    'pubmed.views',

    url(r'import/$', 'view_pubmed_import_form', name='view_pubmed_import_form'),

)
