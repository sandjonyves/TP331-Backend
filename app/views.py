from rest_framework import viewsets
from  rest_framework.permissions  import AllowAny
from .models import Card, Classe, School, Student,CardPrototype
from .serializers import (CardSerializer, ClasseSerializer, CustomUserSerializer, SchoolSerializer,CardPrototypeSerializer,StudentSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators  import action
from rest_framework.views import APIView
import csv
import io
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage


class SchoolViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def get_schools_by_user(self, request, user_id=None):
        schools = self.queryset.filter(user_id=user_id)  # Filtrer les écoles par user_id
        serializer = self.get_serializer(schools, many=True)
        return Response(serializer.data)

class ClasseViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer

    @action(detail=False, methods=['get'], url_path='school/(?P<school_id>[^/.]+)')
    def get_classes_by_school(self, request, school_id=None):
        classes = self.queryset.filter(school_id=school_id)  # Filtrer les classes par school_id
        serializer = self.get_serializer(classes, many=True)
        return Response(serializer.data)



class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='classe/(?P<classe_id>[^/.]+)')
    def get_students_by_classe(self, request, classe_id=None):
        students = self.queryset.filter(classe_id=classe_id)  # Filtrer les étudiants par classe_id
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    # @action(detail=False, methods=['post'], url_path='registers')
    # def post(self, request):
    #     print(Classe.objects.filter(id=1))
    #     # Vérifiez si le fichier est fourni dans la requête
    #     csv_file = request.FILES.get('file')
    #     if not csv_file:
    #         return Response({"error": "Aucun fichier n'a été fourni."}, status=status.HTTP_400_BAD_REQUEST)

    #     # Vérifiez que le fichier a une extension CSV
    #     if not csv_file.name.endswith('.csv'):
    #         return Response({"error": "Le fichier n'est pas un fichier CSV."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         # Décodage et lecture du fichier CSV
    #         decoded_file = csv_file.read().decode('utf-8')
    #         io_string = io.StringIO(decoded_file)
    #         reader = csv.DictReader(io_string)

    #         # Validation des colonnes attendues
    #         expected_columns = {'matricule', 'firstName', 'lastName', 'date_of_birth', 'classe_id'}
    #         if not expected_columns.issubset(reader.fieldnames):
    #             return Response(
    #                 {"error": f"Les colonnes du fichier CSV doivent inclure : {', '.join(expected_columns)}."},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )

    #         # Création des étudiants
    #         for row in reader:
    #             classe_id = int(row['classe_id'].strip())
    #             classe = Classe.objects.filter(id=classe_id).first()
                
    #             if not classe:
    #                 return Response(
    #                     {"error": f"Classe avec ID {classe_id} introuvable."},
    #                     status=status.HTTP_400_BAD_REQUEST,
    #                 )

    #             # Créez l'étudiant
    #             Student.objects.create(
    #                 matricule=row['matricule'].strip(),
    #                 firstName=row['firstName'].strip(),
    #                 lastName=row['lastName'].strip(),
    #                 date_of_birth=row['date_of_birth'].strip(),
    #                 classe=classe,
    #             )

    #         return Response({"message": "Fichier CSV traité avec succès."}, status=status.HTTP_201_CREATED)

    #     except csv.Error as e:
    #         return Response({"error": f"Erreur de traitement du fichier CSV : {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         # Log l'erreur et renvoyer une réponse
    #         print(f"Erreur lors du traitement du fichier CSV : {e}")
    #         return Response({"error": f"Erreur serveur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class CardViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    # def create(self, request, *args, **kwargs):
    #     matricule = request.data.get('matricule')
    #     student_instance = Student.objects.filter(matricule=matricule).first()
    #     request.data['student'] = student_instance
    #     if not student_instance:
    #         return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()  
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class CustomStudentView(viewsets.generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer
    def post(self, request):
       
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "Aucun fichier n'a été fourni."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifiez que le fichier a une extension CSV
        if not csv_file.name.endswith('.csv'):
            return Response({"error": "Le fichier n'est pas un fichier CSV."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Décodage et lecture du fichier CSV
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            # Validation des colonnes attendues
            expected_columns = {'matricule', 'firstName', 'lastName', 'date_of_birth', 'classe_id'}
            if not expected_columns.issubset(reader.fieldnames):
                return Response(
                    {"error": f"Les colonnes du fichier CSV doivent inclure : {', '.join(expected_columns)}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

       
            for row in reader:
               
                try:
                    print(row['classe_id'])
                    classe = Classe.objects.get(id=1)
                    print(classe)
                except Classe.DoesNotExist:
                    return Response(
                        {"error": f"Classe avec ID {row['classe_id']} introuvable."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
             
                Student.objects.create(
                    matricule=row['matricule'].strip(),
                    firstName=row['firstName'].strip(),
                    lastName=row['lastName'].strip(),
                    date_of_birth=row['date_of_birth'].strip(),
                    classe=Classe.objects.get(id=1),
                )

            return Response({"message": "Fichier CSV traité avec succès."}, status=status.HTTP_201_CREATED)

        except csv.Error as e:
            print(e)
            return Response({"error": f"Erreur de traitement du fichier CSV : {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
          
            print(f"Erreur lors du traitement du fichier CSV : {e}")
            return Response({"error": f"Erreur serveur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CardPrototypeView(viewsets.ModelViewSet):
    queryset = CardPrototype.objects.all()
    serializer_class = CardPrototypeSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'], url_path='set-choice')
    def set_choice(self, request, pk=None):
        try:
            instance = self.get_object()

            # Met à jour tous les autres objets pour désactiver le choix
            CardPrototype.objects.exclude(pk=instance.pk).update(choice=False)

            # Active le choix pour l'instance actuelle
            instance.choice = True
            instance.save()

            return Response({"message": "Choice successfully updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='get-choice')
    def get_choice(self, request):
        try:
            prototype = CardPrototype.objects.get(choice=True)
            serializer = CardPrototypeSerializer(prototype)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except CardPrototype.DoesNotExist:
            return Response({"error": "No prototype selected as choice."}, status=status.HTTP_404_NOT_FOUND)






from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML, CSS
from rest_framework.permissions import AllowAny

class RenderPDFView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Récupérer le template par défaut
        try:
            template_choice = CardPrototype.objects.get(choice=True)
        except CardPrototype.DoesNotExist:
            return Response({'error': 'Template non trouvé.'}, status=404)

        # Récupérer les données de la requête
        template_name = request.data.get('template_name', f'{template_choice.id}.html')
        student_id = request.data.get('student_id')
        image_url = request.data.get('image_url')

        if not student_id or not image_url:
            return Response(
                {'error': 'Les champs student_id et image_url sont requis.'},
                status=400
            )

        # Récupérer les informations de l'étudiant
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Étudiant non trouvé.'}, status=404)

        # Récupérer la classe et l'école associées
        try:
            student_classe = student.classe
            student_school = student_classe.school
        except AttributeError:
            return Response({'error': 'Classe ou école non trouvée.'}, status=404)

        # Contexte pour le rendu du PDF
        context = {
            'student_matricule': student.matricule,
            'student_firstName': student.firstName,
            'student_lastName': student.lastName,
            'student_dateOfBirth': student.date_of_birth,
            'student_sexe': student.sexe,
            'student_imageUrl': image_url,
            'student_classe': student_classe.name,
            'school_logo': student_school.logo_url,
            'school_name': student_school.name,
            'academic_year': student_school.academic_year,
            'school_phone': student_school.phone,
        }

        try:
            # Rendre le contenu HTML
            html_string = render_to_string(template_name, context)
        except Exception as e:
            return Response({'error': f"Erreur lors du rendu du template : {str(e)}"}, status=500)

        # Générer le PDF
        css = CSS(string='''
            @page {
                size: 85.6mm 54mm; /* Taille d'une carte d'identité */
                margin: 0; /* Pas de marges */
            }
        ''')
        html = HTML(string=html_string)
        pdf = html.write_pdf(stylesheets=[css])

        # Enregistrer le PDF
        fs = FileSystemStorage()
        pdf_filename = f'carde_{student_id}.pdf'
        pdf_path = fs.save(pdf_filename, ContentFile(pdf))
        pdf_url = fs.url(pdf_path)

        # Mettre à jour les informations de l'étudiant
        student.card_file = pdf_path
        student.image_url = image_url
        student.save()

        # Réponse
        response_data = {
            'message': 'PDF généré avec succès.',
            'pdf_url': request.build_absolute_uri(pdf_url),
            'student': {
                'id': student.id,
                'first_name': student.firstName,
                'last_name': student.lastName,
                'image_url': student.image_url,
            }
        }

        return Response(response_data, status=201)

