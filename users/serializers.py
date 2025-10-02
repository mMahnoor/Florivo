from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fileds = ['id', 'email', 'password', 'first_name', 'last_name', 'address', 'phone', 'role']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fileds = ['id', 'email', 'first_name', 'last_name', 'address', 'phone', 'role']