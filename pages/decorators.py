from django.shortcuts import render

def require_admin(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_staff:
            return function(request, *args, **kwargs)
        else:
            return render(request,'pages/page_not_found.html')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

#add user_is_client
def require_client(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_staff:
            return function(request, *args, **kwargs)
        else:
            return render(request,'pages/page_not_found.html')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

#add user_is_not_authenticated
def require_logout(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            if user.is_staff:
                return render(request,'pages/admin.html')
            else :
                return render(request,'clientdashboard/client.html')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def require_login(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return render(request,'pages/page_not_found.html')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


