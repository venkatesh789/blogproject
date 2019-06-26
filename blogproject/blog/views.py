from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post,Comment
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import ListView
from django.core.mail import send_mail
from blog.forms import EmailSendForm,CommentForm
from taggit.models import Tag


def post_share(request,id):
   post = get_object_or_404(Post, id=id, status = 'published')
   send = False
   form = EmailSendForm 
   if request.method == 'POST':
      #form was submitted
      form = EmailSendForm(request.POST)
      #validation of form
      if form.is_valid():
         cd = form.cleaned_data
         post_url = request.build_absolute_uri(post.get_absolute_url())
         subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
         message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
         send_mail(subject, message, 'gauravpb220@gmail.com', [cd['to']])
         print("Email send ")
         send = True
         #data = cd
      else:
         form = EmailSendForm()
   
   return render(request,'blog/share_post.html',{'post':post,'form':form,'send':send})

class PostListView(ListView):
   queryset = Post.objects.all()
   #model = Post
   context_object_name = 'posts'
   paginate_by =3
   

   template_name = 'blog/post_list.html'
   

# Create your views here.
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag = None
    if tag_slug:
       tag = get_object_or_404(Tag,slug = tag_slug)
       post_list = post_list.filter(tags__in=[tag])


    paginator = Paginator(post_list,2) #pass object and number of objects per page
    page_number = request.GET.get('page') # get the page number
    try:
       posts = paginator.page(page_number)
    except PageNotAnInteger:
       posts = paginator.page(1)

    except EmptyPage:
       posts = paginator.page(paginator.num_pages)

    return render(request,'blog/post_list.html',{'page_number':page_number,'post_list':posts,'tag':tag})


def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    # list of active comments

    comments = post.comments.filter(active=True)
    comment_form = CommentForm
    if request.method =='POST':
       comment_form = CommentForm(data = request.POST)
       if comment_form.is_valid():
          new_comment = comment_form.save(commit = False)
          new_comment.post = post #Assign new post to post
          new_comment.save() #Save the new post
          comment_form = CommentForm
      
       else:
          comment_form = CommentForm

    return render(request,'blog/post_detail.html',{'post':post,'comments':comments,'comment_form':comment_form})


def find_post(request):
   value = ['abc']
   # post = get_object_or_404(Post, status ='publis')
   # post = Post.objects.filter(status__iexact='Published')
   # post = Post.objects.filter(id__gte=3, title='Should I learn React.js or Vue.js?')
   #post = get_object_or_404(Post,slug = x)

   obj = Post.objects.filter(slug__iexact='django-blog')
   return render(request,'blog/find.html',{'obj':obj})