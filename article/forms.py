from django.forms import ModelForm
from article.models import News

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ["title", "content", "category", "thumbnail", "is_featured"]