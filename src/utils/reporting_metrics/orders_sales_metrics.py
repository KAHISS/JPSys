from django.db.models import Sum, Count, Case, When, F, DecimalField, Q


def get_orders_sales_metrics(filtered_queryset):
    metrics = filtered_queryset.aggregate(
        total_orders_count=Count('id'),
        total_revenue=Sum('total_value', filter=Q(status='paid')),
        total_pending=Sum('total_value', filter=Q(status='pending')),
        total_canceled_count=Sum('id', filter=Q(status='canceled'))
    )
    return metrics
