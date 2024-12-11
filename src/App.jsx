import React, { Suspense, useMemo } from 'react';
import SortableRepoTable from './components/SortableRepoTable';
import reposData from './data/repos.json';

const LoadingFallback = () => (
  <div className="min-h-screen bg-gray-100 flex items-center justify-center">
    <div className="text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
      <p className="mt-4 text-gray-600">Loading repositories...</p>
    </div>
  </div>
);

// Simple data validation
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
  // Validate and memoize the repository data
  const validatedData = useMemo(() => validateRepoData(reposData), []);

  // If no valid data, show error state
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
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <Suspense fallback={<LoadingFallback />}>
          <SortableRepoTable initialData={validatedData} />
        </Suspense>
      </div>
    </div>
  );
}

export default App;