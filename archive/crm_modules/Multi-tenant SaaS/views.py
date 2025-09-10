def clientes_empresa(request):
    clientes = Cliente.objects.filter(empresa=request.empresa)
    return JsonResponse({"clientes": list(clientes.values())})
