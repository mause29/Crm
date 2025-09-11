import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const LocationDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  // Sample location data - replace with actual API call
  const locations = {
    1: {
      id: 1,
      name: 'New York Office',
      address: '123 Main St, New York, NY 10001',
      phone: '(555) 123-4567',
      email: 'ny@crmcompany.com',
      manager: 'John Smith',
      employees: 45,
      description: 'Our flagship office in the heart of Manhattan, serving clients across the Northeast region.'
    },
    2: {
      id: 2,
      name: 'Los Angeles Office',
      address: '456 Sunset Blvd, Los Angeles, CA 90210',
      phone: '(555) 987-6543',
      email: 'la@crmcompany.com',
      manager: 'Sarah Johnson',
      employees: 32,
      description: 'Located in the entertainment capital, our LA office specializes in media and entertainment industry clients.'
    },
    3: {
      id: 3,
      name: 'Chicago Office',
      address: '789 Michigan Ave, Chicago, IL 60601',
      phone: '(555) 456-7890',
      email: 'chicago@crmcompany.com',
      manager: 'Mike Davis',
      employees: 28,
      description: 'Serving the Midwest region with expertise in manufacturing and logistics industries.'
    }
  };

  const location = locations[id];

  if (!location) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          Location not found
        </div>
        <button
          onClick={() => navigate('/about')}
          className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Back to About
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <button
        onClick={() => navigate('/about')}
        className="mb-6 bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 transition-colors"
      >
        ← Back to About
      </button>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">{location.name}</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <h2 className="text-xl font-semibold mb-3 text-gray-700">Contact Information</h2>
            <div className="space-y-2">
              <p><strong>Address:</strong> {location.address}</p>
              <p><strong>Phone:</strong> {location.phone}</p>
              <p><strong>Email:</strong> {location.email}</p>
              <p><strong>Manager:</strong> {location.manager}</p>
              <p><strong>Employees:</strong> {location.employees}</p>
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-3 text-gray-700">About This Location</h2>
            <p className="text-gray-600">{location.description}</p>
          </div>
        </div>

        <div className="border-t pt-6">
          <h2 className="text-xl font-semibold mb-3 text-gray-700">Services Offered</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 p-3 rounded-lg text-center">
              <div className="text-2xl mb-2">📊</div>
              <div className="font-medium">Analytics</div>
            </div>
            <div className="bg-green-50 p-3 rounded-lg text-center">
              <div className="text-2xl mb-2">💼</div>
              <div className="font-medium">Consulting</div>
            </div>
            <div className="bg-purple-50 p-3 rounded-lg text-center">
              <div className="text-2xl mb-2">🎯</div>
              <div className="font-medium">Sales Training</div>
            </div>
            <div className="bg-yellow-50 p-3 rounded-lg text-center">
              <div className="text-2xl mb-2">🔧</div>
              <div className="font-medium">Technical Support</div>
            </div>
            <div className="bg-red-50 p-3 rounded-lg text-center">
              <div className="text-2xl mb-2">📈</div>
              <div className="font-medium">Reporting</div>
            </div>
            <div className="bg-indigo-50 p-3 rounded-lg text-center">
              <div className="text-2xl mb-2">🤝</div>
              <div className="font-medium">Client Relations</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LocationDetails;
