from django import template

register = template.Library()


@register.filter(name='get_small_table_data')
def get_small_table_data(value, user):
    """Removes all values of arg from the given string"""
    return value.get_small_table_data(user)
