

from produto.models import Produto


def atualiza_valor_total(request):
    
    produtos = Produto.objects.all()

    return {
        'valor_total': zip(produtos, forms)
    }