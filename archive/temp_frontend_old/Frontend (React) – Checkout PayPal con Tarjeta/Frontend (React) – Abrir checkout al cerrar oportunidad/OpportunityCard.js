import React, { useState } from "react";
import PayPalButton from "./PayPalButton";

const OpportunityCard = ({ opportunity }) => {
    const [status, setStatus] = useState(opportunity.status);
    const [showPayPal, setShowPayPal] = useState(false);

    const closeOpportunity = async () => {
        // Marcar oportunidad como cerrada en backend
        const res = await fetch(`/api/opportunities/${opportunity.id}/`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: 'closed' })
        });
        if (res.ok) {
            setStatus('closed');
            setShowPayPal(true); // mostrar botón de pago automáticamente
        }
    };

    return (
        <div className="opportunity-card">
            <h3>{opportunity.client_name}</h3>
            <p>Monto: ${opportunity.amount}</p>
            <p>Estado: {status}</p>
            {status === 'open' && (
                <button onClick={closeOpportunity}>Cerrar oportunidad</button>
            )}
            {showPayPal && <PayPalButton amount={opportunity.amount} invoiceId={opportunity.id} />}
        </div>
    );
};

export default OpportunityCard;
