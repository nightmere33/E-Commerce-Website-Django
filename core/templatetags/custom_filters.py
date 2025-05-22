from django import template

register = template.Library()

@register.filter
def get_item(lst, index):
    try:
        return lst[index % len(lst)]
    except:
        return None

@register.filter
def get_attr(obj, attr):
    attrs = attr.split('.')
    for a in attrs:
        obj = getattr(obj, a)
    return obj

@register.filter
def get_next_items(items, current_index):
    """
    Returns the next 4 items from the current index.
    """
    total = len(items)
    next_items = []
    for i in range(4):
        next_index = (current_index + i + 1) % total
        next_items.append(items[next_index])
    return next_items