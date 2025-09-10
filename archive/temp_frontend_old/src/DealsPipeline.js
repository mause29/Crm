import React, { useState } from 'react';

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
    <div style={{
      backgroundColor: deal.won ? '#d4edda' : deal.overdue ? '#f8d7da' : 'white',
      borderRadius: '6px',
      padding: '10px',
      marginBottom: '10px',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
      cursor: 'pointer',
      position: 'relative',
    }}>
      <div style={{ fontWeight: 'bold' }}>{deal.title}</div>
      <div style={{ fontSize: '0.9em', color: '#555' }}>{deal.company}</div>
      <div style={{ marginTop: '5px', fontWeight: 'bold' }}>{deal.amount.toLocaleString()} $</div>
      {deal.won && <div style={{ color: '#155724', fontWeight: 'bold' }}>WON</div>}
      {deal.overdue && <div style={{ color: '#721c24', fontWeight: 'bold' }}>3d overdue</div>}
      <img
        src={deal.user}
        alt="User"
        style={{
          width: '30px',
          height: '30px',
          borderRadius: '50%',
          position: 'absolute',
          bottom: '10px',
          right: '10px',
          border: '2px solid white',
        }}
      />
    </div>
  );
};

const FilterBar = ({ filter, setFilter }) => {
  const options = ['Pipeline', 'List', 'Calendar'];
  return (
    <div style={{ marginBottom: '10px', display: 'flex', gap: '10px' }}>
      {options.map(option => (
        <button
          key={option}
          onClick={() => setFilter(option)}
          style={{
            padding: '6px 12px',
            borderRadius: '4px',
            border: filter === option ? '2px solid #5c4ac7' : '1px solid #ccc',
            backgroundColor: filter === option ? '#5c4ac7' : 'white',
            color: filter === option ? 'white' : 'black',
            cursor: 'pointer',
          }}
        >
          {option}
        </button>
      ))}
    </div>
  );
};

const DealsPipeline = () => {
  const [filter, setFilter] = useState('Pipeline');

  return (
    <div>
      <FilterBar filter={filter} setFilter={setFilter} />
      {filter === 'Pipeline' && (
        <div style={{ display: 'flex', padding: '20px', gap: '20px', overflowX: 'auto' }}>
          {stages.map(stage => (
            <div key={stage.id} style={{ minWidth: '250px', backgroundColor: '#f1f1f1', borderRadius: '8px', padding: '10px' }}>
              <h3 style={{ fontWeight: 'bold', marginBottom: '10px' }}>
                {stage.title} <br />
                <span style={{ fontWeight: 'normal', fontSize: '0.9em', color: '#666' }}>
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
        <div style={{ padding: '20px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ backgroundColor: '#f1f1f1' }}>
                <th style={{ padding: '10px', border: '1px solid #ddd' }}>Deal</th>
                <th style={{ padding: '10px', border: '1px solid #ddd' }}>Company</th>
                <th style={{ padding: '10px', border: '1px solid #ddd' }}>Amount</th>
                <th style={{ padding: '10px', border: '1px solid #ddd' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {stages.flatMap(stage =>
                stage.deals.map(deal => (
                  <tr key={deal.id} style={{ backgroundColor: deal.won ? '#d4edda' : deal.overdue ? '#f8d7da' : 'white' }}>
                    <td style={{ padding: '10px', border: '1px solid #ddd' }}>{deal.title}</td>
                    <td style={{ padding: '10px', border: '1px solid #ddd' }}>{deal.company}</td>
                    <td style={{ padding: '10px', border: '1px solid #ddd' }}>{deal.amount.toLocaleString()} $</td>
                    <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                      {deal.won ? 'Won' : deal.overdue ? 'Overdue' : 'Open'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
      {filter === 'Calendar' && (
        <div style={{ padding: '20px' }}>
          <p>Calendar view coming soon...</p>
        </div>
      )}
    </div>
  );
};

