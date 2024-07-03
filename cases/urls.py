from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views


urlpatterns = [
    path(route="case-list/", view=views.case_list, name="case_list"),
    path(
        route="case-detail/<int:case_id>/", view=views.case_detail, name="case_detail"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
