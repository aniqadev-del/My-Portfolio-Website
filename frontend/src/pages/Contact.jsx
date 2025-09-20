import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { toast } from 'sonner';
import { Mail, Phone, MapPin, Clock, MessageCircle, Instagram, Linkedin, Twitter, Loader2 } from 'lucide-react';
import { contactInfo } from '../data/mock';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    phone: '',
    message: '',
    projectType: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Validate required fields
    if (!formData.name.trim() || !formData.email.trim() || !formData.message.trim()) {
      toast.error("Please fill in all required fields");
      setIsSubmitting(false);
      return;
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      toast.error("Please enter a valid email address");
      setIsSubmitting(false);
      return;
    }

    try {
      const response = await axios.post(`${API}/contact`, {
        name: formData.name,
        email: formData.email,
        company: formData.company,
        phone: formData.phone,
        projectType: formData.projectType,
        message: formData.message
      });

      if (response.data.success) {
        toast.success(response.data.message || "Thank you! We'll get back to you within 24 hours.");
        setFormData({
          name: '',
          email: '',
          company: '',
          phone: '',
          message: '',
          projectType: ''
        });
      } else {
        toast.error(response.data.message || "Failed to send message. Please try again.");
      }
    } catch (error) {
      console.error('Contact form submission error:', error);
      if (error.response?.data?.message) {
        toast.error(error.response.data.message);
      } else if (error.response?.status === 400) {
        toast.error("Please check your input and try again.");
      } else {
        toast.error("Failed to send message. Please try again later.");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 px-4 bg-gradient-to-br from-slate-50 to-blue-50">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Let's <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">Connect</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Ready to transform your business with AI and automation? We'd love to discuss your project 
            and show you how we can help streamline your operations.
          </p>
        </div>
      </section>

      {/* Contact Form & Info */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-16">
            {/* Contact Form */}
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-8">
                Start Your Project Today
              </h2>
              
              <Card className="border-0 shadow-lg">
                <CardContent className="p-8">
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <Label htmlFor="name">Full Name *</Label>
                        <Input
                          id="name"
                          name="name"
                          value={formData.name}
                          onChange={handleInputChange}
                          required
                          className="mt-2"
                          placeholder="John Doe"
                        />
                      </div>
                      <div>
                        <Label htmlFor="email">Email Address *</Label>
                        <Input
                          id="email"
                          name="email"
                          type="email"
                          value={formData.email}
                          onChange={handleInputChange}
                          required
                          className="mt-2"
                          placeholder="john@company.com"
                        />
                      </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <Label htmlFor="company">Company Name</Label>
                        <Input
                          id="company"
                          name="company"
                          value={formData.company}
                          onChange={handleInputChange}
                          className="mt-2"
                          placeholder="Your Company"
                        />
                      </div>
                      <div>
                        <Label htmlFor="phone">Phone Number</Label>
                        <Input
                          id="phone"
                          name="phone"
                          type="tel"
                          value={formData.phone}
                          onChange={handleInputChange}
                          className="mt-2"
                          placeholder="+1 (555) 123-4567"
                        />
                      </div>
                    </div>

                    <div>
                      <Label htmlFor="projectType">Project Type</Label>
                      <select
                        id="projectType"
                        name="projectType"
                        value={formData.projectType}
                        onChange={handleInputChange}
                        className="mt-2 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="">Select a service</option>
                        <option value="process-automation">Process Automation</option>
                        <option value="ai-analytics">AI-Powered Analytics</option>
                        <option value="document-intelligence">Document Intelligence</option>
                        <option value="custom-development">Custom Software Development</option>
                        <option value="consultation">General Consultation</option>
                      </select>
                    </div>

                    <div>
                      <Label htmlFor="message">Project Details *</Label>
                      <Textarea
                        id="message"
                        name="message"
                        value={formData.message}
                        onChange={handleInputChange}
                        required
                        className="mt-2"
                        rows={6}
                        placeholder="Tell us about your project, current challenges, and what you'd like to achieve..."
                      />
                    </div>

                    <Button
                      type="submit"
                      disabled={isSubmitting}
                      className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white py-3 rounded-full text-lg font-semibold transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isSubmitting ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Sending...
                        </>
                      ) : (
                        'Send Message'
                      )}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>

            {/* Contact Information */}
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-8">
                Get in Touch
              </h2>

              <div className="space-y-8 mb-12">
                <div className="flex items-start space-x-4">
                  <div className="p-3 bg-gradient-to-br from-blue-100 to-cyan-100 rounded-full">
                    <Mail className="text-blue-600" size={24} />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">Email Us</h3>
                    <p className="text-gray-600">{contactInfo.email}</p>
                    <p className="text-sm text-gray-500">We'll respond within 24 hours</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="p-3 bg-gradient-to-br from-blue-100 to-cyan-100 rounded-full">
                    <Phone className="text-blue-600" size={24} />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">Call Us</h3>
                    <p className="text-gray-600">{contactInfo.phone}</p>
                    <p className="text-sm text-gray-500">Mon-Fri, 9AM-6PM EST</p>
                  </div>
                </div>

                {/* Visit Us and Business Hours sections removed as requested */}
              </div>

              {/* WhatsApp CTA */}
              <Card className="border-0 bg-gradient-to-r from-green-500 to-green-600 text-white mb-8">
                <CardContent className="p-6">
                  <div className="flex items-center space-x-4">
                    <MessageCircle size={32} />
                    <div className="flex-1">
                      <h3 className="font-semibold mb-1">Quick Response via WhatsApp</h3>
                      <p className="text-green-100 text-sm">Get instant answers to your questions</p>
                    </div>
                    <Button 
                      asChild
                      className="bg-white text-green-600 hover:bg-gray-100"
                    >
                      <a 
                        href={`https://wa.me/${contactInfo.whatsapp.replace(/[^0-9]/g, '')}`}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        Chat Now
                      </a>
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* Social Media */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-4">Follow Us</h3>
                <div className="flex space-x-4">
                  <a 
                    href={contactInfo.socialMedia.instagram}
                    className="p-3 bg-gradient-to-br from-pink-100 to-pink-200 rounded-full hover:from-pink-200 hover:to-pink-300 transition-all duration-300"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Instagram className="text-pink-600" size={20} />
                  </a>
                  <a 
                    href={contactInfo.socialMedia.linkedin}
                    className="p-3 bg-gradient-to-br from-blue-100 to-blue-200 rounded-full hover:from-blue-200 hover:to-blue-300 transition-all duration-300"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Linkedin className="text-blue-600" size={20} />
                  </a>
                  <a 
                    href={contactInfo.socialMedia.twitter}
                    className="p-3 bg-gradient-to-br from-cyan-100 to-cyan-200 rounded-full hover:from-cyan-200 hover:to-cyan-300 transition-all duration-300"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Twitter className="text-cyan-600" size={20} />
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}