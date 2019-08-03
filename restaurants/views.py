from django.shortcuts import render


# Create your views here.

def dashboard(request):
    return render(request, 'restaurants/dashboard.html')


def account(request):
    return render(request, 'restaurants/account.html')


def meal(request):
    return render(request, 'restaurants/meal.html')


def order(request):
    return render(request, 'restaurants/order.html')


def report(request):
    return render(request, 'restaurants/report.html')
