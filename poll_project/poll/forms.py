from django.forms import ModelForm
from .models import Blog, Poll

class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'option_one', 'option_two', 'option_three']

class BlogForm(ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Blog
 
        # specify fields to be used
        fields = [
            "title",
            "description",
        ]