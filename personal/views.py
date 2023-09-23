from django.shortcuts import render
from account.models import Account
from .models import pdfFile

#from chatgpt 
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.conf import settings
import os
#rest framework permissions

# for downlaoding files




# Create your views here.

def home_screen_view(request):
       # print(request.headers)

       #first way of passing variable into html
       context ={}   
       

       # context['some_string'] = "this is some string that i'am passing to the view"
       # context['some_number'] = 876432837

       #second way of passing variable into html
       # context = {
       #        'some_string' : "this is some string that i'am passing to the view",
       #        'some_number': 8493874
       # }

       # way of passing list  into html
       # list_of_values =[]
       # list_of_values.append("first entry")
       # list_of_values.append("second entry")
       # list_of_values.append("third entry")
       # list_of_values.append("fourth entry")
       # context['list_of_values'] = list_of_values

       # questions =Question.objects.all()
       # context['questions']=questions

       #quering users 
       accounts =Account.objects.all()
       context['accounts'] = accounts,

       obj = pdfFile.objects.all()

       return render(request,"personal/home.html",context)



# view for success
def success_view(request):
       return render(request, "personal/sandar/SuccessMessage.html",{})  #  success message view

# creating views for sandar pages
def four_basic_operations_view(request):
       return render(request,"personal/sandar/four_basic_operations.html",{})

def directed_numbers_view(request):
       return render(request,"personal/sandar/directed_numbers.html",{})

def all_operations_view(request):
       return render(request,"personal/sandar/all_operations.html",{})

#creating views for decimals pages
def onedigitarithmetics_view(request):
       return render(request,"personal/onduktar/onedigitarithmetics.html",{})


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.conf import settings
import os

@login_required
def download_file(request, file_name):
    # Check if the user is authenticated before allowing file download
    if request.method == 'GET':
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)  # Assuming the file is stored in the media root directory
        
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/vnd.ms-powerpoint')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                return response
        else:
            raise Http404("File does not exist.")