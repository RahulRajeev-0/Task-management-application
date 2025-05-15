from django.shortcuts import render

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        # Handle login logic here
        pass
    return render(request, "login.html")


def register_view(request):
    return render(request, "signup.html")
