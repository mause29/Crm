import React from 'react';
import { useNavigate } from 'react-router-dom';

const About = () => {
  const navigate = useNavigate();

  // Sample locations data - replace with actual data from your backend
  const locations = [
    { id: 1, name: 'New York Office', address: '123 Main St, NY' },
    { id: 2, name: 'Los Angeles Office', address: '456 Sunset Blvd, LA' },
    { id: 3, name: 'Chicago Office', address: '789 Michigan Ave, Chicago' },
  ];

  const handleLocationClick = (loc) => {
    navigate(`/location/${loc.id}`);
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">About Our Company</h1>

      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-2xl font-semibold mb-4 text-gray-700">Our Mission</h2>
        <p className="text-gray-600 mb-4">
          We are a leading CRM solution provider dedicated to helping businesses
          manage their customer relationships effectively. Our platform combines
          powerful analytics, intuitive design, and robust functionality to
          streamline your sales and customer management processes.
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-2xl font-semibold mb-4 text-gray-700">Our Locations</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {locations.map((loc) => (
            <div
              key={loc.id}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
              onClick={() => handleLocationClick(loc)}
            >
              <h3 className="font-semibold text-lg mb-2">{loc.name}</h3>
              <p className="text-gray-600">{loc.address}</p>
              <button className="mt-3 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors">
                View Details
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-semibold mb-4 text-gray-700">Contact Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold mb-2">Headquarters</h3>
            <p className="text-gray-600">123 Business Ave<br />Suite 100<br />New York, NY 10001</p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Support</h3>
            <p className="text-gray-600">Email: support@crmcompany.com<br />Phone: (555) 123-4567</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
