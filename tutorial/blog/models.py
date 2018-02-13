from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from django_comments.moderation import CommentModerator
from django_comments_xtd.moderation import moderator, SpamModerator

from blog.badwords import badwords


class PublicManager(models.Manager):
    def get_queryset(self):
        return super(PublicManager, self).get_queryset()\
                                         .filter(publish__lte=timezone.now())


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    allow_comments = models.BooleanField('allow comments', default=True)
    publish = models.DateTimeField(default=timezone.now)
    objects = PublicManager()  # Our custom manager.

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail',
                       kwargs={'year': self.publish.year,
                               'month': self.publish.strftime('%b'),
                               'day': self.publish.strftime('%d'),
                               'slug': self.slug})


class PostCommentModerator(SpamModerator):
    email_notification = True

    def moderate(self, comment, content_object, request):
        # Make a dictionary where the keys are the words and the message and
        # the values are their relative position in the message.
        def clean(word):
            ret = word
            if word.startswith('.') or word.startswith(','):
                ret = word[1:]
            if word.endswith('.') or word.endswith(','):
                ret = word[:-1]
            return ret

        lowcase_comment = comment.comment.lower()
        msg = dict([(clean(w), i)
                    for i, w in enumerate(lowcase_comment.split())])
        for badword in badwords:
            if isinstance(badword, str):
                if lowcase_comment.find(badword) > -1:
                    return True
            else:
                lastindex = -1
                for subword in badword:
                    if subword in msg:
                        if lastindex > -1:
                            if msg[subword] == (lastindex + 1):
                                lastindex = msg[subword]
                        else:
                            lastindex = msg[subword]
                    else:
                        break
                if msg.get(badword[-1]) and msg[badword[-1]] == lastindex:
                    return True
        return super(PostCommentModerator, self).moderate(comment,
                                                          content_object,
                                                          request)

moderator.register(Post, PostCommentModerator)
