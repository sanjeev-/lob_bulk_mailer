from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm
from .models import Document
import os
import pandas as pd 
from .utils import template_to_lob_postcard
import lob
import numpy as np


# Create your views here.

def dashboard_view(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_DIR = BASE_DIR + '/media'
    qs = Document.objects.all()

    context = {
        'qs': qs,
    }

    if request.method == 'POST':
        lob.api_key = 'test_54a8dbb2a9b9ba5774cb53597f8f2a3e9b9'
        print(request.POST['csv_template'])
        template_path = os.path.join(MEDIA_DIR, request.POST['csv_template'])
        print('api key is: {}'.format(lob.api_key))
        addr = pd.read_csv(template_path)
        print(addr)
        gcp_path = 'https://ribbon-public-assets.storage.googleapis.com/mailers/'
        front = os.path.join(gcp_path, request.POST['front_flyer'])
        back = os.path.join(gcp_path, request.POST['back_flyer'])
        numrows = addr.shape[0]
        for i in range(numrows):
            try:
                print(addr.iloc[i])

                print('OK going to run Template to Lob func now!')
                print('front url is {}'.format(front))
                print('back url is {}'.format(back))
                template_to_lob_postcard(addr.iloc[i], front, back)
            except:
                'address: {} has failed!'.format(addr.iloc[i]['street_address_line_1'])
        

    return render(request,'dashboard.html',context)


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    else:
        form = DocumentForm()
    return render(request, 'upload_csv.html', {
        'form': form
    })
