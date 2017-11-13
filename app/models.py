from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.SET_NULL) # A user can have no school, but then they shouldn't be allowed to answer questions

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Question(models.Model):
    timestamp = models.DateField(auto_now_add=True, editable=False)
    text = models.TextField(max_length=500)
    school = models.ForeignKey(School, on_delete=models.CASCADE) # no school -> no question
    user = models.ForeignKey(User, on_delete=models.CASCADE) # no user -> no question

    def get_answers_by_upvotes(self):
        return self.answer_set.order_by('-num_upvotes')

    def get_answers_by_date(self):
        return self.answer_set.order_by('-timestamp')

class Answer(models.Model):
    timestamp = models.DateField(auto_now_add=True, editable=False)
    text = models.TextField(max_length=2000)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    num_upvotes = models.PositiveIntegerField()

class Upvote(models.Model):
    """
    A separate Upvote schema allows us to track users who have already upvoted a question
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

@receiver(post_save, sender=Upvote)
def increment_num_upvotes(sender, instance, created, **kwargs):
    """
    updating num_upvotes on every Upvote save prevents querying for upvote count 
    (which would be costly when used to filter every answer for a question)
    """
    instance.answer.num_upvotes += 1

@receiver(post_delete, sender=Upvote)
def decrement_num_upvotes(sender, instance, created, **kwargs):
    """
    subtract upvote from answer's upvote count if upvote is deleted
    """
    instance.answer.num_upvotes -= 1

class School(models.Model):
    name = models.CharField(max_length=255)



