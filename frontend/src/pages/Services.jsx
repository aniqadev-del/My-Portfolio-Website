import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { CheckCircle, ArrowRight, Zap, Brain, FileText, Code, Loader2 } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const iconMap = {
  Zap,
  Brain,
  FileText,
  Code
};

export default function Services() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/services`);
      setServices(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching services:', err);
      setError('Failed to load services');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 px-4 bg-gradient-to-br from-slate-50 to-blue-50">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Our <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">Services</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            We specialize in transforming business processes through intelligent automation and AI-powered solutions. 
            From workflow optimization to predictive analytics, we help businesses work smarter, not harder.
          </p>
        </div>
      </section>

      {/* Loading State */}
      {loading && (
        <section className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <Loader2 className="w-12 h-12 animate-spin text-blue-600 mx-auto mb-4" />
            <p className="text-gray-600">Loading services...</p>
          </div>
        </section>
      )}

      {/* Error State */}
      {error && (
        <section className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <p className="text-red-600 mb-4">{error}</p>
            <Button onClick={fetchServices}>Try Again</Button>
          </div>
        </section>
      )}

      {/* Empty State */}
      {!loading && !error && services.length === 0 && (
        <section className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <p className="text-gray-600">No services available yet. Check back soon!</p>
          </div>
        </section>
      )}

      {/* Services Grid */}
      {!loading && !error && services.length > 0 && (
        <section className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4">
            <div className="grid md:grid-cols-2 gap-12">
              {services.map((service, index) => {
                // Try to get icon from iconMap, fallback to emoji or default icon
                let IconComponent = null;
                if (service.icon && iconMap[service.icon]) {
                  IconComponent = iconMap[service.icon];
                }
                
                return (
                  <Card key={service.id} className="group hover:shadow-xl transition-all duration-300 border-0 bg-gradient-to-br from-white to-gray-50">
                    <CardContent className="p-10">
                      <div className="flex items-start space-x-6">
                        <div className="flex-shrink-0">
                          <div className="p-4 bg-gradient-to-br from-blue-100 to-cyan-100 rounded-2xl group-hover:scale-110 transition-transform duration-300">
                            {IconComponent ? (
                              <IconComponent className="text-blue-600" size={32} />
                            ) : service.icon ? (
                              <span className="text-3xl">{service.icon}</span>
                            ) : (
                              <Zap className="text-blue-600" size={32} />
                            )}
                          </div>
                        </div>
                        <div className="flex-1">
                          <h3 className="text-2xl font-bold text-gray-900 mb-4">{service.title}</h3>
                          <p className="text-gray-600 mb-6 leading-relaxed">{service.description}</p>
                          
                          {service.features && service.features.length > 0 && (
                            <div className="space-y-3 mb-8">
                              {service.features.map((feature, idx) => (
                                <div key={idx} className="flex items-center">
                                  <CheckCircle className="text-green-500 mr-3 flex-shrink-0" size={18} />
                                  <span className="text-gray-700">{feature}</span>
                                </div>
                              ))}
                            </div>
                          )}

                          <Button 
                            asChild
                            className="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white rounded-full px-6 py-2 transition-all duration-300 transform hover:scale-105"
                          >
                            <Link to="/contact">
                              Learn More <ArrowRight className="ml-2" size={16} />
                            </Link>
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        </section>
      )}

      {/* Process Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Process</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              We follow a proven methodology to deliver exceptional results every time.
            </p>
          </div>

          <div className="grid md:grid-cols-4 gap-8">
            {[
              { step: "01", title: "Discovery", description: "We analyze your workflows to identify automation opportunities" },
              { step: "02", title: "Design", description: "Custom solutions tailored to your specific business needs" },
              { step: "03", title: "Develop", description: "Agile development with regular progress updates" },
              { step: "04", title: "Deploy", description: "Seamless implementation with comprehensive training" }
            ].map((phase, idx) => (
              <div key={idx} className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-blue-600 to-cyan-500 text-white text-xl font-bold mb-4">
                  {phase.step}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{phase.title}</h3>
                <p className="text-gray-600">{phase.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-blue-600 to-cyan-500 text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Get Started?</h2>
          <p className="text-xl mb-8 text-blue-100">
            Let's discuss how we can help transform your business processes with AI and automation.
          </p>
          <Button 
            asChild
            size="lg"
            className="bg-white text-blue-600 hover:bg-gray-100 rounded-full px-8 py-6 text-lg font-semibold transition-all duration-300 transform hover:scale-105"
          >
            <Link to="/contact">
              Contact Us Today <ArrowRight className="ml-2" size={20} />
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
