from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from community.models import CommunityImage, CommunityComment
from community.forms import CIForm, RespondForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from notifs.models import Notifs

@login_required
def FeedView(request):
    cposts = CommunityImage.objects.all()

    return render(request, 'community.html', {'posts': cposts})


def DetailPostView(request, pk):
    post = CommunityImage.objects.get(id=pk)
    return render(request, 'community_detail.html', {'post': post})

@login_required
def AddCPostView(request):
    if request.method == 'POST':

        form = CIForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            post = CommunityImage.objects.create(
                caption=data['caption'],
                image=data['image'],
                author=request.user,
            )
        return HttpResponseRedirect(reverse('community_feed'))
    form = CIForm()
    return render(request, 'form.html', {'form': form})

@login_required
def AddCComment(request, pk):
    target_post = CommunityImage.objects.get(pk=pk)
    if request .method == 'POST':
        form = RespondForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            posts = CommunityComment.objects.create(
                sender=request.user,
                post=target_post,
                body=data['body']
            )
        commenter = request.user
        owner = target_post.author
        message = "Just commented on your Post."
        if commenter != owner:
            notify = Notifs.objects.create(
                reciever=owner, sender=commenter, message=message)
        return HttpResponseRedirect(reverse('community_feed'))

    form = RespondForm()
    return render(request, 'form.html', {'form': form})

@login_required
def delete_ccomment(request, pk):
    comment = CommunityComment.objects.get(pk=pk)
    comment.delete()
    return redirect('community_feed')

@login_required
def cpost_likes(request, pk):
    post = CommunityImage.objects.get(pk=pk)
    owner = post.author
    user = request.user
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        if user != owner:
            message = "Just liked your post."
            notify = Notifs.objects.create(
                reciever=owner, sender=user, message=message)
    return HttpResponseRedirect(reverse('community_feed'))
