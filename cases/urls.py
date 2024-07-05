from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views


urlpatterns = [
    path(route="", view=views.HomeView.as_view(), name="home"),
    path(
        route="about/",
        view=views.AboutView.as_view(),
        name="about",
    ),

    path('cases/', views.CaseListView.as_view(), name='cases'),
    path('cases/<int:case_id>/', views.CaseDetailView.as_view(), name='case-detail'),

    path(
        route="contacts/",
        view=views.ContactView.as_view(),
        name="contacts",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
