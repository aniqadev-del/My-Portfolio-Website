import React from 'react';
import { Link } from 'react-router-dom';
import { Instagram, Linkedin, Twitter, MessageCircle } from 'lucide-react';
import { companyInfo, contactInfo } from '../data/mock';

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="col-span-1 md:col-span-2">
            <img 
              src={companyInfo.logo} 
              alt={companyInfo.name}
              className="h-12 w-auto mb-4"
            />
            <p className="text-gray-300 mb-4 max-w-md">
              {companyInfo.description}
            </p>
            <div className="flex space-x-4">
              <a 
                href={contactInfo.socialMedia.instagram}
                className="text-gray-400 hover:text-pink-500 transition-colors duration-300"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Instagram size={20} />
              </a>
              <a 
                href={contactInfo.socialMedia.linkedin}
                className="text-gray-400 hover:text-blue-500 transition-colors duration-300"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Linkedin size={20} />
              </a>
              <a 
                href={contactInfo.socialMedia.twitter}
                className="text-gray-400 hover:text-cyan-500 transition-colors duration-300"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Twitter size={20} />
              </a>
              <a 
                href={`https://wa.me/${contactInfo.whatsapp.replace(/[^0-9]/g, '')}`}
                className="text-gray-400 hover:text-green-500 transition-colors duration-300"
                target="_blank"
                rel="noopener noreferrer"
              >
                <MessageCircle size={20} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-gray-300 hover:text-cyan-400 transition-colors duration-300">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/services" className="text-gray-300 hover:text-cyan-400 transition-colors duration-300">
                  Services
                </Link>
              </li>
              <li>
                <Link to="/portfolio" className="text-gray-300 hover:text-cyan-400 transition-colors duration-300">
                  Portfolio
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-300 hover:text-cyan-400 transition-colors duration-300">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact</h3>
            <div className="space-y-2 text-gray-300">
              <p>{contactInfo.email}</p>
              <p>{contactInfo.phone}</p>
              <p className="text-sm">{contactInfo.address}</p>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center">
          <p className="text-gray-400">
            © {currentYear} {companyInfo.name}. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};