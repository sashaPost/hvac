from .models import Contact


def contact_info(request):
    contact = Contact.objects.last()
    return {"global_contact": contact}
