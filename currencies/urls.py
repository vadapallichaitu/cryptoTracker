from django.contrib import admin
from django.urls import path
from .views import BaseView, PortfolioView, CryptoView, RegisterView, LoginView, LogoutView, AccountView,DashboardView,MarketView,deleteModel
app_name = "main"
urlpatterns = [

    path('', BaseView, name="Base"),
    path('market/', MarketView, name="Market"),
    path('portfolio/', PortfolioView, name="Portfolio"),
    path('register/', RegisterView, name="Register"),
    path('login/', LoginView, name="Login"),
    path('logout/', LogoutView, name="Logout"),
    path('account/', AccountView, name="Account"),
    path('dashboard/', DashboardView, name="Dashboard"),
    path('account/delete/',deleteModel),
]
