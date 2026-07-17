from django.db.models import Sum, Count, Case, When, F, DecimalField, Q, Value


def get_promoters_sales_metrics(filtered_queryset):
    metrics = filtered_queryset.aggregate(
        total_sales=Count('id'),
        service_fee_sum=Sum('service_fee_sold'),
        services_count=Count('id', filter=Q(service=True)),
        revenue_sum=Sum(
            Case(
                When(service=True, then=F('price_sold') + F('service_fee_sold')),
                default=F('price_sold'),
                output_field=DecimalField()
            )
        ),
        total_commission_sum=Sum(
            F('promoter__comission') + Case(
                When(service=True, then=Value(2.00)),
                default=Value(0.00),
                output_field=DecimalField()
            )
        )
    )

    return metrics
