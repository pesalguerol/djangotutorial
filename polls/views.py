from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from .forms import NameForm,ContactForm
from django.core.mail import send_mail

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
            "question": question,
            "error_message": "You didn't select a choice",
        },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data["your_name"]
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return  render(request, "polls/thanks.html", {"name": name})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
        action = "thanks"

    return render(request, "polls/name.html", {"form": form, "action": action})


def get_contact(request):
    # if this is a POST request we need to process the form data
    
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]
            recipients = ["info@example.com"]

        if cc_myself:
            recipients.append(sender)

            return  render(request, "polls/showcontact.html", {"subject": subject, "message": message})
    else:
        form = ContactForm()
        action = "showcontact"

   
    return render(request, "polls/name.html", {"form": form, "action": action})


def thanks(request):
    return render(request, "polls/thanks.html")


'''
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)
    

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
        
    return render(request, "polls/detail.html", {"question" : question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
            "question": question,
            "error_message": "You didn't select a choice",
        },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))'''