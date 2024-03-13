from django import forms

from .models import NewsAndEvents, Session


# news and events
class NewsAndEventsForm(forms.ModelForm):
    class Meta:
        model = NewsAndEvents
        fields = (
            "title",
            "summary",
            "posted_as",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["summary"].widget.attrs.update({"class": "form-control"})
        self.fields["posted_as"].widget.attrs.update({"class": "form-control"})


class SessionForm(forms.ModelForm):
    next_session_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                "type": "date",
            }
        ),
        required=True,
    )

    class Meta:
        model = Session
        fields = ["session", "is_current_session", "next_session_begins"]
