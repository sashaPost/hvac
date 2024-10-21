import logging

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, View

from .models import AboutMessage, Case, Contact, ServiceCategory

logger = logging.getLogger(__name__)


class HomeView(ListView):
    model = Case
    template_name = "cases/home.html"
    context_object_name = "cases"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service_categories"] = ServiceCategory.objects.all()
        context["about_message"] = AboutMessage.objects.last()
        context["active_case"] = self.get_queryset().first()
        return context

    def get_queryset(self):
        return Case.objects.filter(main_page_visibility=True).order_by("-created_at")


# class AboutView(DetailView):
#     model = AboutMessage
#     template_name = "cases/about.html"
#     context_object_name = "about_message"
#
#     def get_object(self):
#         return AboutMessage.objects.last()
#


class CaseDetailView(DetailView):
    model = Case
    template_name = "cases/partials/case_detail_modal.html"
    context_object_name = "case"
    pk_url_kwarg = "case_id"


class BaseCaseCarouselView(View):
    def get(self, request, *args, **kwargs):
        current_case_id = request.GET.get("current")
        cases = Case.objects.all()
        active_case = self.get_active_case(cases, current_case_id)
        return render(
            request,
            "cases/partials/cases_carousel.html",
            {"cases": cases, "active_case": active_case},
        )

    def get_active_case(self, cases, current_case_id):
        raise NotImplementedError("Subclasses must implement get_active_case")


class PrevCaseView(BaseCaseCarouselView):
    def get_active_case(self, cases, current_case_id):
        if not current_case_id:
            return cases.last()
        return cases.filter(id__lt=current_case_id).last() or cases.last()


class NextCaseView(BaseCaseCarouselView):
    def get_active_case(self, cases, current_case_id):
        if not current_case_id:
            return cases.first()
        return cases.filter(id__gt=current_case_id).first() or cases.first()


class ContactView(DetailView):
    model = Contact
    template_name = "cases/contacts.html"
    context_object_name = "contact"

    def get_object(self):
        return Contact.objects.last()


def update_active_link(request):
    # logger.debug("update_active_link function called")
    active_section = request.GET.get("section", "home")
    html = (
        f'<script>document.querySelectorAll(".nav-link").forEach(el => el.classList.remove("active"));'
        f'document.querySelector(\'a[href="{active_section}"]\').classList.add("active");</script>'
    )
    return HttpResponse(html)


# def scroll_to(request):
#     logger.debug("scroll_to function called")
#     section = request.GET.get('section', 'home')
#     response = HttpResponse()
#     response['HX-Trigger'] = f'scrollTo'
#     response['HX-Retarget'] = f'#{section}'
#     response['HX-Reswap'] = 'none'
#
#     logger.debug(f"Debug: Scrolling to section: {section}")
#     logger.info(f"Info: Scrolling to section: {section}")
#     logger.warning(f"Warning: Scrolling to section: {section}")
#     logger.error(f"Error: This is a test error message")
#
#     return response
