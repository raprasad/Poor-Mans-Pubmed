from django.db.models.signals import post_save


def update_author_text_from_article(sender, **kwargs):
    """ sender is a JournalArticle object"""
        
    article = kwargs.get('instance', None)
    if article is None:
        return
    
    post_save.disconnect(update_author_text_from_article, sender=article.__class__)
    
    article.author_text = article.get_updated_author_text()
    article.save()
    
    post_save.connect(update_author_text_from_article, sender=article.__class__)
    