from django.test import TestCase
from django.urls import reverse

class CustomStudentViewTests(TestCase):

    def test_upload_csv(self):
        url = reverse('students_registers') 
            
        with open('/home/shooter/Downloads/students_data.csv', 'rb') as file:
            response = self.client.post(url, {'file': file}, format='multipart')
        
        self.assertEqual(response.status_code, 201) 
        
        self.assertIn("Fichier CSV traité avec succès.", response.content.decode('utf-8'))  # Décodez le contenu
