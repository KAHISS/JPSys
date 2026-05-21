from django.http import Http404, JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.pagination import make_pagination
from utils.reporting_metrics import get_inventory_metrics
from apps.inventory.forms import ProductForm
from apps.inventory.models import Product, Category
from apps.inventory.filters import ProductFilter
import json

User = get_user_model()

PER_PAGE = 10


def catalog_list(request):
    return render(request, 'catalog/pages/catalog.html')