from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.db.models import F

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model=Question

    def get_queryset(self) -> QuerySet[Any]:
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    template_name = 'polls/results.html'
    model=Question

def indexOldSyntax(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {"latest_question_list": latest_question_list}
    # output = ", ".join([q.question_text for q in latest_question_list])
    # return HttpResponse("Hello, world. You're at the polls index.")
    return HttpResponse(template.render(context, request))


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    # return render(context=context, template_name="polls/index.html", request=request)
    return render(request, "polls/index.html", context)


def detailOldSyntax(request, question_id):
    # return HttpResponse("You are looking at question %s." % question_id)
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, "polls/detail.html", {"question": question})


def detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, "polls/detail.html", {"question": question})


# Create your views here.


def results(request, question_id):
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You didn't select a choice."},
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    # return HttpResponse("You're voting on question %s." % question_id)
