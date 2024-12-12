import React, { Suspense, useMemo, useState, useEffect } from 'react';
import SortableRepoTable from './components/SortableRepoTable';
import Analytics from './components/Analytics';
import Reddit from './components/Reddit';
import { ChevronDown } from 'lucide-react';
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
  const [currentView, setCurrentView] = useState(() => {
    return localStorage.getItem('preferredView') || 'table'
  });
  const [isLoading, setIsLoading] = useState(false);
  const [showSocialDropdown, setShowSocialDropdown] = useState(false);
  
  const validatedData = useMemo(() => validateRepoData(reposData), []);

  // Handle clicks outside of dropdown to close it
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (!event.target.closest('.social-dropdown')) {
        setShowSocialDropdown(false);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, []);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const view = params.get('view');
    if (view === 'analytics' || view === 'table' || view?.startsWith('social/')) {
      setCurrentView(view);
      window.history.replaceState({}, '', `${import.meta.env.BASE_URL}?view=${view}`);
    }
  }, []);

  const handleViewChange = async (view) => {
    setIsLoading(true);
    setCurrentView(view);
    localStorage.setItem('preferredView', view);
    
    if (view.startsWith('social/')) {
      window.location.href = `${import.meta.env.BASE_URL}${view}`;
    } else {
      window.history.pushState({}, '', `?view=${view}`);
    }
    
    await new Promise(resolve => setTimeout(resolve, 100));
    setIsLoading(false);
  };

  const handleSocialClick = (platform) => {
    setShowSocialDropdown(false);
    handleViewChange(`social/${platform}`);
  };

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
              
              {/* Social Dropdown */}
              <div className="relative social-dropdown">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowSocialDropdown(!showSocialDropdown);
                  }}
                  className={`px-4 py-2 text-sm font-medium rounded-md transition-colors flex items-center space-x-1 ${
                    currentView.startsWith('social/')
                      ? 'bg-blue-500 text-white'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <span>Social</span>
                  <ChevronDown className="w-4 h-4" />
                </button>
                
                {showSocialDropdown && (
                  <div className="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-10">
                    <div className="py-1" role="menu" aria-orientation="vertical">
                      <button
                        onClick={() => handleSocialClick('reddit')}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                        role="menuitem"
                      >
                        Reddit
                      </button>
                      <button
                        onClick={() => handleSocialClick('linkedin')}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                        role="menuitem"
                      >
                        LinkedIn
                      </button>
                      <button
                        onClick={() => handleSocialClick('x')}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                        role="menuitem"
                      >
                        X (Twitter)
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </nav>
          </div>

          {/* Main Content */}
          <Suspense fallback={<LoadingFallback />}>
            {isLoading ? (
              <LoadingFallback />
            ) : (
              <>
                {currentView === 'table' && <SortableRepoTable initialData={validatedData} />}
                {currentView === 'analytics' && (
                  <div className="bg-white rounded-xl shadow-lg p-6">
                    <Analytics data={validatedData} />
                  </div>
                )}
                {currentView === 'social/reddit' && <Reddit />}
                {currentView === 'social/linkedin' && (
                  <div className="bg-white rounded-xl shadow-lg p-6">
                    <h2 className="text-2xl font-bold mb-4">LinkedIn Integration</h2>
                    <p>LinkedIn content goes here</p>
                  </div>
                )}
                {currentView === 'social/x' && (
                  <div className="bg-white rounded-xl shadow-lg p-6">
                    <h2 className="text-2xl font-bold mb-4">X (Twitter) Integration</h2>
                    <p>X content goes here</p>
                  </div>
                )}
              </>
            )}
          </Suspense>
        </div>
      </div>
    </ErrorBoundary>
  );
}

export default App;