// src/App.js
import React, { Suspense, useMemo, useState, useEffect } from 'react';
import SortableRepoTable from './components/SortableRepoTable';
import Analytics from './components/Analytics';
import reposData from './data/repos.json';

// Error Boundary Component
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
          <div className="bg-white p-8 rounded-lg shadow-md max-w-lg w-full text-center">
            <h2 className="text-xl font-bold text-gray-900 mb-2">Something went wrong</h2>
            <p className="text-gray-600">Please refresh the page to try again.</p>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

const LoadingFallback = () => (
  <div className="min-h-screen bg-gray-100 flex items-center justify-center">
    <div className="text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
      <p className="mt-4 text-gray-600">Loading repositories...</p>
    </div>
  </div>
);

const validateRepoData = (data) => {
  if (!Array.isArray(data)) {
    console.error('Repository data must be an array');
    return [];
  }

  return data.map(repo => ({
    name: String(repo.name || ''),
    description: String(repo.description || ''),
    url: String(repo.url || ''),
    language: repo.language || null,
    stars: Number(repo.stars || 0),
    forks: Number(repo.forks || 0),
    last_updated: repo.last_updated || new Date().toISOString(),
    topics: Array.isArray(repo.topics) ? repo.topics : [],
    owner: repo.owner ? {
      username: String(repo.owner.username || ''),
      profile_url: String(repo.owner.profile_url || '')
    } : null
  }));
};

function App() {
  // Initialize state with localStorage value
  const [currentView, setCurrentView] = useState(() => {
    return localStorage.getItem('preferredView') || 'table'
  });
  const [isLoading, setIsLoading] = useState(false);
  
  // Validate and memoize the repository data
  const validatedData = useMemo(() => validateRepoData(reposData), []);

  // Check URL parameters on mount
  useEffect(() => {
    const view = new URLSearchParams(window.location.search).get('view');
    if (view === 'analytics' || view === 'table') {
      setCurrentView(view);
    }
  }, []);

  // Handle view changes
  const handleViewChange = async (view) => {
    setIsLoading(true);
    setCurrentView(view);
    localStorage.setItem('preferredView', view);
    window.history.pushState({}, '', `?view=${view}`);
    await new Promise(resolve => setTimeout(resolve, 100));
    setIsLoading(false);
  };

  // Show error state if no valid data
  if (validatedData.length === 0) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
        <div className="bg-white p-8 rounded-lg shadow-md max-w-lg w-full text-center">
          <h2 className="text-xl font-bold text-gray-900 mb-2">No Repository Data Available</h2>
          <p className="text-gray-600">Please check your data source and try again.</p>
        </div>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          {/* Navigation Tabs */}
          <div className="mb-8 flex justify-center">
            <nav className="flex space-x-4 bg-white rounded-lg shadow p-1" aria-label="View options">
              <button
                onClick={() => handleViewChange('table')}
                className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                  currentView === 'table'
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Table View
              </button>
              <button
                onClick={() => handleViewChange('analytics')}
                className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                  currentView === 'analytics'
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Analytics
              </button>
            </nav>
          </div>

          {/* Main Content */}
          <Suspense fallback={<LoadingFallback />}>
            {isLoading ? (
              <LoadingFallback />
            ) : (
              currentView === 'table' ? (
                <SortableRepoTable initialData={validatedData} />
              ) : (
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <Analytics data={validatedData} />
                </div>
              )
            )}
          </Suspense>
        </div>
      </div>
    </ErrorBoundary>
  );
}

export default App;