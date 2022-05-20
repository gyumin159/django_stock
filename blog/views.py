from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Posts
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

class BlogListView(ListView):
    model = Posts
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    extra_context = {'status_blog': 'active'}
    ordering = ['-date_posted']
    paginate_by = 4
    

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    template_name = 'blog/post_create.html'
    
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ['title', 'content']
    template_name = 'blog/post_create.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    template_name = 'blog/posts_confirm_delete.html'
    
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
def search_func(request):  # 개선할 방법이 있을 거 같다. 지금은 pagination을 위해 kw를 강제로 줘서라도 if문을 돌리는데
                           # (안돌리면 search_result 생성전 참조가 발생.) 한번 if문 돌린걸 저장해서 다시 참조할 순 없을까
    if 'kw' in request.GET:
        query = request.GET.get('kw').strip()
        if query == '':
            return redirect('blog-home')
        search_result = Posts.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
        context = {
            'query': query,
            'status_blog': 'active'
        }
     
    paginator = Paginator(search_result, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['page_obj'] = page_obj
    
    return render(request, 'blog/search_result.html', context)