from django.forms import ModelForm
from article.models import News

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ["title", "content", "category", "sports_type", "thumbnail", "is_featured"]