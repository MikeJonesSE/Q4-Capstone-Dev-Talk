from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
<<<<<<< HEAD
from uploads.models import Image
from uploads.forms import ImageForm


# Create your views here
# def upload_view(request):
#     if request.method == "POST":
#         form=ImageForm(data=request.POST,files=request.FILES)
#         if form.is_valid():
#             form.save()
#             obj=form.instance
#             return HttpResponseRedirect('uploads.html')
#     else:
#         form = ImageForm()
#         img=Image.objects.all()
#     return render(request, 'form.html', {'img':img,'form':form})
=======
from uploads.models import Image, Comment
from uploads.forms import ImageForm, AddCommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
>>>>>>> master

def AddPostView(request):
    if request.method == 'POST':

        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            post = Image.objects.create(
                caption=data['caption'],
                image=data['image'],
                author= request.user,
        )
        return HttpResponseRedirect(reverse('homepage'))
    form = ImageForm()
    return render(request, 'form.html', {'form': form})

def AddComment(request, pk):
    target_post = Image.objects.get(pk = pk)
    if request .method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            posts = Comment.objects.create(
            sender = request.user,
            post = target_post,
            body = data['body']
        )
        return HttpResponseRedirect(reverse('homepage'))

    form = AddCommentForm()
    return render(request, 'form.html', {'form': form})

def delete_comment(request,pk):
        comment = Comment.objects.get(pk=pk)
        if request.user.id == comment.sender.id:
            comment.delete()
            return redirect('homepage')


def post_likes(request, pk):
    post = Image.objects.get(pk=pk)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('homepage'))