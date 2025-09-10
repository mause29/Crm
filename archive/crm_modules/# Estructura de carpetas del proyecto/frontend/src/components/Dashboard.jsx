import React, { useEffect, useState } from "react";
import { getClients } from "../services/api";

export default function Dashboard() {
  const [clients, setClients] = useState([]);

  useEffect(() => {
    getClients().then(res => setClients(res.data));
  }, []);

  return (
    <div>
      <h1>Dashboard CRM</h1>
      <p>Total Clientes: {clients.length}</p>
      {/* Aquí se pueden agregar gráficos de embudo, KPIs, mapas de calor */}
    </div>
  );
}
