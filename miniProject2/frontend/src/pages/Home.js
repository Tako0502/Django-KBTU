import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI-Powered Resume Analyzer
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Get instant feedback on your resume and find your dream job
          </p>
          <div className="space-x-4">
            <Link
              to="/register"
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
            >
              Get Started
            </Link>
            <Link
              to="/login"
              className="bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300"
            >
              Login
            </Link>
          </div>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Resume Analysis</h2>
            <p className="text-gray-600">
              Get detailed feedback on your resume's formatting, content, and keywords.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Job Matching</h2>
            <p className="text-gray-600">
              Find jobs that match your skills and experience.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Skill Development</h2>
            <p className="text-gray-600">
              Identify skill gaps and get recommendations for improvement.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home; 