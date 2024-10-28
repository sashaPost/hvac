from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path(route="", view=views.HomeView.as_view(), name="home"),
    path("update-active-link/", views.update_active_link, name="update_active_link"),
    # path('scroll-to/', views.scroll_to, name='scroll_to'),
    # path(
    #     route="about/",
    #     view=views.AboutView.as_view(),
    #     name="about",
    # ),
    path("case/<int:case_id>/", views.CaseDetailView.as_view(), name="case-detail"),
    path("prev-case/", views.PrevCaseView.as_view(), name="prev-case"),
    path("next-case/", views.NextCaseView.as_view(), name="next-case"),
    path(
        route="contacts/",
        view=views.ContactView.as_view(),
        name="contacts",
    ),
    path("set-language/", views.set_language, name="set_language"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
