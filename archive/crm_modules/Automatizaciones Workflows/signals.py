from django.db.models.signals import post_save
from django.dispatch import receiver
from crm.models import Cliente, Oportunidad
from crm.utils import enviar_email_template, generar_factura

@receiver(post_save, sender=Cliente)
def enviar_email_bienvenida(sender, instance, created, **kwargs):
    if created:
        enviar_email_template(
            to_email=instance.email,
            subject="Bienvenido a nuestro CRM",
            template_name="emails/bienvenida.html",
            context={"cliente": instance}
        )

@receiver(post_save, sender=Oportunidad)
def generar_factura_oportunidad(sender, instance, **kwargs):
    if instance.etapa == "Cerrado":
        generar_factura(instance)
