from django import template

register = template.Library()

@register.filter
def currency_reais(value):
    """Converte um valor numérico para formato de moeda brasileira."""
    try:
        return f'R$ {value:,.2f}'.replace('.', 'x').replace(',', '.').replace('x', ',')
    except (ValueError, TypeError):
        return value
    
@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})