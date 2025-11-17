from django.shortcuts import render


def index(request):
    return render(request, "menu/index.html")


def about(request):
    return render(request, "menu/page.html", {
        "title": "о нас",
        "content": "о нас"
    })


def services(request):
    return render(request, "menu/page.html", {
        "title": "услуги",
        "content": "услуги"
    })


def contact(request):
    return render(request, "menu/page.html", {
        "title": "контакты",
        "content": "контакты"
    })


def service_detail(request, service_id):
    return render(request, "menu/page.html", {
        "title": f"услуга {service_id}",
        "content": f"услуга {service_id}"
    })


def test_404(request):
    return render(request, "menu/404.html", {
        "title": "404",
        "message": "не найдено",
    }, status=404)


def handler404(request, exception):
    return render(request, "menu/404.html", {
        "title": "404",
        "message": "не найдено",
    }, status=404)
