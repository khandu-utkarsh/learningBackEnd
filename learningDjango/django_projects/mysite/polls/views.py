from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader 
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.urls import reverse
from django.views import generic


#Let's use Django templating engine to separate Python code from the design of the page.



class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"    


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


#Commenting out the index, details and results view to use the more generic views

# def index(request):

#     #This is another way, using the django shortcuts for generating the templates
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)


#     # #This is one of the way to render templates
#     # latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     # template = loader.get_template("polls/index.html")  #Loading the template
#     # context = {
#     #     "latest_question_list": latest_question_list,
#     # }
#     # return HttpResponse(template.render(context, request))

#     #This is the second basic repsone. Here were are creating output using some query from the Database but nothing serious

#     # #Returning top 5 questions to django
#     # latest_question_lst = Question.objects.order_by("-pub_date")[:5]
#     # output = ", ".join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)

#     #This is a very basic response:
#     #return HttpResponse("Hello, world. You're at the polls index.")

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})

#     #Another way to generate the response if the object is not found or we get 404 error
#     # question = get_object_or_404(Question, pk=question_id)
#     # return render(request, "polls/detail.html", {"question: ": question})
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
    
#     # return render(request, "polls/detail.html", {"question": question}) #I can pass any object I think. This is great

#     #Another way to show response:

#     # return HttpResponse("You're looking at question %s." % question_id)

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})


#     #Very basic thing
#     # responseContent = "You're looking at the result of the question %s. "
#     # return HttpResponse(responseContent % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

    # #This is a dummy method, 
    # return HttpResponse("You are voting on the question %s" %question_id)