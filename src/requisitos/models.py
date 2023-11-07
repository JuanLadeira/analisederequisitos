from django.db import models
from django.core.validators import MinValueValidator
from simple_history.models import HistoricalRecords
import datetime
from django.utils import timezone

# Create your models here.


class Requisito(models.Model):
    """
    Representa um requisito individual dentro do sistema. Pode ser de diferentes tipos
    (negócio, cliente, sistema, usuário) e categorias (funcional, não funcional),
    com uma prioridade e status definidos."""

    TIPO_REQUISITO = [
        ("NEG", "Negócio"),
        ("CLI", "Cliente"),
        ("SIS", "Sistema"),
        ("USR", "Usuário"),
    ]
    PRIORIDADE_REQUISITO = [
        ("ESS", "Essencial"),
        ("IMP", "Importante"),
        ("DES", "Desejável"),
    ]
    STATUS_REQUISITO = [
        ("PROP", "Proposto"),
        ("APRO", "Aprovado"),
        ("IMPL", "Implementado"),
        ("TEST", "Testado"),
        ("CONC", "Concluído"),
    ]
    CATEGORIA_REQUISITO = [
        ("FUNC", "Funcional"),
        ("NAOFUNC", "Não Funcional"),
    ]
    categoria = models.CharField(
        max_length=8, choices=CATEGORIA_REQUISITO, blank=True, null=True
    )
    history = HistoricalRecords()
    tipo = models.CharField(max_length=3, choices=TIPO_REQUISITO)
    prioridade = models.CharField(max_length=3, choices=PRIORIDADE_REQUISITO)
    status = models.CharField(max_length=4, choices=STATUS_REQUISITO)
    descricao = models.TextField()


class CasoDeUso(models.Model):
    """
    Define um caso de uso do sistema, detalhando seu identificador, nome, descrição,
    atores envolvidos, condições prévias e posteriores, fluxo principal e alternativos,
    e a prioridade. Relaciona-se com os requisitos que ele aborda.
    """

    identificador = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    ator_principal = models.CharField(max_length=100)
    atores_secundarios = models.CharField(max_length=100, blank=True)
    pre_condicoes = models.TextField(blank=True)
    fluxo_principal = models.TextField()
    fluxos_alternativos = models.TextField(blank=True)
    pos_condicoes = models.TextField(blank=True)
    prioridade = models.IntegerField(default=0)
    requisitos = models.ManyToManyField("Requisito", related_name="casos_de_uso")

    def __str__(self):
        return self.nome


class Sprint(models.Model):
    """
    Representa um sprint dentro do processo de desenvolvimento ágil, com um nome,
    data de início e fim, fornecendo uma visão temporal do desenvolvimento.
    """

    nome = models.CharField(max_length=100)
    inicio = models.DateField()
    fim = models.DateField()

    def __str__(self):
        return self.nome


class HistoriaUsuario(models.Model):
    """
    Representa uma história de usuário, que é uma descrição de uma funcionalidade
    do ponto de vista do usuário final.
    Inclui identificador, título, descrição,
    critérios de aceitação, estimativa de esforço, prioridade, status e associação
    com sprints e requisitos específicos."""

    identificador = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    criterios_aceitacao = models.TextField()
    estimativa = models.IntegerField(
        help_text="Estimativa de esforço ou tempo necessário"
    )
    prioridade = models.IntegerField(default=0)
    sprint = models.ForeignKey(
        "Sprint", on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ("Pendente", "Pendente"),
            ("Em Progresso", "Em Progresso"),
            ("Concluída", "Concluída"),
        ],
    )
    requisito = models.ForeignKey(
        "Requisito", related_name="historias_usuario", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    """
    Armazena comentários feitos por usuários sobre requisitos específicos, incluindo
    o autor e a data de criação do comentário."""

    requisito = models.ForeignKey(
        Requisito, related_name="comentarios", on_delete=models.CASCADE
    )
    autor = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)


class Documento(models.Model):
    """
    Representa um documento associado a um requisito, contendo o arquivo em si e
    uma descrição do conteúdo ou propósito do documento."""

    requisito = models.ForeignKey(
        Requisito, related_name="documentos", on_delete=models.CASCADE
    )
    arquivo = models.FileField(upload_to="documentos/")
    descricao = models.CharField(max_length=255)


class MetaModelo(models.Model):
    """
    Atua como um modelo agregador que relaciona diferentes modelos do sistema,
    fornecendo um ponto central para rastrear como os diferentes níveis de
    informação estão interconectados.
    Inclui descrição, datas de criação e
    atualização, e histórico de alterações."""

    descricao = models.TextField()
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    # Relacionamentos com outros modelos
    casos_de_uso = models.ManyToManyField("CasoDeUso", related_name="meta_modelos")
    historias_usuario = models.ManyToManyField(
        "HistoriaUsuario", related_name="meta_modelos"
    )


class Ambiental(models.Model):
    """
    Este modelo representa o nível Ambiental na estrutura de rastreamento de requisitos.
    Ele captura os fatores externos e seus impactos associados que podem afetar o projeto.
    """

    meta_modelo = models.ForeignKey(
        MetaModelo, related_name="ambientais", on_delete=models.CASCADE
    )
    fator_externo = models.CharField(max_length=255)
    impacto = models.TextField()


class Organizacional(models.Model):
    """
    Este modelo representa o nível Organizacional.
    Ele captura os objetivos e estratégias organizacionais que orientam o projeto.
    """

    meta_modelo = models.ForeignKey(
        MetaModelo, related_name="organizacionais", on_delete=models.CASCADE
    )
    objetivo = models.CharField(max_length=255)
    estrategia = models.TextField()


class Gerencial(models.Model):
    """
    Este modelo representa o nível Gerencial na estrutura de rastreamento de requisitos.
    """

    meta_modelo = models.ForeignKey(
        MetaModelo, related_name="gerenciais", on_delete=models.CASCADE
    )
    recurso = models.CharField(max_length=255)
    prazo = models.DateField(validators=[MinValueValidator(datetime.date.today)])

    class Meta:
        ordering = ["prazo"]

    def __str__(self):
        return self.recurso


class Desenvolvimento(models.Model):
    """
    Este modelo representa o nível de Desenvolvimento.
    Ele captura os requisitos funcionais e não funcionais que o sistema deve cumprir.
    """

    meta_modelo = models.ForeignKey(
        MetaModelo, related_name="desenvolvimentos", on_delete=models.CASCADE
    )
    requisitos = models.ManyToManyField(
        Requisito,
        related_name="desenvolvimentos",
        limit_choices_to={"categoria__in": ["FUNC", "NAOFUNC"]},
        blank=True,
    )


class ModeloIntermediario(models.Model):
    """
    Este modelo serve como um modelo intermediário para capturar informações que são comuns entre diferentes Meta-Modelos.
    """

    meta_modelos = models.ManyToManyField(
        MetaModelo, related_name="modelos_intermediarios"
    )
    informacao_comum = models.TextField()


class Tarefa(models.Model):
    """
    Este modelo representa as tarefas individuais associadas a um recurso gerencial.
    Ele captura a descrição da tarefa e seu status atual.
    """

    gerencial = models.ForeignKey(Gerencial, on_delete=models.CASCADE)
    descricao = models.TextField()
    status = models.CharField(
        max_length=50, choices=[("Pendente", "Pendente"), ("Concluído", "Concluído")]
    )
