import React, { useEffect } from "react";

const PayPalButton = ({ amount, invoiceId }) => {
  useEffect(() => {
    window.paypal.Buttons({
      createOrder: function (data, actions) {
        return actions.order.create({
          purchase_units: [{
            amount: { value: amount.toString() },
            invoice_id: invoiceId
          }]
        });
      },
      onApprove: function (data, actions) {
        return actions.order.capture().then(function (details) {
          alert("Pago completado por " + details.payer.name.given_name);
          // Actualizar estado en backend
          fetch(`/api/invoices/${invoiceId}/`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: 'paid' })
          });
          fetch(`/api/opportunities/${invoiceId}/`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: 'paid' })
          });
        });
      }
    }).render(`#paypal-button-${invoiceId}`);
  }, [amount, invoiceId]);

  return <div id={`paypal-button-${invoiceId}`}></div>;
};

export default PayPalButton;
