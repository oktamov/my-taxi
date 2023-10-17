from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = {"status": "success", "status_code": status_code, "message": None, "data": data}

        detail_message = data.pop("detail", None)
        if detail_message:
            response["message"] = detail_message

        if not str(status_code).startswith("2"):
            response["status"] = "error"
            if data.get("phone_number"):
                response["message"] = data.get("phone_number")[0]
            response["data"] = None

        return super().render(response, accepted_media_type, renderer_context)
