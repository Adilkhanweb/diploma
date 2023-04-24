from django.shortcuts import render, get_object_or_404, redirect

from discussions.forms import ReplyForm, DiscussionForm
from discussions.models import Discussion, Vote, Reply, DiscussionVote
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    discussions = Discussion.objects.order_by('-score', '-visits')
    form = DiscussionForm()
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            disc = form.save(commit=False)
            disc.creator = request.user
            disc.save()
    return render(request, "discussions/discussions-list.html"
                  , {
                      "discussions": discussions,
                      "form": form,
                  })


def discussion_detail(request, slug):
    discussion = get_object_or_404(Discussion, slug=slug)
    discussion.sum_visits(request.user.id)
    replies = discussion.replies.order_by('-score')
    form = ReplyForm()
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.discussion = discussion
            reply.save()
    return render(request, "discussions/discussions-detail.html",
                  {"discussion": discussion, "replies": replies, 'form': form})


@login_required
def vote(request, reply_id, vote_type):
    reply = get_object_or_404(Reply, id=reply_id)
    try:
        vote = Vote.objects.get(user=request.user, reply=reply)
        if vote.vote_type == vote_type:
            # User is trying to vote the same way they did before, so undo the vote
            if vote_type == 'up':
                reply.up_votes -= 1
            else:
                reply.down_votes -= 1
            vote.delete()
        else:
            # User is changing their vote
            if vote_type == 'up':
                reply.up_votes += 1
                reply.down_votes -= 1
            else:
                reply.up_votes -= 1
                reply.down_votes += 1
            vote.vote_type = vote_type
            vote.save()
    except Vote.DoesNotExist:
        # User has not voted on this answer before
        if vote_type == 'up':
            reply.up_votes += 1
        else:
            reply.down_votes += 1
        vote = Vote(user=request.user, reply=reply, vote_type=vote_type)
        vote.save()
    reply.save()
    return redirect('discussions:discussion-detail', slug=reply.discussion.slug)


@login_required
def discussion_vote(request, slug, vote_type):
    discussion = get_object_or_404(Discussion, slug=slug)
    try:
        vote = DiscussionVote.objects.get(user=request.user, discussion=discussion)
        if vote.vote_type == vote_type:
            # User is trying to vote the same way they did before, so undo the vote
            if vote_type == 'up':
                discussion.up_votes -= 1
            else:
                discussion.down_votes -= 1
            vote.delete()
        else:
            # User is changing their vote
            if vote_type == 'up':
                discussion.up_votes += 1
                discussion.down_votes -= 1
            else:
                discussion.up_votes -= 1
                discussion.down_votes += 1
            vote.vote_type = vote_type
            vote.save()
    except:
        pass
        # User has not voted on this answer before
        if vote_type == 'up':
            discussion.up_votes += 1
        else:
            discussion.down_votes += 1
        vote = DiscussionVote(user=request.user, discussion=discussion, vote_type=vote_type)
        vote.save()
    discussion.save()
    return redirect('discussions:discussion-detail', slug=discussion.slug)


def discussion_set_correct(request, slug, reply_id):
    discussion = get_object_or_404(Discussion, slug=slug)
    reply = get_object_or_404(Reply, id=reply_id)
    if discussion.correct and discussion.correct == reply:
        discussion.correct = None
        discussion.status = Discussion.Status.NOT_ANSWERED
        discussion.save()
    else:
        discussion.correct = reply
        discussion.status = Discussion.Status.ANSWERED
        discussion.save()
    return redirect('discussions:discussion-detail', slug=discussion.slug)


def delete_reply(request, reply_id):
    reply = Reply.objects.get(id=reply_id)
    discussion = reply.discussion
    reply.delete()
    return redirect('discussions:discussion-detail', slug=discussion.slug)
