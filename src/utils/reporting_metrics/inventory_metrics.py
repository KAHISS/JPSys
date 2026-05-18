from django.db.models import Sum, Count, Case, When, F, DecimalField, Q


def get_inventory_metrics(filtered_queryset):
    metrics = filtered_queryset.aggregate(
        total_products=Count('id'),
        
        # Card 2: Soma de todas as unidades de todos os produtos juntos
        total_units=Sum('stock_quantity'),
        
        # Card 3: Multiplica a quantidade de cada produto pelo seu custo médio e soma tudo
        total_cost=Sum(F('stock_quantity') * F('average_cost'), output_field=DecimalField()),
        
        # Card 4: Multiplica a quantidade de cada produto pelo seu preço de venda e soma tudo
        potential_revenue=Sum(F('stock_quantity') * F('sale_price'), output_field=DecimalField())
    )

    venda_total = metrics['potential_revenue'] or 0.00
    custo_total = metrics['total_cost'] or 0.00

    lucro_total = venda_total - custo_total
    
    metrics["profit"] = lucro_total
    metrics["margin"] = (lucro_total / venda_total * 100) if venda_total > 0 else 0.00
    return metrics