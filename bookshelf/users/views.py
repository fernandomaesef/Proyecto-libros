from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, UsernameChangeForm
from .tokens import account_activation_token
from bookshelf import settings

# Create your views here.

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.is_active = False

            user.save()

            uid = urlsafe_base64_encode(
                force_bytes(user.pk)
            )

            token = account_activation_token.make_token(user)

            activation_url = request.build_absolute_uri(
                reverse(
                    "activate",
                    kwargs={
                        "uidb64": uid,
                        'token': token
                    }
                )
            )

            message = EmailMultiAlternatives(
                subject='Activa tu cuenta bookself',
                body=f"Valide su cuenta aqui{activation_url}",
                from_email=settings.DEFAULT_FROM_EMAIL, 
                to=[user.email]

            )

            html = f"""
                    <h2>Bienvenido a Bookshelf</h2>

                    <p>Gracias por registrarte.</p>

                    <p>Pulsa el siguiente botón para activar tu cuenta:</p>

                    <a href="{activation_url}"
                    style="background-color: #3498db;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 5px;">
                    Activar cuenta
                    </a>
                    """
            message.attach_alternative(html,'text/html')
            message.send()
            return render(
                request,
                'users/check_email.html',
                {'email':user.email}
                )
    else:
        form = RegisterForm()

    return render(
        request,
        "users/register.html",
        {'form':form}
    )

def activate(request,uidb64,token):
    try:

        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )

        user = User.objects.get(pk=uid)

    except(TypeError,OverflowError,ValueError,User.DoesNotExist):

        user = None

    if(
        user is not None 
        and account_activation_token.check_token(user,token)
    ):
        user.is_active = True
        user.save()

        return render(request,'users/activation_success.html',{})

    return render(
        request,
        'users/activation_invalid.html'
    )

@login_required
def username_change(request):

    if request.method == 'POST':
        form = UsernameChangeForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            return redirect('index')

    else:
        form = UsernameChangeForm(
            instance=request.user
        )

        context = {
            'form':form
        }

        return render(request,'users/change_username.html',context)

@login_required
def delete(request):
    error = None

    if request.method == 'POST':
        password = request.POST.get('password')
        print(password)

        if request.user.check_password(password):
            request.user.delete()
            return redirect('index')
        else:
            error = 'Contraseña incorrecta'

    return render(request,'users/delete.html',{'error': error})