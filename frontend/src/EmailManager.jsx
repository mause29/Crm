import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './EmailManager.css';

const EmailManager = () => {
  const [templates, setTemplates] = useState([]);
  const [clients, setClients] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [selectedClients, setSelectedClients] = useState([]);
  const [emailForm, setEmailForm] = useState({
    to_email: '',
    subject: '',
    body: ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [activeTab, setActiveTab] = useState('send');

  useEffect(() => {
    fetchTemplates();
    fetchClients();
  }, []);

  const fetchTemplates = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://127.0.0.1:8000/email/templates', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTemplates(response.data);
    } catch (error) {
      console.error('Error fetching templates:', error);
    }
  };

  const fetchClients = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://127.0.0.1:8000/email/clients', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setClients(response.data);
    } catch (error) {
      console.error('Error fetching clients:', error);
    }
  };

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
    setEmailForm({
      ...emailForm,
      subject: template.subject,
      body: template.body
    });
  };

  const handleClientSelect = (clientId) => {
    setSelectedClients(prev =>
      prev.includes(clientId)
        ? prev.filter(id => id !== clientId)
        : [...prev, clientId]
    );
  };

  const handleSendEmail = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      if (activeTab === 'bulk' && selectedClients.length > 0) {
        await axios.post('http://127.0.0.1:8000/email/send-bulk', {
          client_ids: selectedClients,
          subject: emailForm.subject,
          body: emailForm.body,
          template_id: selectedTemplate?.id
        }, { headers });
        setMessage(`Email sent successfully to ${selectedClients.length} clients!`);
      } else {
        await axios.post('http://127.0.0.1:8000/email/send', {
          to_email: emailForm.to_email,
          subject: emailForm.subject,
          body: emailForm.body,
          template_id: selectedTemplate?.id
        }, { headers });
        setMessage('Email sent successfully!');
      }

      // Reset form
      setEmailForm({ to_email: '', subject: '', body: '' });
      setSelectedClients([]);
      setSelectedTemplate(null);
    } catch (error) {
      setMessage('Error sending email. Please try again.');
      console.error('Error sending email:', error);
    } finally {
      setLoading(false);
    }
  };

  const selectAllClients = () => {
    setSelectedClients(clients.map(client => client.id));
  };

  const clearSelection = () => {
    setSelectedClients([]);
  };

  return (
    <div className="email-manager">
      <h1>Email Manager</h1>

      {message && (
        <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
          {message}
        </div>
      )}

      <div className="email-tabs">
        <button
          className={activeTab === 'send' ? 'active' : ''}
          onClick={() => setActiveTab('send')}
        >
          Send Single Email
        </button>
        <button
          className={activeTab === 'bulk' ? 'active' : ''}
          onClick={() => setActiveTab('bulk')}
        >
          Send Bulk Email
        </button>
      </div>

      <div className="email-content">
        <div className="templates-section">
          <h2>Email Templates</h2>
          <div className="templates-grid">
            {templates.map(template => (
              <div
                key={template.id}
                className={`template-card ${selectedTemplate?.id === template.id ? 'selected' : ''}`}
                onClick={() => handleTemplateSelect(template)}
              >
                <h3>{template.name}</h3>
                <p>{template.category}</p>
                <div className="template-preview">
                  <strong>Subject:</strong> {template.subject}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="email-form-section">
          <h2>{activeTab === 'send' ? 'Send Email' : 'Send Bulk Email'}</h2>

          <form onSubmit={handleSendEmail} className="email-form">
            {activeTab === 'send' && (
              <div className="form-group">
                <label>To:</label>
                <input
                  type="email"
                  value={emailForm.to_email}
                  onChange={(e) => setEmailForm({...emailForm, to_email: e.target.value})}
                  placeholder="recipient@example.com"
                  required
                />
              </div>
            )}

            {activeTab === 'bulk' && (
              <div className="clients-selection">
                <div className="selection-controls">
                  <button type="button" onClick={selectAllClients}>Select All</button>
                  <button type="button" onClick={clearSelection}>Clear</button>
                  <span>{selectedClients.length} clients selected</span>
                </div>
                <div className="clients-list">
                  {clients.map(client => (
                    <div key={client.id} className="client-item">
                      <input
                        type="checkbox"
                        checked={selectedClients.includes(client.id)}
                        onChange={() => handleClientSelect(client.id)}
                      />
                      <span>{client.name} ({client.email})</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="form-group">
              <label>Subject:</label>
              <input
                type="text"
                value={emailForm.subject}
                onChange={(e) => setEmailForm({...emailForm, subject: e.target.value})}
                required
              />
            </div>

            <div className="form-group">
              <label>Message:</label>
              <textarea
                value={emailForm.body}
                onChange={(e) => setEmailForm({...emailForm, body: e.target.value})}
                rows="10"
                required
              />
            </div>

            <button type="submit" disabled={loading || (activeTab === 'bulk' && selectedClients.length === 0)}>
              {loading ? 'Sending...' : `Send ${activeTab === 'bulk' ? 'Bulk ' : ''}Email`}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default EmailManager;
