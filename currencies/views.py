from django.shortcuts import render, redirect
from .models import CryptoModel, PortfolioModel, KeyFormModel
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms.newUserForm import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .forms.keyForm import KeyForm
from .datasets.marketStatusSet import ticker_lit
from .datasets.portfolioSet import Total_holdings
import pandas as pd
import pandasql as ps
import plotly.express as px
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True)
def BaseView(request):
    return(render(request=request, template_name='baseView.html'))


@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='../login')
def CryptoView(request):

    return(render(request, 'cryptoView.html', context={"Cryptos": CryptoModel.objects.all}))


@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='../login')
def MarketView(request):
    ma = ticker_lit()
    return(render(request, 'marketView.html', context={"market": ma}))


@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='../login')
def PortfolioView(request):
    return(render(request, 'portfolioView.html', context={"Portfolios": PortfolioModel.objects.all}))


def RegisterView(request):
    if(request.method == 'POST'):
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'New User created {username}')
            return(redirect("main:Login"))
        else:
            for msg in form.error_messages:
                messages.error(request, f'{msg}')
    form = NewUserForm
    return(render(request, 'register.html', context={"form": form}))


def LoginView(request):

    if(request.method == 'POST'):
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if(form.is_valid()):
            login(request, user)
            return(redirect("main:Dashboard"))
            messages.success(request, f'user logged in {username}')
        else:
            for msg in form.error_messages:
                messages.error(request, f'{msg}')

    form = AuthenticationForm
    return(render(request, 'login.html', context={"form": form}))


@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='../login')
def LogoutView(request):

    logout(request)
    return(render(request, 'logout.html'))


@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='../login')
def AccountView(request):
    keyforce = KeyFormModel.objects.filter(user=request.user)
    if(keyforce):
        return(render(request, 'keyView.html', {"keys": keyforce}))
    else:
        if(request.method == 'POST'):
            form = KeyForm(request.POST)
            if(form.is_valid()):
                primary_key = request.POST['primary_key']
                secret_key = request.POST['secret_key']
                new = KeyFormModel(primary_key=primary_key,
                                   secret_key=secret_key, user=request.user)
                new.save()
                return(redirect("main:Account"))
            else:
                for msg in form.error_messages:
                    messages.error(request, f'{msg}')
        else:
            form = KeyForm

        return(render(request, 'accountView.html', context={"form": form}))


@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='../login')
def KeyView(request):
    if(KeyFormModel.objects.filter(username == request.user)):
        keys = KeyFormModel.objects.filter(username == request.user)
        return(render(request, 'KeyView.html', context={"keys": keys}))


@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='../login')
def DashboardView(request):
    if(KeyFormModel.objects.filter(user=request.user).exists()):
        keys = KeyFormModel.objects.get(user=request.user)
        df = Total_holdings(primary_key=keys.primary_key,
                            secret_key=keys.secret_key)
        total_df = df['total_df']
        pie = df['pie_df']
        total = total_df.to_html()
        tot_sum=ps.sqldf('''
                        SELECT SUM(TOTAL_HOLDING) as holding FROM pie
                        ''').iloc[0]['holding']
        quantity = ps.sqldf('''SELECT MARKET,TOTAL_BALANCE FROM total_df''')
        pie_fig = px.pie(pie,values="TOTAL_HOLDING",names="MARKET",hole=0.5,title=tot_sum)
        pie_fig.update_layout(title={
        'text': u"\u20B9"+" "+str(tot_sum),
        'y':0.1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'bottom'})
        pie_df = pie_fig.to_html()
        quantity_df = px.pie(quantity,values="TOTAL_BALANCE",names="MARKET",hole=0.5).to_html()
        return(render(request, 'dashboardView.html', context={"portfolio": total,"pie":pie_df,"quant":quantity_df}))
        
    else:
        return(render(request, 'redirecttoAccountview.html'))
    
def deleteModel(request):
    if(KeyFormModel.objects.filter(user=request.user).exists()):
        KeyFormModel.objects.filter(user=request.user).delete()
        return(redirect('main:Account'))
        
        
