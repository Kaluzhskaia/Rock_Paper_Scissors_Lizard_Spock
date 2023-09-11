from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def get_icon(move):
    icons = {
        "Rock": "<i class='fa-solid fa-hand-back-fist'></i>",
        "Paper": "<i class='fa-solid fa-hand'></i>",
        "Scissors": "<i class='fa-solid fa-hand-scissors'></i>",
        "Lizard" : "<i class='fa-solid fa-hand-lizard'></i>",
        "Spock": "<i class='fa-solid fa-hand-spock'></i>",
    }
    return mark_safe(icons.get(move, ""))
