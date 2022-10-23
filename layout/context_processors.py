from .models import Socials, Layout

def layouts(request):
    return {
        'layouts': Layout.objects.all()
    }

def socials(request):
    return {
        'socials': Socials.objects.all()
    }

