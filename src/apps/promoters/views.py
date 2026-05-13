from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='users:login', redirect_field_name='next')
def chips_sales_list(request):
    return render(request, 'promoters/pages/chip_sales.html')