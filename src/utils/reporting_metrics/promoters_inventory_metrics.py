from django.db.models import Sum, Count, Case, When, F, DecimalField, Q


def get_promoters_inventory_metrics(filtered_queryset):
    metrics = filtered_queryset.aggregate(
        unique_promoters=Count('promoter', distinct=True),
        total_products=Count('id'),
        total_units=Sum('quantity'),
        potential_revenue=Sum(F('quantity') * F('sale_price'), output_field=DecimalField()),
        potential_revenue_with_service=Sum(F('quantity') * (F('sale_price') + F('service_fee')), output_field=DecimalField())
    )
    return metrics
