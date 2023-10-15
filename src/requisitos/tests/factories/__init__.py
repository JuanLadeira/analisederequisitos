import factory
from factory.django import DjangoModelFactory
from requisitos.models import (
    Ambiental,
    Organizacional,
    Gerencial,
    Desenvolvimento,
    MetaModelo,
    ModeloIntermediario,
    Tarefa,
)
import datetime


class MetaModeloFactory(DjangoModelFactory):
    class Meta:
        model = MetaModelo

    descricao = factory.Faker("text")


class AmbientalFactory(DjangoModelFactory):
    class Meta:
        model = Ambiental

    meta_modelo = factory.SubFactory(MetaModeloFactory)
    fator_externo = factory.Faker("word")
    impacto = factory.Faker("text")


class OrganizacionalFactory(DjangoModelFactory):
    class Meta:
        model = Organizacional

    meta_modelo = factory.SubFactory(MetaModeloFactory)
    objetivo = factory.Faker("sentence")
    estrategia = factory.Faker("text")


class GerencialFactory(DjangoModelFactory):
    class Meta:
        model = Gerencial

    meta_modelo = factory.SubFactory(MetaModeloFactory)
    recurso = factory.Faker("word")
    prazo = factory.Faker("date_between", start_date="-30d", end_date="30d")


class DesenvolvimentoFactory(DjangoModelFactory):
    class Meta:
        model = Desenvolvimento

    meta_modelo = factory.SubFactory(MetaModeloFactory)
    requisito_funcional = factory.Faker("text")
    requisito_nao_funcional = factory.Faker("text")


class ModeloIntermediarioFactory(DjangoModelFactory):
    class Meta:
        model = ModeloIntermediario

    meta_modelo = factory.SubFactory(MetaModeloFactory)
    informacao_comum = factory.Faker("text")


class TarefaFactory(DjangoModelFactory):
    class Meta:
        model = Tarefa

    gerencial = factory.SubFactory(GerencialFactory)
    descricao = factory.Faker("sentence")
    status = factory.Iterator(["Pendente", "Concluído"])
