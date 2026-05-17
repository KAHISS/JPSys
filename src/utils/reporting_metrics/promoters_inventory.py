from django.db.models import Sum, Count, Case, When, F, DecimalField, Q


def get_promoters_inventory_metrics(filtered_queryset):
    metrics = filtered_queryset.aggregate(
        unique_promoters=Count('promoter', distinct=True),
        total_chips=Sum('quantity'),
        estimated_value=Sum(F('quantity') * F('sale_price'),
                            output_field=DecimalField()),
        low_stock_count=Count('id', filter=Q(quantity__gt=0, quantity__lte=5))
    )

    return metrics
