from turtle import update
from django.shortcuts import redirect, render
from .models import StockCode
from django.views.generic import DetailView
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect


def is_user_authenticated(request):
    context = {'status_stock': 'active',}
    if request.user.is_authenticated:  # 유저가 로그인 되어있다면.
        interested_stocks = request.user.interested_code.all()
        context['interested_stocks'] = interested_stocks
        return context

def stock_home(request):
    context = is_user_authenticated(request)
    
    return render(request, 'stock/stock_home.html', context)

class StockDetailView(DetailView):
    model = StockCode
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            interested_stocks = self.request.user.interested_code.all()
            context['interested_stocks'] = interested_stocks
            return context

def stock_register(request):
    if request.user.is_authenticated:
        if request.GET.get('company_code_add'):
            comp_code = request.GET.get('company_code_add')
            stock = StockCode.objects.get(company_code=comp_code)
            stock.interested_user.add(request.user)
            stock.has_user = True
            stock.save()
            messages.success(request, f'{stock.company_name}이 관심목록에 추가되었습니다.')

        elif request.GET.get('company_code_del'):
            comp_code = request.GET.get('company_code_del')
            stock = StockCode.objects.get(company_code=comp_code)
            stock.interested_user.remove(request.user)
            if not stock.interested_user.all():  # 해당 코드에 관심을 가진 유저가 없으면
                stock.has_user = False
                stock.save()
            messages.success(request, f'{stock.company_name}이 관심목록에서 삭제되었습니다.')

        else:
            comp_code = request.GET.get('company_code_del_side')
            stock = StockCode.objects.get(company_code=comp_code)
            stock.interested_user.remove(request.user)
            if not stock.interested_user.all():
                stock.has_user = False
                stock.save()
            messages.success(request, f'{stock.company_name}이 관심목록에서 삭제되었습니다.')
            
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)
    else:
        stock = StockCode.objects.get(company_code=request.GET.get('company_code_add'))
        messages.warning(request, f'로그인이 필요합니다.')
        return redirect('user-login')

def stock_search(request):

    if 'kw' in request.GET:
        query = request.GET.get('kw').strip()
        if query == '':
            return redirect('stock-home')
        search_result = StockCode.objects.filter(
            Q(company_name__icontains=query)
        )
        context = {
            'query': query,
            'status_stock': 'active'
        }
    
    context.update(is_user_authenticated(request))
    paginator = Paginator(search_result, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['page_obj'] = page_obj
    
    return render(request, 'stock/stock_search.html', context)