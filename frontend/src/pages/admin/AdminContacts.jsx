import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdmin } from '../../contexts/AdminContext';
import axios from 'axios';
import { 
  MessageSquare, 
  Search, 
  Filter,
  Download,
  Eye,
  CheckCircle,
  Clock,
  AlertCircle,
  LogOut,
  LayoutDashboard,
  FolderKanban,
  Settings,
  X,
  Send
} from 'lucide-react';
import { toast } from 'sonner';
import ThemeSwitcher from '../../components/ThemeSwitcher';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const AdminContacts = () => {
  const { logout, getAuthHeaders, isAuthenticated } = useAdmin();
  const navigate = useNavigate();
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [selectedContact, setSelectedContact] = useState(null);
  const [showResponseModal, setShowResponseModal] = useState(false);
  const [responseText, setResponseText] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/admin');
      return;
    }
    fetchContacts();
  }, [isAuthenticated, navigate, statusFilter]);

  const fetchContacts = async () => {
    try {
      const params = {};
      if (statusFilter !== 'all') {
        params.status = statusFilter;
      }
      
      const response = await axios.get(`${BACKEND_URL}/api/admin/contacts`, {
        headers: getAuthHeaders(),
        params
      });
      setContacts(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching contacts:', error);
      toast.error('Failed to load contacts');
      if (error.response?.status === 401) {
        logout();
        navigate('/admin');
      }
    }
  };

  const handleStatusUpdate = async (contactId, newStatus) => {
    try {
      await axios.put(
        `${BACKEND_URL}/api/admin/contacts/${contactId}`,
        { status: newStatus },
        { headers: getAuthHeaders() }
      );
      
      toast.success('Status updated successfully');
      fetchContacts();
    } catch (error) {
      console.error('Error updating status:', error);
      toast.error('Failed to update status');
    }
  };

  const handleSendResponse = async () => {
    if (!responseText.trim()) {
      toast.error('Please enter a response');
      return;
    }

    setSubmitting(true);
    try {
      await axios.put(
        `${BACKEND_URL}/api/admin/contacts/${selectedContact.id}`,
        { 
          adminResponse: responseText,
          status: 'in-progress' 
        },
        { headers: getAuthHeaders() }
      );
      
      toast.success('Response sent and saved successfully');
      setShowResponseModal(false);
      setResponseText('');
      setSelectedContact(null);
      fetchContacts();
    } catch (error) {
      console.error('Error sending response:', error);
      toast.error('Failed to send response');
    } finally {
      setSubmitting(false);
    }
  };

  const handleExport = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/admin/contacts/export`, {
        headers: getAuthHeaders(),
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `contacts_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success('Contacts exported successfully');
    } catch (error) {
      console.error('Error exporting contacts:', error);
      toast.error('Failed to export contacts');
    }
  };

  const filteredContacts = contacts.filter(contact => {
    const searchLower = searchTerm.toLowerCase();
    return (
      contact.name.toLowerCase().includes(searchLower) ||
      contact.email.toLowerCase().includes(searchLower) ||
      contact.company.toLowerCase().includes(searchLower) ||
      contact.message.toLowerCase().includes(searchLower)
    );
  });

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
    navigate('/admin');
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'new':
        return <AlertCircle className="w-4 h-4" />;
      case 'in-progress':
        return <Clock className="w-4 h-4" />;
      case 'completed':
        return <CheckCircle className="w-4 h-4" />;
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading contacts...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
                <MessageSquare className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Contact Management</h1>
                <p className="text-sm text-gray-600">View and respond to customer inquiries</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <ThemeSwitcher />
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <LogOut className="w-5 h-5" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8 py-3">
            <button
              onClick={() => navigate('/admin/dashboard')}
              className="flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-gray-900 font-medium"
            >
              <LayoutDashboard className="w-5 h-5" />
              <span>Dashboard</span>
            </button>
            <button
              onClick={() => navigate('/admin/contacts')}
              className="flex items-center space-x-2 px-3 py-2 text-blue-600 border-b-2 border-blue-600 font-medium"
            >
              <MessageSquare className="w-5 h-5" />
              <span>Contacts</span>
            </button>
            <button
              onClick={() => navigate('/admin/portfolio')}
              className="flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-gray-900 font-medium"
            >
              <FolderKanban className="w-5 h-5" />
              <span>Portfolio</span>
            </button>
            <button
              onClick={() => navigate('/admin/services')}
              className="flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-gray-900 font-medium"
            >
              <Settings className="w-5 h-5" />
              <span>Services</span>
            </button>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Filters and Actions */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-6 border border-gray-100">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
            {/* Search */}
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search by name, email, company..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Filters and Actions */}
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Filter className="w-5 h-5 text-gray-400" />
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">All Status</option>
                  <option value="new">New</option>
                  <option value="in-progress">In Progress</option>
                  <option value="completed">Completed</option>
                </select>
              </div>

              <button
                onClick={handleExport}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Download className="w-5 h-5" />
                <span>Export CSV</span>
              </button>
            </div>
          </div>
        </div>

        {/* Contacts Table */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="text-left py-4 px-6 text-sm font-semibold text-gray-700">Name & Email</th>
                  <th className="text-left py-4 px-6 text-sm font-semibold text-gray-700">Company</th>
                  <th className="text-left py-4 px-6 text-sm font-semibold text-gray-700">Message</th>
                  <th className="text-left py-4 px-6 text-sm font-semibold text-gray-700">Status</th>
                  <th className="text-left py-4 px-6 text-sm font-semibold text-gray-700">Date</th>
                  <th className="text-left py-4 px-6 text-sm font-semibold text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredContacts.length > 0 ? (
                  filteredContacts.map((contact) => (
                    <tr key={contact.id} className="border-t border-gray-100 hover:bg-gray-50">
                      <td className="py-4 px-6">
                        <div>
                          <p className="text-sm font-medium text-gray-900">{contact.name}</p>
                          <p className="text-sm text-gray-600">{contact.email}</p>
                        </div>
                      </td>
                      <td className="py-4 px-6">
                        <p className="text-sm text-gray-900">{contact.company || '-'}</p>
                        {contact.phone && (
                          <p className="text-sm text-gray-600">{contact.phone}</p>
                        )}
                      </td>
                      <td className="py-4 px-6">
                        <p className="text-sm text-gray-900 truncate max-w-xs">
                          {contact.message.substring(0, 80)}...
                        </p>
                      </td>
                      <td className="py-4 px-6">
                        <select
                          value={contact.status}
                          onChange={(e) => handleStatusUpdate(contact.id, e.target.value)}
                          className={`inline-flex items-center space-x-1 px-3 py-1 text-xs font-medium rounded-full border cursor-pointer ${
                            contact.status === 'new' ? 'bg-yellow-100 text-yellow-800 border-yellow-300' :
                            contact.status === 'in-progress' ? 'bg-orange-100 text-orange-800 border-orange-300' :
                            'bg-green-100 text-green-800 border-green-300'
                          }`}
                        >
                          <option value="new">New</option>
                          <option value="in-progress">In Progress</option>
                          <option value="completed">Completed</option>
                        </select>
                      </td>
                      <td className="py-4 px-6">
                        <p className="text-sm text-gray-600">
                          {new Date(contact.createdAt).toLocaleDateString()}
                        </p>
                        <p className="text-xs text-gray-500">
                          {new Date(contact.createdAt).toLocaleTimeString()}
                        </p>
                      </td>
                      <td className="py-4 px-6">
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={() => {
                              setSelectedContact(contact);
                              setResponseText(contact.adminResponse || '');
                            }}
                            className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                            title="View Details"
                          >
                            <Eye className="w-5 h-5" />
                          </button>
                          <button
                            onClick={() => {
                              setSelectedContact(contact);
                              setResponseText(contact.adminResponse || '');
                              setShowResponseModal(true);
                            }}
                            className="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                            title="Respond"
                          >
                            <Send className="w-5 h-5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="6" className="py-12 text-center text-gray-500">
                      No contacts found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      {/* Contact Detail Modal */}
      {selectedContact && !showResponseModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200 flex justify-between items-center sticky top-0 bg-white">
              <h3 className="text-xl font-bold text-gray-900">Contact Details</h3>
              <button
                onClick={() => setSelectedContact(null)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-600">Name</label>
                  <p className="text-gray-900 mt-1">{selectedContact.name}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">Email</label>
                  <p className="text-gray-900 mt-1">{selectedContact.email}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">Company</label>
                  <p className="text-gray-900 mt-1">{selectedContact.company || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">Phone</label>
                  <p className="text-gray-900 mt-1">{selectedContact.phone || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">Project Type</label>
                  <p className="text-gray-900 mt-1">{selectedContact.projectType || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">Status</label>
                  <p className="text-gray-900 mt-1 capitalize">{selectedContact.status}</p>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-600">Message</label>
                <p className="text-gray-900 mt-2 bg-gray-50 p-4 rounded-lg">
                  {selectedContact.message}
                </p>
              </div>

              {selectedContact.adminResponse && (
                <div>
                  <label className="text-sm font-medium text-gray-600">Admin Response</label>
                  <p className="text-gray-900 mt-2 bg-blue-50 p-4 rounded-lg">
                    {selectedContact.adminResponse}
                  </p>
                  {selectedContact.respondedAt && (
                    <p className="text-xs text-gray-500 mt-2">
                      Responded on {new Date(selectedContact.respondedAt).toLocaleString()} by {selectedContact.respondedBy}
                    </p>
                  )}
                </div>
              )}

              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => setSelectedContact(null)}
                  className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  Close
                </button>
                <button
                  onClick={() => {
                    setShowResponseModal(true);
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Send Response
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Response Modal */}
      {showResponseModal && selectedContact && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl max-w-2xl w-full">
            <div className="p-6 border-b border-gray-200 flex justify-between items-center">
              <h3 className="text-xl font-bold text-gray-900">Send Response</h3>
              <button
                onClick={() => {
                  setShowResponseModal(false);
                  setResponseText('');
                }}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-600">Contact: {selectedContact.name}</label>
                <p className="text-sm text-gray-500">{selectedContact.email}</p>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 block">Your Response</label>
                <textarea
                  value={responseText}
                  onChange={(e) => setResponseText(e.target.value)}
                  rows={8}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Type your response here..."
                />
              </div>

              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => {
                    setShowResponseModal(false);
                    setResponseText('');
                  }}
                  className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                  disabled={submitting}
                >
                  Cancel
                </button>
                <button
                  onClick={handleSendResponse}
                  disabled={submitting || !responseText.trim()}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {submitting ? 'Sending...' : 'Send Response'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminContacts;
