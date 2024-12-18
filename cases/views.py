import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render  # get_object_or_404,
from django.template.response import TemplateResponse
from django.urls import resolve
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, View

from .models import AboutMessage, Case, Contact, ServiceCategory

logger = logging.getLogger(__name__)


@require_POST
def set_language(request):
    lang_code = request.POST.get("language")

    if lang_code in ["en", "uk"]:
        translation.activate(lang_code)
        request.session["django_language"] = lang_code

        if request.headers.get("HX-Request"):
            # For HTMX requests, return a response that triggers a page refresh
            response = HttpResponse()
            response["HX-Refresh"] = "true"
        else:
            # For regular requests, redirect as before
            next_url = request.POST.get("next", "/")
            response = redirect(next_url)

        # Set cookie with secure flags
        response.set_cookie(
            "django_language",
            lang_code,
            max_age=365 * 24 * 60 * 60,  # 1 year
            path="/",
            secure=request.is_secure(),  # True if HTTPS
            httponly=True,  # Not accessible via JavaScript
            samesite="Lax",
        )
        return response

    return HttpResponseBadRequest("Invalid language code")


# @require_POST
# def set_language(request):
#     lang_code = request.POST.get("language")
#
#     # If valid language code
#     if lang_code in ["en", "uk"]:
#         # Activate the language
#         translation.activate(lang_code)
#         # Set the session
#         request.session["django_language"] = lang_code
#
#     # Get where to redirect
#     next_url = request.POST.get("next", "/")
#     response = redirect(next_url)
#
#     # Set the cookie
#     response.set_cookie("django_language", lang_code)
#
#     return response


class HomeView(ListView):
    model = Case
    template_name = "cases/home.html"
    context_object_name = "cases"

    def get(self, request, *args, **kwargs):
        # Debug info
        logger.info(f"Home view - Current language: {translation.get_language()}")
        logger.info(f"Home view - Session data: {dict(request.session)}")
        logger.info(f"Home view - Cookies: {request.COOKIES}")
        return super().get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # Get language from session or cookie
        lang_code = request.session.get("django_language") or request.COOKIES.get(
            "django_language"
        )

        if lang_code:
            translation.activate(lang_code)
            request.LANGUAGE_CODE = lang_code

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service_categories"] = ServiceCategory.objects.all()
        context["about_message"] = AboutMessage.objects.last()
        context["active_case"] = self.get_queryset().first()
        return context

    def get_queryset(self):
        return Case.objects.filter(main_page_visibility=True).order_by("-created_at")


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
