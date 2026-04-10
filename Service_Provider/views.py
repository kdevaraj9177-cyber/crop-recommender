


from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Q
import datetime
import xlwt
from django.http import HttpResponse
from django.db.models import FloatField
from django.db.models.functions import Cast
# from django.db.models import Cast, FloatField


# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import re
# from sklearn.ensemble import VotingClassifier
# import warnings
# warnings.filterwarnings("ignore")
# plt.style.use('ggplot')
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import f1_score

# Create your views here.
from Remote_User.models import ClientRegister_Model,crop_prediction,detection_ratio,detection_accuracy,crop_recommendation


# def serviceproviderlogin(request):
#     if request.method  == "POST":
#         admin = request.POST.get('username')
#         password = request.POST.get('password')
#         if admin == "Admin" and password =="Admin":
#             return redirect('View_Remote_Users')

#     return render(request,'SProvider/serviceproviderlogin.html')


def serviceproviderlogin(request):
    if request.method == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')

        if admin == "Admin" and password == "Admin":
            request.session['service_provider'] = admin   # ✅ ADD THIS
            return redirect('View_Remote_Users')

    return render(request, 'SProvider/serviceproviderlogin.html')

def login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check user safely
        user = ClientRegister_Model.objects.filter(
            username=username,
            password=password
        ).first()

        if user:
            # save user id in session
            request.session['userid'] = user.id

            return redirect('View_Remote_Users')
        else:
            # login failed
            return render(
                request,
                'RUser/login.html',
                {'error': 'Invalid username or password'}
            )

    return render(request, 'RUser/login.html')

def View_All_Crop_Yield_Prediction(request):

    obj = crop_prediction.objects.all()
    return render(request, 'SProvider/View_All_Crop_Yield_Prediction.html', {'objs': obj})

def View_All_Crop_Recommendations(request):
    obj = crop_recommendation.objects.all()
    return render(request, 'SProvider/View_All_Crop_Recommendations.html', {'objs': obj})

# def View_Remote_Users(request):
#     obj=ClientRegister_Model.objects.all()
#     return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

def View_Remote_Users(request):
    obj = ClientRegister_Model.objects.all()
    return render(request, 'SProvider/View_Remote_Users.html', {'objects': obj})

# from django.http import HttpResponse

# def View_Remote_Users(request):
#     return HttpResponse("Working fine")

def ViewTrendings(request):
    topic = crop_prediction.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return  render(request,'SProvider/ViewTrendings.html',{'objects':topic})

def negativechart(request,chart_type):
    dd = {}
    pos, neu, neg = 0, 0, 0
    poss = None
    topic = crop_prediction.objects.values('ratings').annotate(dcount=Count('ratings')).order_by('-dcount')
    for t in topic:
        topics = t['ratings']
        pos_count = crop_prediction.objects.filter(topics=topics).values('names').annotate(topiccount=Count('ratings'))
        poss = pos_count
        for pp in pos_count:
            senti = pp['names']
            if senti == 'positive':
                pos = pp['topiccount']
            elif senti == 'negative':
                neg = pp['topiccount']
            elif senti == 'nutral':
                neu = pp['topiccount']
        dd[topics] = [pos, neg, neu]
    return render(request,'SProvider/negativechart.html',{'object':topic,'dd':dd,'chart_type':chart_type})

def charts(request,chart_type):
    chart1 = crop_prediction.objects.values('names').annotate(dcount=Avg(Cast('Yield_Prediction', FloatField())))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def charts1(request,chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts1.html", {'form':chart1, 'chart_type':chart_type})

def likeschart(request,like_chart):
    charts =detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})

def likeschart1(request,like_chart):
    charts =crop_prediction.objects.values('names').annotate(dcount=Avg('Production_Prediction'))
    return render(request,"SProvider/likeschart1.html", {'form':charts, 'like_chart':like_chart})

def Download_Trained_DataSets(request):

    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="TrainedData.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj = crop_prediction.objects.all()
    data = obj  # dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row.State_Name, font_style)
        ws.write(row_num, 1, my_row.names, font_style)
        ws.write(row_num, 2, my_row.Area, font_style)
        ws.write(row_num, 3, my_row.Soil_Type, font_style)
        ws.write(row_num, 4, my_row.Yield_Prediction, font_style)
        ws.write(row_num, 5, my_row.Production_Prediction, font_style)

    wb.save(response)
    return response

def Train_Test_DataSets(request):
    return render(request, 'SProvider/Train_Test_DataSets.html', {'objs': []})













