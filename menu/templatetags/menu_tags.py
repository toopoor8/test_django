from django import template
from menu.models import MenuItem

register = template.Library()


def build_tree(items):
    d = {}
    roots = []
    
    for i in items:
        d[i.id] = i
        i.children_list = []
    
    for i in items:
        if i.parent_id:
            p = d.get(i.parent_id)
            if p:
                p.children_list.append(i)
                i._parent_obj = p
        else:
            roots.append(i)
            i._parent_obj = None
    
    return roots


def find_active(items, url):
    url = url.rstrip("/") or "/"
    
    for i in items:
        i_url = i.get_url().rstrip("/") or "/"
        if i_url == url:
            return i
        if i.children_list:
            found = find_active(i.children_list, url)
            if found:
                return found
    return None


def get_ancestors(active):
    res = []
    if not active:
        return res
    curr = getattr(active, "_parent_obj", None)
    while curr:
        res.append(curr.id)
        curr = getattr(curr, "_parent_obj", None)
    return res


def mark_expanded(item, active, ancestor_ids):
    item.is_active = False
    item.is_expanded = False
    
    if active and item.id == active.id:
        item.is_active = True
        item.is_expanded = True
        for c in item.children_list:
            c.is_expanded = True
            mark_expanded(c, None, [])
        return
    
    if item.id in ancestor_ids:
        item.is_expanded = True
        for c in item.children_list:
            mark_expanded(c, active, ancestor_ids)
        return
    
    for c in item.children_list:
        mark_expanded(c, active, ancestor_ids)


@register.inclusion_tag("menu/menu.html", takes_context=True)
def draw_menu(context):
    req = context.get("request")
    url = req.path if req else "/"
    
    items = list(MenuItem.objects.all().select_related("parent"))
    if not items:
        return {"menu_items": []}
    
    roots = build_tree(items)
    active = find_active(roots, url)
    ancestor_ids = get_ancestors(active) if active else []
    
    for i in roots:
        mark_expanded(i, active, ancestor_ids)
    
    return {"menu_items": roots}
