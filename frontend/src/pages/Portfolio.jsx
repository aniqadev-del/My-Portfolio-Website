import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { ArrowRight, ExternalLink, CheckCircle } from 'lucide-react';
import { portfolioProjects } from '../data/mock';

export default function Portfolio() {
  const [selectedCategory, setSelectedCategory] = useState('All');
  
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

      {/* Projects Grid */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-12">
            {filteredProjects.map((project, index) => (
              <Card key={project.id} className="group hover:shadow-xl transition-all duration-300 border-0 bg-white overflow-hidden">
                <div className="aspect-video bg-gradient-to-br from-blue-100 to-cyan-100 relative overflow-hidden">
                  <img 
                    src={project.mockImage}
                    alt={project.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                </div>
                
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
                  <div className="space-y-4 mb-6">
                    <div>
                      <h4 className="font-semibold text-red-600 mb-2">Challenge:</h4>
                      <p className="text-sm text-gray-600">{project.challenge}</p>
                    </div>
                    <div>
                      <h4 className="font-semibold text-green-600 mb-2">Solution:</h4>
                      <p className="text-sm text-gray-600">{project.solution}</p>
                    </div>
                  </div>

                  {/* Impact */}
                  <div className="mb-6">
                    <div className="flex items-start space-x-3 p-4 bg-green-50 rounded-lg">
                      <CheckCircle className="text-green-500 mt-1 flex-shrink-0" size={20} />
                      <div>
                        <h4 className="font-semibold text-green-800 mb-1">Impact:</h4>
                        <p className="text-sm text-green-700">{project.impact}</p>
                      </div>
                    </div>
                  </div>

                  {/* Technologies */}
                  <div className="mb-6">
                    <h4 className="font-semibold text-gray-900 mb-3">Technologies Used:</h4>
                    <div className="flex flex-wrap gap-2">
                      {project.technologies.map((tech, idx) => (
                        <Badge key={idx} variant="secondary" className="text-xs">
                          {tech}
                        </Badge>
                      ))}
                    </div>
                  </div>

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

      {/* Results Summary */}
      
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 text-center">
          {/*
          <h2 className="text-4xl font-bold text-gray-900 mb-8">
            Measurable Results Across All Projects
          </h2>
          */}
          <div className="grid md:grid-cols-3 gap-8 mb-12">
            
            <div className="p-8 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-2xl">
              {/*
              <div className="text-4xl font-bold text-blue-600 mb-2">90+%</div>
              <div className="text-gray-700">Reduction in Manual Work</div>
              */}
            </div>
            
            <div className="p-8 bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl">
              {*/
              <div className="text-4xl font-bold text-green-600 mb-2">500+</div>
              <div className="text-gray-700">Hours Saved Monthly</div>
              */}
            </div>
            <div className="p-8 bg-gradient-to-br from-orange-50 to-amber-50 rounded-2xl">
              {/*
              <div className="text-4xl font-bold text-orange-600 mb-2">100%</div>
              <div className="text-gray-700">Client Satisfaction Rate</div>
              */}
            </div>
      
          </div>

          <Button 
            asChild
            size="lg"
            className="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white px-8 py-4 rounded-full text-lg font-semibold transition-all duration-300 transform hover:scale-105"
          >
            <Link to="/contact">
              Discuss Your Project <ArrowRight className="ml-2" size={20} />
            </Link>
          </Button>
        </div>
      </section>
      
    </div>
  );
}
