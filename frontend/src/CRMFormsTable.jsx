import React, { useState } from 'react';
import ClientForm from './ClientForm';
import OpportunityForm from './OpportunityForm';

const CRMFormsTable = () => {
  const [activeForm, setActiveForm] = useState('client');

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">CRM Forms</h2>
      <div className="mb-4">
        <button
          onClick={() => setActiveForm('client')}
          className={`px-4 py-2 mr-2 rounded ${activeForm === 'client' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
        >
          Client Form
        </button>
        <button
          onClick={() => setActiveForm('opportunity')}
          className={`px-4 py-2 rounded ${activeForm === 'opportunity' ? 'bg-green-600 text-white' : 'bg-gray-200'}`}
        >
          Opportunity Form
        </button>
      </div>
      {activeForm === 'client' && <ClientForm />}
      {activeForm === 'opportunity' && <OpportunityForm />}
    </div>
  );
};

export default CRMFormsTable;
