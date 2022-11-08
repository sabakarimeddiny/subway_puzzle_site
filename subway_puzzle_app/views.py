import re
import json
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.urls import reverse
from .src.puzzle import Puzzle
from .forms import TrainForm

def index(request, form=None, start=None, end=None, colors=None):
   # if this is a POST request we need to process the form data
   a = Puzzle()

   if request.method == 'POST':
      # create a form instance and populate it with data from the request:
      form = TrainForm(request.POST, auto_id="trainForm_%s")
      # check whether it's valid:
      if form.is_valid(): # also fills the cleaned_data attr
         train_1 = form.cleaned_data.get('train_1')
         train_2 = form.cleaned_data.get('train_2')
         train_3 = form.cleaned_data.get('train_3')
         solution = json.loads(form.cleaned_data.get('solution'))
         # print(request.POST['sol'])
         # print(request.POST.get("sol", ""))
         # solution = json.loads(request.POST.get("sol", ""))
         answer = [train_1, train_2, train_3]
         answer = [x for x in answer if x != '']
         print(a.check_solution(answer, solution))
         colors = [0,0,0]
         return index(request, form, start, end, colors)
         # return render(request, 'index.html', {'form': form, 'start': start, 'end': end, 'colors': colors})
         # is_correct = a.verify_solution(answer, solution)
         # if is_correct:
         #    return correct(request)
         # else:
         #    return incorrect(request)

   elif start is not None:
      solution = a.find_connecting_lines(a.find_shortest_paths(start, end))
      print(solution)
   
   else:
      stations = a.choose_random_stations()
      start = stations[0]
      end = stations[1]
      solution = a.find_connecting_lines(a.find_shortest_paths(start, end))
      print(solution)
      form = TrainForm(auto_id="trainForm_%s", initial={'solution': json.dumps(solution)})
      colors = [0,0,0]
      index(request, form, start, end, colors)
      return render(request, 'index.html', {'form': form, 'start': start, 'end': end, 'colors': colors})

def indexPost(request, start, end, colors):
   # if this is a POST request we need to process the form data
   # create a form instance and populate it with data from the request:
   form = TrainForm(request.POST, auto_id="trainForm_%s")
   # check whether it's valid:
   if form.is_valid(): # also fills the cleaned_data attr
      train_1 = form.cleaned_data.get('train_1')
      train_2 = form.cleaned_data.get('train_2')
      train_3 = form.cleaned_data.get('train_3')
      solution = json.loads(form.cleaned_data.get('solution'))
      # print(request.POST['sol'])
      # print(request.POST.get("sol", ""))
      # solution = json.loads(request.POST.get("sol", ""))
      answer = [train_1, train_2, train_3]
      answer = [x for x in answer if x != '']
      print(a.check_solution(answer, solution))
      colors = [0,0,0]
      return render(request, 'index.html', {'form': form, 'start': start, 'end': end, 'colors': colors})
      # is_correct = a.verify_solution(answer, solution)
      # if is_correct:
      #    return correct(request)
      # else:
      #    return incorrect(request)

def correct(request):
    return render(request, 'correct.html')

def incorrect(request):
    return render(request, 'incorrect.html')

# def login(request):
#     return render(request, 'login.html')


# def index(request):
#    return render(request, 'index.html')
