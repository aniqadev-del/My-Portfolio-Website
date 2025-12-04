import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { ArrowRight, ExternalLink, CheckCircle, Loader2 } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

export default function Portfolio() {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [portfolioProjects, setPortfolioProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    fetchPortfolio();
  }, []);

  const fetchPortfolio = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${BACKEND_URL}/api/portfolio`);
      setPortfolioProjects(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching portfolio:', err);
      setError('Failed to load portfolio projects');
    } finally {
      setLoading(false);
    }
  };
  
  const categories = ['All', ...new Set(portfolioProjects.map(project => project.category))];
  
  const filteredProjects = selectedCategory === 'All' 
    ? portfolioProjects 
    : portfolioProjects.filter(project => project.category === selectedCategory);

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 px-4 bg-gradient-to-br from-slate-50 to-blue-50">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Our <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">Portfolio</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Discover how we've helped businesses transform their operations through intelligent automation and AI-powered solutions.
            Each project showcases measurable results and real-world impact.
          </p>
        </div>
      </section>

      {/* Filter Tabs */}
      {!loading && !error && portfolioProjects.length > 0 && (
        <section className="py-12 bg-white border-b">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex flex-wrap justify-center gap-4">
              {categories.map((category) => (
                <Button
                  key={category}
                  variant={selectedCategory === category ? "default" : "outline"}
                  className={`px-6 py-2 rounded-full transition-all duration-300 ${
                    selectedCategory === category 
                      ? 'bg-gradient-to-r from-blue-600 to-cyan-500 text-white' 
                      : 'border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white'
                  }`}
                  onClick={() => setSelectedCategory(category)}
                >
                  {category}
                </Button>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Loading State */}
      {loading && (
        <section className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <Loader2 className="w-12 h-12 animate-spin text-blue-600 mx-auto mb-4" />
            <p className="text-gray-600">Loading portfolio projects...</p>
          </div>
        </section>
      )}

      {/* Error State */}
      {error && (
        <section className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <p className="text-red-600 mb-4">{error}</p>
            <Button onClick={fetchPortfolio}>Try Again</Button>
          </div>
        </section>
      )}

      {/* Empty State */}
      {!loading && !error && portfolioProjects.length === 0 && (
        <section className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <p className="text-gray-600">No portfolio projects available yet. Check back soon!</p>
          </div>
        </section>
      )}

      {/* Projects Grid */}
      {!loading && !error && filteredProjects.length > 0 && (
        <section className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4">
            <div className="grid lg:grid-cols-2 gap-12">
              {filteredProjects.map((project, index) => (
                <Card key={project.id} className="group hover:shadow-xl transition-all duration-300 border-0 bg-white overflow-hidden">
                  {project.image && (
                    <div className="aspect-video bg-gradient-to-br from-blue-100 to-cyan-100 relative overflow-hidden">
                      <img 
                        src={project.image}
                        alt={project.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    </div>
                  )}
                  
                  <CardContent className="p-8">
                    <div className="flex items-center justify-between mb-4">
                      <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-200">
                        {project.category}
                      </Badge>
                      <ExternalLink className="text-gray-400 group-hover:text-blue-600 transition-colors duration-300" size={20} />
                    </div>
                    
                    <h3 className="text-2xl font-bold text-gray-900 mb-4 group-hover:text-blue-600 transition-colors duration-300">
                      {project.title}
                    </h3>
                    
                    <p className="text-gray-600 mb-6 leading-relaxed">
                      {project.description}
                    </p>

                    {/* Challenge & Solution */}
                    {(project.challenge || project.solution) && (
                      <div className="space-y-4 mb-6">
                        {project.challenge && (
                          <div>
                            <h4 className="font-semibold text-red-600 mb-2">Challenge:</h4>
                            <p className="text-sm text-gray-600">{project.challenge}</p>
                          </div>
                        )}
                        {project.solution && (
                          <div>
                            <h4 className="font-semibold text-green-600 mb-2">Solution:</h4>
                            <p className="text-sm text-gray-600">{project.solution}</p>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Results */}
                    {project.results && (
                      <div className="mb-6">
                        <div className="flex items-start space-x-3 p-4 bg-green-50 rounded-lg">
                          <CheckCircle className="text-green-600 flex-shrink-0 mt-0.5" size={20} />
                          <div>
                            <h4 className="font-semibold text-green-900 mb-1">Results:</h4>
                            <p className="text-sm text-green-800">{project.results}</p>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Technologies */}
                    {project.technologies && project.technologies.length > 0 && (
                      <div className="flex flex-wrap gap-2 mb-6">
                        {project.technologies.map((tech, idx) => (
                          <span key={idx} className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                            {tech}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* CTA */}
                    <Button 
                      asChild
                      className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white rounded-full transition-all duration-300 transform hover:scale-105"
                    >
                      <Link to="/contact">
                        Start Similar Project <ArrowRight className="ml-2" size={16} />
                      </Link>
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-blue-600 to-cyan-500 text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Transform Your Business?</h2>
          <p className="text-xl mb-8 text-blue-100">
            Let's discuss how our AI and automation solutions can help you achieve similar results.
          </p>
          <Button 
            asChild
            size="lg"
            className="bg-white text-blue-600 hover:bg-gray-100 rounded-full px-8 py-6 text-lg font-semibold transition-all duration-300 transform hover:scale-105"
          >
            <Link to="/contact">
              Get Started Today <ArrowRight className="ml-2" size={20} />
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
