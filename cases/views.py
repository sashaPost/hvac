from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from .models import AboutMessage, Case, Contact


class CaseListView(ListView):
    model = Case
    template_name = "cases/cases.html"
    context_object_name = "cases"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case_id = self.request.GET.get("case_id", None)
        if case_id:
            case = get_object_or_404(Case, id=case_id)
        else:
            case = Case.objects.latest("created_at")

        context["case"] = case
        context["next_case"] = Case.objects.filter(id__gt=case.id).order_by("id").first()
        context["previous_case"] = Case.objects.filter(id__lt=case.id).order_by("-id").first()
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.htmx:
            self.template_name = "cases/partials/case_preview.html"
        return super().render_to_response(context, **response_kwargs)


class CaseDetailView(DetailView):
    model = Case
    template_name = "cases/partials/case_detail.html"
    context_object_name = "case"


class HomeView(ListView):
    model = Case
    template_name = "cases/home.html"
    context_object_name = "cases"


class AboutView(DetailView):
    model = AboutMessage
    template_name = "cases/about.html"
    context_object_name = "about_message"

    def get_object(self):
        return AboutMessage.objects.last()


class ContactView(DetailView):
    model = Contact
    template_name = "cases/contacts.html"
    context_object_name = "contact"

    def get_object(self):
        return Contact.objects.last()


# def case_list(request):
#     case_id = request.GET.get('case_id')
#     if case_id:
#         case = get_object_or_404(Case, id=case_id)
#     else:
#         case = Case.objects.latest('created_at')
#
#     next_case = Case.objects.filter(id__gt=case.id).order_by('id').first()
#     prev_case = Case.objects.filter(id__lt=case.id).order_by('-id').first()
#
#     context = {
#         'case': case,
#         'next_case': next_case,
#         'prev_case': prev_case,
#     }
#
#     if request.htmx:
#         return render(request, 'cases/partials/case_preview.html', context)
#     else:
#         return render(request, 'cases/cases.html', context)
#
#
# def case_detail(request, case_id) -> HttpResponse:
#     print(f"*'case_detail' was triggered*")
#     case = get_object_or_404(Case, id=case_id)
#     return render(request, "cases/partials/case_detail.html", {"case": case})
#
#
# def home(request):
#     cases = Case.objects.all()
#     return render(
#         request,
#         template_name="cases/home.html",
#         context={"cases": cases},
#     )
#
#
# def about(request):
#     about_message = AboutMessage.objects.last()
#     # print(about_message.title)
#     # print(about_message.content)
#     context = {
#         "about_message": about_message,
#     }
#     return render(
#         request,
#         template_name="cases/about.html",
#         context=context,
#     )
#
#
# def contacts(request):
#     contact = Contact.objects.last()
#     context = {
#         "contact": contact,
#     }
#     return render(
#         request,
#         template_name="cases/contacts.html",
#         context=context,
#     )
