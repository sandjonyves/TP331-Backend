from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Classe, Student
import csv
import io

class CustomStudentView(APIView):
    permission_classes = [AllowAny]

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

            # Création des étudiants
            for row in reader:
                # Vérifiez si la classe existe
                try:
                    print(row['classe_id'])
                    classe = Classe.objects.filter(id=1).first()
                    print(classe)
                except Classe.DoesNotExist:
                    return Response(
                        {"error": f"Classe avec ID {row['classe_id']} introuvable."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                print('ttttttttttttttttttttttttttttt')
                # Créez l'étudiant
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
            # Log l'erreur et renvoyer une réponse
            print(f"Erreur lors du traitement du fichier CSV : {e}")
            return Response({"error": f"Erreur serveur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
