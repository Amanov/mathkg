from django.shortcuts import render
from account.models import Account
# from .models import pdfFile

#from chatgpt 
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.conf import settings

from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from .models import Resource  # only once
import os


from .models import (
    Topic,
    Subtopic,
)

from .services import (
    get_resources_by_goal,
)


# from .models import Resource
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

       # obj = pdfFile.objects.all()

       return render(request,"resources/home.html",context)



# view for success
def success_view(request):
       return render(request, "personal/sandar/SuccessMessage.html",{})  #  success message view

# # creating views for sandar pages
# def four_basic_operations_view(request):
#        return render(request,"personal/sandar/four_basic_operations.html",{})
def four_basic_operations_view(request):
    resources = Resource.objects.filter(is_active=True)
    res = {r.title: r for r in resources}
    return render(request, 'personal/sandar/four_basic_operations.html', {
        'res': res,
    })

#old hardcoded view for directed numbers

def directed_numbers_view(request):
    resources = Resource.objects.filter(is_active=True)
    res = {r.title: r for r in resources}
    return render(request, 'personal/sandar/directed_numbers.html', {
        'res': res,
    })








# def all_operations_view(request):
#        return render(request,"personal/sandar/all_operations.html",{})

# def all_operations_view(request):
#     resources = Resource.objects.filter(is_active=True)
#     res = {r.title: r for r in resources}
#     return render(request, 'personal/sandar/all_operations.html', {
#         'res': res,
#     })

# Trying to loop trough the files

# Step 4
# One generic view, instead of creating many views

def subtopic_page(request, topic_slug, subtopic_slug):

    topic = get_object_or_404(
        Topic,
        slug=topic_slug
    )

    subtopic = get_object_or_404(
        Subtopic,
        topic=topic,
        slug=subtopic_slug
    )

    resources = Resource.objects.filter(
        subtopic=subtopic,
        is_active=True
    )

    return render(
        request,
        "resources/topic_page.html",
        {
            "topic": topic,
            "subtopic": subtopic,
            "resources": resources,
        }
    )

def all_operations_view(request):
    resources = Resource.objects.filter(is_active=True)
    res = {r.title: r for r in resources}

    # Organized by section - each section can have multiple blocks
    sections = [
        {
            "header": "Сабакка даяр презентациялар",
            "blocks": [
                {
                    "title": "Сабактын көрсөтүү - түшүндүрүү",
                    "files": ["BaardykAmaldarIntro.pptx"],
                    "fallback_image": "img/4-amal-ARALASHAMALDARINTRO-Screenshot.png"
                },
            ]
        },
        {
            "header": "Көрсөтмө суроолору",
            "blocks": [
                {
                    "title": "жеңил, орто, оор",
                    "files": ["BaardykAmaldarJenilOrtoOor.pptx"],
                    "fallback_image": "img/4-amal-ARALASHAMALDARJenilOrtoOor-Screenshot.png"
                },
                {
                    "title": "1234",
                    "files": ["BaardykAmaldar1234.pptx"],
                    "fallback_image": "img/4-amal-ARALASHAMALDAR1234-Screenshot.png"
                },
            ]
        },
        {
            "header": "сабакка даяр иш барактар",
            "blocks": [
                {
                    "title": "цифралык табышмак",
                    "subtitle": "3 деңгээлде",
                    "files": [
                        "BaardykAmaldarMenenSandykBashkatyrma.pptx",
                        "BaardykAmaldarMenenSandykBashkatyrmaA6.pdf",
                        "BaardykAmaldarMenenSandykBashkatyrmaA7.pdf"
                    ],
                    "fallback_image": "img/4-amal-ARALASHAMALDARSandykBashkatyrma-Screenshot.png"
                },
                {
                    "title": "Катаны тап",
                    "files": [
                        "BaardykAmaldarKatanyTap.pptx",
                        "BaardykAmaldarKatanyTapA4.pdf",
                        "BaardykAmaldarKatanyTapA5.pdf"
                    ],
                    "fallback_image": "img/4-amal-katanytapTarsiaKurak.png"
                },
                {
                    "title": "тема боюнча көндүмдөр 1",
                    "files": [
                        "BaardykAmaldar4Fours.pptx",
                        "BaardykAmaldar4FoursA5.pdf"
                    ],
                    "fallback_image": "img/4-amal-ARALASHAMALDARFourFour-Screenshot.png"
                },
                {
                    "title": "тема боюнча көндүмдөр 2",
                    "files": [
                        "BaardykAmaldarMegaEsepter.pptx",
                        "BaardykAmaldarMegaEsepterA4.pdf",
                        "BaardykAmaldarMegaEsepterA5.pdf",
                        "BaardykAmaldarMegaEsepterA6.pdf"
                    ],
                    "fallback_image": "img/4-amal-ARALASHAMALDARMegaEsepter-Screenshot.png"
                },
            ]
        },
        {
            "header": "сабак учурундагы активдүүлүк",
            "blocks": [
                {
                    "title": "карта сорттоо",
                    "files": [
                        "BaardykAmaldarTuuraJeKata.pptx",
                        "BaardykAmaldarTuuraJeKataA4.pdf",
                        "BaardykAmaldarTuuraJeKataA5.pdf",
                        "BaardykAmaldarTuuraJeKataA6.pdf"
                    ],
                    "fallback_image": "img/4-amal-ARALASHAMALDARTuuraJeKata-Screenshot.png"
                },
                {
                    "title": "Тарсия курак",
                    "files": [
                        "BaardykAmaldarTarsiaKurak.pptx",
                        "BaardykAmaldarTarsiaKurakA4.pdf",
                        "BaardykAmaldarTarsiaKurakA5.pdf"
                    ],
                    "fallback_image": "img/4-amal-ARALASHAMALDARTarsiaKurak-Screenshot.png"
                },
                {
                    "title": "Салыштыруу",
                    "files": [
                        "BaardykAmaldarSalywtyr.pptx",
                        "BaardykAmaldarSalywtyrA4.pdf",
                        "BaardykAmaldarSalywtyrA5.pdf"
                    ],
                    "fallback_image": "img/4-amal-ARALASHAMALDARSalywtyr-Screenshot.png"
                },
            ]
        },
        {
            "header": "мугалим жетектеген көндүмдөр",
            "blocks": [
                {
                    "title": "Блокбастер оюну",
                    "files": ["BaardykAmaldarBlockBusterOyunu.pptx"],
                    "fallback_image": "img/4-amal-ARALASHAMALDARBlockBusterOyunu-Screenshot.png"
                },
                {
                    "title": "Жыдымай оюну",
                    "files": ["BaardykAmaldarJydymaiOyunu.pptx"],
                    "fallback_image": "img/4-amal-ARALASHAMALDARJYDYMAIOYUNU-Screenshot.png"
                },
                {
                    "title": "Мага көрсөт",
                    "files": ["BaardykAmaldarMisalKorsot.pptx"],
                    "fallback_image": "img/4-amal-ARALASHAMALDARMisalKorsot-Screenshot.png"
                },
            ]
        },
    ]

    return render(request, 'personal/sandar/all_operations.html', {
        'res': res,
        'sections': sections,
    })

d

#creating views for decimals pages
# def onedigitarithmetics_view(request):
#        return render(request,"personal/onduktar/onedigitarithmetics.html",{})

def onedigitarithmetics_view(request):
    resources = Resource.objects.filter(is_active=True)
    res = {r.title: r for r in resources}
    return render(request, 'personal/onduktar/onedigitarithmetics.html', {
        'res': res,
    })

    

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


#here I want to count the number of downloads of files
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404

def download_file(request, slug):
    file_obj = get_object_or_404(DownloadFile, slug=slug)

    # ✅ Count download
    file_obj.increment_download()

    try:
        return FileResponse(file_obj.file.open('rb'), as_attachment=True)
    except:
        raise Http404("File not found")


# here is update
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from .models import Resource


# --- Show resources on a page ---
def resources_view(request):
    category  = request.GET.get('category', None)     # ?category=worksheet
    resources = Resource.objects.filter(is_active=True)

    if category:
        resources = resources.filter(category=category)

    context = {
        'resources': resources,
        'categories': Resource.CATEGORY_CHOICES,
        'selected_category': category,
    }
    return render(request, 'personal/resources.html', context)


# --- Serve the file + count the download ---
def download_resource_view(request, pk):
    resource = get_object_or_404(Resource, pk=pk, is_active=True)
    resource.increment_download()                      # counts every download
    response = FileResponse(resource.file.open('rb'), as_attachment=True)
    return response


from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum

@staff_member_required  # only site owner can access
def dashboard_view(request):
    resources = Resource.objects.all()

    context = {
        'total_resources'     : resources.count(),
        'active_resources'    : resources.filter(is_active=True).count(),
        'total_downloads'     : resources.aggregate(Sum('download_count'))['download_count__sum'] or 0,
        'presentations'       : resources.filter(category='presentation'),
        'worksheets'          : resources.filter(category='worksheet'),
        'activities'          : resources.filter(category='activity'),
    }
    return render(request, 'resources/dashboard.html', context)

# personal/views.py

from django.shortcuts import get_object_or_404, render
from django.http import FileResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Resource, ResourceDownload


def get_client_ip(request):
    """Extract IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# UPDATE THIS FUNCTION
def download_resource_view(request, pk):
    resource = get_object_or_404(Resource, pk=pk, is_active=True)
    
    # Track the download
    ResourceDownload.objects.create(
        resource=resource,
        user=request.user if request.user.is_authenticated else None,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
    )
    
    # Increment counter
    resource.increment_download()
    
    # Serve file
    response = FileResponse(resource.file.open('rb'), as_attachment=True)
    return response


# ADD THIS NEW VIEW
@staff_member_required
def analytics_dashboard_view(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Overall stats
    total_resources = Resource.objects.filter(is_active=True).count()
    total_downloads = ResourceDownload.objects.count()
    unique_users = ResourceDownload.objects.filter(user__isnull=False).values('user').distinct().count()
    
    # Downloads this week/month
    downloads_this_week = ResourceDownload.objects.filter(downloaded_at__date__gte=week_ago).count()
    downloads_this_month = ResourceDownload.objects.filter(downloaded_at__date__gte=month_ago).count()
    
    # Top 10 most downloaded resources
    top_resources = Resource.objects.annotate(
        dl_count=Count('downloads')
    ).order_by('-dl_count')[:10]
    
    # Top 10 most active users
    top_users = ResourceDownload.objects.filter(
        user__isnull=False
    ).values(
        'user__username', 'user__email'
    ).annotate(
        download_count=Count('id')
    ).order_by('-download_count')[:10]
    
    # Downloads by category
    category_stats = Resource.objects.values('category').annotate(
        total_downloads=Count('downloads')
    ).order_by('-total_downloads')
    
    # Recent activity
    recent_downloads = ResourceDownload.objects.select_related(
        'resource', 'user'
    ).order_by('-downloaded_at')[:20]
    
    # Daily download trend (last 30 days)
    daily_stats = []
    for i in range(30):
        date = today - timedelta(days=i)
        count = ResourceDownload.objects.filter(downloaded_at__date=date).count()
        daily_stats.append({
            'date': date.strftime('%m/%d'),
            'count': count
        })
    daily_stats.reverse()
    
    context = {
        'total_resources': total_resources,
        'total_downloads': total_downloads,
        'unique_users': unique_users,
        'downloads_this_week': downloads_this_week,
        'downloads_this_month': downloads_this_month,
        'top_resources': top_resources,
        'top_users': top_users,
        'category_stats': category_stats,
        'recent_downloads': recent_downloads,
        'daily_stats': daily_stats,
    }
    
    return render(request, 'analytics/analytics_dashboard.html', context)

    