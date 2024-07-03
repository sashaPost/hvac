from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Case


# Create your views here.
def case_list(request) -> HttpResponse:
    """
    Renders the 'case_list.html' template, displaying a list of all cases.

    Args:
        request (HttpRequest): The incoming HTTP request object.

    Returns:
        HttpResponse: The rendered response containing the case list.
    """
    cases = Case.objects.all()
    context = {"cases": cases}
    return render(
        request=request, template_name="cases/case_list.html", context=context
    )


def case_detail(request, case_id) -> HttpResponse:
    case = get_object_or_404(Case, pk=case_id)
    context = {"case": case}
    return render(request, "cases/case_detail.html", context)
