from django.urls import path
from .views import (
    assessment_result,
    result_sheet_pdf_view,
)


urlpatterns = [
    path("assessment/", assessment_result, name="ass_results"),
    path("result/print/<int:id>/", result_sheet_pdf_view, name="result_sheet_pdf_view"),
    
]