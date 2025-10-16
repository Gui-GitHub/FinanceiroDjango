from django.urls import path

from . import views

# Cada URL
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('relatorio/', views.RelatorioView.as_view(), name='relatorio'),

    path('cadastro-usuario/', views.cadastro_usuario, name='cadastro_usuario'),
    path('editar-perfil/', views.EditarPerfilView.as_view(), name='editar_perfil'),

    path('meus-gastos/', views.GastoListView.as_view(), name='meus_gastos'),
    path('cadastro-gasto/', views.GastoCreateView.as_view(), name='cadastro_gastos'),
    path('editar-gasto/<int:pk>/', views.GastoUpdateView.as_view(), name='editar_gasto'),
    path('meus-gastos/excluir/<int:pk>/', views.GastoDeleteView.as_view(), name='excluir_gasto'),
    path('gerar_gastos/', views.gerar_gastos_exemplo, name='gerar_gastos_exemplo'),
    path('excluir_gastos/', views.excluir_todos_gastos, name='excluir_todos_gastos'),

    path('meus-ganhos/', views.GanhoListView.as_view(), name='meus_ganhos'),
    path('cadastrar-ganho/', views.GanhoCreateView.as_view(), name='cadastrar_ganho'),
    path('editar-ganho/<int:pk>/', views.GanhoUpdateView.as_view(), name='editar_ganho'),
    path('meus-ganhos/excluir/<int:pk>', views.GanhoDeleteView.as_view(), name='deletar_ganho'),
    path('gerar_ganhos/', views.gerar_ganhos_exemplo, name='gerar_ganhos_exemplo'),
    path('excluir_ganhos/', views.excluir_todos_ganhos, name='excluir_todos_ganhos'),

]