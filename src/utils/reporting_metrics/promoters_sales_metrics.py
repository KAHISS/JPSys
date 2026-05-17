from django.db.models import Sum, Count, Case, When, F, DecimalField, Q, ExpressionWrapper


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
            ExpressionWrapper(
                Case(
                    When(service=True, then=F('price_sold') +
                         F('service_fee_sold')),
                    default=F('price_sold')
                ) * (F('promoter__comission') / 100.0),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
    )

    return metrics
