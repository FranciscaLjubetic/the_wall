from django.shortcuts import render, redirect, HttpResponse
from django.db import IntegrityError
from django.contrib import messages

def login_protect(func):
    def wrapper(request, *args, **kwargs):
        #si el ctm no esta logueado, no puede ver nada excepto el register y el login
        if 'user' not in request.session:
            messages.error(request, 'Please, sign in')
            return redirect('/register')
        
        resp = func(request, *args, **kwargs)
        return resp
    return wrapper