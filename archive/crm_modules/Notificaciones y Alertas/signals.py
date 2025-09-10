@receiver(post_save, sender=Oportunidad)
def alerta_cambio_etapa(sender, instance, **kwargs):
    Notificacion.objects.create(
        usuario=instance.asignado,
        mensaje=f"La oportunidad {instance.nombre} cambió a etapa {instance.etapa}"
    )
