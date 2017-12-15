from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView, View
from .models import Question, Choice
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.utils import timezone

# Create your views here.
#classes
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest'

    def get_queryset(self):
        """Return the last five published questions."""
        #return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#functions
def index(request):
	latest = Question.objects.order_by('-pub_date')[:5]
	#output = ', '.join([q.question_text for q in latest])
	#template = loader.get_template('polls/index.html')
	template = 'polls/index.html'
	context = {
		'latest':latest
	}
	#return HttpResponse(template.render(context, request))
	return render(request, template, context )

def detail(request, qid):
	template = 'polls/detail.html'
	question = get_object_or_404(Question, pk=qid)
	context = {
		'question':question
	}
	#try:
	#	question = Question.objects.get(pk=qid)
	#	context = {
	#		'question':question
	#	}
	#except Question.DoesNotExist:
	#	raise Http404
	#return HttpResponse('question %s' % qid)
	return render(request, template, context)

def results(request, qid):
	question = get_object_or_404(Question, pk=qid)
	return render(request, 'polls/results.html', {'question': question})

	#return HttpResponse('Results of question %s' % qid)

def vote(request, qid):
	question = get_object_or_404(Question, pk=qid)
	context = {
		'question':question
	}
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
	# Redisplay the question voting form
		return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    #return HttpResponse('voting on question %s' % qid)