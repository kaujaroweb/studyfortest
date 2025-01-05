from django.shortcuts import render

def home_view(request):
    return render(request, "paginas/home.html",{})
def afterLogin(request):
    return render(request, "paginas/afterlogin.html",{})