from django.http import Http404, JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.pagination import make_pagination
from utils.reporting_metrics import get_promoters_sales_metrics
from apps.sales.forms import PromoterSaleForm
from apps.sales.models import ChipSale
from apps.inventory.models import PromoterStock
from apps.sales.filters import ChipSaleFilter

User = get_user_model()

PER_PAGE = 10

def teste(request):
    return render(request, "sales/pages/orders_sales.html")