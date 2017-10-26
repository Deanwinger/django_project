from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog\post\list.html'


# Create your views here.
def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog\post\list.html',
                  {'posts': posts,
                   'page': page})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog\post\detail.html', {'post': post})



def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status ='published')
    cd = None
    if request.method == 'POST':
        # 保存在request.POST中提交的数据创建一个表单实例
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 如果表单数据验证通过，form.cleaned_data获取验证过的数据(dict)
            cd = form.cleaned_data
            #...send eamil
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', 
        {'post': post, 'form': form})


