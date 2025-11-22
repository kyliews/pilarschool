# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Sala, Curso, Matricula, MaterialAula, DisponibilidadeSala

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfis'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

#configs pra facilitar
class DisponibilidadeAdmin(admin.ModelAdmin):
    list_display = ('sala', 'dias_horarios', 'data_inicio', 'data_fim', 'livre')
    list_filter = ('livre', 'sala')

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome_curso', 'professor', 'get_sala', 'get_horario')
    
    def get_sala(self, obj):
        return obj.agenda.sala if obj.agenda else "Sem sala"
    def get_horario(self, obj):
        return obj.agenda.dias_horarios if obj.agenda else "-"

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Sala)
admin.site.register(DisponibilidadeSala, DisponibilidadeAdmin) # NOVO
admin.site.register(Curso, CursoAdmin)
admin.site.register(Matricula)
admin.site.register(MaterialAula)