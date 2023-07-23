from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    #phone_number = serializers.RegexField(regex="^\+\d{9,15}$") #validation happens

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['age'] = instance.age()
        return data

    def validate(self, args):
        email = args.get("email", None)
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "email already taken."})
        return super().validate(args)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        #instance = CustomUser.objects.create_user(**validated_data)

        instance.is_active = True
        if password is not None:
            # Set password does the hash, so you don't need to call make_password
            instance.set_password(password)  # without this step password is not hashed, user cannot login.
        instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'date_of_birth', 'state', 'gender', 'phone_number','is_admin','is_staff']
        read_only_fields = ['id']
        #fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        refresh["my_claim"] = "value"  # here you can add custom claim
        refresh['username'] = self.user.username
        refresh['foo'] = ["foo1", "foo2", "foo3"]
        # refresh['groups'] = self.user.groups.values_list('name', flat=True)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'date_of_birth', 'state']
        #fields = ['id']
