import React, { useState, useEffect } from 'react';
import opportunityService from './services/opportunity';

const stages = [
  { id: 'qualified', title: 'Qualified', deals: [
    { id: 1, title: 'Umbrella Corp deal', company: 'Umbrella Corp', amount: 1500, user: 'https://randomuser.me/api/portraits/women/44.jpg' },
    { id: 2, title: 'JMVD Inc deal', company: 'JMVD Inc', amount: 4500, user: 'https://randomuser.me/api/portraits/men/45.jpg' },
    { id: 3, title: 'Ownerate LLP deal', company: 'Ownerate LLP', amount: 3000, user: 'https://randomuser.me/api/portraits/women/46.jpg' },
    { id: 4, title: 'Silicon Links Inc deal', company: 'Silicon Links Inc', amount: 1000, user: 'https://randomuser.me/api/portraits/men/47.jpg' },
  ]},
  { id: 'contact_made', title: 'Contact Made', deals: [
    { id: 5, title: 'Principalspace Inc deal', company: 'Principalspace Inc', amount: 2300, overdue: true, user: 'https://randomuser.me/api/portraits/women/48.jpg' },
    { id: 6, title: 'Blue Marble LLP deal', company: 'Blue Marble LLP', amount: 1900, user: 'https://randomuser.me/api/portraits/men/49.jpg' },
    { id: 7, title: 'ABC Inc deal', company: 'ABC Inc', amount: 1150, user: 'https://randomuser.me/api/portraits/women/50.jpg' },
  ]},
  { id: 'demo_scheduled', title: 'Demo Scheduled', deals: [
    { id: 8, title: 'Moveer Limited deal', company: 'Moveer Limited', amount: 1400, user: 'https://randomuser.me/api/portraits/men/51.jpg' },
    { id: 9, title: 'Wolfs Corp deal', company: 'Wolfs Corp', amount: 1700, user: 'https://randomuser.me/api/portraits/women/52.jpg' },
  ]},
  { id: 'proposal_made', title: 'Proposal Made', deals: [
    { id: 10, title: 'Omnicorp deal', company: 'Omnicorp', amount: 2700, user: 'https://randomuser.me/api/portraits/men/53.jpg' },
  ]},
  { id: 'negotiations_started', title: 'Negotiations Started', deals: [
    { id: 11, title: 'Big Wheels Inc deal', company: 'Big Wheels Inc', amount: 2600, user: 'https://randomuser.me/api/portraits/women/54.jpg' },
    { id: 12, title: 'Mindbend LLP deal', company: 'Mindbend LLP', amount: 1600, won: true, user: 'https://randomuser.me/api/portraits/men/55.jpg' },
  ]},
];

const DealCard = ({ deal }) => {
  return (
    <div className={`bg-white rounded-md p-4 mb-4 shadow relative cursor-pointer ${deal.won ? 'bg-green-100' : deal.overdue ? 'bg-red-100' : ''}`}>
      <div className="font-bold text-gray-900">{deal.title}</div>
      <div className="text-sm text-gray-600">{deal.company}</div>
      <div className="mt-2 font-semibold text-gray-900">{deal.amount.toLocaleString()} $</div>
      {deal.won && (
        <div className="absolute top-2 left-2 bg-green-600 text-white text-xs font-bold px-2 py-0.5 rounded">WON</div>
      )}
      {deal.overdue && (
        <div className="absolute top-2 left-2 bg-red-600 text-white text-xs font-bold px-2 py-0.5 rounded flex items-center gap-1">
          ⏰ 3d
        </div>
      )}
      <img
        src={deal.user}
        alt="User"
        className="w-8 h-8 rounded-full border-2 border-white absolute bottom-2 right-2"
      />
    </div>
  );
};

const FilterBar = ({ filter, setFilter }) => {
  const options = ['Pipeline', 'List', 'Calendar'];
  return (
    <div className="mb-4 flex gap-2">
      {options.map(option => (
        <button
          key={option}
          onClick={() => setFilter(option)}
          className={`px-3 py-1 rounded ${filter === option ? 'bg-purple-700 text-white border-2 border-purple-800' : 'bg-white border border-gray-300 text-gray-700'}`}
        >
          {option}
        </button>
      ))}
    </div>
  );
};

const DealsPipeline = () => {
  const [filter, setFilter] = useState('Pipeline');
  const [opportunities, setOpportunities] = useState([]);
  const [stagesData, setStagesData] = useState(stages);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchOpportunities = async () => {
      try {
        const ops = await opportunityService.getOpportunities();
        setOpportunities(ops);
        // Group opportunities by stage
        const groupedStages = stages.map(stage => ({
          ...stage,
          deals: ops.filter(op => op.stage === stage.id)
        }));
        setStagesData(groupedStages);
      } catch (err) {
        setError('Failed to load opportunities.');
      } finally {
        setLoading(false);
      }
    };
    fetchOpportunities();
  }, []);

  if (loading) return <p>Loading opportunities...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <FilterBar filter={filter} setFilter={setFilter} />
      {filter === 'Pipeline' && (
        <div className="flex p-5 gap-5 overflow-x-auto">
          {stagesData.map(stage => (
            <div key={stage.id} className="min-w-[250px] bg-gray-100 rounded-lg p-4">
              <h3 className="font-bold mb-2">
                {stage.title} <br />
                <span className="font-normal text-sm text-gray-600">
                  {stage.deals.reduce((sum, d) => sum + d.amount, 0).toLocaleString()} $ · {stage.deals.length} deals
                </span>
              </h3>
              {stage.deals.map(deal => (
                <DealCard key={deal.id} deal={deal} />
              ))}
            </div>
          ))}
        </div>
      )}
      {filter === 'List' && (
        <div className="p-5">
          <table className="w-full border-collapse border border-gray-300">
            <thead>
              <tr className="bg-gray-100">
                <th className="border border-gray-300 p-2 text-left">Deal</th>
                <th className="border border-gray-300 p-2 text-left">Company</th>
                <th className="border border-gray-300 p-2 text-left">Amount</th>
                <th className="border border-gray-300 p-2 text-left">Status</th>
              </tr>
            </thead>
            <tbody>
              {stagesData.flatMap(stage =>
                stage.deals.map(deal => (
                  <tr key={deal.id} className={deal.won ? 'bg-green-100' : deal.overdue ? 'bg-red-100' : 'white'}>
                    <td className="border border-gray-300 p-2">{deal.title}</td>
                    <td className="border border-gray-300 p-2">{deal.company}</td>
                    <td className="border border-gray-300 p-2">{deal.amount.toLocaleString()} $</td>
                    <td className="border border-gray-300 p-2">{deal.won ? 'Won' : deal.overdue ? 'Overdue' : 'Open'}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
      {filter === 'Calendar' && (
        <div className="p-5">
          <p>Calendar view coming soon...</p>
        </div>
      )}
    </div>
  );
};

export default DealsPipeline;

