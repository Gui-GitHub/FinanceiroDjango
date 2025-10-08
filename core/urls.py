from django.urls import path
from .views import IndexView, PessoaCreateView, GastoCreateView, RelatorioView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('cadastro_pessoa/', PessoaCreateView.as_view(), name='cadastro_pessoa'),
    path('cadastro_gastos/', GastoCreateView.as_view(), name='cadastro_gastos'),
    path('relatorio/', RelatorioView.as_view(), name='relatorio'),
]