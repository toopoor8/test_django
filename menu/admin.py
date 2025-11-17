from django.contrib import admin
from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ["title", "url", "parent", "order", "get_path"]
    search_fields = ["title", "url"]
    list_editable = ["order"]
    ordering = ["order", "id"]
    
    fieldsets = (
        ("основная информация", {"fields": ("title", "url")}),
        ("иерархия", {"fields": ("parent", "order")}),
    )

    def get_path(self, obj):
        path = []
        curr = obj
        while curr:
            path.insert(0, curr.title)
            curr = curr.parent
        return " > ".join(path)
    get_path.short_description = "путь"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("parent")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            obj_id = request.resolver_match.kwargs.get("object_id")
            if obj_id:
                try:
                    obj = MenuItem.objects.get(pk=obj_id)
                    exclude = [obj.id]
                    for child in MenuItem.objects.filter(parent=obj):
                        exclude.append(child.id)
                    kwargs["queryset"] = MenuItem.objects.exclude(id__in=exclude)
                except:
                    pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
