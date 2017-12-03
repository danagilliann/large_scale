from django import forms
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Answer, AnswerForm, MyUserCreationForm, Profile, ProfileForm, Question, QuestionForm, University, UniversityForm, Following, FollowingForm

# Anonymous views
#################
def index(request):
  if request.user.is_authenticated():
    return home(request)
  else:
    return anon_home(request)

def anon_home(request):
  return render(request, 'micro/public.html')

def register(request):
  if request.method == 'POST':
    form = MyUserCreationForm(request.POST)
    new_user = form.save(commit=True)
    # Log in that user.
    _user = authenticate(username=new_user.username,
                        password=form.clean_password2())
    if _user is not None:
      login(request, _user)
    else:
      raise Exception
    return home(request)
  else:
    form = MyUserCreationForm
  return render(request, 'micro/register.html', {'form' : form})

def universities(request):
  # get all universities from DB (names and id)
  university_list = University.objects.all();
  context = {
    'university_list' : university_list,
    'form': UniversityForm
  }
  return render(request, 'micro/universities.html', context)

def university(request, university_id, message=None):
  # get uni with the specific id
  _university = University.objects.get(id=university_id)

  # get all questions from this university
  question_list = Question.objects.filter(university_id=university_id);

  context = {
    'university' : _university,
    'question_list': question_list,
    'question_form' : QuestionForm,
    'message' : message
  }
  return render(request, 'micro/university.html', context)

def question(request, question_id, message=None):
  # get question and university with the specific id
  _question = Question.objects.get(id=question_id)
  _university = University.objects.get(id=_question.university_id)

  # get all answers from this question
  answer_list = Answer.objects.filter(question_id=question_id)

  # check if user has already followed this question
  not_followed = Following.objects.filter(question_id=question_id).filter(user_id=request.user.id).count() == 0

  context = {
    'question' : _question,
    'university' : _university,
    'answer_list' : answer_list,
    'answer_form' : AnswerForm,
    'not_followed': not_followed,
    'message' : message
  }

  return render(request, 'micro/question.html', context)

def answer(request, answer_id):
  # get answer and question with the specified id
  _answer = Answer.objects.get(id=answer_id)

  context = {
    'answer' : _answer
  }

  return render(request, 'micro/answer.html', context)

def user(request, user_id):
  return render(request, 'micro/user.html')


# Authenticated views
#####################
@login_required
def home(request):
  return universities(request)

@login_required
def user(request, user_id):
  _user = User.objects.get(id=user_id)
  _profile = Profile.objects.get(user_id=user_id)
  _university = None
  profile_form = None
  if _profile.university_id:
    _university = University.objects.get(id=_profile.university_id)
  if _user == request.user:
    if request.method == 'POST':
      profile_form = ProfileForm(request.POST, instance=request.user.profile)
      _profile = profile_form.save(commit=True)
      _university = _university = University.objects.get(id=_profile.university_id)
    else:
      profile_form = ProfileForm(instance=request.user.profile)

  context = {
    'user' : _user,
    'profile' : _profile,
    'university': _university,
    'profile_form' : profile_form
  }
  return render(request, 'micro/user.html', context)


@login_required
def post_university(request):
  if request.method == 'POST':
      form = UniversityForm(request.POST)
      form.save(commit=True)
  return universities(request)

@login_required
def follow_question(request, question_id):
  # follow this question
  print(request.user)
  print(question_id)

  if request.method == 'POST':
    form = FollowingForm(request.POST)
    follow = form.save(commit=False)
    follow.user = request.user
    follow.question = Question.objects.get(id=question_id)
    follow = form.save(commit=True)

  return redirect('/micro/question/' + question_id)

@login_required
def post_question(request, university_id):
  message = None
  _profile = Profile.objects.get(user_id=request.user.id)
  if request.method == 'POST':
    _university = University.objects.get(id=university_id)
    print(_profile.university_id)
    print(university_id)
    print(str(_profile.university_id) + " and " + str(university_id))
    if long(_profile.university_id) == long(university_id):
      form = QuestionForm(request.POST)
      new_question = form.save(commit=False)
      new_question.user = request.user
      new_question.university = _university
      if (form.is_valid()):
        new_question = form.save(commit=True)
        return question(request, new_question.id)
      else:
        message = "Form invalid"
    else:
      print("HEREEEE")
      message = "You must be in " + str(_university) + " to ask a question."
  return university(request, university_id, message)

@login_required
def post_answer(request, question_id):
  _question = Question.objects.get(id=question_id)
  _profile = Profile.objects.get(user_id=request.user.id)
  message = None
  if request.method == 'POST':
    if long(_profile.university_id) == long(_question.university_id):
      form = AnswerForm(request.POST)
      new_answer = form.save(commit=False)
      new_answer.question = _question
      new_answer.user = request.user
      if (form.is_valid()):
        new_answer = form.save(commit=True)
      else:
        message = "Form invalid"
    else:
      _university = University.objects.get(id=_question.university_id)
      message="You must be in " + str(_university) + " to answer this question."
  return question(request, question_id, message)