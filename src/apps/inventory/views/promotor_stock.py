from datetime import timedelta
from django.utils import timezone
from django.http import Http404, JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.settings import STATIC_URL
from django.middleware.csrf import get_token
from utils.pagination import make_pagination
from apps.inventory.forms import ProductForm
from apps.inventory.models import Product, Category
from django.db.models import Q, Sum
from decimal import Decimal
from apps.inventory.filters import ProductFilter
import json
import os
