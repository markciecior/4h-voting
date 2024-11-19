from __future__ import annotations

from django.conf import settings

# from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html


def django_fingerprint_script() -> str:
    return format_html(
        """<script src="https://cdn.jsdelivr.net/npm/@thumbmarkjs/thumbmarkjs/dist/thumbmark.umd.js"></script>
        <script>
        ThumbmarkJS.getFingerprint().then(
            function(fp) {{
                url = '{}' + fp;
                fetch(url) // api for the get request
                  .then(response => response.json())
                  .then(data => console.log(data));
            }}
        );
        </script>""",
        # "console.log()" if not settings.DEBUG else "console.log(fp)",
        reverse("django_fingerprint:fp") + "?fpid=",
    )
