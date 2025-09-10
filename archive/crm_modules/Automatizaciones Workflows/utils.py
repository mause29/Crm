from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def enviar_email_template(to_email, subject, template_name, context):
    html_content = render_to_string(template_name, context)
    email = EmailMultiAlternatives(subject, "", to=[to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()

def generar_factura(oportunidad):
    # Aquí integrar PayPal o Stripe para generar factura
    print(f"Generando factura para {oportunidad.cliente.nombre}")
