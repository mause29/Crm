def capturar_pago(request, order_id):
    """
    Captura el pago después que el cliente completa la tarjeta o PayPal.
    """
    request_capture = OrdersCaptureRequest(order_id)
    request_capture.prefer("return=representation")
    response = client.execute(request_capture)
    
    # Aquí actualizamos la factura en tu base de datos
    if response.result.status == "COMPLETED":
        # Ejemplo: marcar factura como pagada
        # Factura.objects.filter(id=factura_id).update(estado="PAGADO")
        return JsonResponse({"status": "PAGADO", "detalles": response.result.__dict__})
    else:
        return JsonResponse({"status": "FALLIDO", "detalles": response.result.__dict__})
