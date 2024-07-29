from django.db import transaction,connection
from django.db.models import Count,ExpressionWrapper,F,DecimalField
from django.shortcuts import render

from accounts.models import Profile
from cloths.models import Cloth
from orders.models import Order,OrderItem

# @transaction.atomic
# def show_data(request):
#     # queryset = OrderItem.objects.annotate(total_price=ExpressionWrapper(F('price')*0.95,output_field=DecimalField()))
#     # queryset = list(Cloth.objects.raw("SELECT title,id FROM cloths_cloth"))
#     with connection.cursor() as cursor:
#         cursor.callproc(procname="testfunc")
#         results = cursor.fetchall()

#     return render(request,"cloths/hello.html")