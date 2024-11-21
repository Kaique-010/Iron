'''from django.db.models.signals import post_save
from django.dispatch import receiver
from OrdemProducao.models import Etapa, EtapaProducao, OrdemProducao

@receiver(post_save, sender=OrdemProducao)
def criar_etapas_padrao(sender, instance, created, **kwargs):
    if created:
        etapas = Etapa.objects.filter(empresa=instance.empresa).order_by('ordem')
        for etapa in etapas:
            EtapaProducao.objects.create(
                ordem_producao=instance,
                etapa=etapa,
                responsavel=etapa.responsavel_padrao,
                empresa=instance.empresa
            )
'''