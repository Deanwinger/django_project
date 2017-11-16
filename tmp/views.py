from django.http import HttpResponse    
from django.shortcuts import render    
from django.contrib.auth import authenticate, login    
from .forms import LoginForm
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # authenticate()方法通过数据库对这个用户进行认证（authentication
            user = authenticate(username=cd["username"],
                                password=cd["password"])
            if user is not None:
                # is_active属性来检查用户是否可用
                if user.is_active:
                    # login()将用户设置到当前的会话（session）中
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:            
            form = LoginForm()
        return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html',
                 {'section': 'dashboard'})
