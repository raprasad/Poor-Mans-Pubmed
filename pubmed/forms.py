from django import forms
from papers.models import JournalArticle
import re


class PubMedImportForm(forms.Form):
    pubmed_id = forms.CharField(label='PubMed ID', max_length=200, required=True, initial='15497569')
  
    def clean_pubmed_id(self):
        pid = self.cleaned_data.get('pubmed_id', None)
        if pid is None:
            raise forms.ValidationError('Please enter a PubMed ID')
        pid = pid.strip()
        if re.match('^\d{1,25}$', pid):
            if JournalArticle.objects.filter(pubmed_id=pid).count() > 0:
                raise forms.ValidationError('Sorry!  This PubMed ID is already in the database')
            return pid

        raise forms.ValidationError('Please enter a valid PubMed ID (digits only).')
        
        