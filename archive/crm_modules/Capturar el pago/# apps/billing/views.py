# apps/billing/views.py (continuación)
class PayPalCaptureOrderView(APIView, PayPalClient):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('orderID')
        request_capture = OrdersCaptureRequest(order_id)
        request_capture.prefer('return=representation')
        response = self.client.client.execute(request_capture)
        if response.result.status == "COMPLETED":
            # Aquí puedes guardar el pago en tu base de datos
            return Response({'status': 'success', 'details': response.result})
        return Response({'status': 'failed', 'details': response.result})
