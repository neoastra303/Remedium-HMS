from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
import logging

logger = logging.getLogger(__name__)


class CustomRenderer(JSONRenderer):
    """
    Standardized API success response format:
    {
        "status": "success",
        "code": 200,
        "data": { ... }
    }
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response")

        # If it's already an error response (processed by exception handler),
        # or if it's already enveloped, don't envelope again.
        if response and response.status_code >= 400:
            return super().render(data, accepted_media_type, renderer_context)

        if (
            data is not None
            and "status" in data
            and (data["status"] == "success" or data["status"] == "error")
        ):
            return super().render(data, accepted_media_type, renderer_context)

        custom_data = {
            "status": "success",
            "code": response.status_code if response else 200,
            "data": data,
        }
        return super().render(custom_data, accepted_media_type, renderer_context)


def custom_exception_handler(exc, context):
    """
    Standardized API error response format:
    {
        "status": "error",
        "code": 400,
        "message": "Validation Failed",
        "errors": { ... }
    }
    """
    # Call DRF's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "status": "error",
            "code": response.status_code,
            "message": response.data.get("detail", "Request failed"),
            "errors": response.data if "detail" not in response.data else None,
        }
        # If detail was the only key, remove the empty errors field
        if custom_data["errors"] is None:
            del custom_data["errors"]

        response.data = custom_data
    else:
        # For unhandled exceptions (500), return a standardized response
        logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
        return Response(
            {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An internal server error occurred.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
