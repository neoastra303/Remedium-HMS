from rest_framework import serializers


class StandardErrorSerializer(serializers.Serializer):
    """
    Standard format for all API error responses.
    """

    status = serializers.CharField(
        default="error", help_text="Always 'error' for failure responses."
    )
    code = serializers.IntegerField(help_text="HTTP status code.")
    message = serializers.CharField(help_text="A human-readable error message.")
    errors = serializers.DictField(
        required=False,
        help_text="Detailed validation errors, mapping field names to lists of messages.",
    )
