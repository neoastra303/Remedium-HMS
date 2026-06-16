from django import template

register = template.Library()


@register.inclusion_tag("partials/stat_card.html")
def stat_card(icon, label, value, sub_text="", color="blue", sub_badges=None):
    return {
        "icon": icon,
        "label": label,
        "value": value,
        "sub_text": sub_text,
        "color": color,
        "sub_badges": sub_badges or [],
    }


@register.inclusion_tag("partials/quick_action.html")
def quick_action(url, icon, title, sub, bg_class="primary", text_class="primary"):
    return {
        "url": url,
        "icon": icon,
        "title": title,
        "sub": sub,
        "bg_class": bg_class,
        "text_class": text_class,
    }
