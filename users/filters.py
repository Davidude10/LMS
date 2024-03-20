
from django.db.models import Q
import django_filters
from .models import User,Student




class StudentFilter(django_filters.FilterSet):
   
    Course = django_filters.CharFilter(
        field_name="Course", lookup_expr="icontains", label=""
    )

    class Meta:
        model = Student
        fields = [
            "Course",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Change html classes and placeholders
        
        self.filters["Course"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "Course"}
        )

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            Q(user__first_name__icontains=value)
            | Q(user__last_name__icontains=value)
        )
