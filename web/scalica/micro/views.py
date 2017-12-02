from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Answer, AnswerForm, MyUserCreationForm, Question, QuestionForm, University, UniversityForm

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
    user = authenticate(username=new_user.username,
                        password=form.clean_password2())
    if user is not None:
      login(request, user)
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

def university(request, university_id):
  # get uni with the specific id
  _university = University.objects.get(id=university_id)

  # get all questions from this university
  question_list = Question.objects.filter(university_id=university_id);

  context = {
    'university' : _university,
    'question_list': question_list,
    'question_form' : QuestionForm
  }
  return render(request, 'micro/university.html', context)

def question(request, question_id):
  # get question and university with the specific id
  _question = Question.objects.get(id=question_id)
  _university = University.objects.get(id=_question.university_id)

  # get all answers from this question
  answer_list = Answer.objects.filter(question_id=question_id)

  context = {
    'question' : _question,
    'university' : _university,
    'answer_list' : answer_list,
    'answer_form' : AnswerForm
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
def post_university(request):
  if request.method == 'POST':
      form = UniversityForm(request.POST)
      form.save(commit=True)
  return universities(request)

@login_required
def follow_question(request):
  # follow this question
  return render(request, 'micro/question.html')

@login_required
def post_question(request, university_id):
  if request.method == 'POST':
    form = QuestionForm(request.POST)
    new_question = form.save(commit=False)
    new_question.user = request.user

    _university = University.objects.get(id=university_id)
    new_question.university = _university
    new_question = form.save(commit=True)
    return question(request, new_question.id)

  else:
    return university(request, university_id)

@login_required
def post_answer(request, question_id):
  _question = Question.objects.get(id=question_id)
  if request.method == 'POST':
    form = AnswerForm(request.POST)
    new_answer = form.save(commit=False)
    new_answer.question = _question
    new_answer.num_upvotes = 0
    new_answer = form.save(commit=True)
  return question(request, _question.id)