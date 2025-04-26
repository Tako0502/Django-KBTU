import React from 'react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Resume Analysis Card */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Resume Analysis</h2>
            <p className="text-gray-600 mb-4">
              Upload your resume to get detailed feedback and suggestions for improvement.
            </p>
            <Link
              to="/resume-upload"
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Upload Resume
            </Link>
          </div>

          {/* Job Search Card */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Job Search</h2>
            <p className="text-gray-600 mb-4">
              Find jobs that match your skills and experience.
            </p>
            <Link
              to="/job-search"
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Search Jobs
            </Link>
          </div>

          {/* Profile Card */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Profile</h2>
            <p className="text-gray-600 mb-4">
              Update your personal information and preferences.
            </p>
            <Link
              to="/profile"
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              View Profile
            </Link>
          </div>
        </div>

        {/* Recent Activity Section */}
        <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
          <div className="space-y-4">
            <div className="border-b pb-4">
              <p className="text-gray-600">No recent activity</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 