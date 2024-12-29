from rest_framework import serializers
from .models import School, Classe, Student ,Card,CardPrototype


class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    # classe_id = serializers.PrimaryKeyRelatedField(source='classe', write_only=True, queryset=Classe.objects.all())
    
    # classe =serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields ='__all__'
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


class SchoolSerializer(serializers.ModelSerializer):
    prototypes = CardPrototypeSerializer(many=True,read_only=True, source='prototype')

    class Meta:
        model = School
        fields = [
            'id',                 # Identifiant de l'établissement
            'name',               # Nom de l'établissement
            'phone',              # Numéro de téléphone
            'logo_url',           # URL du logo
            'academic_year',      # Année académique
            'devise',             # Devise
            'contact',            # Contact
            'logo',               # Logo
            'cachet',             # Cachet
            'signature_principale', # Signature principale
            'prototypes'          # Prototypes de carte associés
        ]