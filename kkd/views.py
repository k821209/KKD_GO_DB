from django.shortcuts import render

def show_go_list(request):
   return render(request, 'kkd/go_index.html',{})



# Create your views here.
