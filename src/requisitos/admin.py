from django.contrib import admin
from requisitos.models import (
    Ambiental,
    Organizacional,
    Gerencial,
    Desenvolvimento,
    MetaModelo,
    ModeloIntermediario,
    Tarefa,
    Sprint,
)


# Inlines
class CasoDeUsoInline(admin.TabularInline):
    model = MetaModelo.casos_de_uso.through
    extra = 1


class HistoriaUsuarioInline(admin.TabularInline):
    model = MetaModelo.historias_usuario.through
    extra = 1


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


class TarefaInline(admin.TabularInline):
    model = Tarefa
    extra = 1


# Admin para o modelo MetaModelo
class MetaModeloAdmin(admin.ModelAdmin):
    list_display = ("descricao",)
    search_fields = ["descricao"]
    inlines = [
        AmbientalInline,
        OrganizacionalInline,
        GerencialInline,
        DesenvolvimentoInline,
        CasoDeUsoInline,
        HistoriaUsuarioInline,
    ]
    list_per_page = 20
    filter_horizontal = ("modelos_intermediarios",)


# Admin para o modelo Gerencial
class GerencialAdmin(admin.ModelAdmin):
    list_display = ("recurso", "prazo")
    list_filter = ["prazo"]
    inlines = [TarefaInline]
    list_per_page = 20  # Paginação


# Admin para o modelo Sprint, assumindo que você criou um modelo Sprint
class SprintAdmin(admin.ModelAdmin):
    list_display = ("nome", "inicio", "fim")
    list_filter = ["inicio", "fim"]
    search_fields = ["nome"]
    list_per_page = 20


# Registre o novo admin
admin.site.register(Sprint, SprintAdmin)

# Registre os modelos e suas classes de administração personalizadas
admin.site.register(MetaModelo, MetaModeloAdmin)
admin.site.register(Gerencial, GerencialAdmin)
