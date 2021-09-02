import bcrypt
from django.shortcuts import render, redirect, HttpResponse
from .models import textmessages, Users, comments
from django.contrib import messages
from django.db import IntegrityError
from .decorators import *

@login_protect
def index(request):
    usuarios = Users.objects.all()
    texting = textmessages.objects.all()
    

    context = {
        'Users': usuarios,
        'Messages': texting,
        
    }
    return render(request, 'otherwall.html', context)

@login_protect
def wall(request):
    
    usuarios = Users.objects.all()
    texting = textmessages.objects.all().order_by('-created_at')
    commentarios = comments.objects.all()

    context = {
        'Users': usuarios,
        'Messages': texting,
        'Comments': commentarios,
    }
    
    return render(request,'wall.html', context)

def register(request):
    if request.method == 'GET':
        context = {
            'Users': Users.objects.all(),
        }
        return render(request, 'login.html')
    
    else:
        name= request.POST['name']
        email =request.POST['email']
        password =request.POST['password']
        password_confirm=request.POST['password_confirm']
        
    errors = Users.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for llave, error_message in errors.items():
            messages.error(request, error_message)
        return redirect('/register')
        #avatar =request.POST['avatar']
    '''
    if password != password_confirm:
        messages.errorr(request, 'Passwords don´t match. Try again')
        return redirect('/register') ahora la validacion la hago en el validador
    '''
    try:
        user = Users.objects.create(
            name = name,
            email= email,
            password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        )
        request.session['user']={
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'avatar': user.avatar
        }
    except IntegrityError:
        messages.error(request, 'This Email already exist')
        return redirect('/register')

    messages.success(request, 'User successfully created')
    return redirect('/wall')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        user = Users.objects.get(email=email)
    except Users.DoesNotExist:
        messages.error(request, 'User does not exist')
        return redirect('/register')
    
    # si llegamos acá, estamos seguros que al  menos el usuario SI existe
    if not bcrypt.checkpw(password.encode(), user.password.encode()): 
        messages.error(request, 'User or Password are wrong')
        return redirect('/register')
    
    # si llegamos hasta acá, estamos seguros que es el usuario y la contraseña está correcta
    request.session['user'] = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'avatar': user.avatar
    }
    messages.success(request, f'Hello, {user.name}')
    return redirect('/wall')

@login_protect
def logout(request):
    del request.session['user'] 
    return redirect('/register')

@login_protect
def makepost(request):
    user_id = request.session['user']['id']
    mensaje = request.POST['mensaje']
    usuario = Users.objects.get(id= user_id)
    
    new_message = textmessages.objects.create(message = mensaje, user = usuario)
    messages.success(request, 'Message successfully posted')
    return redirect('/wall')

@login_protect
def comment(request):
    comentario = request.POST['coment']
    user_id = request.session['user']['id']
    usuario = Users.objects.get(id= int(user_id))
    msaje = int(request.POST['message_id'])
    mensaje = textmessages.objects.get(id =msaje)

    new_comment = comments.objects.create(message = mensaje, comment= comentario, user = usuario)
    messages.success(request, 'Comment successfully posted')  
    return redirect('/wall')

@login_protect
def delete(request, nam):
    msn= textmessages.objects.get(id= int(nam))
    msn.delete()
    return redirect('/wall')

@login_protect
def edit(request, nom):
    edit_msn = textmessages.objects.get(id= int(nom))
    comentarios = comments.objects.all()
    
    if request.method== 'GET':
        # yo no tuve ese problema, pero en caso de que me de jugo la fecha hago lo siguiente:
        #time_str=edit_show.release_date.strftime('%Y-%m-%d')
        context = {
            'edit_msn': edit_msn,
            #'time_str':time_str,
            'Comments': comentarios
        }
        return render(request,'shows_edit.html',  context)
    
    else:
        fresh_msn = request.POST['new_msj']
        edit_msn.message = fresh_msn
        #aqui no hago create, porque lo que necesito es sobreescribir algo que ya existe
        edit_msn.save()
        messages.success(request, 'Message successfully updated')
        
        return redirect('/wall')

