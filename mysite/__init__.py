from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.conf import settings
import os

def download_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='application/vnd.ms-powerpoint')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    
    raise Http404("File does not exist")
