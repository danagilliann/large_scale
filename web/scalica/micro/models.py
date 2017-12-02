from django.conf import settings
from django.db import models
from django.forms import ModelForm, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class University(models.Model):
    name = models.CharField(max_length=255)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=255)
    university = models.ForeignKey('University', null=True, on_delete=models.SET_NULL) # A user can have no university, but then they shouldn't be allowed to answer questions

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
    university = models.ForeignKey(University, on_delete=models.CASCADE) # no university -> no question
    user = models.ForeignKey(User, on_delete=models.CASCADE) # no user -> no question
    duplicate_of = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)

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

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        help_texts = {
            'username' : '',
        }

"""
MyUserCreationForm and ProfileForm can be used in the same view for user creation
Reference: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
"""
class ProfileForm(ModelForm):
    class Meta():
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'university']

class QuestionForm(ModelForm):
    class Meta():
        model = Question
        fields = ['text']
        widgets = {
            'text': TextInput(attrs={'id' : 'input_question'}),
        }

class AnswerForm(ModelForm):
    class Meta():
        model = Answer
        fields = ['text']
        widgets = {
           'text': TextInput(attrs={'id' : 'input_answer'}),
         }

class UniversityForm(ModelForm):
    class Meta():
        model = University
        fields = ['name']

"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.forms import ModelForm, TextInput

class Post(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  text = models.CharField(max_length=256, default="")
  pub_date = models.DateTimeField('date_posted')
  def __str__(self):
    if len(self.text) < 16:
      desc = self.text
    else:
      desc = self.text[0:16]
    return self.user.username + ':' + desc

class Following(models.Model):
  follower = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="user_follows")
  followee = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="user_followed")
  follow_date = models.DateTimeField('follow data')
  def __str__(self):
    return self.follower.username + "->" + self.followee.username

# Model Forms
class PostForm(ModelForm):
  class Meta:
    model = Post
    fields = ('text',)
    widgets = {
      'text': TextInput(attrs={'id' : 'input_post'}),
    }

class FollowingForm(ModelForm):
  class Meta:
    model = Following
    fields = ('followee',)

class MyUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    help_texts = {
      'username' : '',
    }
"""
