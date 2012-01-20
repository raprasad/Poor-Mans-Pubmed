### pubmed ###

## dependencies ##
1. # requires Tag model from [https://github.com/raprasad/Poor-Mans-Tag](https://github.com/raprasad/Poor-Mans-Tag). 

## adding to project ##
1. add "Poor-Mans-Pubmed" to sys.path e.g. sys.path.append('/opt/some-django-dir/Poor-Mans-Pubmed)
2. settings.py: INSTALLED_APPS, add "papers" and "pubmed"
3. settings.py: TEMPLATE_DIRS, add "papers/templates"
4. settings.py: add a PAPERS_UPLOAD directory for uploaded PDFs
5. urls.py: add papers.urls.py

(documentation to come)
