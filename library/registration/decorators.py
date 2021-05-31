from django.shortcuts import redirect

def logout_required(my_function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return my_function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper