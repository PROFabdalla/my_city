from core.utils.base import CustomModelSerializer
from user_app.models import User


class AD_UserActivationSerializer(CustomModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "role", "is_active")
