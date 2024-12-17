from django.contrib import admin
from .models import School,Cart,Classe,Student

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'contact', 'academic_year')
    list_filter = ('academic_year',)
    search_fields = ('name', 'contact', 'academic_year')
    readonly_fields = ('logo_preview', 'cachet_preview', 'signature_preview')
    fieldsets = (
        ("Informations Générales", {
            'fields': ('user', 'name', 'devise', 'contact', 'academic_year')
        }),
        ("Logos et Signatures", {
            'fields': ('logo', 'logo_preview', 'cachet', 'cachet_preview', 'signature_principale', 'signature_preview')
        }),
    )

    def logo_preview(self, obj):
        """Afficher un aperçu du logo si possible."""
        if obj.logo:
            return f'<img src="data:image/png;base64,{obj.logo}" style="max-width: 200px; max-height: 100px;" />'
        return "Pas de logo"
    logo_preview.allow_tags = True
    logo_preview.short_description = "Aperçu du logo"

    def cachet_preview(self, obj):
        """Afficher un aperçu du cachet si possible."""
        if obj.cachet:
            return f'<img src="data:image/png;base64,{obj.cachet}" style="max-width: 200px; max-height: 100px;" />'
        return "Pas de cachet"
    cachet_preview.allow_tags = True
    cachet_preview.short_description = "Aperçu du cachet"

    def signature_preview(self, obj):
        """Afficher un aperçu de la signature principale si possible."""
        if obj.signature_principale:
            return f'<img src="data:image/png;base64,{obj.signature_principale}" style="max-width: 200px; max-height: 100px;" />'
        return "Pas de signature principale"
    signature_preview.allow_tags = True
    signature_preview.short_description = "Aperçu de la signature"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('student', 'student_matricule')
    search_fields = ('student__matricule', 'student__firstName', 'student__lastName')
    readonly_fields = ('image_preview',)
    fieldsets = (
        ("Carte Étudiant", {
            'fields': ('student', 'image', 'image_preview')
        }),
    )

    def student_matricule(self, obj):
        """Affiche le matricule de l'étudiant associé."""
        return obj.student.matricule
    student_matricule.short_description = "Matricule étudiant"

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="data:image/png;base64,{obj.image}" style="max-width: 150px; max-height: 150px;" />'
        return "Pas d'image"
    image_preview.allow_tags = True
    image_preview.short_description = "Aperçu de la carte"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'firstName', 'lastName', 'classe', 'date_of_birth')
    list_filter = ('classe', 'date_of_birth')
    search_fields = ('matricule', 'firstName', 'lastName', 'classe__name')
    readonly_fields = ('photos_preview',)
    fieldsets = (
        ("Informations Générales", {
            'fields': ('classe', 'matricule', 'firstName', 'lastName', 'date_of_birth')
        }),
        ("Photo", {
            'fields': ('photos', 'photos_preview')
        }),
    )

    def photos_preview(self, obj):
        """Affiche un aperçu de la photo si elle est disponible."""
        if obj.photos:
            return f'<img src="data:image/png;base64,{obj.photos}" style="max-width: 150px; max-height: 150px;" />'
        return "Pas de photo"
    photos_preview.allow_tags = True
    photos_preview.short_description = "Aperçu de la photo"


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')
    list_filter = ('school',)
    search_fields = ('name', 'school__name')
    inlines = []

    def get_students_count(self, obj):
        """Affiche le nombre d'étudiants dans une classe."""
        return obj.students.count()
    get_students_count.short_description = "Nombre d'étudiants"

