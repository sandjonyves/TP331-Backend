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

class ClasseViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer




class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

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

    @action(detail=True, methods=['post'], url_path='choice')
    def choice(self, request, pk=None):
        try:
            instance = self.get_object()

            CardPrototype.objects.exclude(pk=instance.pk).update(choice=False)

           
            instance.choice = True
            instance.save()

            return Response({"message": "Choice successfully updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class RenderPDFView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Récupérer le template
        try:
            template_choice = CardPrototype.objects.get(choice=True)
        except CardPrototype.DoesNotExist:  # Correction de l'exception
            return Response({'error': 'Template non trouvé.'}, status=404)

        template_name = request.data.get('template_name', f'{template_choice.id}.html')
        student_id = request.data.get('student_id')
        image_url = request.data.get('image_url')

        # Vérifier les données de la requête
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

        try:
            student_classe = Classe.objects.get(id=student.classe.id)  # Correction de l'accès aux champs
            student_school = School.objects.get(id=student_classe.school.id)  # Correction de l'accès aux champs
        except (Classe.DoesNotExist, School.DoesNotExist):
            return Response({'error': 'Classe ou école non trouvée.'}, status=404)

      
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

        # Rendre le contenu HTML
        html_string = render_to_string(template_name, context)

        # Définir le CSS pour le PDF
        css = CSS(string='''
            @page {
                size: 85.6mm 54mm; /* Taille d'une carde d'identité */
                margin: 0; /* Pas de marges pour correspondre exactement à la taille */
            }
        ''')

        # Générer le PDF
        html = HTML(string=html_string)
        pdf = html.write_pdf(stylesheets=[css])

        # Enregistrer le PDF sur le serveur
        fs = FileSystemStorage()
        pdf_filename = f'carde_{student_id}.pdf'
        pdf_path = fs.save(pdf_filename, ContentFile(pdf))
        pdf_url = fs.url(pdf_path)

        # Enregistrer dans la table Card
        card = Card(student=student, card_file=pdf_url)
        card.save()

        # Mettre à jour l'image de l'étudiant
        student.image_url = image_url
        student.save()

        # Préparer la réponse
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
