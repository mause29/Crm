import React from 'react';
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";

const PayPalButton = ({ amount, invoiceId }) => {
    return (
        <PayPalScriptProvider options={{
            "client-id": "TU_CLIENT_ID",
            "components": "buttons",
            "currency": "USD"
        }}>
            <PayPalButtons
                style={{ layout: "vertical" }}
                createOrder={(data, actions) => {
                    return actions.order.create({
                        purchase_units: [{
                            amount: { value: amount },
                            description: `Factura #${invoiceId}`
                        }]
                    });
                }}
                onApprove={async (data, actions) => {
                    const order = await actions.order.capture();
                    console.log('Pago completado:', order);
                    alert('Pago completado correctamente');
                }}
                onError={(err) => {
                    console.error('Error PayPal:', err);
                    alert('Ocurrió un error en el pago');
                }}
            />
        </PayPalScriptProvider>
    );
};

export default PayPalButton;
