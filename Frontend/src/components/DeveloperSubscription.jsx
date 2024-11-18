import React, { useState, useEffect } from 'react';
import { Loader2, CheckCircle, XCircle, Users, Mail, Shield, Calendar } from 'lucide-react';

const DeveloperSubscription = () => {
  const [submissionCount, setSubmissionCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    transaction_reference: ''
  });
  
  useEffect(() => {
    fetchSubmissionCount();
  }, []);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const reference = urlParams.get('reference');
    if (reference) {
      setFormData(prev => ({ ...prev, transaction_reference: reference }));
    }
  }, []);

  const fetchSubmissionCount = async () => {
    try {
      const response = await fetch('https://mailer.backend.kumotechs.com/api/submission-count/');
      const data = await response.json();
      setSubmissionCount(data.count);
    } catch (err) {
      console.error('Failed to fetch count:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    try {
      const response = await fetch('https://mailer.backend.kumotechs.com/api/submissions/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Submission failed');
      }

      setSuccess(true);
      setFormData({
        name: '',
        email: '',
        phone: '',
        transaction_reference: ''
      });
      fetchSubmissionCount();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        {/* Logo and Header */}
        <div className="flex flex-col items-center mb-8">
          <img src="/vite.svg" alt="Tutorial Logo" className="h-16 w-16 mb-4" />
          <h1 className="text-3xl font-bold text-center text-gray-900 mb-2">Welcome to Web Development Mastery</h1>
          <p className="text-center text-gray-600 max-w-md">
            You're just one step away from accessing our premium web development tutorials. Please complete your registration below.
          </p>
        </div>

        {/* Developer Count Display */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8 transform hover:scale-102 transition-transform duration-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Users className="h-6 w-6 text-blue-500" />
              <h2 className="text-xl font-semibold text-gray-900">Registered Developers</h2>
            </div>
            <span className="text-2xl font-bold text-blue-600">{submissionCount}</span>
          </div>
        </div>

        {/* Email Usage Info */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">What to Expect:</h3>
          <div className="space-y-3">
            <div className="flex items-start space-x-3">
              <Mail className="h-5 w-5 text-blue-500 mt-0.5" />
              <p className="text-gray-600">Immediate access to our online group tutorial link</p>
            </div>
            <div className="flex items-start space-x-3">
              <Calendar className="h-5 w-5 text-blue-500 mt-0.5" />
              <p className="text-gray-600">Weekly schedule updates and course materials</p>
            </div>
            <div className="flex items-start space-x-3">
              <Shield className="h-5 w-5 text-blue-500 mt-0.5" />
              <p className="text-gray-600">Your email is protected - we never share your information or send spam</p>
            </div>
          </div>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Complete Registration</h2>
          
          {error && (
            <div className="mb-4 flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-md">
              <XCircle className="h-5 w-5" />
              <p>{error}</p>
            </div>
          )}
          
          {success && (
            <div className="mb-4 flex items-center space-x-2 text-green-600 bg-green-50 p-3 rounded-md">
              <CheckCircle className="h-5 w-5" />
              <p>Registration completed successfully! Check your email for next steps.</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Full Name
              </label>
              <input
                type="text"
                id="name"
                name="name"
                required
                value={formData.name}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm
                         px-4 py-3 border transition-colors duration-200"
                placeholder="John Doe"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email Address
              </label>
              <input
                type="email"
                id="email"
                name="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm
                         px-4 py-3 border transition-colors duration-200"
                placeholder="john@example.com"
              />
            </div>

            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                Phone Number
              </label>
              <input
                type="tel"
                id="phone"
                name="phone"
                required
                value={formData.phone}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm
                         px-4 py-3 border transition-colors duration-200"
                placeholder="+234 800 000 0000"
              />
            </div>

            <button
              type="submit"
              disabled={loading || !formData.transaction_reference}
              className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white 
                       bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
                       disabled:bg-blue-300 disabled:cursor-not-allowed transition-all duration-200 hover:shadow-lg"
            >
              {loading ? (
                <span className="flex items-center space-x-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Processing...</span>
                </span>
              ) : (
                'Complete Registration'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default DeveloperSubscription;