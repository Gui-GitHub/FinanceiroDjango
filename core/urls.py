from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Cada URL
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro-gasto/', views.GastoCreateView.as_view(), name='cadastro_gastos'),
    path('relatorio/', views.RelatorioView.as_view(), name='relatorio'),
    path('cadastro-usuario/', views.cadastro_usuario, name='cadastro_usuario'),
    # path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
]