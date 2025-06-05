from django import template

register = template.Library()

@register.filter
def variable_letter(index):
    letters = ['x', 'y', 'z', 'w', 'v', 'u', 't', 's']
    return letters[index] if index < len(letters) else f'var_{index+1}'