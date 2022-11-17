import os
from os import truncate
from time import time
from django.shortcuts import render, redirect
from .models import DataEntry
from cassandra.cluster import Cluster
from .forms import UserRegisterForm, EditProfileForm, UploadFileForm, DownloadFileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
import pandas as pd
from django.forms import model_to_dict
from django_pandas.io import read_frame
from cassandra.auth import PlainTextAuthProvider

def index(request):
    return render(request, 'user/index.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}, your account was created successfully, you just need to login')
            return redirect('index')
    else:
        form = UserRegisterForm()

    return render(request, 'user/register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'user/profile.html')
@login_required()
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'user/edit_profile.html', args)
@login_required()
def delete_user(request,pk):
    user = User.objects.filter(username=pk)
    user.delete()
    return redirect('index')

from django.http import HttpResponse
from io import BytesIO

def download(df):
    with BytesIO() as b:
        writer = pd.ExcelWriter(b, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        filename = str(datetime.now().date()) + '.xlsx'
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

def return_updown(request, path, form):
    return render(request, path, {'form': form})

def pass_request(request):
    if request.method == "POST":
        form = request.POST
        brand_name = form.get('brand_name').split(";")
        shop_id = form.get('shop_id').split(";")
        item_id = form.get('item_id').split(";")
        start_date = form.get('start_date')
        end_date = form.get('end_date')
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except:
            pass
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except:
            pass
        q = DataEntry.objects.limit(None)
        if not (brand_name == ['']):
            q = q.filter(brand_name__in=brand_name)
        if not (shop_id == ['']):
            q = q.filter(shop_id__in=shop_id)
        if not (item_id == ['']):
            q = q.filter(item_id__in=item_id)
        if (isinstance(type(start_date),datetime)):
            q = q.filter(date__gt=start_date)
        if (isinstance(type(end_date),datetime)):
            q = q.filter(date__lt=end_date)
        lst = list(q[:])
        df = pd.DataFrame.from_records([s.to_dict() for s in lst])
        return download(df)
    return return_updown(request, 'visualisation/query_data.html', DownloadFileForm())
def display_request():
    return redirect('index')

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            df = pd.DataFrame()
            if (".csv" in f.name):
                df = pd.read_csv(f)
            elif (".xlsx" in f.name):
                df = pd.read_excel(f)
            else:
                return return_updown(request, 'visualisation/upload.html', UploadFileForm())
            auth_provider = PlainTextAuthProvider(username=os.getenv('CASSANDRA_DB_USER'), password=os.getenv('CASSANDRA_DB_PASSWORD'))
            cluster = Cluster(contact_points=[os.getenv('CASSANDRA_DB_HOST')],auth_provider=auth_provider)
            session = cluster.connect()
            session.set_keyspace('RS')
            for index, row in df.iterrows():
                print(index)
                try:
                    insert = DataEntry(brand_name=row['brand_name'], shop_id=row['shop_id'], item_id=row['item_id'] ,date=datetime.strptime(row['date'], '%Y-%m-%d') ,shop_name=row['shop_name'], item_name=row['item_name'], item_price=row['item_price'], item_cnt_day=row['item_cnt_day'])
                    insert.save()
                except:
                    insert = DataEntry(brand_name=row['brand_name'], shop_id=row['shop_id'], item_id=row['item_id'] ,date=row['date'].date() ,shop_name=row['shop_name'], item_name=row['item_name'], item_price=row['item_price'], item_cnt_day=row['item_cnt_day'])
                    insert.save()
            cluster.shutdown()
            return redirect('index')
    return return_updown(request, 'visualisation/upload.html', UploadFileForm())