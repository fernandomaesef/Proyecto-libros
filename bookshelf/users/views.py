from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import RegisterForm
from .tokens import account_activation_token

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

            send_mail(
                "Verifica tu cuenta",
                f"Pulsa este enlace para verificar tu cuenta:\n\n{activation_url}",
                None,
                [user.email],
                fail_silently=False
            )

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