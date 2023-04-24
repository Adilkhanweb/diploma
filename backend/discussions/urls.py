from django.urls import path

from discussions import views

# Create your models here.
app_name = 'discussions'
urlpatterns = [
    path('', views.index, name='discussions-list'),
    path('<slug:slug>/', views.discussion_detail, name='discussion-detail'),
    path('reply/<int:reply_id>/<str:vote_type>/vote/', views.vote, name='vote'),
    path('discussion/<slug:slug>/<str:vote_type>/vote/', views.discussion_vote, name='discussion-vote'),
    path('discussion/<slug:slug>/<int:reply_id>/set-correct/', views.discussion_set_correct,
         name='discussion-set-correct'),
    path('reply/<int:reply_id>/delete/', views.delete_reply, name='delete-reply'),
]
