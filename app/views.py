from rest_framework import viewsets
from  rest_framework.permissions  import AllowAny
from .models import Cart, Classe, School, Student
from .serializers import (CartSerializer, ClasseSerializer, CustomUserSerializer, SchoolSerializer,
    StudentSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators  import action
from rest_framework.views import APIView
import csv
import io



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




class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

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
        print(Student.objects.filter(id=1))
        # Vérifiez si le fichier est fourni dans la requête
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
