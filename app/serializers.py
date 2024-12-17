from rest_framework import serializers
from .models import School, Classe, Student ,Card,CardPrototype
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    # classe_id = serializers.PrimaryKeyRelatedField(source='classe', write_only=True, queryset=Classe.objects.all())
    
    # classe =serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ['id', 'matricule', 'firstName', 'lastName', 'date_of_birth','classe']
        # read_only_fields = ['classe']

    # def create(self, validated_data):
    #     classe = validated_data.pop('classe')
    #     student = Student.objects.create(classe=classe, **validated_data)
    #     return student

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class CardPrototypeSerializer(serializers.ModelSerializer):
    class Meta :
        model = CardPrototype
        fields = '__all__'


class CustomUserSerializer(serializers.Serializer):
    file = serializers.FileField()


class CardGenerateSerializer(serializers.Serializer):
    template_name =  serializers.CharField()