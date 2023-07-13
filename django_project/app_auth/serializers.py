from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer( serializers.ModelSerializer):
    data_of_birth=serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model=CustomUser
        fields='__all__'
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['age'] = instance.age()
        return data