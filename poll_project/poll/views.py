from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import CreatePollForm, BlogForm
from .models import Poll, Blog

# Function Based Views

def home(request):
    polls = Poll.objects.all()

    context = {
        'polls' : polls
    }
    return render(request, 'poll/home.html', context)

def create(request):
    if request.method == 'POST':
        print(CreatePollForm(request.POST))
        form = CreatePollForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form = CreatePollForm()

    return render(request, 'poll/create.html', {'form' : form})

def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    context = {
        'poll' : poll
    }
    return render(request, 'poll/results.html', context)

def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form option')
    
        poll.save()

        return redirect('results', poll.id)

    context = {
        'poll' : poll
    }
    return render(request, 'poll/vote.html', context)

def update(request, poll_id):                                         
    data = get_object_or_404(Poll, id=poll_id)
    form = CreatePollForm(instance=data)                                                               

    if request.method == "POST":
        form = CreatePollForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect ('home')
    context = {
        "form":form
    }
    return render(request, 'poll/create.html', context)

# delete view for details
def delete_view(request, poll_id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Poll, id = poll_id)
 
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect('home')
 
    return render(request, "poll/delete_view.html", context)


# Class Based Views
from django.views.generic import DeleteView, CreateView, ListView, DetailView, UpdateView

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')  # Get the search query from the URL parameter 'q'

        if query:
            queryset = queryset.filter(title__icontains=query)  # Modify this to match your model fields

        return queryset


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
 
class BlogCreate(CreateView):
 
    # specify the model for create view
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('blog_list')

class BlogUpdateView(UpdateView):
 
    # specify the model for create view
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('blog_list')

class BlogDeleteView(DeleteView):
 
    # specify the model for create view
    model = Blog
    template_name = 'blog/blog_delete.html'
    success_url = reverse_lazy('blog_list')


from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            error_message = "Username already exists. Please choose a different one."
            return render(request, 'register.html', {'error_message': error_message})

        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Optionally, you can log in the user immediately after registration
        # login(request, user)

        return redirect('login')  # Redirect to the login page after successful registration

    return render(request, 'register.html')

from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is authenticated, log them in
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired redirect URL after successful login
        else:
            # Authentication failed, display an error message
            error_message = "Invalid login credentials."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')
