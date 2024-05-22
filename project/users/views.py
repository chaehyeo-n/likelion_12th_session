from django.shortcuts import render, redirect

# Create your views here.

def mypage(request):
    return render(request, 'users/mypage.html')