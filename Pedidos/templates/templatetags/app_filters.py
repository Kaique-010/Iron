from django import template
from django.forms import BoundField


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



register = template.Library()

@register.filter
def add_class(field, css_class):
    """
    Adiciona uma classe CSS ao campo de formulário.
    """
    if isinstance(field, BoundField):
        existing_classes = field.field.widget.attrs.get('class', '')
        new_classes = f"{existing_classes} {css_class}".strip()
        field.field.widget.attrs['class'] = new_classes
        return field
    return field