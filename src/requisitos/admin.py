from django.contrib import admin
from requisitos.models import Ambiental, Organizacional, Gerencial, Desenvolvimento, MetaModelo, ModeloIntermediario, Tarefa

# Inlines
class AmbientalInline(admin.TabularInline):
    model = Ambiental
    extra = 1  # Número de linhas vazias

class OrganizacionalInline(admin.TabularInline):
    model = Organizacional
    extra = 1

class GerencialInline(admin.TabularInline):
    model = Gerencial
    extra = 1

class DesenvolvimentoInline(admin.TabularInline):
    model = Desenvolvimento
    extra = 1

class ModeloIntermediarioInline(admin.TabularInline):
    model = ModeloIntermediario
    extra = 1

class TarefaInline(admin.TabularInline):
    model = Tarefa
    extra = 1

# Admin para o modelo MetaModelo
class MetaModeloAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    search_fields = ['descricao']
    inlines = [AmbientalInline, OrganizacionalInline, GerencialInline, DesenvolvimentoInline, ModeloIntermediarioInline]
    list_per_page = 20

# Admin para o modelo Gerencial
class GerencialAdmin(admin.ModelAdmin):
    list_display = ('recurso', 'prazo')
    list_filter = ['prazo']
    inlines = [TarefaInline]
    list_per_page = 20  # Paginação

# Registre os modelos e suas classes de administração personalizadas
admin.site.register(MetaModelo, MetaModeloAdmin)
admin.site.register(Gerencial, GerencialAdmin)
