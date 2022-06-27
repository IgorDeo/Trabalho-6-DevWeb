from curses.ascii import HT
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify


from categoria.models import Categoria
from produto.forms import ProdutoForm, QuantidadeForm

from produto.models import Produto

def index(request):
    return render(request, 'produto/index.html')


def lista_produto(request):

    produtos = Produto.objects.all()
    print(produtos)

    forms = []
    for produto in produtos:
        form = QuantidadeForm(initial={'quantidade': produto.quantidade, 'produto_id': produto.id})
        forms.append(form)

    return render(request, 'produto/lista_produto.html', {'listas':zip(produtos, forms)})

def cadastra_produto(request):
    if request.POST:
        produto_id = request.session.get('produto_id')
        print('produto_id na sessão = ' + str(produto_id))
        if produto_id:
            produto = get_object_or_404(Produto, pk=produto_id)
            produto_form = ProdutoForm(request.POST, request.FILES, instance=produto)
        else:
            produto_form = ProdutoForm(request.POST, request.FILES)

        if produto_form.is_valid():
            produto = produto_form.save(commit=False)
            produto.slug = slugify(produto.nome)
            total = int(produto.quantidade) * int(produto.preco)
            produto.save()
            print('produto salvo com sucesso')
            if produto_id:
                messages.add_message(request, messages.INFO, 'Produto alterado com sucesso!')
                del request.session['produto_id']
            else:
                messages.add_message(request, messages.INFO, 'Produto cadastrado com sucesso!')

            # retornar JSON response com os dados aqui
            return JsonResponse([model_to_dict(produto), {'categoria': produto.categoria, 'total': total }], safe=False)
            # return render(request, 'produto/index.html', {'form': produto_form})
    else:
        try:
            del request.session['produto_id']
        except KeyError:
            pass
        produto_form = ProdutoForm()

    return render(request, 'produto/cadastra_produto.html', {'form': produto_form})
