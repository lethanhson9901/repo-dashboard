# Code Export from /home/son/Documents/note/project/repo-dashboard/src

Generated on: 2024-12-11 13:20:47


## index.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --font-inter: 'Inter', sans-serif;
}

body {
  font-family: var(--font-inter);
}

@layer base {
  html {
    @apply antialiased;
  }
}

```

## App.jsx

```jsx
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
```

## main.jsx

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

```

## utils/dataValidation.js

```javascript
export const validateRepoData = (data) => {
    if (!Array.isArray(data)) {
      throw new Error('Repository data must be an array');
    }
  
    return data.map(repo => {
      if (!repo || typeof repo !== 'object') {
        throw new Error('Each repository must be an object');
      }
  
      // Ensure required fields exist with proper types
      const validatedRepo = {
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
      };
  
      return validatedRepo;
    });
  };
```

## components/SortableRepoTable/index.jsx

```jsx
import React, { useState, useMemo } from 'react';
import { Search } from 'lucide-react';
import ViewToggle from './ViewToggle';
import TableView from './TableView';
import CardView from './CardView';
import StatsSection from './StatsSection';
import SortOptions from './SortOptions';
import { useRepoData } from './hooks/useRepoData';
import SearchBar from './SearchBar';

const SortableRepoTable = ({ initialData = [] }) => {
  const [isTableView, setIsTableView] = useState(true);
  const {
    filteredAndSortedData,
    paginatedData,
    searchTerm,
    setSearchTerm,
    sortConfig,
    handleSort,
    pagination,
    totalItems
  } = useRepoData(initialData);

  if (!Array.isArray(initialData) || initialData.length === 0) {
    return (
      <div className="w-full bg-white rounded-xl shadow-lg p-8">
        <div className="text-center text-gray-500">
          No repositories available
        </div>
      </div>
    );
  }

  return (
    <div className="w-full bg-white rounded-xl shadow-lg">
      {/* Header */}
      <div className="p-4 border-b">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div className="flex items-center gap-4">
            <h2 className="text-xl font-bold text-gray-900">Featured Repositories</h2>
            <ViewToggle isTableView={isTableView} onToggle={() => setIsTableView(!isTableView)} />
          </div>
          <SearchBar searchTerm={searchTerm} onSearch={setSearchTerm} />
        </div>
      </div>

      {/* Stats */}
      <StatsSection data={initialData} />

      {/* Sort Options */}
      <SortOptions sortConfig={sortConfig} onSort={handleSort} />

      {/* Main Content */}
      <div className="transition-all duration-300 ease-in-out">
        {isTableView ? (
          <TableView 
            data={paginatedData}
            sortConfig={sortConfig}
            onSort={handleSort}
            pagination={pagination}
          />
        ) : (
          <CardView data={paginatedData} />
        )}
      </div>

      {/* Empty State */}
      {filteredAndSortedData.length === 0 && (
        <div className="p-8 text-center text-gray-500">
          <div className="mx-auto w-24 h-24 mb-4">
            <Search className="w-full h-full text-gray-300" />
          </div>
          <h3 className="text-lg font-medium mb-2">No repositories found</h3>
          <p className="text-sm text-gray-400">
            Try adjusting your search or filter criteria
          </p>
        </div>
      )}

      {/* Footer */}
      <div className="p-4 border-t text-sm text-gray-500 text-center">
        Showing {paginatedData.length} of {totalItems} repositories
      </div>
    </div>
  );
};

export default SortableRepoTable;
```

## components/SortableRepoTable/TableView/index.jsx

```jsx
import React, { useState, useRef } from 'react';
import { 
  ArrowUp, 
  ArrowDown, 
  ArrowUpDown,
  ChevronUp,
  ChevronDown,
  ExternalLink,
  User,
  Tag,
  Star,
  GitFork,
  Code,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import { formatDate, getLanguageColor } from '../utils/dataUtils';
import Pagination from '../Pagination';

const TableView = ({ data, sortConfig, onSort, pagination }) => {
  const [expandedRows, setExpandedRows] = useState(new Set());
  const scrollContainerRef = useRef(null);

  const toggleRowExpansion = (index) => {
    const newExpandedRows = new Set(expandedRows);
    if (newExpandedRows.has(index)) {
      newExpandedRows.delete(index);
    } else {
      newExpandedRows.add(index);
    }
    setExpandedRows(newExpandedRows);
  };

  const handleScroll = (direction) => {
    if (scrollContainerRef.current) {
      const scrollAmount = 300;
      const newScrollLeft = scrollContainerRef.current.scrollLeft + (direction === 'left' ? -scrollAmount : scrollAmount);
      scrollContainerRef.current.scrollTo({
        left: newScrollLeft,
        behavior: 'smooth'
      });
    }
  };

  const columns = [
    { key: 'name', label: 'Repository', width: 'w-64 min-w-[16rem]' },
    { key: 'description', label: 'Description', width: 'w-96 min-w-[24rem]' },
    { key: 'language', label: 'Language', width: 'w-32 min-w-[8rem]' },
    { key: 'stars', label: 'Stars', width: 'w-28 min-w-[7rem]' },
    { key: 'forks', label: 'Forks', width: 'w-28 min-w-[7rem]' },
    { key: 'owner', label: 'Owner', width: 'w-40 min-w-[10rem]' },
    { key: 'last_updated', label: 'Last Updated', width: 'w-44 min-w-[11rem]' }
  ];

  return (
    <div className="relative space-y-4">
      {/* Scroll Controls - Fixed at top */}
      <div className="flex justify-end mb-2">
        <div className="flex gap-2">
          <button
            onClick={() => handleScroll('left')}
            className="p-2 rounded-lg bg-white shadow-sm hover:bg-gray-50 border border-gray-200 text-gray-600"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          <button
            onClick={() => handleScroll('right')}
            className="p-2 rounded-lg bg-white shadow-sm hover:bg-gray-50 border border-gray-200 text-gray-600"
          >
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Table Container */}
      <div 
        ref={scrollContainerRef}
        className="overflow-x-auto overflow-y-visible scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100 rounded-lg shadow-sm"
      >
        <table className="min-w-full border-separate border-spacing-0">
          <thead className="bg-gray-50">
            <tr>
              <th className="sticky top-0 z-10 w-8 px-2 py-3 bg-gray-50 border-b border-gray-200">
                <div className="h-4"></div>
              </th>
              {columns.map(({ key, label, width }) => (
                <th
                  key={key}
                  className={`sticky top-0 z-10 ${width} px-4 py-3 bg-gray-50 border-b border-gray-200 text-left`}
                >
                  <button
                    onClick={() => onSort(key)}
                    className="group flex items-center gap-1 text-xs font-medium text-gray-500 uppercase tracking-wider hover:text-gray-700"
                  >
                    {label}
                    <span className="text-gray-400 group-hover:text-gray-600">
                      {sortConfig.key === key ? (
                        sortConfig.direction === 'asc' ? 
                          <ArrowUp className="h-4 w-4" /> : 
                          <ArrowDown className="h-4 w-4" />
                      ) : (
                        <ArrowUpDown className="h-4 w-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                      )}
                    </span>
                  </button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((repo, index) => (
              <React.Fragment key={index}>
                <tr className={`group transition-colors ${
                  expandedRows.has(index) 
                    ? 'bg-blue-50 hover:bg-blue-100' 
                    : 'hover:bg-gray-50'
                }`}>
                  <td className="pl-4 py-4 border-b border-gray-200">
                    <button
                      onClick={() => toggleRowExpansion(index)}
                      className="p-1 rounded-full hover:bg-white/50 transition-colors"
                    >
                      {expandedRows.has(index) ? 
                        <ChevronUp className="h-4 w-4 text-blue-500" /> : 
                        <ChevronDown className="h-4 w-4 text-gray-400 group-hover:text-gray-600" />
                      }
                    </button>
                  </td>
                  {/* Repository Name */}
                  <td className="px-4 py-4 border-b border-gray-200">
                    <a 
                      href={repo.url}
                      className="text-sm font-medium text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-1 group"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {repo.name}
                      <ExternalLink className="h-3 w-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </a>
                  </td>
                  {/* Description */}
                  <td className="px-4 py-4 border-b border-gray-200">
                    <p className="text-sm text-gray-500 truncate max-w-md">
                      {repo.description || 'No description available'}
                    </p>
                  </td>
                  {/* Language */}
                  <td className="px-4 py-4 border-b border-gray-200">
                    {repo.language && (
                      <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${getLanguageColor(repo.language)}`}>
                        <Code className="h-3 w-3 mr-1" />
                        {repo.language}
                      </span>
                    )}
                  </td>
                  {/* Stars */}
                  <td className="px-4 py-4 border-b border-gray-200">
                    <div className="flex items-center gap-1.5 text-sm text-gray-500">
                      <Star className="h-4 w-4 text-amber-500" />
                      {(repo.stars || 0).toLocaleString()}
                    </div>
                  </td>
                  {/* Forks */}
                  <td className="px-4 py-4 border-b border-gray-200">
                    <div className="flex items-center gap-1.5 text-sm text-gray-500">
                      <GitFork className="h-4 w-4 text-blue-500" />
                      {(repo.forks || 0).toLocaleString()}
                    </div>
                  </td>
                  {/* Owner */}
                  <td className="px-4 py-4 border-b border-gray-200">
                    <a
                      href={repo.owner?.profile_url}
                      className="flex items-center gap-1.5 text-sm text-gray-600 hover:text-gray-900 group"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <User className="h-4 w-4" />
                      <span>{repo.owner?.username}</span>
                      <ExternalLink className="h-3 w-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </a>
                  </td>
                  {/* Last Updated */}
                  <td className="px-4 py-4 border-b border-gray-200">
                    <div className="text-sm text-gray-500">
                      {formatDate(repo.last_updated)}
                    </div>
                  </td>
                </tr>
                {/* Expanded Row Content */}
                {expandedRows.has(index) && (
                  <tr className="bg-blue-50">
                    <td colSpan="9" className="px-6 py-4 border-b border-gray-200">
                      <div className="grid gap-4">
                        <div>
                          <h4 className="text-sm font-medium text-gray-900 mb-2">Topics</h4>
                          <div className="flex flex-wrap gap-2">
                            {repo.topics?.length ? (
                              repo.topics.map(topic => (
                                <span 
                                  key={topic}
                                  className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200"
                                >
                                  <Tag className="h-3 w-3 mr-1" />
                                  {topic}
                                </span>
                              ))
                            ) : (
                              <span className="text-sm text-gray-500">No topics available</span>
                            )}
                          </div>
                        </div>
                        {repo.description && (
                          <div>
                            <h4 className="text-sm font-medium text-gray-900 mb-2">Full Description</h4>
                            <p className="text-sm text-gray-600 bg-white/50 p-4 rounded-lg border border-gray-200">
                              {repo.description}
                            </p>
                          </div>
                        )}
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="mt-4 border-t border-gray-200">
        <Pagination {...pagination} />
      </div>
    </div>
  );
};

export default TableView;
```

## components/SortableRepoTable/CardView/index.jsx

```jsx
import React from 'react';
import { 
  Star, 
  GitFork, 
  Code, 
  User,
  Tag,
  ExternalLink,
  Calendar 
} from 'lucide-react';
import { formatDate, getLanguageColor } from '../utils/dataUtils';

const RepoCard = ({ repo }) => (
  <div className="border rounded-lg p-4 hover:shadow-md transition-shadow bg-white">
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <a 
          href={repo.url}
          className="text-lg font-semibold text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-2"
          target="_blank"
          rel="noopener noreferrer"
        >
          {repo.name}
          <ExternalLink className="h-4 w-4" />
        </a>
      </div>
    </div>

    {repo.language && (
      <div className="mt-2">
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getLanguageColor(repo.language)}`}>
          <Code className="h-3 w-3 mr-1" />
          {repo.language}
        </span>
      </div>
    )}

    <p className="mt-2 text-sm text-gray-600 line-clamp-2">
      {repo.description || 'No description available'}
    </p>

    <div className="mt-3 flex items-center gap-4 text-sm text-gray-600">
      <div className="flex items-center gap-1">
        <Star className="h-4 w-4 text-amber-500" />
        <span>{(repo.stars || 0).toLocaleString()}</span>
      </div>
      <div className="flex items-center gap-1">
        <GitFork className="h-4 w-4 text-blue-500" />
        <span>{(repo.forks || 0).toLocaleString()}</span>
      </div>
    </div>

    {repo.topics && repo.topics.length > 0 && (
      <div className="mt-3">
        <div className="flex flex-wrap gap-2">
          {repo.topics.map(topic => (
            <span 
              key={topic}
              className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-blue-50 text-blue-700"
            >
              <Tag className="h-3 w-3 mr-1" />
              {topic}
            </span>
          ))}
        </div>
      </div>
    )}

    {repo.owner && (
      <div className="mt-3 pt-3 border-t flex items-center justify-between">
        <a
          href={repo.owner.profile_url}
          className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
          target="_blank"
          rel="noopener noreferrer"
        >
          <User className="h-4 w-4" />
          {repo.owner.username}
        </a>
        <div className="flex items-center gap-1 text-sm text-gray-500">
          <Calendar className="h-4 w-4" />
          {formatDate(repo.last_updated)}
        </div>
      </div>
    )}
  </div>
);

const CardView = ({ data }) => (
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
    {data.map((repo, index) => (
      <RepoCard key={index} repo={repo} />
    ))}
  </div>
);

export default CardView;
```

## components/SortableRepoTable/utils/dataUtils.js

```javascript
export const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };
  
  export const getLanguageColor = (language) => {
    const colors = {
      'JavaScript': 'bg-yellow-100 text-yellow-800 border-yellow-300',
      'Python': 'bg-blue-100 text-blue-800 border-blue-300',
      'TypeScript': 'bg-blue-100 text-blue-800 border-blue-300',
      'Java': 'bg-red-100 text-red-800 border-red-300',
      'Go': 'bg-cyan-100 text-cyan-800 border-cyan-300',
      'Rust': 'bg-orange-100 text-orange-800 border-orange-300',
      'Ruby': 'bg-red-100 text-red-800 border-red-300',
      'C++': 'bg-purple-100 text-purple-800 border-purple-300',
      'PHP': 'bg-indigo-100 text-indigo-800 border-indigo-300'
    };
    return colors[language] || 'bg-gray-100 text-gray-800 border-gray-300';
  };
  
  export const filterData = (data, searchTerm) => {
    if (!searchTerm) return data;
    
    return data.filter(repo => {
      if (!repo) return false;
      
      const searchFields = [
        repo.name,
        repo.description,
        repo.language,
        ...(repo.topics || []),
        repo.owner?.username
      ].filter(Boolean);
  
      return searchFields.some(field => 
        field.toLowerCase().includes(searchTerm.toLowerCase())
      );
    });
  };
  
  export const sortData = (data, { key, direction }) => {
    return [...data].sort((a, b) => {
      if (!a || !b) return 0;
      
      if (key === 'last_updated') {
        const dateA = new Date(a[key] || 0);
        const dateB = new Date(b[key] || 0);
        return direction === 'asc' ? dateA - dateB : dateB - dateA;
      }
      
      if (key === 'owner') {
        const valueA = a.owner?.username ?? '';
        const valueB = b.owner?.username ?? '';
        return direction === 'asc'
          ? valueA.localeCompare(valueB)
          : valueB.localeCompare(valueA);
      }
      
      const valueA = a[key] ?? 0;
      const valueB = b[key] ?? 0;
      
      if (typeof valueA === 'number' && typeof valueB === 'number') {
        return direction === 'asc' ? valueA - valueB : valueB - valueA;
      }
      
      const stringA = String(valueA).toLowerCase();
      const stringB = String(valueB).toLowerCase();
      return direction === 'asc'
        ? stringA.localeCompare(stringB)
        : stringB.localeCompare(stringA);
    });
  };
```

## components/SortableRepoTable/StatsSection/index.jsx

```jsx
import React from 'react';
import { Star, GitFork, Code } from 'lucide-react';

const StatItem = ({ icon: Icon, label, value, color }) => (
  <div className="flex items-center gap-2 px-4 py-2">
    <Icon className={`h-4 w-4 ${color}`} />
    <div>
      <div className="text-xs text-gray-500">{label}</div>
      <div className="font-bold text-gray-900">{value}</div>
    </div>
  </div>
);

const StatsSection = ({ data }) => {
  const stats = {
    stars: data.reduce((acc, repo) => acc + (repo.stars || 0), 0),
    forks: data.reduce((acc, repo) => acc + (repo.forks || 0), 0),
    languages: new Set(data.map(repo => repo.language).filter(Boolean)).size
  };

  return (
    <div className="grid grid-cols-3 gap-2 p-4 border-b bg-gray-50">
      <StatItem
        icon={Star}
        label="Total Stars"
        value={stats.stars.toLocaleString()}
        color="text-amber-500"
      />
      <StatItem
        icon={GitFork}
        label="Total Forks"
        value={stats.forks.toLocaleString()}
        color="text-blue-500"
      />
      <StatItem
        icon={Code}
        label="Languages"
        value={stats.languages}
        color="text-green-500"
      />
    </div>
  );
};

export default StatsSection;
```

## components/SortableRepoTable/hooks/useRepoData.js

```javascript
import { useState, useMemo } from 'react';

export const useRepoData = (initialData) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: 'stars', direction: 'desc' });
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(50);

  const filteredAndSortedData = useMemo(() => {
    let filtered = [...initialData];
    
    if (searchTerm) {
      filtered = filtered.filter(repo => {
        const searchFields = [
          repo.name,
          repo.description,
          repo.language,
          ...(repo.topics || []),
          repo.owner?.username
        ].filter(Boolean);

        return searchFields.some(field => 
          field.toLowerCase().includes(searchTerm.toLowerCase())
        );
      });
    }

    return filtered.sort((a, b) => {
      const { key, direction } = sortConfig;
      
      if (key === 'last_updated') {
        const dateA = new Date(a[key] || 0);
        const dateB = new Date(b[key] || 0);
        return direction === 'asc' ? dateA - dateB : dateB - dateA;
      }
      
      if (key === 'owner') {
        const valueA = a.owner?.username ?? '';
        const valueB = b.owner?.username ?? '';
        return direction === 'asc'
          ? valueA.localeCompare(valueB)
          : valueB.localeCompare(valueA);
      }
      
      const valueA = a[key] ?? 0;
      const valueB = b[key] ?? 0;
      
      if (typeof valueA === 'number' && typeof valueB === 'number') {
        return direction === 'asc' ? valueA - valueB : valueB - valueA;
      }
      
      const stringA = String(valueA).toLowerCase();
      const stringB = String(valueB).toLowerCase();
      return direction === 'asc'
        ? stringA.localeCompare(stringB)
        : stringB.localeCompare(stringA);
    });
  }, [initialData, searchTerm, sortConfig]);

  const paginatedData = useMemo(() => {
    if (itemsPerPage === -1) return filteredAndSortedData;
    const startIndex = (currentPage - 1) * itemsPerPage;
    return filteredAndSortedData.slice(startIndex, startIndex + itemsPerPage);
  }, [filteredAndSortedData, currentPage, itemsPerPage]);

  const handleSort = (key) => {
    setSortConfig(prevConfig => ({
      key,
      direction: prevConfig.key === key && prevConfig.direction === 'asc' ? 'desc' : 'asc'
    }));
  };

  const pagination = {
    currentPage,
    totalPages: itemsPerPage === -1 ? 1 : Math.ceil(filteredAndSortedData.length / itemsPerPage),
    itemsPerPage,
    setCurrentPage,
    setItemsPerPage
  };

  return {
    filteredAndSortedData,
    paginatedData,
    searchTerm,
    setSearchTerm,
    sortConfig,
    handleSort,
    pagination,
    totalItems: filteredAndSortedData.length
  };
};
```

## components/SortableRepoTable/SortOptions/index.jsx

```jsx
import React from 'react';
import { ArrowUp, ArrowDown } from 'lucide-react';

const SortOptions = ({ sortConfig, onSort }) => {
  const sortButtons = [
    { key: 'stars', label: 'Stars' },
    { key: 'forks', label: 'Forks' },
    { key: 'name', label: 'Name' },
    { key: 'last_updated', label: 'Last Updated' }
  ];

  return (
    <div className="p-4 border-b bg-gray-50">
      <div className="flex flex-wrap gap-2 text-sm">
        <span className="text-gray-500">Sort by:</span>
        {sortButtons.map(({ key, label }) => (
          <button 
            key={key}
            onClick={() => onSort(key)}
            className={`px-2 py-1 rounded transition-colors ${
              sortConfig.key === key 
                ? 'bg-blue-100 text-blue-700' 
                : 'hover:bg-gray-200'
            }`}
          >
            <div className="flex items-center gap-1">
              {label}
              {sortConfig.key === key && (
                sortConfig.direction === 'asc' 
                  ? <ArrowUp className="h-3 w-3" />
                  : <ArrowDown className="h-3 w-3" />
              )}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default SortOptions;
```

## components/SortableRepoTable/ViewToggle/index.jsx

```jsx
import React from 'react';
import { LayoutGrid, LayoutList } from 'lucide-react';

const ViewToggle = ({ isTableView, onToggle }) => (
  <button
    onClick={onToggle}
    className="flex items-center gap-2 px-3 py-2 bg-white border rounded-lg hover:bg-gray-50 transition-colors"
  >
    {isTableView ? (
      <>
        <LayoutGrid className="h-4 w-4" />
        <span>Card View</span>
      </>
    ) : (
      <>
        <LayoutList className="h-4 w-4" />
        <span>Table View</span>
      </>
    )}
  </button>
);

export default ViewToggle;
```

## components/SortableRepoTable/SearchBar/index.jsx

```jsx
import React from 'react';
import { Search } from 'lucide-react';

const SearchBar = ({ searchTerm, onSearch }) => (
  <div className="relative w-full sm:w-96">
    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
    <input
      type="text"
      placeholder="Search repositories, topics, or languages..."
      className="w-full pl-9 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm"
      value={searchTerm}
      onChange={(e) => onSearch(e.target.value)}
    />
  </div>
);

export default SearchBar;
```

## components/SortableRepoTable/Pagination/index.jsx

```jsx
import React from 'react';
import { 
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight 
} from 'lucide-react';

const Pagination = ({ 
  currentPage, 
  totalPages, 
  setCurrentPage, 
  itemsPerPage, 
  setItemsPerPage,
  totalItems 
}) => {
  const handleItemsPerPageChange = (newValue) => {
    setItemsPerPage(Number(newValue));
    setCurrentPage(1);
  };

  const startItem = totalItems === 0 ? 0 : Math.min((currentPage - 1) * itemsPerPage + 1, totalItems);
  const endItem = Math.min(currentPage * itemsPerPage, totalItems);

  return (
    <div className="flex items-center justify-between px-4 py-3 border-t">
      <div className="flex items-center gap-2">
        <span className="text-sm text-gray-700">Show</span>
        <select
          value={itemsPerPage}
          onChange={(e) => handleItemsPerPageChange(e.target.value)}
          className="border rounded px-2 py-1 text-sm"
        >
          <option value={50}>50</option>
          <option value={100}>100</option>
          <option value={-1}>All</option>
        </select>
        <span className="text-sm text-gray-700">entries</span>
      </div>
      
      <div className="flex items-center gap-2">
        <span className="text-sm text-gray-700">
          {totalItems > 0 ? `Showing ${startItem} to ${endItem} of ${totalItems} entries` : 'No entries'}
        </span>
        
        <div className="flex gap-1">
          <button
            onClick={() => setCurrentPage(1)}
            disabled={currentPage === 1}
            className="p-1 rounded hover:bg-gray-100 disabled:opacity-50"
          >
            <ChevronsLeft className="h-4 w-4" />
          </button>
          <button
            onClick={() => setCurrentPage(currentPage - 1)}
            disabled={currentPage === 1}
            className="p-1 rounded hover:bg-gray-100 disabled:opacity-50"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          <button
            onClick={() => setCurrentPage(currentPage + 1)}
            disabled={currentPage === totalPages}
            className="p-1 rounded hover:bg-gray-100 disabled:opacity-50"
          >
            <ChevronRight className="h-4 w-4" />
          </button>
          <button
            onClick={() => setCurrentPage(totalPages)}
            disabled={currentPage === totalPages}
            className="p-1 rounded hover:bg-gray-100 disabled:opacity-50"
          >
            <ChevronsRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Pagination;
```

## data/repos.json

```json
[
  {
    "name": "QuivrHQ/MegaParse",
    "description": "File Parser optimised for LLM Ingestion with no loss \ud83e\udde0 Parse PDFs, Docx, PPTx in a format that is ideal for LLMs. ",
    "url": "https://github.com/QuivrHQ/MegaParse",
    "stars": 3939,
    "forks": 203,
    "language": "Python",
    "last_updated": "2024-12-11T04:06:59Z",
    "topics": [
      "docx",
      "llm",
      "parser",
      "pdf",
      "powerpoint"
    ],
    "owner": {
      "username": "QuivrHQ",
      "profile_url": "https://github.com/QuivrHQ"
    }
  },
  {
    "name": "imputnet/cobalt",
    "description": "best way to save what you love",
    "url": "https://github.com/imputnet/cobalt",
    "stars": 19185,
    "forks": 1551,
    "language": "Svelte",
    "last_updated": "2024-12-11T04:13:38Z",
    "topics": [
      "collaboration",
      "downloader",
      "javascript",
      "music",
      "reddit",
      "social-media",
      "soundcloud",
      "svelte",
      "tiktok",
      "twitter",
      "typescript",
      "video",
      "vimeo",
      "vk",
      "webapp",
      "youtube",
      "youtube-downloader"
    ],
    "owner": {
      "username": "imputnet",
      "profile_url": "https://github.com/imputnet"
    }
  },
  {
    "name": "aws-samples/dify-aws-tool",
    "description": null,
    "url": "https://github.com/aws-samples/dify-aws-tool",
    "stars": 38,
    "forks": 8,
    "language": "Python",
    "last_updated": "2024-12-10T10:29:28Z",
    "topics": [],
    "owner": {
      "username": "aws-samples",
      "profile_url": "https://github.com/aws-samples"
    }
  },
  {
    "name": "skills/github-pages",
    "description": "Create a site or blog from your GitHub repositories with GitHub Pages.",
    "url": "https://github.com/skills/github-pages",
    "stars": 1333,
    "forks": 701,
    "language": null,
    "last_updated": "2024-12-11T04:08:09Z",
    "topics": [
      "github-pages",
      "pages",
      "skills-course"
    ],
    "owner": {
      "username": "skills",
      "profile_url": "https://github.com/skills"
    }
  },
  {
    "name": "pydantic/pydantic-ai",
    "description": "Agent Framework / shim to use Pydantic with LLMs",
    "url": "https://github.com/pydantic/pydantic-ai",
    "stars": 3451,
    "forks": 198,
    "language": "Python",
    "last_updated": "2024-12-11T04:06:50Z",
    "topics": [
      "agent-framework",
      "llms",
      "pydantic",
      "python"
    ],
    "owner": {
      "username": "pydantic",
      "profile_url": "https://github.com/pydantic"
    }
  },
  {
    "name": "2-fly-4-ai/V0-system-prompt",
    "description": null,
    "url": "https://github.com/2-fly-4-ai/V0-system-prompt",
    "stars": 1446,
    "forks": 427,
    "language": null,
    "last_updated": "2024-12-11T03:06:34Z",
    "topics": [],
    "owner": {
      "username": "2-fly-4-ai",
      "profile_url": "https://github.com/2-fly-4-ai"
    }
  },
  {
    "name": "huggingface/smol-course",
    "description": "A course on aligning smol models.",
    "url": "https://github.com/huggingface/smol-course",
    "stars": 2940,
    "forks": 809,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T04:09:29Z",
    "topics": [],
    "owner": {
      "username": "huggingface",
      "profile_url": "https://github.com/huggingface"
    }
  },
  {
    "name": "BerriAI/litellm",
    "description": "Python SDK, Proxy Server (LLM Gateway) to call 100+ LLM APIs in OpenAI format - [Bedrock, Azure, OpenAI, VertexAI, Cohere, Anthropic, Sagemaker, HuggingFace, Replicate, Groq]",
    "url": "https://github.com/BerriAI/litellm",
    "stars": 14988,
    "forks": 1759,
    "language": "Python",
    "last_updated": "2024-12-11T03:40:10Z",
    "topics": [
      "ai-gateway",
      "anthropic",
      "azure-openai",
      "bedrock",
      "gateway",
      "langchain",
      "llm",
      "llm-gateway",
      "llmops",
      "openai",
      "openai-proxy",
      "vertex-ai"
    ],
    "owner": {
      "username": "BerriAI",
      "profile_url": "https://github.com/BerriAI"
    }
  },
  {
    "name": "minhpq331/devops-training",
    "description": "Devops Training materials",
    "url": "https://github.com/minhpq331/devops-training",
    "stars": 145,
    "forks": 56,
    "language": null,
    "last_updated": "2024-12-10T18:01:34Z",
    "topics": [],
    "owner": {
      "username": "minhpq331",
      "profile_url": "https://github.com/minhpq331"
    }
  },
  {
    "name": "sdmg15/Best-websites-a-programmer-should-visit",
    "description": ":link: Some useful websites for programmers.",
    "url": "https://github.com/sdmg15/Best-websites-a-programmer-should-visit",
    "stars": 64043,
    "forks": 7918,
    "language": null,
    "last_updated": "2024-12-11T04:12:09Z",
    "topics": [
      "books",
      "cs",
      "hacktoberfest",
      "links",
      "programmer",
      "sites"
    ],
    "owner": {
      "username": "sdmg15",
      "profile_url": "https://github.com/sdmg15"
    }
  },
  {
    "name": "anthropics/prompt-eng-interactive-tutorial",
    "description": "Anthropic's Interactive Prompt Engineering Tutorial",
    "url": "https://github.com/anthropics/prompt-eng-interactive-tutorial",
    "stars": 1877,
    "forks": 198,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T04:12:21Z",
    "topics": [],
    "owner": {
      "username": "anthropics",
      "profile_url": "https://github.com/anthropics"
    }
  },
  {
    "name": "keephq/keep",
    "description": "The open-source alert management and AIOps platform",
    "url": "https://github.com/keephq/keep",
    "stars": 8504,
    "forks": 777,
    "language": "Python",
    "last_updated": "2024-12-11T03:55:48Z",
    "topics": [
      "aiops",
      "alarm",
      "alarms",
      "alerting",
      "alerts",
      "monitoring",
      "monitoring-tool",
      "python",
      "python3",
      "workflow-automation"
    ],
    "owner": {
      "username": "keephq",
      "profile_url": "https://github.com/keephq"
    }
  },
  {
    "name": "myhhub/stock",
    "description": "stock\u80a1\u7968.\u83b7\u53d6\u80a1\u7968\u6570\u636e,\u8ba1\u7b97\u80a1\u7968\u6307\u6807,\u8bc6\u522b\u80a1\u7968\u5f62\u6001,\u7efc\u5408\u9009\u80a1,\u9009\u80a1\u7b56\u7565,\u80a1\u7968\u9a8c\u8bc1\u56de\u6d4b,\u80a1\u7968\u81ea\u52a8\u4ea4\u6613,\u652f\u6301PC\u53ca\u79fb\u52a8\u8bbe\u5907\u3002",
    "url": "https://github.com/myhhub/stock",
    "stars": 6002,
    "forks": 1078,
    "language": "Python",
    "last_updated": "2024-12-11T03:42:48Z",
    "topics": [
      "backtest",
      "backtesting",
      "broker-trading-platform",
      "quantitative",
      "quantitative-finance",
      "stock",
      "stocks",
      "strategies",
      "strategy"
    ],
    "owner": {
      "username": "myhhub",
      "profile_url": "https://github.com/myhhub"
    }
  },
  {
    "name": "lobehub/lobe-chat",
    "description": "\ud83e\udd2f Lobe Chat - an open-source, modern-design AI chat framework. Supports Multi AI Providers( OpenAI / Claude 3 / Gemini / Ollama / Qwen /  DeepSeek), Knowledge Base (file upload / knowledge management / RAG ), Multi-Modals (Vision/TTS/Plugins/Artifacts). One-click FREE deployment of your private ChatGPT/ Claude application.",
    "url": "https://github.com/lobehub/lobe-chat",
    "stars": 48622,
    "forks": 10550,
    "language": "TypeScript",
    "last_updated": "2024-12-11T04:12:18Z",
    "topics": [
      "ai",
      "artifacts",
      "azure-openai-api",
      "chat",
      "chatglm",
      "chatgpt",
      "claude",
      "dalle-3",
      "function-calling",
      "gemini",
      "gpt",
      "gpt-4",
      "gpt-4-vision",
      "knowledge-base",
      "nextjs",
      "ollama",
      "openai",
      "qwen2",
      "rag",
      "tts"
    ],
    "owner": {
      "username": "lobehub",
      "profile_url": "https://github.com/lobehub"
    }
  },
  {
    "name": "SeekStorm/SeekStorm",
    "description": "SeekStorm - sub-millisecond full-text search library & multi-tenancy server in Rust",
    "url": "https://github.com/SeekStorm/SeekStorm",
    "stars": 1259,
    "forks": 30,
    "language": "Rust",
    "last_updated": "2024-12-11T03:33:39Z",
    "topics": [
      "apache2",
      "bm25",
      "enterprise-search",
      "faceting",
      "full-text-search",
      "geosearch",
      "index",
      "lexical-search",
      "okapi-bm25",
      "query",
      "realtime",
      "rust",
      "saas",
      "search",
      "search-engine",
      "search-server",
      "search-service",
      "sparse-retrieval"
    ],
    "owner": {
      "username": "SeekStorm",
      "profile_url": "https://github.com/SeekStorm"
    }
  },
  {
    "name": "andrewyng/aisuite",
    "description": "Simple, unified interface to multiple Generative AI providers ",
    "url": "https://github.com/andrewyng/aisuite",
    "stars": 7594,
    "forks": 662,
    "language": "Python",
    "last_updated": "2024-12-11T04:04:19Z",
    "topics": [],
    "owner": {
      "username": "andrewyng",
      "profile_url": "https://github.com/andrewyng"
    }
  },
  {
    "name": "QwenLM/Qwen2.5",
    "description": "Qwen2.5 is the large language model series developed by Qwen team, Alibaba Cloud.",
    "url": "https://github.com/QwenLM/Qwen2.5",
    "stars": 10776,
    "forks": 664,
    "language": "Shell",
    "last_updated": "2024-12-11T03:14:20Z",
    "topics": [],
    "owner": {
      "username": "QwenLM",
      "profile_url": "https://github.com/QwenLM"
    }
  },
  {
    "name": "allenai/open-instruct",
    "description": null,
    "url": "https://github.com/allenai/open-instruct",
    "stars": 2085,
    "forks": 235,
    "language": "Python",
    "last_updated": "2024-12-11T03:46:25Z",
    "topics": [],
    "owner": {
      "username": "allenai",
      "profile_url": "https://github.com/allenai"
    }
  },
  {
    "name": "jianchang512/pyvideotrans",
    "description": "Translate the video from one language to another and add dubbing.         \u5c06\u89c6\u9891\u4ece\u4e00\u79cd\u8bed\u8a00\u7ffb\u8bd1\u4e3a\u53e6\u4e00\u79cd\u8bed\u8a00\uff0c\u540c\u65f6\u652f\u6301\u8bed\u97f3\u8bc6\u522b\u8f6c\u5f55\u3001\u8bed\u97f3\u5408\u6210\u3001\u5b57\u5e55\u7ffb\u8bd1\u3002",
    "url": "https://github.com/jianchang512/pyvideotrans",
    "stars": 11020,
    "forks": 1235,
    "language": "Python",
    "last_updated": "2024-12-11T02:58:41Z",
    "topics": [
      "speech-to-text",
      "text-to-speech",
      "video-transition"
    ],
    "owner": {
      "username": "jianchang512",
      "profile_url": "https://github.com/jianchang512"
    }
  },
  {
    "name": "Lightricks/LTX-Video",
    "description": "Official repository for LTX-Video",
    "url": "https://github.com/Lightricks/LTX-Video",
    "stars": 1849,
    "forks": 123,
    "language": "Python",
    "last_updated": "2024-12-11T03:53:02Z",
    "topics": [
      "diffusion-models",
      "dit",
      "image-to-video",
      "image-to-video-generation",
      "text-to-video",
      "text-to-video-generation"
    ],
    "owner": {
      "username": "Lightricks",
      "profile_url": "https://github.com/Lightricks"
    }
  },
  {
    "name": "yangchris11/samurai",
    "description": "Official repository of \"SAMURAI: Adapting Segment Anything Model for Zero-Shot Visual Tracking with Motion-Aware Memory\"",
    "url": "https://github.com/yangchris11/samurai",
    "stars": 5808,
    "forks": 339,
    "language": "Python",
    "last_updated": "2024-12-11T03:44:44Z",
    "topics": [],
    "owner": {
      "username": "yangchris11",
      "profile_url": "https://github.com/yangchris11"
    }
  },
  {
    "name": "TheBlewish/Automated-AI-Web-Researcher-Ollama",
    "description": "A python program that turns an LLM, running on Ollama, into an automated researcher, which will with a single query determine focus areas to investigate, do websearches and scrape content from various relevant websites and do research for you all on its own! And more, not limited to but including saving the findings for you!",
    "url": "https://github.com/TheBlewish/Automated-AI-Web-Researcher-Ollama",
    "stars": 2330,
    "forks": 232,
    "language": "Python",
    "last_updated": "2024-12-10T21:58:03Z",
    "topics": [],
    "owner": {
      "username": "TheBlewish",
      "profile_url": "https://github.com/TheBlewish"
    }
  },
  {
    "name": "mediar-ai/screenpipe",
    "description": "one API to get all user desktop data  (local, cross platform, 24/7, screen, voice, keyboard, mouse, camera recording). sandboxed js plugin system. keyboard and mouse control",
    "url": "https://github.com/mediar-ai/screenpipe",
    "stars": 10845,
    "forks": 672,
    "language": "TypeScript",
    "last_updated": "2024-12-11T04:12:27Z",
    "topics": [
      "agents",
      "agi",
      "ai",
      "computer-vision",
      "llm",
      "machine-learning",
      "ml",
      "multimodal",
      "vision"
    ],
    "owner": {
      "username": "mediar-ai",
      "profile_url": "https://github.com/mediar-ai"
    }
  },
  {
    "name": "arkohut/pensieve",
    "description": "A passive recording project allows you to have complete control over your data. Automatically take screenshots of all your screens, index them, and save them locally.",
    "url": "https://github.com/arkohut/pensieve",
    "stars": 1081,
    "forks": 47,
    "language": "Python",
    "last_updated": "2024-12-11T02:59:02Z",
    "topics": [],
    "owner": {
      "username": "arkohut",
      "profile_url": "https://github.com/arkohut"
    }
  },
  {
    "name": "danielmiessler/SecLists",
    "description": "SecLists is the security tester's companion. It's a collection of multiple types of lists used during security assessments, collected in one place. List types include usernames, passwords, URLs, sensitive data patterns, fuzzing payloads, web shells, and many more.",
    "url": "https://github.com/danielmiessler/SecLists",
    "stars": 59158,
    "forks": 23994,
    "language": "PHP",
    "last_updated": "2024-12-11T03:14:29Z",
    "topics": [],
    "owner": {
      "username": "danielmiessler",
      "profile_url": "https://github.com/danielmiessler"
    }
  },
  {
    "name": "DataExpert-io/data-engineer-handbook",
    "description": "This is a repo with links to everything you'd ever want to learn about data engineering",
    "url": "https://github.com/DataExpert-io/data-engineer-handbook",
    "stars": 22783,
    "forks": 3849,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T03:43:52Z",
    "topics": [
      "apachespark",
      "awesome",
      "bigdata",
      "data",
      "dataengineering",
      "sql"
    ],
    "owner": {
      "username": "DataExpert-io",
      "profile_url": "https://github.com/DataExpert-io"
    }
  },
  {
    "name": "gregpr07/browser-use",
    "description": "Make websites accessible for AI agents",
    "url": "https://github.com/gregpr07/browser-use",
    "stars": 2993,
    "forks": 244,
    "language": "Python",
    "last_updated": "2024-12-11T03:54:26Z",
    "topics": [
      "agent",
      "anthropic",
      "automation",
      "browser",
      "llm",
      "openai",
      "python",
      "python-library",
      "scraping",
      "web"
    ],
    "owner": {
      "username": "gregpr07",
      "profile_url": "https://github.com/gregpr07"
    }
  },
  {
    "name": "NVIDIA/NeMo",
    "description": "A scalable generative AI framework built for researchers and developers working on Large Language Models, Multimodal, and Speech AI (Automatic Speech Recognition and Text-to-Speech)",
    "url": "https://github.com/NVIDIA/NeMo",
    "stars": 12404,
    "forks": 2562,
    "language": "Python",
    "last_updated": "2024-12-11T03:44:16Z",
    "topics": [
      "asr",
      "deeplearning",
      "generative-ai",
      "large-language-models",
      "machine-translation",
      "multimodal",
      "neural-networks",
      "speaker-diariazation",
      "speaker-recognition",
      "speech-synthesis",
      "speech-translation",
      "tts"
    ],
    "owner": {
      "username": "NVIDIA",
      "profile_url": "https://github.com/NVIDIA"
    }
  },
  {
    "name": "SLAM-Handbook-contributors/slam-handbook-public-release",
    "description": "Release repo for our SLAM Handbook",
    "url": "https://github.com/SLAM-Handbook-contributors/slam-handbook-public-release",
    "stars": 2028,
    "forks": 88,
    "language": null,
    "last_updated": "2024-12-10T23:24:40Z",
    "topics": [],
    "owner": {
      "username": "SLAM-Handbook-contributors",
      "profile_url": "https://github.com/SLAM-Handbook-contributors"
    }
  },
  {
    "name": "microsoft/TinyTroupe",
    "description": "LLM-powered multiagent persona simulation for imagination enhancement and business insights.",
    "url": "https://github.com/microsoft/TinyTroupe",
    "stars": 4800,
    "forks": 367,
    "language": "Python",
    "last_updated": "2024-12-11T03:51:32Z",
    "topics": [],
    "owner": {
      "username": "microsoft",
      "profile_url": "https://github.com/microsoft"
    }
  },
  {
    "name": "Huanshere/VideoLingo",
    "description": "Netflix-level subtitle cutting, translation, alignment, and even dubbing - one-click fully automated AI video subtitle team | Netflix\u7ea7\u5b57\u5e55\u5207\u5272\u3001\u7ffb\u8bd1\u3001\u5bf9\u9f50\u3001\u751a\u81f3\u52a0\u4e0a\u914d\u97f3\uff0c\u4e00\u952e\u5168\u81ea\u52a8\u89c6\u9891\u642c\u8fd0AI\u5b57\u5e55\u7ec4",
    "url": "https://github.com/Huanshere/VideoLingo",
    "stars": 8215,
    "forks": 791,
    "language": "Python",
    "last_updated": "2024-12-11T03:42:33Z",
    "topics": [
      "ai-translation",
      "dubbing",
      "localization",
      "video-translation",
      "voice-cloning"
    ],
    "owner": {
      "username": "Huanshere",
      "profile_url": "https://github.com/Huanshere"
    }
  },
  {
    "name": "google-gemini/cookbook",
    "description": "Examples and guides for using the Gemini API",
    "url": "https://github.com/google-gemini/cookbook",
    "stars": 5538,
    "forks": 858,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T02:15:57Z",
    "topics": [
      "gemini",
      "gemini-api"
    ],
    "owner": {
      "username": "google-gemini",
      "profile_url": "https://github.com/google-gemini"
    }
  },
  {
    "name": "svcvit/Awesome-Dify-Workflow",
    "description": "\u5206\u4eab\u4e00\u4e9b\u597d\u7528\u7684 Dify DSL \u5de5\u4f5c\u6d41\u7a0b\uff0c\u81ea\u7528\u3001\u5b66\u4e60\u4e24\u76f8\u5b9c\u3002 Sharing some Dify workflows.",
    "url": "https://github.com/svcvit/Awesome-Dify-Workflow",
    "stars": 1734,
    "forks": 176,
    "language": null,
    "last_updated": "2024-12-11T04:12:26Z",
    "topics": [],
    "owner": {
      "username": "svcvit",
      "profile_url": "https://github.com/svcvit"
    }
  },
  {
    "name": "weaveworks/awesome-gitops",
    "description": "A curated list for awesome GitOps resources",
    "url": "https://github.com/weaveworks/awesome-gitops",
    "stars": 1538,
    "forks": 125,
    "language": null,
    "last_updated": "2024-12-07T16:26:56Z",
    "topics": [
      "awesome",
      "awesome-list"
    ],
    "owner": {
      "username": "weaveworks",
      "profile_url": "https://github.com/weaveworks"
    }
  },
  {
    "name": "sottlmarek/DevSecOps",
    "description": "Ultimate DevSecOps library",
    "url": "https://github.com/sottlmarek/DevSecOps",
    "stars": 5804,
    "forks": 1017,
    "language": null,
    "last_updated": "2024-12-10T16:07:43Z",
    "topics": [
      "automation",
      "awesome",
      "awesome-list",
      "aws",
      "azure",
      "ci-cd",
      "cloud",
      "containers",
      "cybersecurity",
      "devops",
      "devsecops",
      "docker",
      "gcp",
      "k8s",
      "kubernetes",
      "security",
      "serverless",
      "ssdlc",
      "tool"
    ],
    "owner": {
      "username": "sottlmarek",
      "profile_url": "https://github.com/sottlmarek"
    }
  },
  {
    "name": "intelligencedev/eternal",
    "description": "Eternal is an experimental platform for machine learning models and workflows.",
    "url": "https://github.com/intelligencedev/eternal",
    "stars": 68,
    "forks": 4,
    "language": "Go",
    "last_updated": "2024-11-19T04:36:22Z",
    "topics": [
      "ai",
      "claude-ai",
      "comfyui",
      "gemini-pro",
      "go",
      "gpt-4",
      "htmx",
      "inference-api",
      "llamacpp",
      "ml",
      "stable-diffusion"
    ],
    "owner": {
      "username": "intelligencedev",
      "profile_url": "https://github.com/intelligencedev"
    }
  },
  {
    "name": "QwenLM/Qwen2.5-Coder",
    "description": "Qwen2.5-Coder is the code version of Qwen2.5, the large language model series developed by Qwen team, Alibaba Cloud.",
    "url": "https://github.com/QwenLM/Qwen2.5-Coder",
    "stars": 3332,
    "forks": 225,
    "language": "Python",
    "last_updated": "2024-12-11T03:58:58Z",
    "topics": [],
    "owner": {
      "username": "QwenLM",
      "profile_url": "https://github.com/QwenLM"
    }
  },
  {
    "name": "PrefectHQ/prefect",
    "description": "Prefect is a workflow orchestration framework for building resilient data pipelines in Python.",
    "url": "https://github.com/PrefectHQ/prefect",
    "stars": 17743,
    "forks": 1658,
    "language": "Python",
    "last_updated": "2024-12-11T02:57:57Z",
    "topics": [
      "automation",
      "data",
      "data-engineering",
      "data-ops",
      "data-science",
      "infrastructure",
      "ml-ops",
      "observability",
      "orchestration",
      "pipeline",
      "prefect",
      "python",
      "workflow",
      "workflow-engine"
    ],
    "owner": {
      "username": "PrefectHQ",
      "profile_url": "https://github.com/PrefectHQ"
    }
  },
  {
    "name": "asweigart/pyautogui",
    "description": "A cross-platform GUI automation Python module for human beings. Used to programmatically control the mouse & keyboard.",
    "url": "https://github.com/asweigart/pyautogui",
    "stars": 10556,
    "forks": 1275,
    "language": "Python",
    "last_updated": "2024-12-10T23:05:22Z",
    "topics": [],
    "owner": {
      "username": "asweigart",
      "profile_url": "https://github.com/asweigart"
    }
  },
  {
    "name": "iterative/datachain",
    "description": "ETL, Analytics, Versioning for Unstructured Data",
    "url": "https://github.com/iterative/datachain",
    "stars": 2066,
    "forks": 94,
    "language": "Python",
    "last_updated": "2024-12-11T03:57:43Z",
    "topics": [
      "ai",
      "cv",
      "data-analytics",
      "data-wrangling",
      "embeddings",
      "llm",
      "llm-eval",
      "machine-learning",
      "mlops",
      "multimodal"
    ],
    "owner": {
      "username": "iterative",
      "profile_url": "https://github.com/iterative"
    }
  },
  {
    "name": "EdwardDali/erag",
    "description": "an AI interaction tool with RAG hybrid search, conversation context, web content processing and structured data analysis with LLM / GPT",
    "url": "https://github.com/EdwardDali/erag",
    "stars": 130,
    "forks": 15,
    "language": "Python",
    "last_updated": "2024-12-07T19:35:33Z",
    "topics": [],
    "owner": {
      "username": "EdwardDali",
      "profile_url": "https://github.com/EdwardDali"
    }
  },
  {
    "name": "DS4SD/docling",
    "description": "Get your documents ready for gen AI",
    "url": "https://github.com/DS4SD/docling",
    "stars": 13098,
    "forks": 648,
    "language": "Python",
    "last_updated": "2024-12-11T04:08:55Z",
    "topics": [
      "ai",
      "convert",
      "document-parser",
      "document-parsing",
      "documents",
      "docx",
      "html",
      "markdown",
      "pdf",
      "pdf-converter",
      "pdf-to-json",
      "pdf-to-text",
      "pptx",
      "tables",
      "xlsx"
    ],
    "owner": {
      "username": "DS4SD",
      "profile_url": "https://github.com/DS4SD"
    }
  },
  {
    "name": "timescale/pgai",
    "description": "A suite of tools to develop RAG, semantic search, and other AI applications more easily with PostgreSQL",
    "url": "https://github.com/timescale/pgai",
    "stars": 2392,
    "forks": 118,
    "language": "PLpgSQL",
    "last_updated": "2024-12-11T03:34:29Z",
    "topics": [
      "ai",
      "llm",
      "postgresql",
      "rag"
    ],
    "owner": {
      "username": "timescale",
      "profile_url": "https://github.com/timescale"
    }
  },
  {
    "name": "anthropics/courses",
    "description": "Anthropic's educational courses",
    "url": "https://github.com/anthropics/courses",
    "stars": 8323,
    "forks": 648,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T02:52:02Z",
    "topics": [],
    "owner": {
      "username": "anthropics",
      "profile_url": "https://github.com/anthropics"
    }
  },
  {
    "name": "Integuru-AI/Integuru",
    "description": "The first AI agent that builds third-party integrations through reverse engineering platforms' internal APIs.",
    "url": "https://github.com/Integuru-AI/Integuru",
    "stars": 3017,
    "forks": 210,
    "language": "Python",
    "last_updated": "2024-12-10T19:59:03Z",
    "topics": [
      "agent",
      "agents",
      "ai-agent",
      "ai-agents",
      "api",
      "apis",
      "automation",
      "integration",
      "integrations",
      "llm",
      "open-source",
      "openapi",
      "robotic-process-automation",
      "rpa",
      "unofficial-api",
      "unofficial-apis"
    ],
    "owner": {
      "username": "Integuru-AI",
      "profile_url": "https://github.com/Integuru-AI"
    }
  },
  {
    "name": "AmitXShukla/RPA",
    "description": "AI Bots - Robotic Processing automation Python and Julia lang scripts to support automating repetitive tasks",
    "url": "https://github.com/AmitXShukla/RPA",
    "stars": 73,
    "forks": 28,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-01T05:39:30Z",
    "topics": [],
    "owner": {
      "username": "AmitXShukla",
      "profile_url": "https://github.com/AmitXShukla"
    }
  },
  {
    "name": "yigitkonur/swift-ocr-llm-powered-pdf-to-markdown",
    "description": "An open-source OCR API that leverages OpenAI's powerful language models with optimized performance techniques like parallel processing and batching to deliver high-quality text extraction from complex PDF documents. Ideal for businesses seeking efficient document digitization and data extraction solutions.",
    "url": "https://github.com/yigitkonur/swift-ocr-llm-powered-pdf-to-markdown",
    "stars": 741,
    "forks": 54,
    "language": "Python",
    "last_updated": "2024-12-11T04:00:02Z",
    "topics": [],
    "owner": {
      "username": "yigitkonur",
      "profile_url": "https://github.com/yigitkonur"
    }
  },
  {
    "name": "dgtlmoon/changedetection.io",
    "description": "The best and simplest free open source web page change detection, website watcher,  restock monitor and notification service. Restock Monitor, change detection. Designed for simplicity - Simply monitor which websites had a text change for free. Free Open source web page change detection, Website defacement monitoring, Price change notification",
    "url": "https://github.com/dgtlmoon/changedetection.io",
    "stars": 20319,
    "forks": 1102,
    "language": "Python",
    "last_updated": "2024-12-11T03:41:48Z",
    "topics": [
      "back-in-stock",
      "change-alert",
      "change-detection",
      "change-monitoring",
      "changedetection",
      "monitoring",
      "notifications",
      "restock-monitor",
      "self-hosted",
      "url-monitor",
      "web-scraping",
      "website-change-detection",
      "website-change-detector",
      "website-change-monitor",
      "website-change-notification",
      "website-change-tracker",
      "website-defacement-monitoring",
      "website-monitor",
      "website-monitoring",
      "website-watcher"
    ],
    "owner": {
      "username": "dgtlmoon",
      "profile_url": "https://github.com/dgtlmoon"
    }
  },
  {
    "name": "paperless-ngx/paperless-ngx",
    "description": "A community-supported supercharged version of paperless: scan, index and archive all your physical documents",
    "url": "https://github.com/paperless-ngx/paperless-ngx",
    "stars": 22833,
    "forks": 1274,
    "language": "Python",
    "last_updated": "2024-12-11T03:34:23Z",
    "topics": [
      "angular",
      "archiving",
      "django",
      "dms",
      "document-management",
      "document-management-system",
      "machine-learning",
      "ocr",
      "optical-character-recognition",
      "pdf"
    ],
    "owner": {
      "username": "paperless-ngx",
      "profile_url": "https://github.com/paperless-ngx"
    }
  },
  {
    "name": "airtai/faststream",
    "description": "FastStream is a powerful and easy-to-use Python framework for building asynchronous services interacting with event streams such as Apache Kafka, RabbitMQ, NATS and Redis.",
    "url": "https://github.com/airtai/faststream",
    "stars": 3227,
    "forks": 164,
    "language": "Python",
    "last_updated": "2024-12-10T22:27:46Z",
    "topics": [
      "asyncapi",
      "asyncio",
      "distributed-systems",
      "fastkafka",
      "faststream",
      "kafka",
      "nats",
      "propan",
      "python",
      "rabbitmq",
      "redis",
      "stream-processing"
    ],
    "owner": {
      "username": "airtai",
      "profile_url": "https://github.com/airtai"
    }
  },
  {
    "name": "VikParuchuri/tabled",
    "description": "Detect and extract tables to markdown and csv",
    "url": "https://github.com/VikParuchuri/tabled",
    "stars": 679,
    "forks": 38,
    "language": "Python",
    "last_updated": "2024-12-09T17:39:48Z",
    "topics": [
      "deep-learning",
      "ocr",
      "tables"
    ],
    "owner": {
      "username": "VikParuchuri",
      "profile_url": "https://github.com/VikParuchuri"
    }
  },
  {
    "name": "ServiceNow/TapeAgents",
    "description": "TapeAgents is a framework that facilitates all stages of the LLM Agent development lifecycle",
    "url": "https://github.com/ServiceNow/TapeAgents",
    "stars": 152,
    "forks": 14,
    "language": "Python",
    "last_updated": "2024-12-11T01:58:43Z",
    "topics": [
      "agentic",
      "agents",
      "ai-agents",
      "finetuning",
      "llm-agent",
      "multi-agent",
      "multi-agent-simulation",
      "prompt-tuning"
    ],
    "owner": {
      "username": "ServiceNow",
      "profile_url": "https://github.com/ServiceNow"
    }
  },
  {
    "name": "open-mmlab/Amphion",
    "description": "Amphion (/\u00e6m\u02c8fa\u026a\u0259n/) is a toolkit for Audio, Music, and Speech Generation. Its purpose is to support reproducible research and help junior researchers and engineers get started in the field of audio, music, and speech generation research and development.",
    "url": "https://github.com/open-mmlab/Amphion",
    "stars": 7896,
    "forks": 596,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T04:06:42Z",
    "topics": [
      "audio-generation",
      "audio-synthesis",
      "audioldm",
      "audit",
      "emilia",
      "fastspeech2",
      "maskgct",
      "music-generation",
      "naturalspeech2",
      "singing-voice-conversion",
      "speech-synthesis",
      "text-to-audio",
      "text-to-speech",
      "vall-e",
      "vits",
      "vocoder",
      "voice-conversion"
    ],
    "owner": {
      "username": "open-mmlab",
      "profile_url": "https://github.com/open-mmlab"
    }
  },
  {
    "name": "THUDM/GLM-4-Voice",
    "description": "GLM-4-Voice | \u7aef\u5230\u7aef\u4e2d\u82f1\u8bed\u97f3\u5bf9\u8bdd\u6a21\u578b",
    "url": "https://github.com/THUDM/GLM-4-Voice",
    "stars": 2427,
    "forks": 196,
    "language": "Python",
    "last_updated": "2024-12-11T04:07:14Z",
    "topics": [],
    "owner": {
      "username": "THUDM",
      "profile_url": "https://github.com/THUDM"
    }
  },
  {
    "name": "Skyvern-AI/skyvern",
    "description": "Automate browser-based workflows with LLMs and Computer Vision",
    "url": "https://github.com/Skyvern-AI/skyvern",
    "stars": 11016,
    "forks": 765,
    "language": "Python",
    "last_updated": "2024-12-11T03:45:28Z",
    "topics": [
      "api",
      "automation",
      "browser",
      "browser-automation",
      "computer",
      "gpt",
      "llm",
      "playwright",
      "python",
      "rpa",
      "vision",
      "workflow"
    ],
    "owner": {
      "username": "Skyvern-AI",
      "profile_url": "https://github.com/Skyvern-AI"
    }
  },
  {
    "name": "donnemartin/awesome-aws",
    "description": "A curated list of awesome Amazon Web Services (AWS) libraries, open source repos, guides, blogs, and other resources.  Featuring the Fiery Meter of AWSome.",
    "url": "https://github.com/donnemartin/awesome-aws",
    "stars": 12540,
    "forks": 1697,
    "language": "Python",
    "last_updated": "2024-12-10T22:31:29Z",
    "topics": [
      "aws",
      "aws-cli",
      "aws-sdk",
      "cloud",
      "cloud-management",
      "cloudformation",
      "cloudwatch",
      "dynamodb",
      "ec2",
      "ecs",
      "elasticsearch",
      "iam",
      "kinesis",
      "lambda",
      "machine-learning",
      "rds",
      "redshift",
      "route53",
      "s3",
      "serverless"
    ],
    "owner": {
      "username": "donnemartin",
      "profile_url": "https://github.com/donnemartin"
    }
  },
  {
    "name": "awslabs/aws-well-architected-labs",
    "description": "Hands on labs and code to help you learn, measure, and build using architectural best practices.",
    "url": "https://github.com/awslabs/aws-well-architected-labs",
    "stars": 2010,
    "forks": 1055,
    "language": "Python",
    "last_updated": "2024-12-08T22:47:43Z",
    "topics": [
      "aws",
      "cost",
      "lab",
      "reliability",
      "reliability-engineering",
      "resilience",
      "resiliency",
      "security",
      "well-architected",
      "wellarchitected"
    ],
    "owner": {
      "username": "awslabs",
      "profile_url": "https://github.com/awslabs"
    }
  },
  {
    "name": "mailtoharshit/awesome-aws-well-architected",
    "description": "Curated List of all AWS Well-Architected Resources",
    "url": "https://github.com/mailtoharshit/awesome-aws-well-architected",
    "stars": 22,
    "forks": 7,
    "language": null,
    "last_updated": "2024-12-04T00:40:52Z",
    "topics": [],
    "owner": {
      "username": "mailtoharshit",
      "profile_url": "https://github.com/mailtoharshit"
    }
  },
  {
    "name": "ranaroussi/yfinance",
    "description": "Download market data from Yahoo! Finance's API",
    "url": "https://github.com/ranaroussi/yfinance",
    "stars": 15072,
    "forks": 2468,
    "language": "Python",
    "last_updated": "2024-12-11T03:57:11Z",
    "topics": [
      "financial-data",
      "fix-yahoo-finance",
      "market-data",
      "pandas",
      "python",
      "stock-data",
      "yahoo-finance",
      "yahoo-finance-api"
    ],
    "owner": {
      "username": "ranaroussi",
      "profile_url": "https://github.com/ranaroussi"
    }
  },
  {
    "name": "getomni-ai/zerox",
    "description": "PDF to Markdown with vision models",
    "url": "https://github.com/getomni-ai/zerox",
    "stars": 6911,
    "forks": 386,
    "language": "Python",
    "last_updated": "2024-12-11T02:01:38Z",
    "topics": [
      "ocr",
      "pdf"
    ],
    "owner": {
      "username": "getomni-ai",
      "profile_url": "https://github.com/getomni-ai"
    }
  },
  {
    "name": "norvig/pytudes",
    "description": "Python programs, usually short, of considerable difficulty, to perfect particular skills.",
    "url": "https://github.com/norvig/pytudes",
    "stars": 23204,
    "forks": 2443,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T23:30:41Z",
    "topics": [
      "demonstrate-skills",
      "practice",
      "programming",
      "python",
      "python-3"
    ],
    "owner": {
      "username": "norvig",
      "profile_url": "https://github.com/norvig"
    }
  },
  {
    "name": "huggingface/transformers",
    "description": "\ud83e\udd17 Transformers: State-of-the-art Machine Learning for Pytorch, TensorFlow, and JAX.",
    "url": "https://github.com/huggingface/transformers",
    "stars": 136139,
    "forks": 27270,
    "language": "Python",
    "last_updated": "2024-12-11T04:03:59Z",
    "topics": [
      "bert",
      "deep-learning",
      "flax",
      "hacktoberfest",
      "jax",
      "language-model",
      "language-models",
      "machine-learning",
      "model-hub",
      "natural-language-processing",
      "nlp",
      "nlp-library",
      "pretrained-models",
      "python",
      "pytorch",
      "pytorch-transformers",
      "seq2seq",
      "speech-recognition",
      "tensorflow",
      "transformer"
    ],
    "owner": {
      "username": "huggingface",
      "profile_url": "https://github.com/huggingface"
    }
  },
  {
    "name": "rany2/edge-tts",
    "description": "Use Microsoft Edge's online text-to-speech service from Python WITHOUT needing Microsoft Edge or Windows or an API key",
    "url": "https://github.com/rany2/edge-tts",
    "stars": 6517,
    "forks": 639,
    "language": "Python",
    "last_updated": "2024-12-10T20:50:21Z",
    "topics": [
      "speech-synthesis",
      "text-to-speech",
      "tts"
    ],
    "owner": {
      "username": "rany2",
      "profile_url": "https://github.com/rany2"
    }
  },
  {
    "name": "serengil/deepface",
    "description": "A Lightweight Face Recognition and Facial Attribute Analysis (Age, Gender, Emotion and Race) Library for Python",
    "url": "https://github.com/serengil/deepface",
    "stars": 15013,
    "forks": 2268,
    "language": "Python",
    "last_updated": "2024-12-11T03:00:30Z",
    "topics": [
      "age-prediction",
      "arcface",
      "deep-learning",
      "deepface",
      "deepid",
      "emotion-recognition",
      "face-analysis",
      "face-recognition",
      "facenet",
      "facial-expression-recognition",
      "facial-recognition",
      "gender-prediction",
      "machine-learning",
      "openface",
      "python",
      "race-classification",
      "vgg-face"
    ],
    "owner": {
      "username": "serengil",
      "profile_url": "https://github.com/serengil"
    }
  },
  {
    "name": "facebookresearch/lingua",
    "description": "Meta Lingua: a lean, efficient, and easy-to-hack codebase to research LLMs.",
    "url": "https://github.com/facebookresearch/lingua",
    "stars": 4294,
    "forks": 223,
    "language": "Python",
    "last_updated": "2024-12-11T03:23:29Z",
    "topics": [],
    "owner": {
      "username": "facebookresearch",
      "profile_url": "https://github.com/facebookresearch"
    }
  },
  {
    "name": "phidatahq/phidata",
    "description": "Build multi-modal Agents with memory, knowledge, tools and reasoning. Chat with them using a beautiful Agent UI.",
    "url": "https://github.com/phidatahq/phidata",
    "stars": 16110,
    "forks": 2205,
    "language": "Python",
    "last_updated": "2024-12-11T04:11:36Z",
    "topics": [
      "agents",
      "ai",
      "developer-tools",
      "python"
    ],
    "owner": {
      "username": "phidatahq",
      "profile_url": "https://github.com/phidatahq"
    }
  },
  {
    "name": "microsoft/BitNet",
    "description": "Official inference framework for 1-bit LLMs",
    "url": "https://github.com/microsoft/BitNet",
    "stars": 12275,
    "forks": 855,
    "language": "C++",
    "last_updated": "2024-12-11T03:50:50Z",
    "topics": [],
    "owner": {
      "username": "microsoft",
      "profile_url": "https://github.com/microsoft"
    }
  },
  {
    "name": "cvat-ai/cvat",
    "description": "Annotate better with CVAT, the industry-leading data engine for machine learning. Used and trusted by teams at any scale, for data of any scale.",
    "url": "https://github.com/cvat-ai/cvat",
    "stars": 12782,
    "forks": 3038,
    "language": "Python",
    "last_updated": "2024-12-10T17:01:55Z",
    "topics": [
      "annotation",
      "annotation-tool",
      "annotations",
      "boundingbox",
      "computer-vision",
      "computer-vision-annotation",
      "dataset",
      "deep-learning",
      "image-annotation",
      "image-classification",
      "image-labeling",
      "image-labelling-tool",
      "imagenet",
      "labeling",
      "labeling-tool",
      "object-detection",
      "pytorch",
      "semantic-segmentation",
      "tensorflow",
      "video-annotation"
    ],
    "owner": {
      "username": "cvat-ai",
      "profile_url": "https://github.com/cvat-ai"
    }
  },
  {
    "name": "HKUDS/LightRAG",
    "description": "\"LightRAG: Simple and Fast Retrieval-Augmented Generation\"",
    "url": "https://github.com/HKUDS/LightRAG",
    "stars": 11121,
    "forks": 1445,
    "language": "Python",
    "last_updated": "2024-12-11T04:04:07Z",
    "topics": [
      "genai",
      "gpt",
      "gpt-4",
      "graphrag",
      "knowledge-graph",
      "large-language-models",
      "llm",
      "rag",
      "retrieval-augmented-generation"
    ],
    "owner": {
      "username": "HKUDS",
      "profile_url": "https://github.com/HKUDS"
    }
  },
  {
    "name": "openai/swarm",
    "description": "Educational framework exploring ergonomic, lightweight multi-agent orchestration. Managed by OpenAI Solution team.",
    "url": "https://github.com/openai/swarm",
    "stars": 16793,
    "forks": 1706,
    "language": "Python",
    "last_updated": "2024-12-11T03:43:34Z",
    "topics": [],
    "owner": {
      "username": "openai",
      "profile_url": "https://github.com/openai"
    }
  },
  {
    "name": "d2l-ai/d2l-en",
    "description": "Interactive deep learning book with multi-framework code, math, and discussions. Adopted at 500 universities from 70 countries including Stanford, MIT, Harvard, and Cambridge.",
    "url": "https://github.com/d2l-ai/d2l-en",
    "stars": 24179,
    "forks": 4392,
    "language": "Python",
    "last_updated": "2024-12-11T00:14:13Z",
    "topics": [
      "book",
      "computer-vision",
      "data-science",
      "deep-learning",
      "gaussian-processes",
      "hyperparameter-optimization",
      "jax",
      "kaggle",
      "keras",
      "machine-learning",
      "mxnet",
      "natural-language-processing",
      "notebook",
      "python",
      "pytorch",
      "recommender-system",
      "reinforcement-learning",
      "tensorflow"
    ],
    "owner": {
      "username": "d2l-ai",
      "profile_url": "https://github.com/d2l-ai"
    }
  },
  {
    "name": "d2l-ai/d2l-zh",
    "description": "\u300a\u52a8\u624b\u5b66\u6df1\u5ea6\u5b66\u4e60\u300b\uff1a\u9762\u5411\u4e2d\u6587\u8bfb\u8005\u3001\u80fd\u8fd0\u884c\u3001\u53ef\u8ba8\u8bba\u3002\u4e2d\u82f1\u6587\u7248\u88ab70\u591a\u4e2a\u56fd\u5bb6\u7684500\u591a\u6240\u5927\u5b66\u7528\u4e8e\u6559\u5b66\u3002",
    "url": "https://github.com/d2l-ai/d2l-zh",
    "stars": 64273,
    "forks": 11097,
    "language": "Python",
    "last_updated": "2024-12-11T03:45:18Z",
    "topics": [
      "book",
      "chinese",
      "computer-vision",
      "deep-learning",
      "machine-learning",
      "natural-language-processing",
      "notebook",
      "python"
    ],
    "owner": {
      "username": "d2l-ai",
      "profile_url": "https://github.com/d2l-ai"
    }
  },
  {
    "name": "ManimCommunity/manim",
    "description": "A community-maintained Python framework for creating mathematical animations. ",
    "url": "https://github.com/ManimCommunity/manim",
    "stars": 27108,
    "forks": 1857,
    "language": "Python",
    "last_updated": "2024-12-11T02:52:59Z",
    "topics": [
      "animations",
      "hacktoberfest",
      "manim",
      "math",
      "python"
    ],
    "owner": {
      "username": "ManimCommunity",
      "profile_url": "https://github.com/ManimCommunity"
    }
  },
  {
    "name": "neuml/txtai",
    "description": "\ud83d\udca1 All-in-one open-source embeddings database for semantic search, LLM orchestration and language model workflows",
    "url": "https://github.com/neuml/txtai",
    "stars": 9630,
    "forks": 616,
    "language": "Python",
    "last_updated": "2024-12-11T03:09:35Z",
    "topics": [
      "embeddings",
      "information-retrieval",
      "language-model",
      "large-language-models",
      "llm",
      "machine-learning",
      "neural-search",
      "nlp",
      "python",
      "rag",
      "retrieval-augmented-generation",
      "search",
      "search-engine",
      "semantic-search",
      "sentence-embeddings",
      "transformers",
      "txtai",
      "vector-database",
      "vector-search",
      "vector-search-engine"
    ],
    "owner": {
      "username": "neuml",
      "profile_url": "https://github.com/neuml"
    }
  },
  {
    "name": "localstack/localstack",
    "description": "\ud83d\udcbb A fully functional local AWS cloud stack. Develop and test your cloud & Serverless apps offline",
    "url": "https://github.com/localstack/localstack",
    "stars": 56724,
    "forks": 4035,
    "language": "Python",
    "last_updated": "2024-12-11T03:58:09Z",
    "topics": [
      "aws",
      "cloud",
      "continuous-integration",
      "developer-tools",
      "localstack",
      "python",
      "testing"
    ],
    "owner": {
      "username": "localstack",
      "profile_url": "https://github.com/localstack"
    }
  },
  {
    "name": "pymupdf/PyMuPDF",
    "description": "PyMuPDF is a high performance Python library for data extraction, analysis, conversion & manipulation of PDF (and other) documents.",
    "url": "https://github.com/pymupdf/PyMuPDF",
    "stars": 5859,
    "forks": 541,
    "language": "Python",
    "last_updated": "2024-12-11T02:10:44Z",
    "topics": [
      "data-science",
      "epub",
      "extract-data",
      "font",
      "mupdf",
      "ocr",
      "pdf",
      "pdf-documents",
      "pymupdf",
      "python",
      "table-extraction",
      "tesseract",
      "text-processing",
      "text-shaping",
      "xps"
    ],
    "owner": {
      "username": "pymupdf",
      "profile_url": "https://github.com/pymupdf"
    }
  },
  {
    "name": "livekit/agents",
    "description": "Build real-time multimodal AI applications \ud83e\udd16\ud83c\udf99\ufe0f\ud83d\udcf9 ",
    "url": "https://github.com/livekit/agents",
    "stars": 4159,
    "forks": 457,
    "language": "Python",
    "last_updated": "2024-12-11T03:43:44Z",
    "topics": [
      "agents",
      "ai",
      "multimodal",
      "real-time",
      "video",
      "voice",
      "voice-assistant"
    ],
    "owner": {
      "username": "livekit",
      "profile_url": "https://github.com/livekit"
    }
  },
  {
    "name": "lukasz-madon/awesome-remote-job",
    "description": "A curated list of awesome remote jobs and resources. Inspired by https://github.com/vinta/awesome-python",
    "url": "https://github.com/lukasz-madon/awesome-remote-job",
    "stars": 35316,
    "forks": 3959,
    "language": null,
    "last_updated": "2024-12-11T03:01:42Z",
    "topics": [
      "awesome",
      "awesome-list",
      "list"
    ],
    "owner": {
      "username": "lukasz-madon",
      "profile_url": "https://github.com/lukasz-madon"
    }
  },
  {
    "name": "huggingface/alignment-handbook",
    "description": "Robust recipes to align language models with human and AI preferences",
    "url": "https://github.com/huggingface/alignment-handbook",
    "stars": 4778,
    "forks": 416,
    "language": "Python",
    "last_updated": "2024-12-10T17:57:09Z",
    "topics": [
      "llm",
      "rlhf",
      "transformers"
    ],
    "owner": {
      "username": "huggingface",
      "profile_url": "https://github.com/huggingface"
    }
  },
  {
    "name": "SciPhi-AI/R2R",
    "description": "The most advanced AI retrieval system. Containerized, Retrieval-Augmented Generation (RAG) with a RESTful API.",
    "url": "https://github.com/SciPhi-AI/R2R",
    "stars": 3941,
    "forks": 290,
    "language": "Python",
    "last_updated": "2024-12-11T03:50:25Z",
    "topics": [
      "artificial-intelligence",
      "large-language-models",
      "python",
      "question-answering",
      "rag",
      "retrieval-augmented-generation",
      "retrieval-systems",
      "search"
    ],
    "owner": {
      "username": "SciPhi-AI",
      "profile_url": "https://github.com/SciPhi-AI"
    }
  },
  {
    "name": "shaopengw/Awesome-Music-Generation",
    "description": "Awesome music generation model\u2014\u2014MG\u00b2",
    "url": "https://github.com/shaopengw/Awesome-Music-Generation",
    "stars": 121,
    "forks": 11,
    "language": "Python",
    "last_updated": "2024-12-08T00:26:14Z",
    "topics": [
      "alignment",
      "artificial-intelligence",
      "creation",
      "diffusion-models",
      "generative-ai",
      "generative-art",
      "large-language-models",
      "melody",
      "multimodal",
      "multimodal-large-language-models",
      "music",
      "music-generation",
      "retrieval-augmented-generation",
      "stable-diffusion"
    ],
    "owner": {
      "username": "shaopengw",
      "profile_url": "https://github.com/shaopengw"
    }
  },
  {
    "name": "aryn-ai/sycamore",
    "description": "\ud83c\udf41 Sycamore is an LLM-powered search and analytics platform for unstructured data.",
    "url": "https://github.com/aryn-ai/sycamore",
    "stars": 400,
    "forks": 46,
    "language": "Python",
    "last_updated": "2024-12-11T00:18:17Z",
    "topics": [
      "ai",
      "dataprep",
      "etl",
      "information-retrieval",
      "llm",
      "ml",
      "nlp",
      "opensearch",
      "search",
      "semantic-search"
    ],
    "owner": {
      "username": "aryn-ai",
      "profile_url": "https://github.com/aryn-ai"
    }
  },
  {
    "name": "pytorch/ao",
    "description": "PyTorch native quantization and sparsity for training and inference",
    "url": "https://github.com/pytorch/ao",
    "stars": 1650,
    "forks": 183,
    "language": "Python",
    "last_updated": "2024-12-10T23:17:25Z",
    "topics": [
      "brrr",
      "cuda",
      "dtypes",
      "float8",
      "inference",
      "llama",
      "mx",
      "offloading",
      "optimizer",
      "pytorch",
      "quantization",
      "sparsity",
      "training",
      "transformer"
    ],
    "owner": {
      "username": "pytorch",
      "profile_url": "https://github.com/pytorch"
    }
  },
  {
    "name": "Doriandarko/o1-engineer",
    "description": "o1-engineer is a command-line tool designed to assist developers in managing and interacting with their projects efficiently. Leveraging the power of OpenAI's API, this tool provides functionalities such as code generation, file editing, and project planning to streamline your development workflow.",
    "url": "https://github.com/Doriandarko/o1-engineer",
    "stars": 2838,
    "forks": 292,
    "language": "Python",
    "last_updated": "2024-12-10T05:01:38Z",
    "topics": [],
    "owner": {
      "username": "Doriandarko",
      "profile_url": "https://github.com/Doriandarko"
    }
  },
  {
    "name": "Avaiga/taipy",
    "description": "Turns Data and AI algorithms into production-ready web applications in no time.",
    "url": "https://github.com/Avaiga/taipy",
    "stars": 17209,
    "forks": 1867,
    "language": "Python",
    "last_updated": "2024-12-11T04:00:18Z",
    "topics": [
      "automation",
      "data-engineering",
      "data-integration",
      "data-ops",
      "data-visualization",
      "datascience",
      "developer-tools",
      "hacktoberfest",
      "hacktoberfest2023",
      "job-scheduler",
      "mlops",
      "orchestration",
      "pipeline",
      "pipelines",
      "python",
      "scenario",
      "scenario-analysis",
      "taipy-core",
      "taipy-gui",
      "workflow"
    ],
    "owner": {
      "username": "Avaiga",
      "profile_url": "https://github.com/Avaiga"
    }
  },
  {
    "name": "unclecode/crawl4ai",
    "description": "\ud83d\udd25\ud83d\udd77\ufe0f Crawl4AI: Crawl Smarter, Faster, Freely. For AI.",
    "url": "https://github.com/unclecode/crawl4ai",
    "stars": 18362,
    "forks": 1341,
    "language": "HTML",
    "last_updated": "2024-12-11T03:57:24Z",
    "topics": [],
    "owner": {
      "username": "unclecode",
      "profile_url": "https://github.com/unclecode"
    }
  },
  {
    "name": "ultralytics/ultralytics",
    "description": "Ultralytics YOLO11 \ud83d\ude80",
    "url": "https://github.com/ultralytics/ultralytics",
    "stars": 33802,
    "forks": 6496,
    "language": "Python",
    "last_updated": "2024-12-11T03:59:23Z",
    "topics": [
      "cli",
      "computer-vision",
      "deep-learning",
      "hub",
      "image-classification",
      "instance-segmentation",
      "machine-learning",
      "object-detection",
      "pose-estimation",
      "python",
      "pytorch",
      "rotated-object-detection",
      "segment-anything",
      "tracking",
      "ultralytics",
      "yolo",
      "yolo-world",
      "yolo11",
      "yolov10",
      "yolov8"
    ],
    "owner": {
      "username": "ultralytics",
      "profile_url": "https://github.com/ultralytics"
    }
  },
  {
    "name": "Filimoa/open-parse",
    "description": "Improved file parsing for LLM\u2019s",
    "url": "https://github.com/Filimoa/open-parse",
    "stars": 2566,
    "forks": 98,
    "language": "Python",
    "last_updated": "2024-12-10T21:40:26Z",
    "topics": [
      "document-parser",
      "document-structure",
      "layout-parsing",
      "table-detection"
    ],
    "owner": {
      "username": "Filimoa",
      "profile_url": "https://github.com/Filimoa"
    }
  },
  {
    "name": "infiniflow/ragflow",
    "description": "RAGFlow is an open-source RAG (Retrieval-Augmented Generation) engine based on deep document understanding.",
    "url": "https://github.com/infiniflow/ragflow",
    "stars": 25073,
    "forks": 2417,
    "language": "Python",
    "last_updated": "2024-12-11T04:11:02Z",
    "topics": [
      "agent",
      "agents",
      "ai-search",
      "chatbot",
      "chatgpt",
      "data-pipelines",
      "deep-learning",
      "document-parser",
      "document-understanding",
      "genai",
      "graph",
      "graphrag",
      "llm",
      "nlp",
      "pdf-to-text",
      "preprocessing",
      "rag",
      "retrieval-augmented-generation",
      "table-structure-recognition",
      "text2sql"
    ],
    "owner": {
      "username": "infiniflow",
      "profile_url": "https://github.com/infiniflow"
    }
  },
  {
    "name": "Unstructured-IO/unstructured",
    "description": "Open source libraries and APIs to build custom preprocessing pipelines for labeling, training, or production machine learning pipelines. ",
    "url": "https://github.com/Unstructured-IO/unstructured",
    "stars": 9385,
    "forks": 781,
    "language": "HTML",
    "last_updated": "2024-12-11T01:13:01Z",
    "topics": [
      "data-pipelines",
      "deep-learning",
      "document-image-analysis",
      "document-image-processing",
      "document-parser",
      "document-parsing",
      "docx",
      "donut",
      "information-retrieval",
      "langchain",
      "llm",
      "machine-learning",
      "ml",
      "natural-language-processing",
      "nlp",
      "ocr",
      "pdf",
      "pdf-to-json",
      "pdf-to-text",
      "preprocessing"
    ],
    "owner": {
      "username": "Unstructured-IO",
      "profile_url": "https://github.com/Unstructured-IO"
    }
  },
  {
    "name": "ProtonX-AI-for-Devs-01/quang-le-vietnamese-rag",
    "description": null,
    "url": "https://github.com/ProtonX-AI-for-Devs-01/quang-le-vietnamese-rag",
    "stars": 10,
    "forks": 5,
    "language": "Python",
    "last_updated": "2024-11-20T05:47:47Z",
    "topics": [],
    "owner": {
      "username": "ProtonX-AI-for-Devs-01",
      "profile_url": "https://github.com/ProtonX-AI-for-Devs-01"
    }
  },
  {
    "name": "krishnadey30/LeetCode-Questions-CompanyWise",
    "description": "Contains Company Wise Questions sorted based on Frequency and all time",
    "url": "https://github.com/krishnadey30/LeetCode-Questions-CompanyWise",
    "stars": 12265,
    "forks": 3909,
    "language": null,
    "last_updated": "2024-12-11T03:56:21Z",
    "topics": [],
    "owner": {
      "username": "krishnadey30",
      "profile_url": "https://github.com/krishnadey30"
    }
  },
  {
    "name": "Hannibal046/Awesome-LLM",
    "description": "Awesome-LLM: a curated list of Large Language Model",
    "url": "https://github.com/Hannibal046/Awesome-LLM",
    "stars": 19287,
    "forks": 1588,
    "language": null,
    "last_updated": "2024-12-11T03:59:08Z",
    "topics": [],
    "owner": {
      "username": "Hannibal046",
      "profile_url": "https://github.com/Hannibal046"
    }
  },
  {
    "name": "microsoft/RD-Agent",
    "description": "Research and development (R&D) is crucial for the enhancement of industrial productivity, especially in the AI era, where the core aspects of R&D are mainly focused on data and models. We are committed to automating these high-value generic R&D processes through our open source R&D automation tool RD-Agent, which lets AI drive data-driven AI.",
    "url": "https://github.com/microsoft/RD-Agent",
    "stars": 1247,
    "forks": 102,
    "language": "Python",
    "last_updated": "2024-12-11T01:26:49Z",
    "topics": [
      "agent",
      "ai",
      "automation",
      "data-mining",
      "data-science",
      "development",
      "llm",
      "research"
    ],
    "owner": {
      "username": "microsoft",
      "profile_url": "https://github.com/microsoft"
    }
  },
  {
    "name": "exo-explore/exo",
    "description": "Run your own AI cluster at home with everyday devices \ud83d\udcf1\ud83d\udcbb \ud83d\udda5\ufe0f\u231a",
    "url": "https://github.com/exo-explore/exo",
    "stars": 17196,
    "forks": 925,
    "language": "Python",
    "last_updated": "2024-12-11T02:51:41Z",
    "topics": [],
    "owner": {
      "username": "exo-explore",
      "profile_url": "https://github.com/exo-explore"
    }
  },
  {
    "name": "Mintplex-Labs/anything-llm",
    "description": "The all-in-one Desktop & Docker AI application with built-in RAG, AI agents, and more.",
    "url": "https://github.com/Mintplex-Labs/anything-llm",
    "stars": 28374,
    "forks": 2878,
    "language": "JavaScript",
    "last_updated": "2024-12-11T04:08:32Z",
    "topics": [
      "agent-framework-javascript",
      "ai-agents",
      "crewai",
      "custom-ai-agents",
      "desktop-app",
      "llama3",
      "llm",
      "llm-application",
      "llm-webui",
      "lmstudio",
      "local-llm",
      "localai",
      "multimodal",
      "nodejs",
      "ollama",
      "rag",
      "vector-database",
      "webui"
    ],
    "owner": {
      "username": "Mintplex-Labs",
      "profile_url": "https://github.com/Mintplex-Labs"
    }
  },
  {
    "name": "ucbepic/docetl",
    "description": "A system for agentic LLM-powered data processing and ETL",
    "url": "https://github.com/ucbepic/docetl",
    "stars": 1350,
    "forks": 120,
    "language": "Python",
    "last_updated": "2024-12-10T19:04:30Z",
    "topics": [
      "agents",
      "data",
      "data-pipelines",
      "elt",
      "etl",
      "llm",
      "python",
      "workflow"
    ],
    "owner": {
      "username": "ucbepic",
      "profile_url": "https://github.com/ucbepic"
    }
  },
  {
    "name": "tw93/Pake",
    "description": "\ud83e\udd31\ud83c\udffb Turn any webpage into a desktop app with Rust.  \ud83e\udd31\ud83c\udffb \u5229\u7528 Rust \u8f7b\u677e\u6784\u5efa\u8f7b\u91cf\u7ea7\u591a\u7aef\u684c\u9762\u5e94\u7528",
    "url": "https://github.com/tw93/Pake",
    "stars": 33470,
    "forks": 5890,
    "language": "Rust",
    "last_updated": "2024-12-11T04:08:57Z",
    "topics": [
      "chatgpt",
      "gpt-4",
      "high-performance",
      "linux-desktop",
      "mac",
      "mac-desktop",
      "music",
      "no-electron",
      "open",
      "openai",
      "poe",
      "productivity",
      "programming",
      "rust",
      "tauri",
      "twitter",
      "webview",
      "windows-desktop",
      "youtube"
    ],
    "owner": {
      "username": "tw93",
      "profile_url": "https://github.com/tw93"
    }
  },
  {
    "name": "Surfer-Org/Protocol",
    "description": "Open-source framework for exporting and building applications off of your personal data.",
    "url": "https://github.com/Surfer-Org/Protocol",
    "stars": 949,
    "forks": 49,
    "language": "TypeScript",
    "last_updated": "2024-12-09T12:08:20Z",
    "topics": [],
    "owner": {
      "username": "Surfer-Org",
      "profile_url": "https://github.com/Surfer-Org"
    }
  },
  {
    "name": "alan2207/bulletproof-react",
    "description": "\ud83d\udee1\ufe0f \u269b\ufe0f A simple, scalable, and powerful architecture for building production ready React applications. ",
    "url": "https://github.com/alan2207/bulletproof-react",
    "stars": 28879,
    "forks": 2619,
    "language": "TypeScript",
    "last_updated": "2024-12-11T02:59:01Z",
    "topics": [
      "react",
      "react-applications",
      "react-architecture-patterns",
      "react-best-practice",
      "react-guidelines",
      "react-project-structure",
      "react-typescript"
    ],
    "owner": {
      "username": "alan2207",
      "profile_url": "https://github.com/alan2207"
    }
  },
  {
    "name": "meta-llama/llama-recipes",
    "description": "Scripts for fine-tuning Meta Llama with composable FSDP & PEFT methods to cover single/multi-node GPUs. Supports default & custom datasets for applications such as summarization and Q&A. Supporting a number of candid inference solutions such as HF TGI, VLLM for local or cloud deployment. Demo apps to showcase Meta Llama for WhatsApp & Messenger.",
    "url": "https://github.com/meta-llama/llama-recipes",
    "stars": 15539,
    "forks": 2247,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T03:05:51Z",
    "topics": [
      "ai",
      "finetuning",
      "langchain",
      "llama",
      "llama2",
      "llm",
      "machine-learning",
      "python",
      "pytorch",
      "vllm"
    ],
    "owner": {
      "username": "meta-llama",
      "profile_url": "https://github.com/meta-llama"
    }
  },
  {
    "name": "meta-llama/llama-stack",
    "description": "Composable building blocks to build Llama Apps",
    "url": "https://github.com/meta-llama/llama-stack",
    "stars": 4830,
    "forks": 629,
    "language": "Python",
    "last_updated": "2024-12-11T04:03:36Z",
    "topics": [],
    "owner": {
      "username": "meta-llama",
      "profile_url": "https://github.com/meta-llama"
    }
  },
  {
    "name": "meta-llama/llama-stack-apps",
    "description": "Agentic components of the Llama Stack APIs",
    "url": "https://github.com/meta-llama/llama-stack-apps",
    "stars": 3955,
    "forks": 571,
    "language": "Python",
    "last_updated": "2024-12-10T21:19:59Z",
    "topics": [],
    "owner": {
      "username": "meta-llama",
      "profile_url": "https://github.com/meta-llama"
    }
  },
  {
    "name": "3b1b/manim",
    "description": "Animation engine for explanatory math videos",
    "url": "https://github.com/3b1b/manim",
    "stars": 71820,
    "forks": 6305,
    "language": "Python",
    "last_updated": "2024-12-11T03:40:44Z",
    "topics": [
      "3b1b-videos",
      "animation",
      "explanatory-math-videos",
      "python"
    ],
    "owner": {
      "username": "3b1b",
      "profile_url": "https://github.com/3b1b"
    }
  },
  {
    "name": "localsend/localsend",
    "description": "An open-source cross-platform alternative to AirDrop",
    "url": "https://github.com/localsend/localsend",
    "stars": 54254,
    "forks": 2920,
    "language": "Dart",
    "last_updated": "2024-12-11T04:13:24Z",
    "topics": [
      "dart",
      "file-sharing",
      "flutter",
      "flutter-apps"
    ],
    "owner": {
      "username": "localsend",
      "profile_url": "https://github.com/localsend"
    }
  },
  {
    "name": "letta-ai/letta",
    "description": "Letta (formerly MemGPT) is a framework for creating LLM services with memory.",
    "url": "https://github.com/letta-ai/letta",
    "stars": 13252,
    "forks": 1452,
    "language": "Python",
    "last_updated": "2024-12-11T03:56:03Z",
    "topics": [
      "ai",
      "ai-agents",
      "llm",
      "llm-agent"
    ],
    "owner": {
      "username": "letta-ai",
      "profile_url": "https://github.com/letta-ai"
    }
  },
  {
    "name": "rasbt/LLMs-from-scratch",
    "description": "Implement a ChatGPT-like LLM in PyTorch from scratch, step by step",
    "url": "https://github.com/rasbt/LLMs-from-scratch",
    "stars": 35023,
    "forks": 4320,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T04:08:59Z",
    "topics": [
      "chatgpt",
      "gpt",
      "large-language-models",
      "llm",
      "python",
      "pytorch"
    ],
    "owner": {
      "username": "rasbt",
      "profile_url": "https://github.com/rasbt"
    }
  },
  {
    "name": "roboflow/supervision",
    "description": "We write your reusable computer vision tools. \ud83d\udc9c",
    "url": "https://github.com/roboflow/supervision",
    "stars": 24420,
    "forks": 1811,
    "language": "Python",
    "last_updated": "2024-12-11T02:12:11Z",
    "topics": [
      "classification",
      "coco",
      "computer-vision",
      "deep-learning",
      "hacktoberfest",
      "image-processing",
      "instance-segmentation",
      "low-code",
      "machine-learning",
      "metrics",
      "object-detection",
      "oriented-bounding-box",
      "pascal-voc",
      "python",
      "pytorch",
      "tensorflow",
      "tracking",
      "video-processing",
      "yolo"
    ],
    "owner": {
      "username": "roboflow",
      "profile_url": "https://github.com/roboflow"
    }
  },
  {
    "name": "Kanaries/pygwalker",
    "description": "PyGWalker: Turn your pandas dataframe into an interactive UI for visual analysis",
    "url": "https://github.com/Kanaries/pygwalker",
    "stars": 13494,
    "forks": 710,
    "language": "Python",
    "last_updated": "2024-12-10T22:22:07Z",
    "topics": [
      "data-analysis",
      "data-exploration",
      "dataframe",
      "matplotlib",
      "pandas",
      "plotly",
      "tableau",
      "tableau-alternative",
      "visualization"
    ],
    "owner": {
      "username": "Kanaries",
      "profile_url": "https://github.com/Kanaries"
    }
  },
  {
    "name": "anthropics/anthropic-cookbook",
    "description": "A collection of notebooks/recipes showcasing some fun and effective ways of using Claude.",
    "url": "https://github.com/anthropics/anthropic-cookbook",
    "stars": 7262,
    "forks": 899,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T21:43:37Z",
    "topics": [],
    "owner": {
      "username": "anthropics",
      "profile_url": "https://github.com/anthropics"
    }
  },
  {
    "name": "bernaferrari/FigmaToCode",
    "description": "Generate responsive pages and apps on HTML, Tailwind, Flutter and SwiftUI.",
    "url": "https://github.com/bernaferrari/FigmaToCode",
    "stars": 3820,
    "forks": 308,
    "language": "TypeScript",
    "last_updated": "2024-12-10T10:36:04Z",
    "topics": [
      "conversion",
      "figma",
      "figma-plugins",
      "flutter",
      "html",
      "responsive",
      "svelte",
      "swift",
      "swiftui",
      "tailwind",
      "tailwindcss",
      "typescript"
    ],
    "owner": {
      "username": "bernaferrari",
      "profile_url": "https://github.com/bernaferrari"
    }
  },
  {
    "name": "GrapesJS/grapesjs",
    "description": "Free and Open source Web Builder Framework. Next generation tool for building templates without coding",
    "url": "https://github.com/GrapesJS/grapesjs",
    "stars": 22827,
    "forks": 4121,
    "language": "TypeScript",
    "last_updated": "2024-12-11T00:18:49Z",
    "topics": [
      "drag-and-drop",
      "framework",
      "no-code",
      "nocode",
      "page-builder",
      "site-builder",
      "site-generator",
      "template-builder",
      "ui-builder",
      "web-builder",
      "web-builder-framework",
      "website-builder"
    ],
    "owner": {
      "username": "GrapesJS",
      "profile_url": "https://github.com/GrapesJS"
    }
  },
  {
    "name": "kyutai-labs/moshi",
    "description": null,
    "url": "https://github.com/kyutai-labs/moshi",
    "stars": 6956,
    "forks": 548,
    "language": "Python",
    "last_updated": "2024-12-10T22:34:21Z",
    "topics": [],
    "owner": {
      "username": "kyutai-labs",
      "profile_url": "https://github.com/kyutai-labs"
    }
  },
  {
    "name": "tungbq/devops-basics",
    "description": "\ud83d\ude80 Practical and document place for DevOps toolchain",
    "url": "https://github.com/tungbq/devops-basics",
    "stars": 1680,
    "forks": 148,
    "language": "HCL",
    "last_updated": "2024-12-06T12:54:46Z",
    "topics": [
      "ansible",
      "aws",
      "cd",
      "ci",
      "ci-cd",
      "cloud",
      "devops",
      "devops-basic",
      "devops-project",
      "devops-tool",
      "devops-tools",
      "docker",
      "elk",
      "helm",
      "iac",
      "jenkins",
      "k8s",
      "monitoring",
      "python",
      "terraform"
    ],
    "owner": {
      "username": "tungbq",
      "profile_url": "https://github.com/tungbq"
    }
  },
  {
    "name": "hijkzzz/Awesome-LLM-Strawberry",
    "description": "A collection of LLM papers, blogs, and projects, with a focus on OpenAI o1 and reasoning techniques.",
    "url": "https://github.com/hijkzzz/Awesome-LLM-Strawberry",
    "stars": 5578,
    "forks": 302,
    "language": null,
    "last_updated": "2024-12-11T04:04:34Z",
    "topics": [
      "chain-of-thought",
      "coding",
      "llm",
      "mathematics",
      "mcts",
      "openai-o1",
      "reinforcement-learning",
      "strawberry"
    ],
    "owner": {
      "username": "hijkzzz",
      "profile_url": "https://github.com/hijkzzz"
    }
  },
  {
    "name": "barun-saha/slide-deck-ai",
    "description": "Co-create a PowerPoint presentation with Generative AI",
    "url": "https://github.com/barun-saha/slide-deck-ai",
    "stars": 72,
    "forks": 12,
    "language": "Python",
    "last_updated": "2024-12-09T16:55:12Z",
    "topics": [
      "cohere-ai",
      "cohere-command",
      "gemini-ai",
      "gemini-api",
      "gemini-flash",
      "generative-ai",
      "hackathon",
      "langchain",
      "large-language-models",
      "mistral-7b-instruct",
      "ollama",
      "powerpoint-presentations",
      "streamlit"
    ],
    "owner": {
      "username": "barun-saha",
      "profile_url": "https://github.com/barun-saha"
    }
  },
  {
    "name": "Ucas-HaoranWei/GOT-OCR2.0",
    "description": "Official code implementation of General OCR Theory:  Towards OCR-2.0 via a Unified End-to-end Model",
    "url": "https://github.com/Ucas-HaoranWei/GOT-OCR2.0",
    "stars": 6274,
    "forks": 545,
    "language": "Python",
    "last_updated": "2024-12-11T02:59:18Z",
    "topics": [],
    "owner": {
      "username": "Ucas-HaoranWei",
      "profile_url": "https://github.com/Ucas-HaoranWei"
    }
  },
  {
    "name": "ictnlp/LLaMA-Omni",
    "description": "LLaMA-Omni is a low-latency and high-quality end-to-end speech interaction model built upon Llama-3.1-8B-Instruct, aiming to achieve speech capabilities at the GPT-4o level.",
    "url": "https://github.com/ictnlp/LLaMA-Omni",
    "stars": 2654,
    "forks": 182,
    "language": "Python",
    "last_updated": "2024-12-10T16:15:10Z",
    "topics": [
      "large-language-models",
      "multimodal-large-language-models",
      "speech-interaction",
      "speech-language-model",
      "speech-to-speech",
      "speech-to-text"
    ],
    "owner": {
      "username": "ictnlp",
      "profile_url": "https://github.com/ictnlp"
    }
  },
  {
    "name": "OpenGVLab/InternVL",
    "description": "[CVPR 2024 Oral] InternVL Family: A Pioneering Open-Source Alternative to GPT-4o.  \u63a5\u8fd1GPT-4o\u8868\u73b0\u7684\u5f00\u6e90\u591a\u6a21\u6001\u5bf9\u8bdd\u6a21\u578b",
    "url": "https://github.com/OpenGVLab/InternVL",
    "stars": 6311,
    "forks": 483,
    "language": "Python",
    "last_updated": "2024-12-11T04:13:37Z",
    "topics": [
      "gpt",
      "gpt-4o",
      "gpt-4v",
      "image-classification",
      "image-text-retrieval",
      "llm",
      "multi-modal",
      "semantic-segmentation",
      "video-classification",
      "vision-language-model",
      "vit-22b",
      "vit-6b"
    ],
    "owner": {
      "username": "OpenGVLab",
      "profile_url": "https://github.com/OpenGVLab"
    }
  },
  {
    "name": "NirDiamant/GenAI_Agents",
    "description": "This repository provides tutorials and implementations for various Generative AI Agent techniques, from basic to advanced. It serves as a comprehensive guide for building intelligent, interactive AI systems.",
    "url": "https://github.com/NirDiamant/GenAI_Agents",
    "stars": 4659,
    "forks": 569,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T03:33:22Z",
    "topics": [
      "agents",
      "ai",
      "genai",
      "langchain",
      "langgraph",
      "llm",
      "llms",
      "openai",
      "tutorials"
    ],
    "owner": {
      "username": "NirDiamant",
      "profile_url": "https://github.com/NirDiamant"
    }
  },
  {
    "name": "bklieger-groq/g1",
    "description": "g1: Using Llama-3.1 70b on Groq to create o1-like reasoning chains",
    "url": "https://github.com/bklieger-groq/g1",
    "stars": 3986,
    "forks": 360,
    "language": "Python",
    "last_updated": "2024-12-11T03:19:04Z",
    "topics": [],
    "owner": {
      "username": "bklieger-groq",
      "profile_url": "https://github.com/bklieger-groq"
    }
  },
  {
    "name": "ToTheBeginning/PuLID",
    "description": "[NeurIPS 2024] Official code for PuLID: Pure and Lightning ID Customization via Contrastive Alignment",
    "url": "https://github.com/ToTheBeginning/PuLID",
    "stars": 2771,
    "forks": 193,
    "language": "Python",
    "last_updated": "2024-12-11T02:56:36Z",
    "topics": [],
    "owner": {
      "username": "ToTheBeginning",
      "profile_url": "https://github.com/ToTheBeginning"
    }
  },
  {
    "name": "HariSekhon/DevOps-Bash-tools",
    "description": "1000+ DevOps Bash Scripts - AWS, GCP, Kubernetes, Docker, CI/CD, APIs, SQL, PostgreSQL, MySQL, Hive, Impala, Kafka, Hadoop, Jenkins, GitHub, GitLab, BitBucket, Azure DevOps, TeamCity, Spotify, MP3, LDAP, Code/Build Linting, pkg mgmt for Linux, Mac, Python, Perl, Ruby, NodeJS, Golang, Advanced dotfiles: .bashrc, .vimrc, .gitconfig, .screenrc, tmux..",
    "url": "https://github.com/HariSekhon/DevOps-Bash-tools",
    "stars": 5851,
    "forks": 1099,
    "language": "Shell",
    "last_updated": "2024-12-11T03:39:22Z",
    "topics": [
      "api",
      "aws",
      "bash",
      "ci",
      "cloudera",
      "devops",
      "docker",
      "gcp",
      "git",
      "github",
      "hacktoberfest",
      "hadoop",
      "jenkins",
      "kafka",
      "kubernetes",
      "linux",
      "mysql",
      "perl",
      "postgresql",
      "terraform"
    ],
    "owner": {
      "username": "HariSekhon",
      "profile_url": "https://github.com/HariSekhon"
    }
  },
  {
    "name": "langgptai/awesome-claude-prompts",
    "description": "This repo includes Claude prompt curation to use Claude better.",
    "url": "https://github.com/langgptai/awesome-claude-prompts",
    "stars": 1385,
    "forks": 140,
    "language": null,
    "last_updated": "2024-12-10T22:36:43Z",
    "topics": [
      "anthropic",
      "anthropic-claude",
      "awesome-claude",
      "awesome-claude-prompts",
      "awesome-prompts",
      "chatgpt",
      "chatgpt-4",
      "chatgpt3",
      "claude",
      "claude-ai",
      "openai",
      "openai-chatgpt",
      "prompt",
      "prompt-learning",
      "prompt-toolkit",
      "prompts"
    ],
    "owner": {
      "username": "langgptai",
      "profile_url": "https://github.com/langgptai"
    }
  },
  {
    "name": "sissbruecker/linkding",
    "description": "Self-hosted bookmark manager that is designed be to be minimal, fast, and easy to set up using Docker.",
    "url": "https://github.com/sissbruecker/linkding",
    "stars": 6907,
    "forks": 328,
    "language": "Python",
    "last_updated": "2024-12-11T03:40:50Z",
    "topics": [
      "bookmark-manager",
      "bookmark-service",
      "bookmarks",
      "self-hosted"
    ],
    "owner": {
      "username": "sissbruecker",
      "profile_url": "https://github.com/sissbruecker"
    }
  },
  {
    "name": "fishaudio/fish-speech",
    "description": "SOTA Open Source TTS",
    "url": "https://github.com/fishaudio/fish-speech",
    "stars": 16643,
    "forks": 1254,
    "language": "Python",
    "last_updated": "2024-12-11T03:59:39Z",
    "topics": [
      "llama",
      "transformer",
      "tts",
      "valle",
      "vits",
      "vqgan",
      "vqvae"
    ],
    "owner": {
      "username": "fishaudio",
      "profile_url": "https://github.com/fishaudio"
    }
  },
  {
    "name": "wordware-ai/twitter",
    "description": "AI Agent for Twitter Personality Analysis",
    "url": "https://github.com/wordware-ai/twitter",
    "stars": 1303,
    "forks": 222,
    "language": "TypeScript",
    "last_updated": "2024-12-10T15:59:44Z",
    "topics": [],
    "owner": {
      "username": "wordware-ai",
      "profile_url": "https://github.com/wordware-ai"
    }
  },
  {
    "name": "vllm-project/vllm",
    "description": "A high-throughput and memory-efficient inference and serving engine for LLMs",
    "url": "https://github.com/vllm-project/vllm",
    "stars": 31657,
    "forks": 4810,
    "language": "Python",
    "last_updated": "2024-12-11T04:05:02Z",
    "topics": [
      "amd",
      "cuda",
      "gpt",
      "hpu",
      "inference",
      "inferentia",
      "llama",
      "llm",
      "llm-serving",
      "llmops",
      "mlops",
      "model-serving",
      "pytorch",
      "rocm",
      "tpu",
      "trainium",
      "transformer",
      "xpu"
    ],
    "owner": {
      "username": "vllm-project",
      "profile_url": "https://github.com/vllm-project"
    }
  },
  {
    "name": "aishwaryanr/awesome-generative-ai-guide",
    "description": "A one stop repository for generative AI research updates, interview resources, notebooks and much more!",
    "url": "https://github.com/aishwaryanr/awesome-generative-ai-guide",
    "stars": 9467,
    "forks": 2053,
    "language": null,
    "last_updated": "2024-12-10T17:20:32Z",
    "topics": [
      "awesome",
      "awesome-list",
      "generative-ai",
      "interview-questions",
      "large-language-models",
      "llms",
      "notebook-jupyter",
      "vision-and-language"
    ],
    "owner": {
      "username": "aishwaryanr",
      "profile_url": "https://github.com/aishwaryanr"
    }
  },
  {
    "name": "unclecode/hermes",
    "description": "\ud83c\udfa5\u27a1\ufe0f\ud83d\udcdd Hermes: Blazing-fast video transcription powered by AI gods! Transcribe 6.5 minutes of video in just 1 second using Groq's LPU. Choose your transcription deity: MLX Whisper (local), Groq (speed demon), or OpenAI (cloud classic). Convert speech to text faster than Hermes delivering messages on Olympus!",
    "url": "https://github.com/unclecode/hermes",
    "stars": 65,
    "forks": 10,
    "language": "Python",
    "last_updated": "2024-12-07T02:26:01Z",
    "topics": [],
    "owner": {
      "username": "unclecode",
      "profile_url": "https://github.com/unclecode"
    }
  },
  {
    "name": "truemagic-coder/nemo-agent",
    "description": "Your Python AI Coder!",
    "url": "https://github.com/truemagic-coder/nemo-agent",
    "stars": 31,
    "forks": 9,
    "language": "Python",
    "last_updated": "2024-12-08T00:37:20Z",
    "topics": [],
    "owner": {
      "username": "truemagic-coder",
      "profile_url": "https://github.com/truemagic-coder"
    }
  },
  {
    "name": "OpenBMB/IoA",
    "description": "An open-source framework for collaborative AI agents, enabling diverse, distributed agents to team up and tackle complex tasks through internet-like connectivity.",
    "url": "https://github.com/OpenBMB/IoA",
    "stars": 598,
    "forks": 52,
    "language": "Python",
    "last_updated": "2024-12-07T16:58:44Z",
    "topics": [
      "agent",
      "ai",
      "genai",
      "ioa",
      "llm"
    ],
    "owner": {
      "username": "OpenBMB",
      "profile_url": "https://github.com/OpenBMB"
    }
  },
  {
    "name": "deepfakes/faceswap",
    "description": "Deepfakes Software For All",
    "url": "https://github.com/deepfakes/faceswap",
    "stars": 52668,
    "forks": 13257,
    "language": "Python",
    "last_updated": "2024-12-11T00:33:04Z",
    "topics": [
      "deep-face-swap",
      "deep-learning",
      "deep-neural-networks",
      "deepface",
      "deepfakes",
      "deeplearning",
      "face-swap",
      "faceswap",
      "fakeapp",
      "machine-learning",
      "myfakeapp",
      "neural-nets",
      "neural-networks",
      "openfaceswap"
    ],
    "owner": {
      "username": "deepfakes",
      "profile_url": "https://github.com/deepfakes"
    }
  },
  {
    "name": "Azure/PyRIT",
    "description": "The Python Risk Identification Tool for generative AI (PyRIT) is an open source framework built to empower security professionals and engineers to proactively identify risks in generative AI systems.",
    "url": "https://github.com/Azure/PyRIT",
    "stars": 1966,
    "forks": 377,
    "language": "Python",
    "last_updated": "2024-12-10T21:48:33Z",
    "topics": [
      "ai-red-team",
      "generative-ai",
      "red-team-tools",
      "responsible-ai"
    ],
    "owner": {
      "username": "Azure",
      "profile_url": "https://github.com/Azure"
    }
  },
  {
    "name": "allenai/OLMo",
    "description": "Modeling, training, eval, and inference code for OLMo",
    "url": "https://github.com/allenai/OLMo",
    "stars": 4878,
    "forks": 499,
    "language": "Python",
    "last_updated": "2024-12-11T03:52:56Z",
    "topics": [],
    "owner": {
      "username": "allenai",
      "profile_url": "https://github.com/allenai"
    }
  },
  {
    "name": "m-bain/whisperX",
    "description": "WhisperX:  Automatic Speech Recognition with Word-level Timestamps (& Diarization)",
    "url": "https://github.com/m-bain/whisperX",
    "stars": 12811,
    "forks": 1361,
    "language": "Python",
    "last_updated": "2024-12-11T02:25:55Z",
    "topics": [
      "asr",
      "speech",
      "speech-recognition",
      "speech-to-text",
      "whisper"
    ],
    "owner": {
      "username": "m-bain",
      "profile_url": "https://github.com/m-bain"
    }
  },
  {
    "name": "simbianai/taskgen",
    "description": "Task-based Agentic Framework using StrictJSON as the core",
    "url": "https://github.com/simbianai/taskgen",
    "stars": 440,
    "forks": 44,
    "language": "Jupyter Notebook",
    "last_updated": "2024-11-25T20:42:09Z",
    "topics": [],
    "owner": {
      "username": "simbianai",
      "profile_url": "https://github.com/simbianai"
    }
  },
  {
    "name": "anthropics/anthropic-quickstarts",
    "description": "A collection of projects designed to help developers quickly get started with building deployable applications using the Anthropic API",
    "url": "https://github.com/anthropics/anthropic-quickstarts",
    "stars": 7115,
    "forks": 1086,
    "language": "TypeScript",
    "last_updated": "2024-12-11T03:57:02Z",
    "topics": [],
    "owner": {
      "username": "anthropics",
      "profile_url": "https://github.com/anthropics"
    }
  },
  {
    "name": "ShengranHu/ADAS",
    "description": "Automated Design of Agentic Systems",
    "url": "https://github.com/ShengranHu/ADAS",
    "stars": 1060,
    "forks": 155,
    "language": "Python",
    "last_updated": "2024-12-10T02:29:15Z",
    "topics": [],
    "owner": {
      "username": "ShengranHu",
      "profile_url": "https://github.com/ShengranHu"
    }
  },
  {
    "name": "langchain-ai/langgraph",
    "description": "Build resilient language agents as graphs.",
    "url": "https://github.com/langchain-ai/langgraph",
    "stars": 7140,
    "forks": 1142,
    "language": "Python",
    "last_updated": "2024-12-11T04:04:14Z",
    "topics": [],
    "owner": {
      "username": "langchain-ai",
      "profile_url": "https://github.com/langchain-ai"
    }
  },
  {
    "name": "AppFlowy-IO/AppFlowy-Cloud",
    "description": "AppFlowy is an open-source alternative to Notion. You are in charge of your data and customizations. Built with Flutter and Rust.",
    "url": "https://github.com/AppFlowy-IO/AppFlowy-Cloud",
    "stars": 1119,
    "forks": 241,
    "language": "Rust",
    "last_updated": "2024-12-11T02:58:08Z",
    "topics": [],
    "owner": {
      "username": "AppFlowy-IO",
      "profile_url": "https://github.com/AppFlowy-IO"
    }
  },
  {
    "name": "Zeyi-Lin/HivisionIDPhotos",
    "description": "\u26a1\ufe0fHivisionIDPhotos: a lightweight and efficient AI ID photos tools. \u4e00\u4e2a\u8f7b\u91cf\u7ea7\u7684AI\u8bc1\u4ef6\u7167\u5236\u4f5c\u7b97\u6cd5\u3002",
    "url": "https://github.com/Zeyi-Lin/HivisionIDPhotos",
    "stars": 13247,
    "forks": 1375,
    "language": "Python",
    "last_updated": "2024-12-11T04:12:00Z",
    "topics": [
      "cnn",
      "demo",
      "docker",
      "face-recognition",
      "fastapi",
      "gradio",
      "idphoto",
      "machine-learning",
      "matting",
      "mtcnn",
      "tools",
      "unet"
    ],
    "owner": {
      "username": "Zeyi-Lin",
      "profile_url": "https://github.com/Zeyi-Lin"
    }
  },
  {
    "name": "weaviate/Verba",
    "description": "Retrieval Augmented Generation (RAG) chatbot powered by Weaviate",
    "url": "https://github.com/weaviate/Verba",
    "stars": 6462,
    "forks": 702,
    "language": "TypeScript",
    "last_updated": "2024-12-11T03:51:41Z",
    "topics": [],
    "owner": {
      "username": "weaviate",
      "profile_url": "https://github.com/weaviate"
    }
  },
  {
    "name": "YassKhazzan/openperplex_backend_os",
    "description": "openperplex is an opensource AI search engine",
    "url": "https://github.com/YassKhazzan/openperplex_backend_os",
    "stars": 776,
    "forks": 79,
    "language": "Python",
    "last_updated": "2024-12-11T02:20:07Z",
    "topics": [],
    "owner": {
      "username": "YassKhazzan",
      "profile_url": "https://github.com/YassKhazzan"
    }
  },
  {
    "name": "frappe/erpnext",
    "description": "Free and Open Source Enterprise Resource Planning (ERP)",
    "url": "https://github.com/frappe/erpnext",
    "stars": 22168,
    "forks": 7426,
    "language": "Python",
    "last_updated": "2024-12-11T02:23:00Z",
    "topics": [
      "accounting",
      "asset-management",
      "crm",
      "distribution",
      "erp",
      "erpnext",
      "frappe",
      "healthcare",
      "hrms",
      "manufacturing",
      "point-of-sale",
      "procurement",
      "project-management",
      "python",
      "retail",
      "support"
    ],
    "owner": {
      "username": "frappe",
      "profile_url": "https://github.com/frappe"
    }
  },
  {
    "name": "Cinnamon/kotaemon",
    "description": "An open-source RAG-based tool for chatting with your documents.",
    "url": "https://github.com/Cinnamon/kotaemon",
    "stars": 17920,
    "forks": 1392,
    "language": "Python",
    "last_updated": "2024-12-11T03:23:36Z",
    "topics": [
      "chatbot",
      "llms",
      "open-source",
      "rag"
    ],
    "owner": {
      "username": "Cinnamon",
      "profile_url": "https://github.com/Cinnamon"
    }
  },
  {
    "name": "Doriandarko/claude-engineer",
    "description": "Claude Engineer is an interactive command-line interface (CLI) that leverages the power of Anthropic's Claude-3.5-Sonnet model to assist with software development tasks. This tool combines the capabilities of a large language model with practical file system operations and web search functionality.",
    "url": "https://github.com/Doriandarko/claude-engineer",
    "stars": 9710,
    "forks": 1030,
    "language": "Python",
    "last_updated": "2024-12-11T01:31:17Z",
    "topics": [],
    "owner": {
      "username": "Doriandarko",
      "profile_url": "https://github.com/Doriandarko"
    }
  },
  {
    "name": "zjunlp/LLMAgentPapers",
    "description": "Must-read Papers on LLM Agents.",
    "url": "https://github.com/zjunlp/LLMAgentPapers",
    "stars": 1937,
    "forks": 104,
    "language": null,
    "last_updated": "2024-12-11T03:18:31Z",
    "topics": [
      "agent",
      "agents",
      "awsome-list",
      "environment",
      "in-context-learning",
      "instruction-following",
      "interactive",
      "large-language-models",
      "llm",
      "multiagent-systems",
      "natural-language-processing",
      "nlp",
      "paper-list",
      "prompt",
      "review",
      "survey",
      "surveys"
    ],
    "owner": {
      "username": "zjunlp",
      "profile_url": "https://github.com/zjunlp"
    }
  },
  {
    "name": "codefuse-ai/codefuse-devops-eval",
    "description": "Industrial-first evaluation benchmark for  LLMs in the DevOps/AIOps domain.",
    "url": "https://github.com/codefuse-ai/codefuse-devops-eval",
    "stars": 689,
    "forks": 44,
    "language": "Python",
    "last_updated": "2024-12-09T13:49:53Z",
    "topics": [],
    "owner": {
      "username": "codefuse-ai",
      "profile_url": "https://github.com/codefuse-ai"
    }
  },
  {
    "name": "Yuan-ManX/AI-Startups",
    "description": "AI Startups are all you need! Here we will track the latest AI Startups, including AI Applications, AI Developer Tools, AI Infrastructure and AI Hardware. \ud83d\udd25",
    "url": "https://github.com/Yuan-ManX/AI-Startups",
    "stars": 7,
    "forks": 1,
    "language": null,
    "last_updated": "2024-11-28T05:39:02Z",
    "topics": [
      "ai-ml",
      "ai-startup",
      "chatgpt",
      "startups"
    ],
    "owner": {
      "username": "Yuan-ManX",
      "profile_url": "https://github.com/Yuan-ManX"
    }
  },
  {
    "name": "linkedin/Liger-Kernel",
    "description": "Efficient Triton Kernels for LLM Training",
    "url": "https://github.com/linkedin/Liger-Kernel",
    "stars": 3762,
    "forks": 222,
    "language": "Python",
    "last_updated": "2024-12-11T04:05:38Z",
    "topics": [
      "finetuning",
      "gemma2",
      "llama",
      "llama3",
      "llm-training",
      "llms",
      "mistral",
      "phi3",
      "triton",
      "triton-kernels"
    ],
    "owner": {
      "username": "linkedin",
      "profile_url": "https://github.com/linkedin"
    }
  },
  {
    "name": "facebookresearch/sapiens",
    "description": "High-resolution models for human tasks.",
    "url": "https://github.com/facebookresearch/sapiens",
    "stars": 4613,
    "forks": 262,
    "language": "Python",
    "last_updated": "2024-12-11T03:27:20Z",
    "topics": [],
    "owner": {
      "username": "facebookresearch",
      "profile_url": "https://github.com/facebookresearch"
    }
  },
  {
    "name": "bunkerity/bunkerweb",
    "description": "\ud83d\udee1\ufe0f Open-source and next-generation Web Application Firewall (WAF)",
    "url": "https://github.com/bunkerity/bunkerweb",
    "stars": 7027,
    "forks": 389,
    "language": "Python",
    "last_updated": "2024-12-11T03:43:14Z",
    "topics": [
      "antibot",
      "bunkerized-nginx",
      "cybersecurity",
      "devops",
      "devsecops",
      "dnsbl",
      "docker",
      "hardening",
      "hosting",
      "kubernetes",
      "letsencrypt",
      "modsecurity",
      "nginx",
      "reverse-proxy",
      "security",
      "security-tuning",
      "swarm",
      "waf",
      "web-application-firewall",
      "web-security"
    ],
    "owner": {
      "username": "bunkerity",
      "profile_url": "https://github.com/bunkerity"
    }
  },
  {
    "name": "Lightning-AI/LitServe",
    "description": "Lightning-fast serving engine for any AI model of any size. Flexible. Easy. Enterprise-scale.",
    "url": "https://github.com/Lightning-AI/LitServe",
    "stars": 2555,
    "forks": 165,
    "language": "Python",
    "last_updated": "2024-12-10T22:26:57Z",
    "topics": [
      "ai",
      "api",
      "artificial-intelligence",
      "deep-learning",
      "developer-tools",
      "fastapi",
      "rest-api",
      "serving",
      "web"
    ],
    "owner": {
      "username": "Lightning-AI",
      "profile_url": "https://github.com/Lightning-AI"
    }
  },
  {
    "name": "ArronAI007/Awesome-AGI",
    "description": "AGI\u8d44\u6599\u6c47\u603b\u5b66\u4e60\uff08\u4e3b\u8981\u5305\u62ecLLM\u548cAIGC\uff09\uff0c\u6301\u7eed\u66f4\u65b0......",
    "url": "https://github.com/ArronAI007/Awesome-AGI",
    "stars": 317,
    "forks": 26,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-09T09:37:35Z",
    "topics": [],
    "owner": {
      "username": "ArronAI007",
      "profile_url": "https://github.com/ArronAI007"
    }
  },
  {
    "name": "aurelio-labs/semantic-router",
    "description": "Superfast AI decision making and intelligent processing of multi-modal data.",
    "url": "https://github.com/aurelio-labs/semantic-router",
    "stars": 2193,
    "forks": 228,
    "language": "Python",
    "last_updated": "2024-12-11T03:41:05Z",
    "topics": [
      "ai",
      "artificial-intelligence",
      "chatbot",
      "computer-vision",
      "generative-ai",
      "machine-learning",
      "nlp"
    ],
    "owner": {
      "username": "aurelio-labs",
      "profile_url": "https://github.com/aurelio-labs"
    }
  },
  {
    "name": "mongodb-developer/GenAI-Showcase",
    "description": "GenAI Cookbook",
    "url": "https://github.com/mongodb-developer/GenAI-Showcase",
    "stars": 694,
    "forks": 130,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T23:22:23Z",
    "topics": [
      "agents",
      "artificial-intelligence",
      "generative-ai",
      "llms",
      "rag"
    ],
    "owner": {
      "username": "mongodb-developer",
      "profile_url": "https://github.com/mongodb-developer"
    }
  },
  {
    "name": "QuivrHQ/quivr",
    "description": "Opiniated RAG for integrating GenAI in your apps \ud83e\udde0   Focus on your product rather than the RAG. Easy integration in existing products with customisation!  Any LLM: GPT4, Groq, Llama. Any Vectorstore: PGVector, Faiss. Any Files. Anyway you want. ",
    "url": "https://github.com/QuivrHQ/quivr",
    "stars": 36864,
    "forks": 3601,
    "language": "Python",
    "last_updated": "2024-12-11T03:37:20Z",
    "topics": [
      "ai",
      "api",
      "chatbot",
      "chatgpt",
      "database",
      "docker",
      "framework",
      "frontend",
      "groq",
      "html",
      "javascript",
      "llm",
      "openai",
      "postgresql",
      "privacy",
      "rag",
      "react",
      "security",
      "typescript",
      "vector"
    ],
    "owner": {
      "username": "QuivrHQ",
      "profile_url": "https://github.com/QuivrHQ"
    }
  },
  {
    "name": "deepset-ai/haystack",
    "description": "AI orchestration framework to build customizable, production-ready LLM applications. Connect components (models, vector DBs, file converters) to pipelines or agents that can interact with your data. With advanced retrieval methods, it's best suited for building RAG, question answering, semantic search or conversational agent chatbots.",
    "url": "https://github.com/deepset-ai/haystack",
    "stars": 18068,
    "forks": 1938,
    "language": "Python",
    "last_updated": "2024-12-11T02:08:04Z",
    "topics": [
      "ai",
      "bert",
      "chatgpt",
      "generative-ai",
      "gpt-3",
      "information-retrieval",
      "language-model",
      "large-language-models",
      "llm",
      "machine-learning",
      "nlp",
      "python",
      "pytorch",
      "question-answering",
      "rag",
      "retrieval-augmented-generation",
      "semantic-search",
      "squad",
      "summarization",
      "transformers"
    ],
    "owner": {
      "username": "deepset-ai",
      "profile_url": "https://github.com/deepset-ai"
    }
  },
  {
    "name": "GURPREETKAURJETHRA/Advanced_RAG",
    "description": "Advanced Retrieval-Augmented Generation (RAG) through practical notebooks, using the power of the Langchain, OpenAI GPTs ,META LLAMA3 , Agents.",
    "url": "https://github.com/GURPREETKAURJETHRA/Advanced_RAG",
    "stars": 42,
    "forks": 13,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-09T18:58:48Z",
    "topics": [
      "agent",
      "chatgpt",
      "genai",
      "generative-ai",
      "langchain",
      "large-language-models",
      "llama3",
      "llm",
      "llms",
      "nlp",
      "openai",
      "rag",
      "retrieval-augmented"
    ],
    "owner": {
      "username": "GURPREETKAURJETHRA",
      "profile_url": "https://github.com/GURPREETKAURJETHRA"
    }
  },
  {
    "name": "Shubhamsaboo/awesome-llm-apps",
    "description": "Collection of awesome LLM apps with RAG using OpenAI, Anthropic, Gemini and opensource models.",
    "url": "https://github.com/Shubhamsaboo/awesome-llm-apps",
    "stars": 4675,
    "forks": 562,
    "language": "Python",
    "last_updated": "2024-12-11T04:12:40Z",
    "topics": [
      "llms",
      "python",
      "rag"
    ],
    "owner": {
      "username": "Shubhamsaboo",
      "profile_url": "https://github.com/Shubhamsaboo"
    }
  },
  {
    "name": "thuml/Time-Series-Library",
    "description": "A Library for Advanced Deep Time Series Models.",
    "url": "https://github.com/thuml/Time-Series-Library",
    "stars": 7363,
    "forks": 1169,
    "language": "Python",
    "last_updated": "2024-12-11T03:07:32Z",
    "topics": [
      "deep-learning",
      "time-series"
    ],
    "owner": {
      "username": "thuml",
      "profile_url": "https://github.com/thuml"
    }
  },
  {
    "name": "s0md3v/roop",
    "description": "one-click face swap",
    "url": "https://github.com/s0md3v/roop",
    "stars": 28749,
    "forks": 7041,
    "language": "Python",
    "last_updated": "2024-12-11T03:50:39Z",
    "topics": [
      "ai",
      "face-swap"
    ],
    "owner": {
      "username": "s0md3v",
      "profile_url": "https://github.com/s0md3v"
    }
  },
  {
    "name": "AGI-Edgerunners/LLM-Agents-Papers",
    "description": "A repo lists papers related to LLM based agent",
    "url": "https://github.com/AGI-Edgerunners/LLM-Agents-Papers",
    "stars": 1125,
    "forks": 76,
    "language": "Python",
    "last_updated": "2024-12-10T17:23:18Z",
    "topics": [
      "agents",
      "large-language-models",
      "llm-agent",
      "paper-list"
    ],
    "owner": {
      "username": "AGI-Edgerunners",
      "profile_url": "https://github.com/AGI-Edgerunners"
    }
  },
  {
    "name": "goauthentik/authentik",
    "description": "The authentication glue you need.",
    "url": "https://github.com/goauthentik/authentik",
    "stars": 13884,
    "forks": 942,
    "language": "Python",
    "last_updated": "2024-12-11T00:19:36Z",
    "topics": [
      "authentication",
      "authentik",
      "authorization",
      "kubernetes",
      "oauth2",
      "oauth2-client",
      "oauth2-server",
      "oidc",
      "oidc-client",
      "oidc-provider",
      "proxy",
      "reverse-proxy",
      "saml",
      "saml-idp",
      "saml-sp",
      "security",
      "sso"
    ],
    "owner": {
      "username": "goauthentik",
      "profile_url": "https://github.com/goauthentik"
    }
  },
  {
    "name": "WooooDyy/LLM-Agent-Paper-List",
    "description": "The paper list of the 86-page paper \"The Rise and Potential of Large Language Model Based Agents: A Survey\" by Zhiheng Xi et al.",
    "url": "https://github.com/WooooDyy/LLM-Agent-Paper-List",
    "stars": 6945,
    "forks": 414,
    "language": null,
    "last_updated": "2024-12-11T03:32:17Z",
    "topics": [
      "agent",
      "large-language-models",
      "llm",
      "nlp",
      "survey"
    ],
    "owner": {
      "username": "WooooDyy",
      "profile_url": "https://github.com/WooooDyy"
    }
  },
  {
    "name": "NisaarAgharia/Advanced_RAG",
    "description": "Advanced Retrieval-Augmented Generation (RAG) through practical  notebooks, using the power of the Langchain, OpenAI GPTs ,META LLAMA3 ,Agents.",
    "url": "https://github.com/NisaarAgharia/Advanced_RAG",
    "stars": 257,
    "forks": 51,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-09T19:21:54Z",
    "topics": [
      "agent",
      "agents",
      "ai",
      "chatgpt",
      "genai",
      "langchain",
      "llama3",
      "llm",
      "machine-learning",
      "nlp",
      "openai",
      "rag",
      "retrival-augmented",
      "vectordb"
    ],
    "owner": {
      "username": "NisaarAgharia",
      "profile_url": "https://github.com/NisaarAgharia"
    }
  },
  {
    "name": "MuhammadBinUsman03/Real-Time-3-pipeline-LLM-Financial-Advisor",
    "description": "3-Pipeline LLMOps Financial advisor. Steaming pipeline deployed on AWS, 24/7 collects, embeds live-data into QdrantDB. Training pipeline finetunes model on serverless GPU and logs best model on WandB Registry.Inference pipeline downloads best model from registry for inference, utilizes Langchain to maintain history and context retrieval.",
    "url": "https://github.com/MuhammadBinUsman03/Real-Time-3-pipeline-LLM-Financial-Advisor",
    "stars": 21,
    "forks": 5,
    "language": "Python",
    "last_updated": "2024-12-07T03:46:33Z",
    "topics": [
      "aws",
      "docker",
      "langchain",
      "llmops",
      "mlops",
      "qdrant",
      "qlora",
      "rag",
      "streaming",
      "wandb"
    ],
    "owner": {
      "username": "MuhammadBinUsman03",
      "profile_url": "https://github.com/MuhammadBinUsman03"
    }
  },
  {
    "name": "qodo-ai/qodo-cover",
    "description": "Qodo-Cover: An AI-Powered Tool for Automated Test Generation and Code Coverage Enhancement! \ud83d\udcbb\ud83e\udd16\ud83e\uddea\ud83d\udc1e",
    "url": "https://github.com/qodo-ai/qodo-cover",
    "stars": 4621,
    "forks": 354,
    "language": "Python",
    "last_updated": "2024-12-11T02:57:52Z",
    "topics": [
      "agents",
      "ai",
      "test-automation",
      "testing"
    ],
    "owner": {
      "username": "qodo-ai",
      "profile_url": "https://github.com/qodo-ai"
    }
  },
  {
    "name": "LibreTranslate/LibreTranslate",
    "description": "Free and Open Source Machine Translation API. Self-hosted, offline capable and easy to setup.",
    "url": "https://github.com/LibreTranslate/LibreTranslate",
    "stars": 9907,
    "forks": 904,
    "language": "Python",
    "last_updated": "2024-12-11T02:02:14Z",
    "topics": [
      "api",
      "machine",
      "translate",
      "translation",
      "translator"
    ],
    "owner": {
      "username": "LibreTranslate",
      "profile_url": "https://github.com/LibreTranslate"
    }
  },
  {
    "name": "naklecha/llama3-from-scratch",
    "description": "llama3 implementation one matrix multiplication at a time",
    "url": "https://github.com/naklecha/llama3-from-scratch",
    "stars": 13868,
    "forks": 1128,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T00:19:00Z",
    "topics": [],
    "owner": {
      "username": "naklecha",
      "profile_url": "https://github.com/naklecha"
    }
  },
  {
    "name": "zylon-ai/private-gpt",
    "description": "Interact with your documents using the power of GPT, 100% privately, no data leaks",
    "url": "https://github.com/zylon-ai/private-gpt",
    "stars": 54399,
    "forks": 7306,
    "language": "Python",
    "last_updated": "2024-12-11T03:46:59Z",
    "topics": [],
    "owner": {
      "username": "zylon-ai",
      "profile_url": "https://github.com/zylon-ai"
    }
  },
  {
    "name": "invariantlabs-ai/invariant",
    "description": "Helps you build better AI agents through debuggable unit testing",
    "url": "https://github.com/invariantlabs-ai/invariant",
    "stars": 128,
    "forks": 10,
    "language": "Python",
    "last_updated": "2024-12-10T23:17:42Z",
    "topics": [
      "agents",
      "ai",
      "security"
    ],
    "owner": {
      "username": "invariantlabs-ai",
      "profile_url": "https://github.com/invariantlabs-ai"
    }
  },
  {
    "name": "soimort/you-get",
    "description": ":arrow_double_down: Dumb downloader that scrapes the web",
    "url": "https://github.com/soimort/you-get",
    "stars": 54113,
    "forks": 9661,
    "language": "Python",
    "last_updated": "2024-12-10T23:33:35Z",
    "topics": [],
    "owner": {
      "username": "soimort",
      "profile_url": "https://github.com/soimort"
    }
  },
  {
    "name": "langchain-ai/rag-from-scratch",
    "description": null,
    "url": "https://github.com/langchain-ai/rag-from-scratch",
    "stars": 2925,
    "forks": 876,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T01:42:10Z",
    "topics": [],
    "owner": {
      "username": "langchain-ai",
      "profile_url": "https://github.com/langchain-ai"
    }
  },
  {
    "name": "binary-husky/gpt_academic",
    "description": "\u4e3aGPT/GLM\u7b49LLM\u5927\u8bed\u8a00\u6a21\u578b\u63d0\u4f9b\u5b9e\u7528\u5316\u4ea4\u4e92\u63a5\u53e3\uff0c\u7279\u522b\u4f18\u5316\u8bba\u6587\u9605\u8bfb/\u6da6\u8272/\u5199\u4f5c\u4f53\u9a8c\uff0c\u6a21\u5757\u5316\u8bbe\u8ba1\uff0c\u652f\u6301\u81ea\u5b9a\u4e49\u5feb\u6377\u6309\u94ae&\u51fd\u6570\u63d2\u4ef6\uff0c\u652f\u6301Python\u548cC++\u7b49\u9879\u76ee\u5256\u6790&\u81ea\u8bd1\u89e3\u529f\u80fd\uff0cPDF/LaTex\u8bba\u6587\u7ffb\u8bd1&\u603b\u7ed3\u529f\u80fd\uff0c\u652f\u6301\u5e76\u884c\u95ee\u8be2\u591a\u79cdLLM\u6a21\u578b\uff0c\u652f\u6301chatglm3\u7b49\u672c\u5730\u6a21\u578b\u3002\u63a5\u5165\u901a\u4e49\u5343\u95ee, deepseekcoder, \u8baf\u98de\u661f\u706b, \u6587\u5fc3\u4e00\u8a00, llama2, rwkv, claude2, moss\u7b49\u3002",
    "url": "https://github.com/binary-husky/gpt_academic",
    "stars": 66269,
    "forks": 8132,
    "language": "Python",
    "last_updated": "2024-12-11T04:04:07Z",
    "topics": [
      "academic",
      "chatglm-6b",
      "chatgpt",
      "gpt-4",
      "large-language-models"
    ],
    "owner": {
      "username": "binary-husky",
      "profile_url": "https://github.com/binary-husky"
    }
  },
  {
    "name": "langgptai/LangGPT",
    "description": "LangGPT: Empowering everyone to become a prompt expert!\ud83d\ude80  Structured Prompt\uff0cLanguage of GPT, \u7ed3\u6784\u5316\u63d0\u793a\u8bcd\uff0c\u7ed3\u6784\u5316Prompt",
    "url": "https://github.com/langgptai/LangGPT",
    "stars": 6992,
    "forks": 559,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T01:51:39Z",
    "topics": [
      "chatgpt",
      "deeplearning",
      "framework",
      "gpt-4",
      "gpt3-prompts",
      "langgpt",
      "prompt-engineering"
    ],
    "owner": {
      "username": "langgptai",
      "profile_url": "https://github.com/langgptai"
    }
  },
  {
    "name": "andysingal/llm-course",
    "description": null,
    "url": "https://github.com/andysingal/llm-course",
    "stars": 390,
    "forks": 41,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T04:07:41Z",
    "topics": [],
    "owner": {
      "username": "andysingal",
      "profile_url": "https://github.com/andysingal"
    }
  },
  {
    "name": "SWE-agent/SWE-agent",
    "description": "SWE-agent takes a GitHub issue and tries to automatically fix it, using GPT-4, or your LM of choice. It can also be employed for offensive cybersecurity or competitive coding challenges. [NeurIPS 2024] ",
    "url": "https://github.com/SWE-agent/SWE-agent",
    "stars": 13901,
    "forks": 1412,
    "language": "Python",
    "last_updated": "2024-12-11T03:32:00Z",
    "topics": [
      "agent",
      "agent-based-model",
      "ai",
      "cybersecurity",
      "developer-tools",
      "llm",
      "lms"
    ],
    "owner": {
      "username": "SWE-agent",
      "profile_url": "https://github.com/SWE-agent"
    }
  },
  {
    "name": "OpenBB-finance/OpenBB",
    "description": "Investment Research for Everyone, Everywhere.",
    "url": "https://github.com/OpenBB-finance/OpenBB",
    "stars": 34336,
    "forks": 3153,
    "language": "Python",
    "last_updated": "2024-12-11T02:49:13Z",
    "topics": [
      "ai",
      "artificial-intelligence",
      "crypto",
      "cryptocurrency",
      "economics",
      "finance",
      "investment",
      "investment-research",
      "machine-learning",
      "openbb",
      "python",
      "quantitative-finance",
      "stocks"
    ],
    "owner": {
      "username": "OpenBB-finance",
      "profile_url": "https://github.com/OpenBB-finance"
    }
  },
  {
    "name": "danielmiessler/fabric",
    "description": "fabric is an open-source framework for augmenting humans using AI. It provides a modular framework for solving specific problems using a crowdsourced set of AI prompts that can be used anywhere.",
    "url": "https://github.com/danielmiessler/fabric",
    "stars": 25882,
    "forks": 2749,
    "language": "Go",
    "last_updated": "2024-12-11T02:59:47Z",
    "topics": [
      "ai",
      "augmentation",
      "flourishing",
      "life",
      "work"
    ],
    "owner": {
      "username": "danielmiessler",
      "profile_url": "https://github.com/danielmiessler"
    }
  },
  {
    "name": "NirDiamant/Controllable-RAG-Agent",
    "description": "This repository provides an advanced Retrieval-Augmented Generation (RAG) solution for complex question answering. It uses sophisticated graph based algorithm to handle the tasks.",
    "url": "https://github.com/NirDiamant/Controllable-RAG-Agent",
    "stars": 851,
    "forks": 112,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T12:40:16Z",
    "topics": [
      "advanced-rag",
      "agent",
      "genai",
      "langchain",
      "langgraph",
      "llm",
      "llms",
      "openai",
      "python",
      "rag"
    ],
    "owner": {
      "username": "NirDiamant",
      "profile_url": "https://github.com/NirDiamant"
    }
  },
  {
    "name": "huggingface/speech-to-speech",
    "description": "Speech To Speech: an effort for an open-sourced and modular GPT4-o",
    "url": "https://github.com/huggingface/speech-to-speech",
    "stars": 3600,
    "forks": 376,
    "language": "Python",
    "last_updated": "2024-12-10T16:57:16Z",
    "topics": [
      "ai",
      "assistant",
      "language-model",
      "machine-learning",
      "python",
      "speech",
      "speech-synthesis",
      "speech-to-text",
      "speech-translation"
    ],
    "owner": {
      "username": "huggingface",
      "profile_url": "https://github.com/huggingface"
    }
  },
  {
    "name": "mealie-recipes/mealie",
    "description": "Mealie is a self hosted recipe manager and meal planner with a RestAPI backend and a reactive frontend application built in Vue for a pleasant user experience for the whole family. Easily add recipes into your database by providing the url and mealie will automatically import the relevant data or add a family recipe with the UI editor",
    "url": "https://github.com/mealie-recipes/mealie",
    "stars": 7570,
    "forks": 758,
    "language": "Python",
    "last_updated": "2024-12-11T02:29:21Z",
    "topics": [
      "hacktoberfest",
      "hacktoberfest2022",
      "meal-plans",
      "recipe-manager",
      "self-hosted"
    ],
    "owner": {
      "username": "mealie-recipes",
      "profile_url": "https://github.com/mealie-recipes"
    }
  },
  {
    "name": "NirDiamant/RAG_Techniques",
    "description": "This repository showcases various advanced techniques for Retrieval-Augmented Generation (RAG) systems. RAG systems combine information retrieval with generative models to provide accurate and contextually rich responses.",
    "url": "https://github.com/NirDiamant/RAG_Techniques",
    "stars": 9134,
    "forks": 936,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T03:57:26Z",
    "topics": [
      "ai",
      "langchain",
      "llama-index",
      "llm",
      "llms",
      "opeani",
      "python",
      "rag",
      "tutorials"
    ],
    "owner": {
      "username": "NirDiamant",
      "profile_url": "https://github.com/NirDiamant"
    }
  },
  {
    "name": "PromtEngineer/Verbi",
    "description": "A modular voice assistant application for experimenting with state-of-the-art transcription, response generation, and text-to-speech models. Supports OpenAI, Groq, Elevanlabs, CartesiaAI, and Deepgram APIs, plus local models via Ollama. Ideal for research and development in voice technology.",
    "url": "https://github.com/PromtEngineer/Verbi",
    "stars": 822,
    "forks": 158,
    "language": "Python",
    "last_updated": "2024-12-10T23:01:09Z",
    "topics": [],
    "owner": {
      "username": "PromtEngineer",
      "profile_url": "https://github.com/PromtEngineer"
    }
  },
  {
    "name": "SylphAI-Inc/AdalFlow",
    "description": "AdalFlow: The library to build & auto-optimize LLM applications.",
    "url": "https://github.com/SylphAI-Inc/AdalFlow",
    "stars": 2318,
    "forks": 207,
    "language": "Python",
    "last_updated": "2024-12-10T22:39:10Z",
    "topics": [
      "agent",
      "ai",
      "bm25",
      "chatbot",
      "faiss",
      "framework",
      "generative-ai",
      "information-retrieval",
      "llm",
      "machine-learning",
      "nlp",
      "optimizer",
      "python",
      "question-answering",
      "rag",
      "reranker",
      "retriever",
      "summarization",
      "trainer"
    ],
    "owner": {
      "username": "SylphAI-Inc",
      "profile_url": "https://github.com/SylphAI-Inc"
    }
  },
  {
    "name": "xorbitsai/inference",
    "description": "Replace OpenAI GPT with another LLM in your app by changing a single line of code. Xinference gives you the freedom to use any LLM you need. With Xinference, you're empowered to run inference with any open-source language models, speech recognition models, and multimodal models, whether in the cloud, on-premises, or even on your laptop.",
    "url": "https://github.com/xorbitsai/inference",
    "stars": 5630,
    "forks": 468,
    "language": "Python",
    "last_updated": "2024-12-11T02:55:43Z",
    "topics": [
      "artificial-intelligence",
      "chatglm",
      "deployment",
      "flan-t5",
      "gemma",
      "ggml",
      "glm4",
      "inference",
      "llama",
      "llama3",
      "llamacpp",
      "llm",
      "machine-learning",
      "mistral",
      "openai-api",
      "pytorch",
      "qwen",
      "vllm",
      "whisper",
      "wizardlm"
    ],
    "owner": {
      "username": "xorbitsai",
      "profile_url": "https://github.com/xorbitsai"
    }
  },
  {
    "name": "Zipstack/unstract",
    "description": "No-code LLM Platform to launch APIs and ETL Pipelines to structure unstructured documents",
    "url": "https://github.com/Zipstack/unstract",
    "stars": 2530,
    "forks": 155,
    "language": "Python",
    "last_updated": "2024-12-10T05:28:50Z",
    "topics": [
      "etl-pipeline",
      "llm-platform",
      "unstructured-data"
    ],
    "owner": {
      "username": "Zipstack",
      "profile_url": "https://github.com/Zipstack"
    }
  },
  {
    "name": "ostris/ai-toolkit",
    "description": "Various AI scripts. Mostly Stable Diffusion stuff.",
    "url": "https://github.com/ostris/ai-toolkit",
    "stars": 3587,
    "forks": 386,
    "language": "Python",
    "last_updated": "2024-12-10T20:29:37Z",
    "topics": [],
    "owner": {
      "username": "ostris",
      "profile_url": "https://github.com/ostris"
    }
  },
  {
    "name": "THUDM/LongWriter",
    "description": "LongWriter: Unleashing 10,000+ Word Generation from Long Context LLMs",
    "url": "https://github.com/THUDM/LongWriter",
    "stars": 1529,
    "forks": 142,
    "language": "Python",
    "last_updated": "2024-12-10T14:38:26Z",
    "topics": [
      "fine-tuning",
      "llm",
      "long-context",
      "long-text"
    ],
    "owner": {
      "username": "THUDM",
      "profile_url": "https://github.com/THUDM"
    }
  },
  {
    "name": "SakanaAI/AI-Scientist",
    "description": "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery \ud83e\uddd1\u200d\ud83d\udd2c",
    "url": "https://github.com/SakanaAI/AI-Scientist",
    "stars": 8325,
    "forks": 1182,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T03:17:50Z",
    "topics": [],
    "owner": {
      "username": "SakanaAI",
      "profile_url": "https://github.com/SakanaAI"
    }
  },
  {
    "name": "ThuCCSLab/Awesome-LM-SSP",
    "description": "A reading list for large models safety, security, and privacy (including Awesome LLM Security, Safety, etc.).",
    "url": "https://github.com/ThuCCSLab/Awesome-LM-SSP",
    "stars": 997,
    "forks": 67,
    "language": null,
    "last_updated": "2024-12-11T03:23:19Z",
    "topics": [
      "adversarial-attacks",
      "awesome-list",
      "diffusion-models",
      "jailbreak",
      "language-model",
      "llm",
      "nlp",
      "privacy",
      "safety",
      "security",
      "vlm"
    ],
    "owner": {
      "username": "ThuCCSLab",
      "profile_url": "https://github.com/ThuCCSLab"
    }
  },
  {
    "name": "ydyjya/Awesome-LLM-Safety",
    "description": "A curated list of safety-related papers, articles, and resources focused on Large Language Models (LLMs). This repository aims to provide researchers, practitioners, and enthusiasts with insights into the safety implications, challenges, and advancements surrounding these powerful models. ",
    "url": "https://github.com/ydyjya/Awesome-LLM-Safety",
    "stars": 1049,
    "forks": 55,
    "language": null,
    "last_updated": "2024-12-11T01:27:09Z",
    "topics": [],
    "owner": {
      "username": "ydyjya",
      "profile_url": "https://github.com/ydyjya"
    }
  },
  {
    "name": "ksm26/Multi-AI-Agent-Systems-with-crewAI",
    "description": "Master the art of designing and organizing AI agents. Learn to automate complex, multi-step business processes by creating specialized AI agent teams using the open-source library crewAI.",
    "url": "https://github.com/ksm26/Multi-AI-Agent-Systems-with-crewAI",
    "stars": 46,
    "forks": 18,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-09T16:50:03Z",
    "topics": [
      "agent-cooperation",
      "ai-agents",
      "ai-memory",
      "ai-workflow-optimization",
      "business-process-automation",
      "complex-task-management",
      "crewai",
      "custom-tools",
      "customer-support-automation",
      "error-handling",
      "event-planning",
      "financial-analysis",
      "multi-agent-systems",
      "natural-language-prompting",
      "open-source-ai",
      "resume-tailoring",
      "role-playing",
      "task-automation",
      "technical-writing"
    ],
    "owner": {
      "username": "ksm26",
      "profile_url": "https://github.com/ksm26"
    }
  },
  {
    "name": "Jenqyang/Awesome-AI-Agents",
    "description": "A collection of autonomous agents \ud83e\udd16\ufe0f powered by LLM.",
    "url": "https://github.com/Jenqyang/Awesome-AI-Agents",
    "stars": 349,
    "forks": 20,
    "language": null,
    "last_updated": "2024-12-10T23:51:30Z",
    "topics": [
      "agent",
      "agents",
      "llm",
      "llm-powered-agents",
      "multi-agent"
    ],
    "owner": {
      "username": "Jenqyang",
      "profile_url": "https://github.com/Jenqyang"
    }
  },
  {
    "name": "supermemoryai/opensearch-ai",
    "description": "SearchGPT / Perplexity clone, but personalised for you.",
    "url": "https://github.com/supermemoryai/opensearch-ai",
    "stars": 969,
    "forks": 135,
    "language": "TypeScript",
    "last_updated": "2024-12-10T13:29:40Z",
    "topics": [],
    "owner": {
      "username": "supermemoryai",
      "profile_url": "https://github.com/supermemoryai"
    }
  },
  {
    "name": "InternLM/InternLM",
    "description": "Official release of InternLM2.5 base and chat models. 1M context support",
    "url": "https://github.com/InternLM/InternLM",
    "stars": 6559,
    "forks": 461,
    "language": "Python",
    "last_updated": "2024-12-10T07:38:20Z",
    "topics": [
      "chatbot",
      "chinese",
      "fine-tuning-llm",
      "flash-attention",
      "gpt",
      "large-language-model",
      "llm",
      "long-context",
      "pretrained-models",
      "rlhf"
    ],
    "owner": {
      "username": "InternLM",
      "profile_url": "https://github.com/InternLM"
    }
  },
  {
    "name": "huggingface/text-generation-inference",
    "description": "Large Language Model Text Generation Inference",
    "url": "https://github.com/huggingface/text-generation-inference",
    "stars": 9274,
    "forks": 1090,
    "language": "Python",
    "last_updated": "2024-12-11T03:48:07Z",
    "topics": [
      "bloom",
      "deep-learning",
      "falcon",
      "gpt",
      "inference",
      "nlp",
      "pytorch",
      "starcoder",
      "transformer"
    ],
    "owner": {
      "username": "huggingface",
      "profile_url": "https://github.com/huggingface"
    }
  },
  {
    "name": "geekan/MetaGPT",
    "description": "\ud83c\udf1f The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programming",
    "url": "https://github.com/geekan/MetaGPT",
    "stars": 45825,
    "forks": 5441,
    "language": "Python",
    "last_updated": "2024-12-11T03:34:38Z",
    "topics": [
      "agent",
      "gpt",
      "hacktoberfest",
      "llm",
      "metagpt",
      "multi-agent"
    ],
    "owner": {
      "username": "geekan",
      "profile_url": "https://github.com/geekan"
    }
  },
  {
    "name": "AIHawk-FOSS/Auto_Jobs_Applier_AI_Agent",
    "description": "Auto_Jobs_Applier_AI_Agent aims to easy job hunt process by automating the job application process. Utilizing artificial intelligence, it enables users to apply for multiple jobs in an automated and personalized way.",
    "url": "https://github.com/AIHawk-FOSS/Auto_Jobs_Applier_AI_Agent",
    "stars": 23512,
    "forks": 3463,
    "language": "Python",
    "last_updated": "2024-12-11T03:53:49Z",
    "topics": [
      "agent",
      "application-resume",
      "artificial-intelligence",
      "automate",
      "automation",
      "bot",
      "chatgpt",
      "chrome",
      "gpt",
      "human-resources",
      "job",
      "jobs",
      "jobsearch",
      "jobseeker",
      "opeai",
      "python",
      "resume",
      "scraper",
      "scraping",
      "selenium"
    ],
    "owner": {
      "username": "AIHawk-FOSS",
      "profile_url": "https://github.com/AIHawk-FOSS"
    }
  },
  {
    "name": "vbskycn/iptv",
    "description": "iptv\u6700\u65b0\u53ef\u7528\u76f4\u64ad\u6e90iptv4/iptv6\u3002\u76f4\u64ad\u7535\u89c6\u7cfb\u7edf\uff0c\u8fd9\u91cc\u6709\u6298\u817e\u597d\u4e86\u7684\uff0c\u76f4\u63a5\u4e0b\u8f7d\u7528\u5427\u3002\u76f4\u64ad\u7535\u89c6app\u7535\u89c6\u624b\u673a\u5168\u90e8\u517c\u5bb9\u3002\uff08\u5305\u542b\u6e2f\u6fb3\u53f0\uff09",
    "url": "https://github.com/vbskycn/iptv",
    "stars": 1659,
    "forks": 207,
    "language": "Python",
    "last_updated": "2024-12-11T02:43:08Z",
    "topics": [],
    "owner": {
      "username": "vbskycn",
      "profile_url": "https://github.com/vbskycn"
    }
  },
  {
    "name": "LLaVA-VL/LLaVA-NeXT",
    "description": null,
    "url": "https://github.com/LLaVA-VL/LLaVA-NeXT",
    "stars": 3075,
    "forks": 263,
    "language": "Python",
    "last_updated": "2024-12-11T03:22:05Z",
    "topics": [],
    "owner": {
      "username": "LLaVA-VL",
      "profile_url": "https://github.com/LLaVA-VL"
    }
  },
  {
    "name": "hacksider/Deep-Live-Cam",
    "description": "real time face swap and one-click video deepfake with only a single image",
    "url": "https://github.com/hacksider/Deep-Live-Cam",
    "stars": 41538,
    "forks": 6075,
    "language": "Python",
    "last_updated": "2024-12-11T03:01:39Z",
    "topics": [
      "ai",
      "ai-deep-fake",
      "ai-face",
      "ai-webcam",
      "artificial-intelligence",
      "deep-fake",
      "deepfake",
      "deepfake-webcam",
      "faceswap",
      "fake-webcam",
      "gan",
      "real-time-deepfake",
      "realtime",
      "realtime-deepfake",
      "realtime-face-changer",
      "video-deepfake",
      "webcam",
      "webcamera"
    ],
    "owner": {
      "username": "hacksider",
      "profile_url": "https://github.com/hacksider"
    }
  },
  {
    "name": "OpenBMB/MiniCPM-V",
    "description": "MiniCPM-V 2.6: A GPT-4V Level MLLM for Single Image, Multi Image and Video on Your Phone",
    "url": "https://github.com/OpenBMB/MiniCPM-V",
    "stars": 12830,
    "forks": 897,
    "language": "Python",
    "last_updated": "2024-12-11T03:48:11Z",
    "topics": [
      "minicpm",
      "minicpm-v",
      "multi-modal"
    ],
    "owner": {
      "username": "OpenBMB",
      "profile_url": "https://github.com/OpenBMB"
    }
  },
  {
    "name": "assafelovic/gpt-researcher",
    "description": "LLM based autonomous agent that conducts local and web research on any topic and generates a comprehensive report with citations.",
    "url": "https://github.com/assafelovic/gpt-researcher",
    "stars": 15221,
    "forks": 2047,
    "language": "Python",
    "last_updated": "2024-12-11T03:29:35Z",
    "topics": [
      "agent",
      "ai",
      "automation",
      "llms",
      "openai",
      "python",
      "research",
      "search",
      "webscraping"
    ],
    "owner": {
      "username": "assafelovic",
      "profile_url": "https://github.com/assafelovic"
    }
  },
  {
    "name": "faridrashidi/kaggle-solutions",
    "description": "\ud83c\udfc5 Collection of Kaggle Solutions and Ideas \ud83c\udfc5",
    "url": "https://github.com/faridrashidi/kaggle-solutions",
    "stars": 5023,
    "forks": 1876,
    "language": "HTML",
    "last_updated": "2024-12-11T04:11:21Z",
    "topics": [
      "awesome",
      "competition",
      "data-mining",
      "data-science",
      "kaggle",
      "machine-learning",
      "solutions"
    ],
    "owner": {
      "username": "faridrashidi",
      "profile_url": "https://github.com/faridrashidi"
    }
  },
  {
    "name": "WangRongsheng/awesome-LLM-resourses",
    "description": "\ud83e\uddd1\u200d\ud83d\ude80 \u5168\u4e16\u754c\u6700\u597d\u7684LLM\u8d44\u6599\u603b\u7ed3 | Summary of the world's best LLM resources.",
    "url": "https://github.com/WangRongsheng/awesome-LLM-resourses",
    "stars": 2615,
    "forks": 307,
    "language": null,
    "last_updated": "2024-12-11T03:44:09Z",
    "topics": [
      "awesome-list",
      "book",
      "course",
      "large-language-models",
      "llama",
      "llm",
      "mistral",
      "openai",
      "qwen",
      "rag",
      "retrieval-augmented-generation",
      "webui"
    ],
    "owner": {
      "username": "WangRongsheng",
      "profile_url": "https://github.com/WangRongsheng"
    }
  },
  {
    "name": "resemble-ai/resemble-enhance",
    "description": "AI powered speech denoising and enhancement",
    "url": "https://github.com/resemble-ai/resemble-enhance",
    "stars": 1495,
    "forks": 159,
    "language": "Python",
    "last_updated": "2024-12-10T21:57:16Z",
    "topics": [
      "denoise",
      "speech-denoising",
      "speech-enhancement",
      "speech-processing"
    ],
    "owner": {
      "username": "resemble-ai",
      "profile_url": "https://github.com/resemble-ai"
    }
  },
  {
    "name": "bghira/SimpleTuner",
    "description": "A general fine-tuning kit geared toward diffusion models.",
    "url": "https://github.com/bghira/SimpleTuner",
    "stars": 1872,
    "forks": 178,
    "language": "Python",
    "last_updated": "2024-12-11T01:19:13Z",
    "topics": [
      "diffusers",
      "diffusion-models",
      "fine-tuning",
      "flux-dev",
      "machine-learning",
      "stable-diffusion"
    ],
    "owner": {
      "username": "bghira",
      "profile_url": "https://github.com/bghira"
    }
  },
  {
    "name": "ScrapeGraphAI/Scrapegraph-ai",
    "description": "Python scraper based on AI",
    "url": "https://github.com/ScrapeGraphAI/Scrapegraph-ai",
    "stars": 16178,
    "forks": 1320,
    "language": "Python",
    "last_updated": "2024-12-11T04:10:25Z",
    "topics": [
      "ai",
      "automated-scraper",
      "gpt-3",
      "gpt-4",
      "llama3",
      "llm",
      "machine-learning",
      "sc",
      "scraping",
      "scraping-python",
      "scrapingweb",
      "webscraping"
    ],
    "owner": {
      "username": "ScrapeGraphAI",
      "profile_url": "https://github.com/ScrapeGraphAI"
    }
  },
  {
    "name": "pytorch/torchchat",
    "description": "Run PyTorch LLMs locally on servers, desktop and mobile",
    "url": "https://github.com/pytorch/torchchat",
    "stars": 3422,
    "forks": 226,
    "language": "Python",
    "last_updated": "2024-12-11T03:50:13Z",
    "topics": [
      "llm",
      "local",
      "pytorch"
    ],
    "owner": {
      "username": "pytorch",
      "profile_url": "https://github.com/pytorch"
    }
  },
  {
    "name": "karpathy/nano-llama31",
    "description": "nanoGPT style version of Llama 3.1",
    "url": "https://github.com/karpathy/nano-llama31",
    "stars": 1266,
    "forks": 67,
    "language": "Python",
    "last_updated": "2024-12-08T16:53:28Z",
    "topics": [],
    "owner": {
      "username": "karpathy",
      "profile_url": "https://github.com/karpathy"
    }
  },
  {
    "name": "miurla/morphic",
    "description": "An AI-powered search engine with a generative UI",
    "url": "https://github.com/miurla/morphic",
    "stars": 6430,
    "forks": 1651,
    "language": "TypeScript",
    "last_updated": "2024-12-10T01:55:32Z",
    "topics": [
      "generative-ai",
      "generative-ui",
      "nextjs",
      "react",
      "redis",
      "searxng",
      "shadcn-ui",
      "tailwindcss",
      "tavily",
      "typescript",
      "upstash",
      "vercel-ai-sdk"
    ],
    "owner": {
      "username": "miurla",
      "profile_url": "https://github.com/miurla"
    }
  },
  {
    "name": "developersdigest/llm-answer-engine",
    "description": "Build a Perplexity-Inspired Answer Engine Using Next.js, Groq, Llama-3, Langchain, OpenAI, Upstash, Brave & Serper",
    "url": "https://github.com/developersdigest/llm-answer-engine",
    "stars": 4701,
    "forks": 750,
    "language": "TypeScript",
    "last_updated": "2024-12-09T18:31:28Z",
    "topics": [],
    "owner": {
      "username": "developersdigest",
      "profile_url": "https://github.com/developersdigest"
    }
  },
  {
    "name": "ItzCrazyKns/Perplexica",
    "description": "Perplexica is an AI-powered search engine. It is an Open source alternative to Perplexity AI",
    "url": "https://github.com/ItzCrazyKns/Perplexica",
    "stars": 17256,
    "forks": 1601,
    "language": "TypeScript",
    "last_updated": "2024-12-11T02:15:56Z",
    "topics": [
      "ai-search-engine",
      "artificial-intelligence",
      "machine-learning",
      "open-source-ai-search-engine",
      "open-source-perplexity-ai",
      "perplexica",
      "perplexity-ai",
      "search-engine",
      "searxng",
      "searxng-copilot"
    ],
    "owner": {
      "username": "ItzCrazyKns",
      "profile_url": "https://github.com/ItzCrazyKns"
    }
  },
  {
    "name": "black-forest-labs/flux",
    "description": "Official inference repo for FLUX.1 models",
    "url": "https://github.com/black-forest-labs/flux",
    "stars": 18301,
    "forks": 1290,
    "language": "Python",
    "last_updated": "2024-12-11T03:48:15Z",
    "topics": [],
    "owner": {
      "username": "black-forest-labs",
      "profile_url": "https://github.com/black-forest-labs"
    }
  },
  {
    "name": "IDEA-Research/Grounded-SAM-2",
    "description": "Grounded SAM 2: Ground and Track Anything in Videos with Grounding DINO, Florence-2 and SAM 2",
    "url": "https://github.com/IDEA-Research/Grounded-SAM-2",
    "stars": 1302,
    "forks": 116,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T01:55:09Z",
    "topics": [],
    "owner": {
      "username": "IDEA-Research",
      "profile_url": "https://github.com/IDEA-Research"
    }
  },
  {
    "name": "InternLM/MindSearch",
    "description": "\ud83d\udd0d An LLM-based Multi-agent Framework of Web Search Engine (like Perplexity.ai Pro and SearchGPT)",
    "url": "https://github.com/InternLM/MindSearch",
    "stars": 5441,
    "forks": 547,
    "language": "JavaScript",
    "last_updated": "2024-12-11T02:55:07Z",
    "topics": [
      "ai-search-engine",
      "gpt",
      "llm",
      "llms",
      "multi-agent-systems",
      "perplexity-ai",
      "search",
      "searchgpt",
      "transformer",
      "web-search"
    ],
    "owner": {
      "username": "InternLM",
      "profile_url": "https://github.com/InternLM"
    }
  },
  {
    "name": "freqtrade/freqtrade",
    "description": "Free, open source crypto trading bot",
    "url": "https://github.com/freqtrade/freqtrade",
    "stars": 32123,
    "forks": 6472,
    "language": "Python",
    "last_updated": "2024-12-11T03:51:09Z",
    "topics": [
      "algorithmic-trading",
      "bitcoin",
      "cryptocurrencies",
      "cryptocurrency",
      "freqtrade",
      "python",
      "telegram-bot",
      "trade",
      "trading-bot"
    ],
    "owner": {
      "username": "freqtrade",
      "profile_url": "https://github.com/freqtrade"
    }
  },
  {
    "name": "facebookresearch/sam2",
    "description": "The repository provides code for running inference with the Meta Segment Anything Model 2 (SAM 2), links for downloading the trained model checkpoints, and example notebooks that show how to use the model.",
    "url": "https://github.com/facebookresearch/sam2",
    "stars": 12986,
    "forks": 1235,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T03:03:00Z",
    "topics": [],
    "owner": {
      "username": "facebookresearch",
      "profile_url": "https://github.com/facebookresearch"
    }
  },
  {
    "name": "stanfordnlp/dspy",
    "description": "DSPy: The framework for programming\u2014not prompting\u2014language models",
    "url": "https://github.com/stanfordnlp/dspy",
    "stars": 19974,
    "forks": 1509,
    "language": "Python",
    "last_updated": "2024-12-11T03:16:10Z",
    "topics": [],
    "owner": {
      "username": "stanfordnlp",
      "profile_url": "https://github.com/stanfordnlp"
    }
  },
  {
    "name": "alexta69/metube",
    "description": "Self-hosted YouTube downloader (web UI for youtube-dl / yt-dlp)",
    "url": "https://github.com/alexta69/metube",
    "stars": 7126,
    "forks": 460,
    "language": "Python",
    "last_updated": "2024-12-11T01:57:04Z",
    "topics": [
      "self-hosted",
      "youtube",
      "youtube-dl",
      "yt-dlp"
    ],
    "owner": {
      "username": "alexta69",
      "profile_url": "https://github.com/alexta69"
    }
  },
  {
    "name": "lipku/LiveTalking",
    "description": "Real time interactive streaming digital human",
    "url": "https://github.com/lipku/LiveTalking",
    "stars": 4074,
    "forks": 595,
    "language": "Python",
    "last_updated": "2024-12-11T01:39:23Z",
    "topics": [
      "aigc",
      "digihuman",
      "digital-human",
      "er-nerf",
      "lip-sync",
      "metahuman-stream",
      "musetalk",
      "nerf",
      "realtime",
      "streaming",
      "talking-head",
      "virtualhumans",
      "wav2lip"
    ],
    "owner": {
      "username": "lipku",
      "profile_url": "https://github.com/lipku"
    }
  },
  {
    "name": "Aider-AI/aider",
    "description": "aider is AI pair programming in your terminal",
    "url": "https://github.com/Aider-AI/aider",
    "stars": 23025,
    "forks": 2140,
    "language": "Python",
    "last_updated": "2024-12-11T03:35:31Z",
    "topics": [
      "chatgpt",
      "claude-3",
      "cli",
      "command-line",
      "gpt-3",
      "gpt-35-turbo",
      "gpt-4",
      "gpt-4o",
      "openai",
      "opus"
    ],
    "owner": {
      "username": "Aider-AI",
      "profile_url": "https://github.com/Aider-AI"
    }
  },
  {
    "name": "frdel/agent-zero",
    "description": "Agent Zero AI framework",
    "url": "https://github.com/frdel/agent-zero",
    "stars": 4982,
    "forks": 1119,
    "language": "Python",
    "last_updated": "2024-12-11T04:05:18Z",
    "topics": [],
    "owner": {
      "username": "frdel",
      "profile_url": "https://github.com/frdel"
    }
  },
  {
    "name": "skapadia3214/groq-moa",
    "description": "Mixture of Agents using Groq",
    "url": "https://github.com/skapadia3214/groq-moa",
    "stars": 925,
    "forks": 164,
    "language": "Python",
    "last_updated": "2024-12-05T12:00:15Z",
    "topics": [],
    "owner": {
      "username": "skapadia3214",
      "profile_url": "https://github.com/skapadia3214"
    }
  },
  {
    "name": "e2b-dev/awesome-ai-agents",
    "description": "A list of AI autonomous agents",
    "url": "https://github.com/e2b-dev/awesome-ai-agents",
    "stars": 12007,
    "forks": 890,
    "language": null,
    "last_updated": "2024-12-11T02:44:23Z",
    "topics": [
      "agent",
      "ai",
      "artificial-intelligence",
      "autogpt",
      "autonomous-agents",
      "awesome",
      "babyagi",
      "copilot",
      "gpt",
      "gpt-4",
      "gpt-engineer",
      "openai",
      "python"
    ],
    "owner": {
      "username": "e2b-dev",
      "profile_url": "https://github.com/e2b-dev"
    }
  },
  {
    "name": "michaelfeil/infinity",
    "description": "Infinity is a high-throughput, low-latency serving engine for text-embeddings, reranking models, clip, clap and colpali",
    "url": "https://github.com/michaelfeil/infinity",
    "stars": 1558,
    "forks": 119,
    "language": "Python",
    "last_updated": "2024-12-10T12:46:14Z",
    "topics": [
      "bert-embeddings",
      "llm",
      "text-embeddings"
    ],
    "owner": {
      "username": "michaelfeil",
      "profile_url": "https://github.com/michaelfeil"
    }
  },
  {
    "name": "FunAudioLLM/SenseVoice",
    "description": "Multilingual Voice Understanding Model",
    "url": "https://github.com/FunAudioLLM/SenseVoice",
    "stars": 3656,
    "forks": 327,
    "language": "Python",
    "last_updated": "2024-12-11T02:59:24Z",
    "topics": [
      "ai",
      "aigc",
      "asr",
      "audio-event-classification",
      "cross-lingual",
      "gpt-4o",
      "llm",
      "multilingual",
      "python",
      "pytorch",
      "speech-emotion-recognition",
      "speech-recognition",
      "speech-to-text"
    ],
    "owner": {
      "username": "FunAudioLLM",
      "profile_url": "https://github.com/FunAudioLLM"
    }
  },
  {
    "name": "FunAudioLLM/CosyVoice",
    "description": "Multi-lingual large voice generation model, providing inference, training and deployment full-stack ability.",
    "url": "https://github.com/FunAudioLLM/CosyVoice",
    "stars": 6749,
    "forks": 720,
    "language": "Python",
    "last_updated": "2024-12-11T04:06:54Z",
    "topics": [
      "audio-generation",
      "cantonese",
      "chatbot",
      "chatgpt",
      "chinese",
      "cosyvoice",
      "cross-lingual",
      "english",
      "fine-grained",
      "fine-tuning",
      "gpt-4o",
      "japanese",
      "korean",
      "multi-lingual",
      "natural-language-generation",
      "python",
      "text-to-speech",
      "tts",
      "voice-cloning"
    ],
    "owner": {
      "username": "FunAudioLLM",
      "profile_url": "https://github.com/FunAudioLLM"
    }
  },
  {
    "name": "0nutation/SpeechGPT",
    "description": "SpeechGPT Series: Speech Large Language Models",
    "url": "https://github.com/0nutation/SpeechGPT",
    "stars": 1311,
    "forks": 87,
    "language": "Python",
    "last_updated": "2024-12-10T12:10:09Z",
    "topics": [],
    "owner": {
      "username": "0nutation",
      "profile_url": "https://github.com/0nutation"
    }
  },
  {
    "name": "ollama/ollama",
    "description": "Get up and running with Llama 3.3, Mistral, Gemma 2, and other large language models.",
    "url": "https://github.com/ollama/ollama",
    "stars": 102146,
    "forks": 8149,
    "language": "Go",
    "last_updated": "2024-12-11T04:11:29Z",
    "topics": [
      "gemma",
      "gemma2",
      "go",
      "golang",
      "llama",
      "llama2",
      "llama3",
      "llava",
      "llm",
      "llms",
      "mistral",
      "ollama",
      "phi3"
    ],
    "owner": {
      "username": "ollama",
      "profile_url": "https://github.com/ollama"
    }
  },
  {
    "name": "opendatalab/MinerU",
    "description": "A high-quality tool for convert PDF to Markdown and JSON.\u4e00\u7ad9\u5f0f\u5f00\u6e90\u9ad8\u8d28\u91cf\u6570\u636e\u63d0\u53d6\u5de5\u5177\uff0c\u5c06PDF\u8f6c\u6362\u6210Markdown\u548cJSON\u683c\u5f0f\u3002",
    "url": "https://github.com/opendatalab/MinerU",
    "stars": 20924,
    "forks": 1483,
    "language": "Python",
    "last_updated": "2024-12-11T04:10:33Z",
    "topics": [
      "ai4science",
      "document-analysis",
      "extract-data",
      "layout-analysis",
      "ocr",
      "parser",
      "pdf",
      "pdf-converter",
      "pdf-extractor-llm",
      "pdf-extractor-pretrain",
      "pdf-extractor-rag",
      "pdf-parser",
      "python"
    ],
    "owner": {
      "username": "opendatalab",
      "profile_url": "https://github.com/opendatalab"
    }
  },
  {
    "name": "mlabonne/llm-course",
    "description": "Course to get into Large Language Models (LLMs) with roadmaps and Colab notebooks.",
    "url": "https://github.com/mlabonne/llm-course",
    "stars": 39899,
    "forks": 4234,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T04:02:48Z",
    "topics": [
      "course",
      "large-language-models",
      "llm",
      "machine-learning",
      "roadmap"
    ],
    "owner": {
      "username": "mlabonne",
      "profile_url": "https://github.com/mlabonne"
    }
  },
  {
    "name": "Mozilla-Ocho/llamafile",
    "description": "Distribute and run LLMs with a single file.",
    "url": "https://github.com/Mozilla-Ocho/llamafile",
    "stars": 20841,
    "forks": 1058,
    "language": "C++",
    "last_updated": "2024-12-11T00:37:02Z",
    "topics": [],
    "owner": {
      "username": "Mozilla-Ocho",
      "profile_url": "https://github.com/Mozilla-Ocho"
    }
  },
  {
    "name": "ComposioHQ/composio",
    "description": "Composio equip's your AI agents & LLMs with 100+ high-quality integrations via function calling",
    "url": "https://github.com/ComposioHQ/composio",
    "stars": 13510,
    "forks": 4272,
    "language": "Python",
    "last_updated": "2024-12-11T03:39:07Z",
    "topics": [
      "agents",
      "ai",
      "ai-agents",
      "aiagents",
      "developer-tools",
      "function-calling",
      "gpt-4",
      "gpt-4o",
      "hacktoberfest",
      "hacktoberfest2024",
      "javascript",
      "js",
      "llm",
      "llmops",
      "python",
      "typescript"
    ],
    "owner": {
      "username": "ComposioHQ",
      "profile_url": "https://github.com/ComposioHQ"
    }
  },
  {
    "name": "Stirling-Tools/Stirling-PDF",
    "description": "#1 Locally hosted web application that allows you to perform various operations on PDF files",
    "url": "https://github.com/Stirling-Tools/Stirling-PDF",
    "stars": 47235,
    "forks": 3867,
    "language": "Java",
    "last_updated": "2024-12-11T03:41:19Z",
    "topics": [
      "docker",
      "java",
      "pdf",
      "pdf-converter",
      "pdf-editor",
      "pdf-manipulation",
      "pdf-merger",
      "pdf-ocr",
      "pdf-tools",
      "pdf-web-apps",
      "pdfmerger"
    ],
    "owner": {
      "username": "Stirling-Tools",
      "profile_url": "https://github.com/Stirling-Tools"
    }
  },
  {
    "name": "immich-app/immich",
    "description": "High performance self-hosted photo and video management solution.",
    "url": "https://github.com/immich-app/immich",
    "stars": 53870,
    "forks": 2860,
    "language": "TypeScript",
    "last_updated": "2024-12-11T03:54:27Z",
    "topics": [
      "backup-tool",
      "flutter",
      "google-photos",
      "google-photos-alternative",
      "hacktoberfest",
      "javascript",
      "mobile-app",
      "nestjs",
      "nodejs",
      "photo-gallery",
      "photos",
      "photos-management",
      "self-hosted",
      "svelte",
      "sveltekit",
      "typescript",
      "videos"
    ],
    "owner": {
      "username": "immich-app",
      "profile_url": "https://github.com/immich-app"
    }
  },
  {
    "name": "rainchen/dify-tool-LongTermMemory",
    "description": "a Dify tool for storing and retrieving long-term-memory, using Dify built-in Knowledge dataset for storing memories, each user has a standalone long-term-memory space",
    "url": "https://github.com/rainchen/dify-tool-LongTermMemory",
    "stars": 53,
    "forks": 5,
    "language": null,
    "last_updated": "2024-12-11T02:43:33Z",
    "topics": [],
    "owner": {
      "username": "rainchen",
      "profile_url": "https://github.com/rainchen"
    }
  },
  {
    "name": "microsoft/graphrag",
    "description": "A modular graph-based Retrieval-Augmented Generation (RAG) system",
    "url": "https://github.com/microsoft/graphrag",
    "stars": 20398,
    "forks": 2004,
    "language": "Python",
    "last_updated": "2024-12-11T03:34:11Z",
    "topics": [
      "gpt",
      "gpt-4",
      "gpt4",
      "graphrag",
      "llm",
      "llms",
      "rag"
    ],
    "owner": {
      "username": "microsoft",
      "profile_url": "https://github.com/microsoft"
    }
  },
  {
    "name": "mem0ai/mem0",
    "description": "The Memory layer for your AI apps",
    "url": "https://github.com/mem0ai/mem0",
    "stars": 23243,
    "forks": 2147,
    "language": "Python",
    "last_updated": "2024-12-11T03:44:16Z",
    "topics": [
      "agent",
      "ai",
      "aiagent",
      "application",
      "chatbots",
      "chatgpt",
      "embeddings",
      "llm",
      "long-term-memory",
      "memory",
      "memory-management",
      "python",
      "rag",
      "state-management",
      "vector-database"
    ],
    "owner": {
      "username": "mem0ai",
      "profile_url": "https://github.com/mem0ai"
    }
  },
  {
    "name": "Azure-Samples/graphrag-accelerator",
    "description": "One-click deploy of a Knowledge Graph powered RAG (GraphRAG) in Azure",
    "url": "https://github.com/Azure-Samples/graphrag-accelerator",
    "stars": 1972,
    "forks": 322,
    "language": "Python",
    "last_updated": "2024-12-11T01:49:15Z",
    "topics": [],
    "owner": {
      "username": "Azure-Samples",
      "profile_url": "https://github.com/Azure-Samples"
    }
  },
  {
    "name": "stanford-oval/storm",
    "description": "An LLM-powered knowledge curation system that researches a topic and generates a full-length report with citations.",
    "url": "https://github.com/stanford-oval/storm",
    "stars": 13605,
    "forks": 1254,
    "language": "Python",
    "last_updated": "2024-12-10T23:39:17Z",
    "topics": [
      "agentic-rag",
      "emnlp2024",
      "knowledge-curation",
      "large-language-models",
      "naacl",
      "nlp",
      "report-generation",
      "retrieval-augmented-generation"
    ],
    "owner": {
      "username": "stanford-oval",
      "profile_url": "https://github.com/stanford-oval"
    }
  },
  {
    "name": "lllyasviel/Paints-UNDO",
    "description": "Understand Human Behavior to Align True Needs",
    "url": "https://github.com/lllyasviel/Paints-UNDO",
    "stars": 3545,
    "forks": 318,
    "language": "Python",
    "last_updated": "2024-12-10T20:13:36Z",
    "topics": [],
    "owner": {
      "username": "lllyasviel",
      "profile_url": "https://github.com/lllyasviel"
    }
  },
  {
    "name": "FudanDNN-NLP/RAG",
    "description": "This is an implementation of the paper:  Searching for Best Practices in Retrieval-Augmented Generation (EMNLP2024)",
    "url": "https://github.com/FudanDNN-NLP/RAG",
    "stars": 234,
    "forks": 13,
    "language": "Python",
    "last_updated": "2024-12-06T22:58:20Z",
    "topics": [],
    "owner": {
      "username": "FudanDNN-NLP",
      "profile_url": "https://github.com/FudanDNN-NLP"
    }
  },
  {
    "name": "vanna-ai/vanna",
    "description": "\ud83e\udd16 Chat with your SQL database \ud83d\udcca. Accurate Text-to-SQL Generation via LLMs using RAG \ud83d\udd04.",
    "url": "https://github.com/vanna-ai/vanna",
    "stars": 12242,
    "forks": 991,
    "language": "Python",
    "last_updated": "2024-12-11T02:47:34Z",
    "topics": [
      "agent",
      "ai",
      "data-visualization",
      "database",
      "llm",
      "rag",
      "sql",
      "text-to-sql"
    ],
    "owner": {
      "username": "vanna-ai",
      "profile_url": "https://github.com/vanna-ai"
    }
  },
  {
    "name": "bangoc123/retrieval-backend-with-rag",
    "description": null,
    "url": "https://github.com/bangoc123/retrieval-backend-with-rag",
    "stars": 107,
    "forks": 44,
    "language": "Python",
    "last_updated": "2024-11-28T04:43:55Z",
    "topics": [],
    "owner": {
      "username": "bangoc123",
      "profile_url": "https://github.com/bangoc123"
    }
  },
  {
    "name": "disposable-email-domains/disposable-email-domains",
    "description": "a list of disposable and temporary email address domains",
    "url": "https://github.com/disposable-email-domains/disposable-email-domains",
    "stars": 3221,
    "forks": 575,
    "language": "Python",
    "last_updated": "2024-12-10T20:24:36Z",
    "topics": [
      "allowlist",
      "blocklist",
      "disposable",
      "domain",
      "email",
      "filter",
      "hacktoberfest",
      "pypi"
    ],
    "owner": {
      "username": "disposable-email-domains",
      "profile_url": "https://github.com/disposable-email-domains"
    }
  },
  {
    "name": "Ceelog/DictionaryByGPT4",
    "description": "\u4e00\u672c GPT4 \u751f\u6210\u7684\u5355\u8bcd\u4e66\ud83d\udcda\uff0c\u8d85\u8fc7 8000 \u4e2a\u5355\u8bcd\u5206\u6790\uff0c\u6db5\u76d6\u4e86\u8bcd\u4e49\u3001\u4f8b\u53e5\u3001\u8bcd\u6839\u8bcd\u7f00\u3001\u53d8\u5f62\u3001\u6587\u5316\u80cc\u666f\u3001\u8bb0\u5fc6\u6280\u5de7\u548c\u5c0f\u6545\u4e8b",
    "url": "https://github.com/Ceelog/DictionaryByGPT4",
    "stars": 3914,
    "forks": 256,
    "language": "HTML",
    "last_updated": "2024-12-10T15:48:47Z",
    "topics": [
      "gpt-4",
      "gpt4"
    ],
    "owner": {
      "username": "Ceelog",
      "profile_url": "https://github.com/Ceelog"
    }
  },
  {
    "name": "adithya-s-k/omniparse",
    "description": "Ingest, parse, and optimize any data format \u27a1\ufe0f from documents to multimedia \u27a1\ufe0f for enhanced compatibility with GenAI frameworks",
    "url": "https://github.com/adithya-s-k/omniparse",
    "stars": 5799,
    "forks": 471,
    "language": "Python",
    "last_updated": "2024-12-11T00:02:06Z",
    "topics": [
      "ingestion-api",
      "ocr",
      "omniparser",
      "parse-server",
      "parser-library",
      "vision-transformer",
      "web-crawler",
      "whisper-api"
    ],
    "owner": {
      "username": "adithya-s-k",
      "profile_url": "https://github.com/adithya-s-k"
    }
  },
  {
    "name": "guidance-ai/guidance",
    "description": "A guidance language for controlling large language models.",
    "url": "https://github.com/guidance-ai/guidance",
    "stars": 19239,
    "forks": 1050,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T02:24:20Z",
    "topics": [],
    "owner": {
      "username": "guidance-ai",
      "profile_url": "https://github.com/guidance-ai"
    }
  },
  {
    "name": "xtekky/gpt4free",
    "description": "The official gpt4free repository | various collection of powerful language models",
    "url": "https://github.com/xtekky/gpt4free",
    "stars": 62632,
    "forks": 13424,
    "language": "Python",
    "last_updated": "2024-12-11T02:21:35Z",
    "topics": [
      "chatbot",
      "chatbots",
      "chatgpt",
      "chatgpt-4",
      "chatgpt-api",
      "chatgpt-free",
      "chatgpt4",
      "free-gpt",
      "gpt",
      "gpt-3",
      "gpt-4",
      "gpt3",
      "gpt4",
      "gpt4-api",
      "language-model",
      "openai",
      "openai-api",
      "openai-chatgpt",
      "python",
      "reverse-engineering"
    ],
    "owner": {
      "username": "xtekky",
      "profile_url": "https://github.com/xtekky"
    }
  },
  {
    "name": "zilliztech/GPTCache",
    "description": "Semantic cache for LLMs. Fully integrated with LangChain and llama_index. ",
    "url": "https://github.com/zilliztech/GPTCache",
    "stars": 7275,
    "forks": 509,
    "language": "Python",
    "last_updated": "2024-12-09T21:44:26Z",
    "topics": [
      "aigc",
      "autogpt",
      "babyagi",
      "chatbot",
      "chatgpt",
      "chatgpt-api",
      "dolly",
      "gpt",
      "langchain",
      "llama",
      "llama-index",
      "llm",
      "memcache",
      "milvus",
      "openai",
      "redis",
      "semantic-search",
      "similarity-search",
      "vector-search"
    ],
    "owner": {
      "username": "zilliztech",
      "profile_url": "https://github.com/zilliztech"
    }
  },
  {
    "name": "supermemoryai/markdowner",
    "description": "A fast tool to convert any website into LLM-ready markdown data. Built by https://supermemory.ai",
    "url": "https://github.com/supermemoryai/markdowner",
    "stars": 949,
    "forks": 76,
    "language": "TypeScript",
    "last_updated": "2024-12-10T03:00:20Z",
    "topics": [],
    "owner": {
      "username": "supermemoryai",
      "profile_url": "https://github.com/supermemoryai"
    }
  },
  {
    "name": "1c7/chinese-independent-developer",
    "description": "\ud83d\udc69\ud83c\udfff\u200d\ud83d\udcbb\ud83d\udc68\ud83c\udffe\u200d\ud83d\udcbb\ud83d\udc69\ud83c\udffc\u200d\ud83d\udcbb\ud83d\udc68\ud83c\udffd\u200d\ud83d\udcbb\ud83d\udc69\ud83c\udffb\u200d\ud83d\udcbb\u4e2d\u56fd\u72ec\u7acb\u5f00\u53d1\u8005\u9879\u76ee\u5217\u8868 -- \u5206\u4eab\u5927\u5bb6\u90fd\u5728\u505a\u4ec0\u4e48",
    "url": "https://github.com/1c7/chinese-independent-developer",
    "stars": 37949,
    "forks": 3164,
    "language": null,
    "last_updated": "2024-12-11T03:45:47Z",
    "topics": [
      "china",
      "indie",
      "indie-developer"
    ],
    "owner": {
      "username": "1c7",
      "profile_url": "https://github.com/1c7"
    }
  },
  {
    "name": "mshumer/gpt-prompt-engineer",
    "description": null,
    "url": "https://github.com/mshumer/gpt-prompt-engineer",
    "stars": 9405,
    "forks": 645,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T11:13:35Z",
    "topics": [],
    "owner": {
      "username": "mshumer",
      "profile_url": "https://github.com/mshumer"
    }
  },
  {
    "name": "1Panel-dev/MaxKB",
    "description": "\ud83d\ude80 MaxKB \u662f\u4e00\u6b3e\u57fa\u4e8e\u5927\u6a21\u578b\u548c RAG \u7684\u5f00\u6e90\u77e5\u8bc6\u5e93\u95ee\u7b54\u7cfb\u7edf\uff0c\u5e7f\u6cdb\u5e94\u7528\u4e8e\u667a\u80fd\u5ba2\u670d\u3001\u4f01\u4e1a\u5185\u90e8\u77e5\u8bc6\u5e93\u3001\u5b66\u672f\u7814\u7a76\u4e0e\u6559\u80b2\u7b49\u573a\u666f\u3002",
    "url": "https://github.com/1Panel-dev/MaxKB",
    "stars": 11933,
    "forks": 1557,
    "language": "Python",
    "last_updated": "2024-12-11T03:45:58Z",
    "topics": [
      "1panel",
      "gpt",
      "knowledgebase",
      "llm",
      "maxkb",
      "ollama",
      "openai"
    ],
    "owner": {
      "username": "1Panel-dev",
      "profile_url": "https://github.com/1Panel-dev"
    }
  },
  {
    "name": "mendableai/firecrawl",
    "description": "\ud83d\udd25 Turn entire websites into LLM-ready markdown or structured data. Scrape, crawl and extract with a single API.",
    "url": "https://github.com/mendableai/firecrawl",
    "stars": 19535,
    "forks": 1524,
    "language": "TypeScript",
    "last_updated": "2024-12-11T03:41:45Z",
    "topics": [
      "ai",
      "ai-scraping",
      "crawler",
      "data",
      "html-to-markdown",
      "llm",
      "markdown",
      "rag",
      "scraper",
      "scraping",
      "web-crawler",
      "webscraping"
    ],
    "owner": {
      "username": "mendableai",
      "profile_url": "https://github.com/mendableai"
    }
  },
  {
    "name": "mehdihadeli/awesome-software-architecture",
    "description": "\ud83d\ude80 A curated list of awesome articles, videos, and other resources to learn and practice software architecture, patterns, and principles.",
    "url": "https://github.com/mehdihadeli/awesome-software-architecture",
    "stars": 8582,
    "forks": 680,
    "language": null,
    "last_updated": "2024-12-10T20:42:50Z",
    "topics": [
      "architectural-patterns",
      "architectural-styles",
      "architecture",
      "awesome-list",
      "clean-architecture",
      "ddd",
      "ddd-architecture",
      "design-pattern",
      "design-patterns",
      "design-systems",
      "event-driven-architecture",
      "microservice",
      "microservices",
      "microservices-architecture",
      "modular-monoliths",
      "onion-architecture",
      "oop",
      "software-architecture",
      "system-design",
      "vertical-slice-architecture"
    ],
    "owner": {
      "username": "mehdihadeli",
      "profile_url": "https://github.com/mehdihadeli"
    }
  },
  {
    "name": "modelscope/DiffSynth-Studio",
    "description": "Enjoy the magic of Diffusion models!",
    "url": "https://github.com/modelscope/DiffSynth-Studio",
    "stars": 6639,
    "forks": 605,
    "language": "Python",
    "last_updated": "2024-12-10T14:24:38Z",
    "topics": [],
    "owner": {
      "username": "modelscope",
      "profile_url": "https://github.com/modelscope"
    }
  },
  {
    "name": "Camb-ai/MARS5-TTS",
    "description": "MARS5 speech model (TTS) from CAMB.AI",
    "url": "https://github.com/Camb-ai/MARS5-TTS",
    "stars": 2548,
    "forks": 209,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T22:47:13Z",
    "topics": [
      "prosody",
      "speech",
      "speech-synthesis",
      "text-to-speech",
      "voice-cloneai",
      "voice-cloning"
    ],
    "owner": {
      "username": "Camb-ai",
      "profile_url": "https://github.com/Camb-ai"
    }
  },
  {
    "name": "Doriandarko/maestro",
    "description": "A framework for Claude Opus to intelligently orchestrate subagents.",
    "url": "https://github.com/Doriandarko/maestro",
    "stars": 4171,
    "forks": 650,
    "language": "Python",
    "last_updated": "2024-12-10T23:41:26Z",
    "topics": [],
    "owner": {
      "username": "Doriandarko",
      "profile_url": "https://github.com/Doriandarko"
    }
  },
  {
    "name": "karpathy/LLM101n",
    "description": "LLM101n: Let's build a Storyteller",
    "url": "https://github.com/karpathy/LLM101n",
    "stars": 30462,
    "forks": 1664,
    "language": null,
    "last_updated": "2024-12-11T01:57:15Z",
    "topics": [],
    "owner": {
      "username": "karpathy",
      "profile_url": "https://github.com/karpathy"
    }
  },
  {
    "name": "hpcaitech/Open-Sora",
    "description": "Open-Sora: Democratizing Efficient Video Production for All",
    "url": "https://github.com/hpcaitech/Open-Sora",
    "stars": 22554,
    "forks": 2206,
    "language": "Python",
    "last_updated": "2024-12-11T03:48:20Z",
    "topics": [],
    "owner": {
      "username": "hpcaitech",
      "profile_url": "https://github.com/hpcaitech"
    }
  },
  {
    "name": "kangyiwen/TTSlist",
    "description": "10000 chatTTS voices \uff01chatTTS \u97f3\u8272\u5e93\uff0c\u518d\u4e5f\u4e0d\u4e3a\u97f3\u8272\u62bd\u5361\u70e6\u607c\u5566\u3002\u8fd9\u662f\u6211\u7b2c\u4e00\u4e2a\u9879\u76ee\uff0c\u71ac\u591c\u9f9f\u901f\u751f\u4ea710000\u6761\u97f3\u8272\u5e76\u4e0a\u4f20Github\uff0c\u7ed9\u70b9\u9f13\u52b1\u5457\u54c8\uff01\u4e3b\u57df\u540d\uff1ahttps://www.TTSlist.com  \u5907\u7528\uff1ahttp://ttslist.aiqbh.com/ ",
    "url": "https://github.com/kangyiwen/TTSlist",
    "stars": 144,
    "forks": 12,
    "language": "HTML",
    "last_updated": "2024-12-05T07:27:45Z",
    "topics": [
      "chattts",
      "tts"
    ],
    "owner": {
      "username": "kangyiwen",
      "profile_url": "https://github.com/kangyiwen"
    }
  },
  {
    "name": "danny-avila/LibreChat",
    "description": "Enhanced ChatGPT Clone: Features Agents, Anthropic, AWS, OpenAI, Assistants API, Azure, Groq, o1, GPT-4o, Mistral, OpenRouter, Vertex AI, Gemini, Artifacts, AI model switching, message search, Code Interpreter, langchain, DALL-E-3, OpenAPI Actions, Functions, Secure Multi-User Auth, Presets, open-source for self-hosting. Active project.",
    "url": "https://github.com/danny-avila/LibreChat",
    "stars": 19693,
    "forks": 3278,
    "language": "TypeScript",
    "last_updated": "2024-12-11T04:12:27Z",
    "topics": [
      "ai",
      "anthropic",
      "artifacts",
      "assistant-api",
      "aws",
      "azure",
      "chatgpt",
      "chatgpt-clone",
      "claude",
      "clone",
      "dall-e-3",
      "gemini",
      "google",
      "librechat",
      "o1",
      "openai",
      "plugins",
      "search",
      "vision",
      "webui"
    ],
    "owner": {
      "username": "danny-avila",
      "profile_url": "https://github.com/danny-avila"
    }
  },
  {
    "name": "Anjok07/ultimatevocalremovergui",
    "description": " GUI for a Vocal Remover that uses Deep Neural Networks.",
    "url": "https://github.com/Anjok07/ultimatevocalremovergui",
    "stars": 18603,
    "forks": 1385,
    "language": "Python",
    "last_updated": "2024-12-10T20:44:10Z",
    "topics": [
      "audio",
      "instrumental",
      "karaoke",
      "kareokee",
      "music",
      "pytorch",
      "separation",
      "source",
      "spectrogram",
      "vocal",
      "vocal-remover",
      "vocals"
    ],
    "owner": {
      "username": "Anjok07",
      "profile_url": "https://github.com/Anjok07"
    }
  },
  {
    "name": "Stability-AI/StableSwarmUI",
    "description": "StableSwarmUI, A Modular Stable Diffusion Web-User-Interface, with an emphasis on making powertools easily accessible, high performance, and extensibility.",
    "url": "https://github.com/Stability-AI/StableSwarmUI",
    "stars": 4621,
    "forks": 371,
    "language": "C#",
    "last_updated": "2024-12-10T22:48:47Z",
    "topics": [
      "ai",
      "image-generation",
      "stable-diffusion",
      "stablediffusion",
      "ui"
    ],
    "owner": {
      "username": "Stability-AI",
      "profile_url": "https://github.com/Stability-AI"
    }
  },
  {
    "name": "comfyanonymous/ComfyUI",
    "description": "The most powerful and modular diffusion model GUI, api and backend with a graph/nodes interface.",
    "url": "https://github.com/comfyanonymous/ComfyUI",
    "stars": 59667,
    "forks": 6336,
    "language": "Python",
    "last_updated": "2024-12-11T04:11:25Z",
    "topics": [
      "pytorch",
      "stable-diffusion"
    ],
    "owner": {
      "username": "comfyanonymous",
      "profile_url": "https://github.com/comfyanonymous"
    }
  },
  {
    "name": "Upsonic/gpt-computer-assistant",
    "description": "Dockerized Computer Use Agents with Production Ready API\u2019s - MCP Client for Langchain - GCA",
    "url": "https://github.com/Upsonic/gpt-computer-assistant",
    "stars": 5462,
    "forks": 489,
    "language": "Python",
    "last_updated": "2024-12-11T01:58:13Z",
    "topics": [
      "assistant",
      "chatgpt",
      "chatgpt-app",
      "claude",
      "computer-use",
      "gca",
      "gpt",
      "gpt-4o",
      "langchain",
      "linux",
      "macos",
      "mcp",
      "mcp-client",
      "mcp-server",
      "model-context-protocol",
      "openai",
      "ubuntu",
      "windows"
    ],
    "owner": {
      "username": "Upsonic",
      "profile_url": "https://github.com/Upsonic"
    }
  },
  {
    "name": "papers-we-love/papers-we-love",
    "description": "Papers from the computer science community to read and discuss.",
    "url": "https://github.com/papers-we-love/papers-we-love",
    "stars": 88697,
    "forks": 5755,
    "language": "Shell",
    "last_updated": "2024-12-11T03:54:30Z",
    "topics": [
      "awesome",
      "computer-science",
      "meetup",
      "papers",
      "programming",
      "read-papers",
      "theory"
    ],
    "owner": {
      "username": "papers-we-love",
      "profile_url": "https://github.com/papers-we-love"
    }
  },
  {
    "name": "KenneyNL/Adobe-Alternatives",
    "description": "A list of alternatives for Adobe software",
    "url": "https://github.com/KenneyNL/Adobe-Alternatives",
    "stars": 5717,
    "forks": 242,
    "language": null,
    "last_updated": "2024-12-11T01:23:47Z",
    "topics": [
      "alternatives",
      "list"
    ],
    "owner": {
      "username": "KenneyNL",
      "profile_url": "https://github.com/KenneyNL"
    }
  },
  {
    "name": "coollabsio/coolify",
    "description": "An open-source & self-hostable Heroku / Netlify / Vercel alternative.",
    "url": "https://github.com/coollabsio/coolify",
    "stars": 35256,
    "forks": 1953,
    "language": "PHP",
    "last_updated": "2024-12-11T03:15:32Z",
    "topics": [
      "analytics",
      "couchdb",
      "databases",
      "docker",
      "minio",
      "mongodb",
      "mysql",
      "mysql-database",
      "nextjs",
      "nodejs",
      "php",
      "postgresql",
      "reactjs",
      "redis",
      "self-hosting",
      "static",
      "svelte",
      "vscode",
      "vuejs"
    ],
    "owner": {
      "username": "coollabsio",
      "profile_url": "https://github.com/coollabsio"
    }
  },
  {
    "name": "google/mesop",
    "description": "Rapidly build AI apps in Python",
    "url": "https://github.com/google/mesop",
    "stars": 5671,
    "forks": 278,
    "language": "Python",
    "last_updated": "2024-12-11T03:49:52Z",
    "topics": [],
    "owner": {
      "username": "google",
      "profile_url": "https://github.com/google"
    }
  },
  {
    "name": "microsoft/prompts-for-edu",
    "description": null,
    "url": "https://github.com/microsoft/prompts-for-edu",
    "stars": 1606,
    "forks": 176,
    "language": null,
    "last_updated": "2024-12-10T15:18:53Z",
    "topics": [],
    "owner": {
      "username": "microsoft",
      "profile_url": "https://github.com/microsoft"
    }
  },
  {
    "name": "Doubiiu/ToonCrafter",
    "description": "[SIGGRAPH Asia 2024, Journal Track] ToonCrafter: Generative Cartoon Interpolation",
    "url": "https://github.com/Doubiiu/ToonCrafter",
    "stars": 5435,
    "forks": 453,
    "language": "Python",
    "last_updated": "2024-12-10T20:55:38Z",
    "topics": [],
    "owner": {
      "username": "Doubiiu",
      "profile_url": "https://github.com/Doubiiu"
    }
  },
  {
    "name": "VikParuchuri/marker",
    "description": "Convert PDF to markdown + JSON quickly with high accuracy",
    "url": "https://github.com/VikParuchuri/marker",
    "stars": 18448,
    "forks": 1071,
    "language": "Python",
    "last_updated": "2024-12-11T03:14:33Z",
    "topics": [],
    "owner": {
      "username": "VikParuchuri",
      "profile_url": "https://github.com/VikParuchuri"
    }
  },
  {
    "name": "2noise/ChatTTS",
    "description": "A generative speech model for daily dialogue.",
    "url": "https://github.com/2noise/ChatTTS",
    "stars": 32896,
    "forks": 3568,
    "language": "Python",
    "last_updated": "2024-12-11T03:23:24Z",
    "topics": [
      "agent",
      "chat",
      "chatgpt",
      "chattts",
      "chinese",
      "chinese-language",
      "english",
      "english-language",
      "gpt",
      "llm",
      "llm-agent",
      "natural-language-inference",
      "python",
      "text-to-speech",
      "torch",
      "torchaudio",
      "tts"
    ],
    "owner": {
      "username": "2noise",
      "profile_url": "https://github.com/2noise"
    }
  },
  {
    "name": "ragapp/ragapp",
    "description": "The easiest way to use Agentic RAG in any enterprise",
    "url": "https://github.com/ragapp/ragapp",
    "stars": 3910,
    "forks": 417,
    "language": "TypeScript",
    "last_updated": "2024-12-10T21:28:03Z",
    "topics": [
      "agentic",
      "agents",
      "ai",
      "docker",
      "llamaindex",
      "rag"
    ],
    "owner": {
      "username": "ragapp",
      "profile_url": "https://github.com/ragapp"
    }
  },
  {
    "name": "AI4Finance-Foundation/FinRobot",
    "description": "FinRobot: An Open-Source AI Agent Platform for Financial Analysis using LLMs \ud83d\ude80 \ud83d\ude80 \ud83d\ude80 ",
    "url": "https://github.com/AI4Finance-Foundation/FinRobot",
    "stars": 1798,
    "forks": 279,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T01:44:10Z",
    "topics": [
      "aiagent",
      "chatgpt",
      "finance",
      "fingpt",
      "large-language-models",
      "multimodal-deep-learning",
      "prompt-engineering",
      "robo-advisor"
    ],
    "owner": {
      "username": "AI4Finance-Foundation",
      "profile_url": "https://github.com/AI4Finance-Foundation"
    }
  },
  {
    "name": "langgenius/dify",
    "description": "Dify is an open-source LLM app development platform. Dify's intuitive interface combines AI workflow, RAG pipeline, agent capabilities, model management, observability features and more, letting you quickly go from prototype to production.",
    "url": "https://github.com/langgenius/dify",
    "stars": 54318,
    "forks": 7979,
    "language": "TypeScript",
    "last_updated": "2024-12-11T04:08:14Z",
    "topics": [
      "agent",
      "ai",
      "anthropic",
      "backend-as-a-service",
      "chatbot",
      "gemini",
      "genai",
      "gpt",
      "gpt-4",
      "llama3",
      "llm",
      "llmops",
      "nextjs",
      "openai",
      "orchestration",
      "python",
      "rag",
      "workflow",
      "workflows"
    ],
    "owner": {
      "username": "langgenius",
      "profile_url": "https://github.com/langgenius"
    }
  },
  {
    "name": "RUC-NLPIR/FlashRAG",
    "description": "\u26a1FlashRAG: A Python Toolkit for Efficient RAG Research",
    "url": "https://github.com/RUC-NLPIR/FlashRAG",
    "stars": 1419,
    "forks": 118,
    "language": "Python",
    "last_updated": "2024-12-10T12:37:30Z",
    "topics": [
      "benchmark",
      "datasets",
      "large-language-models",
      "retrieval-augmented-generation"
    ],
    "owner": {
      "username": "RUC-NLPIR",
      "profile_url": "https://github.com/RUC-NLPIR"
    }
  },
  {
    "name": "iyaja/llama-fs",
    "description": "A self-organizing file system with llama 3",
    "url": "https://github.com/iyaja/llama-fs",
    "stars": 5010,
    "forks": 315,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T02:07:51Z",
    "topics": [],
    "owner": {
      "username": "iyaja",
      "profile_url": "https://github.com/iyaja"
    }
  },
  {
    "name": "THU-MIG/yolov10",
    "description": "YOLOv10: Real-Time End-to-End Object Detection [NeurIPS 2024] ",
    "url": "https://github.com/THU-MIG/yolov10",
    "stars": 10096,
    "forks": 1005,
    "language": "Python",
    "last_updated": "2024-12-11T02:04:36Z",
    "topics": [],
    "owner": {
      "username": "THU-MIG",
      "profile_url": "https://github.com/THU-MIG"
    }
  },
  {
    "name": "amalmurali47/git_rce",
    "description": "Exploit PoC for CVE-2024-32002",
    "url": "https://github.com/amalmurali47/git_rce",
    "stars": 518,
    "forks": 144,
    "language": "Shell",
    "last_updated": "2024-12-08T06:37:07Z",
    "topics": [
      "cve-2024-32002",
      "git",
      "proof-of-concept",
      "rce"
    ],
    "owner": {
      "username": "amalmurali47",
      "profile_url": "https://github.com/amalmurali47"
    }
  },
  {
    "name": "khoj-ai/khoj",
    "description": "Your AI second brain. Self-hostable. Get answers from the web or your docs. Build custom agents, schedule automations, do deep research. Turn any online or local LLM into your personal, autonomous AI (gpt, claude, gemini, llama, qwen, mistral). Get started - free.",
    "url": "https://github.com/khoj-ai/khoj",
    "stars": 17045,
    "forks": 828,
    "language": "Python",
    "last_updated": "2024-12-11T04:01:04Z",
    "topics": [
      "agent",
      "ai",
      "assistant",
      "chat",
      "chatgpt",
      "emacs",
      "image-generation",
      "llama3",
      "llamacpp",
      "llm",
      "obsidian",
      "obsidian-md",
      "offline-llm",
      "productivity",
      "rag",
      "research",
      "self-hosted",
      "semantic-search",
      "stt",
      "whatsapp-ai"
    ],
    "owner": {
      "username": "khoj-ai",
      "profile_url": "https://github.com/khoj-ai"
    }
  },
  {
    "name": "it-ebooks-0/geektime-books",
    "description": ":books: \u6781\u5ba2\u65f6\u95f4\u7535\u5b50\u4e66",
    "url": "https://github.com/it-ebooks-0/geektime-books",
    "stars": 11268,
    "forks": 3794,
    "language": null,
    "last_updated": "2024-12-11T02:44:11Z",
    "topics": [],
    "owner": {
      "username": "it-ebooks-0",
      "profile_url": "https://github.com/it-ebooks-0"
    }
  },
  {
    "name": "longphamkhac/IQA",
    "description": null,
    "url": "https://github.com/longphamkhac/IQA",
    "stars": 31,
    "forks": 2,
    "language": "Python",
    "last_updated": "2024-05-23T07:21:15Z",
    "topics": [],
    "owner": {
      "username": "longphamkhac",
      "profile_url": "https://github.com/longphamkhac"
    }
  },
  {
    "name": "Kludex/fastapi-tips",
    "description": "FastAPI Tips by The FastAPI Expert!",
    "url": "https://github.com/Kludex/fastapi-tips",
    "stars": 2210,
    "forks": 80,
    "language": null,
    "last_updated": "2024-12-10T08:36:35Z",
    "topics": [],
    "owner": {
      "username": "Kludex",
      "profile_url": "https://github.com/Kludex"
    }
  },
  {
    "name": "thinhlpg/vixtts-demo",
    "description": "A Vietnamese Voice Cloning Text-to-Speech Model \u2728",
    "url": "https://github.com/thinhlpg/vixtts-demo",
    "stars": 339,
    "forks": 157,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T03:43:43Z",
    "topics": [
      "text-to-speech",
      "vietnamese"
    ],
    "owner": {
      "username": "thinhlpg",
      "profile_url": "https://github.com/thinhlpg"
    }
  },
  {
    "name": "HqWu-HITCS/Awesome-Chinese-LLM",
    "description": "\u6574\u7406\u5f00\u6e90\u7684\u4e2d\u6587\u5927\u8bed\u8a00\u6a21\u578b\uff0c\u4ee5\u89c4\u6a21\u8f83\u5c0f\u3001\u53ef\u79c1\u6709\u5316\u90e8\u7f72\u3001\u8bad\u7ec3\u6210\u672c\u8f83\u4f4e\u7684\u6a21\u578b\u4e3a\u4e3b\uff0c\u5305\u62ec\u5e95\u5ea7\u6a21\u578b\uff0c\u5782\u76f4\u9886\u57df\u5fae\u8c03\u53ca\u5e94\u7528\uff0c\u6570\u636e\u96c6\u4e0e\u6559\u7a0b\u7b49\u3002",
    "url": "https://github.com/HqWu-HITCS/Awesome-Chinese-LLM",
    "stars": 16586,
    "forks": 1560,
    "language": null,
    "last_updated": "2024-12-11T03:55:31Z",
    "topics": [
      "awesome-lists",
      "chatglm",
      "chinese",
      "llama",
      "llm",
      "nlp"
    ],
    "owner": {
      "username": "HqWu-HITCS",
      "profile_url": "https://github.com/HqWu-HITCS"
    }
  },
  {
    "name": "continuedev/continue",
    "description": "\u23e9 Continue is the leading open-source AI code assistant. You can connect any models and any context to build custom autocomplete and chat experiences inside VS Code and JetBrains",
    "url": "https://github.com/continuedev/continue",
    "stars": 19967,
    "forks": 1766,
    "language": "TypeScript",
    "last_updated": "2024-12-11T03:37:32Z",
    "topics": [
      "ai",
      "chatgpt",
      "copilot",
      "developer-tools",
      "intellij",
      "jetbrains",
      "llm",
      "open-source",
      "openai",
      "pycharm",
      "software-development",
      "visual-studio-code",
      "vscode"
    ],
    "owner": {
      "username": "continuedev",
      "profile_url": "https://github.com/continuedev"
    }
  },
  {
    "name": "CrazyBoyM/llama3-Chinese-chat",
    "description": "Llama3\u3001Llama3.1 \u4e2d\u6587\u4ed3\u5e93\uff08\u968f\u4e66\u7c4d\u64b0\u5199\u4e2d...  \u5404\u79cd\u7f51\u53cb\u53ca\u5382\u5546\u5fae\u8c03\u3001\u9b54\u6539\u7248\u672c\u6709\u8da3\u6743\u91cd & \u8bad\u7ec3\u3001\u63a8\u7406\u3001\u8bc4\u6d4b\u3001\u90e8\u7f72\u6559\u7a0b\u89c6\u9891 & \u6587\u6863\uff09",
    "url": "https://github.com/CrazyBoyM/llama3-Chinese-chat",
    "stars": 4070,
    "forks": 335,
    "language": "Python",
    "last_updated": "2024-12-10T15:11:15Z",
    "topics": [
      "llama",
      "llama2",
      "llama3",
      "llama3-chinese",
      "llama3-finetune"
    ],
    "owner": {
      "username": "CrazyBoyM",
      "profile_url": "https://github.com/CrazyBoyM"
    }
  },
  {
    "name": "hiyouga/LLaMA-Factory",
    "description": "Unified Efficient Fine-Tuning of 100+ LLMs (ACL 2024)",
    "url": "https://github.com/hiyouga/LLaMA-Factory",
    "stars": 35857,
    "forks": 4416,
    "language": "Python",
    "last_updated": "2024-12-11T04:00:50Z",
    "topics": [
      "agent",
      "ai",
      "chatglm",
      "fine-tuning",
      "gpt",
      "instruction-tuning",
      "language-model",
      "large-language-models",
      "llama",
      "llama3",
      "llm",
      "lora",
      "mistral",
      "moe",
      "peft",
      "qlora",
      "quantization",
      "qwen",
      "rlhf",
      "transformers"
    ],
    "owner": {
      "username": "hiyouga",
      "profile_url": "https://github.com/hiyouga"
    }
  },
  {
    "name": "twentyhq/twenty",
    "description": "Building a modern alternative to Salesforce, powered by the community.",
    "url": "https://github.com/twentyhq/twenty",
    "stars": 24046,
    "forks": 2486,
    "language": "TypeScript",
    "last_updated": "2024-12-11T02:12:13Z",
    "topics": [
      "crm",
      "crm-system",
      "customer",
      "good-first-issue",
      "graphql",
      "hacktoberfest",
      "javacript",
      "marketing",
      "monorepo",
      "nestjs",
      "open-source",
      "postgresql",
      "react",
      "reactjs",
      "sales",
      "typescript",
      "web"
    ],
    "owner": {
      "username": "twentyhq",
      "profile_url": "https://github.com/twentyhq"
    }
  },
  {
    "name": "huggingface/diarizers",
    "description": null,
    "url": "https://github.com/huggingface/diarizers",
    "stars": 261,
    "forks": 16,
    "language": "Python",
    "last_updated": "2024-11-28T13:51:12Z",
    "topics": [],
    "owner": {
      "username": "huggingface",
      "profile_url": "https://github.com/huggingface"
    }
  },
  {
    "name": "datawhalechina/llm-universe",
    "description": "\u672c\u9879\u76ee\u662f\u4e00\u4e2a\u9762\u5411\u5c0f\u767d\u5f00\u53d1\u8005\u7684\u5927\u6a21\u578b\u5e94\u7528\u5f00\u53d1\u6559\u7a0b\uff0c\u5728\u7ebf\u9605\u8bfb\u5730\u5740\uff1ahttps://datawhalechina.github.io/llm-universe/",
    "url": "https://github.com/datawhalechina/llm-universe",
    "stars": 4943,
    "forks": 603,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T02:41:27Z",
    "topics": [],
    "owner": {
      "username": "datawhalechina",
      "profile_url": "https://github.com/datawhalechina"
    }
  },
  {
    "name": "jwasham/coding-interview-university",
    "description": "A complete computer science study plan to become a software engineer.",
    "url": "https://github.com/jwasham/coding-interview-university",
    "stars": 307687,
    "forks": 77099,
    "language": null,
    "last_updated": "2024-12-11T02:57:05Z",
    "topics": [
      "algorithm",
      "algorithms",
      "coding-interview",
      "coding-interviews",
      "computer-science",
      "data-structures",
      "interview",
      "interview-prep",
      "interview-preparation",
      "programming-interviews",
      "software-engineering",
      "study-plan"
    ],
    "owner": {
      "username": "jwasham",
      "profile_url": "https://github.com/jwasham"
    }
  },
  {
    "name": "GitHubDaily/GitHubDaily",
    "description": "\u575a\u6301\u5206\u4eab GitHub \u4e0a\u9ad8\u8d28\u91cf\u3001\u6709\u8da3\u5b9e\u7528\u7684\u5f00\u6e90\u6280\u672f\u6559\u7a0b\u3001\u5f00\u53d1\u8005\u5de5\u5177\u3001\u7f16\u7a0b\u7f51\u7ad9\u3001\u6280\u672f\u8d44\u8baf\u3002A list cool, interesting projects of GitHub.",
    "url": "https://github.com/GitHubDaily/GitHubDaily",
    "stars": 32839,
    "forks": 3593,
    "language": null,
    "last_updated": "2024-12-11T02:21:30Z",
    "topics": [
      "ai",
      "algorithms-and-data-structures",
      "backend",
      "developer-tools",
      "development",
      "frontend",
      "github",
      "java",
      "javascript",
      "kubernetes",
      "linux",
      "markdown",
      "open-source",
      "python",
      "tutorials",
      "web"
    ],
    "owner": {
      "username": "GitHubDaily",
      "profile_url": "https://github.com/GitHubDaily"
    }
  },
  {
    "name": "ashishps1/awesome-behavioral-interviews",
    "description": "Tips and resources to prepare for Behavioral interviews.",
    "url": "https://github.com/ashishps1/awesome-behavioral-interviews",
    "stars": 4992,
    "forks": 867,
    "language": null,
    "last_updated": "2024-12-10T11:59:04Z",
    "topics": [
      "behavioral-interviews",
      "interview-preparation",
      "interviews",
      "software-engineering"
    ],
    "owner": {
      "username": "ashishps1",
      "profile_url": "https://github.com/ashishps1"
    }
  },
  {
    "name": "ashishps1/awesome-leetcode-resources",
    "description": "Awesome LeetCode resources to learn Data Structures and Algorithms and prepare for Coding Interviews.",
    "url": "https://github.com/ashishps1/awesome-leetcode-resources",
    "stars": 6492,
    "forks": 1751,
    "language": "Java",
    "last_updated": "2024-12-11T00:03:32Z",
    "topics": [
      "algorithms",
      "coding",
      "data-structures",
      "leetcode",
      "leetcode-patterns"
    ],
    "owner": {
      "username": "ashishps1",
      "profile_url": "https://github.com/ashishps1"
    }
  },
  {
    "name": "ashishps1/awesome-low-level-design",
    "description": "Learn Low Level Design (LLD) and prepare for interviews using free resources.",
    "url": "https://github.com/ashishps1/awesome-low-level-design",
    "stars": 8993,
    "forks": 2332,
    "language": "Java",
    "last_updated": "2024-12-11T00:21:06Z",
    "topics": [
      "awesome",
      "design-patterns",
      "interview",
      "interview-practice",
      "interview-questions",
      "lld",
      "low-level-design",
      "machine-coding",
      "object-oriented-programming",
      "oops",
      "solid-principles",
      "uml"
    ],
    "owner": {
      "username": "ashishps1",
      "profile_url": "https://github.com/ashishps1"
    }
  },
  {
    "name": "ashishps1/awesome-system-design-resources",
    "description": "Learn System Design concepts and prepare for interviews using free resources.",
    "url": "https://github.com/ashishps1/awesome-system-design-resources",
    "stars": 18851,
    "forks": 4533,
    "language": "Java",
    "last_updated": "2024-12-11T03:36:22Z",
    "topics": [
      "awesome",
      "backend",
      "computer-science",
      "distributed-systems",
      "high-level-design",
      "hld",
      "interview",
      "interview-questions",
      "scalability",
      "system-design"
    ],
    "owner": {
      "username": "ashishps1",
      "profile_url": "https://github.com/ashishps1"
    }
  },
  {
    "name": "nashsu/FreeAskInternet",
    "description": "FreeAskInternet is a completely free, PRIVATE and LOCALLY running search aggregator & answer generate using MULTI LLMs, without GPU needed. The user can ask a question and the system will  make a multi engine search and combine the search result to LLM and generate the answer based on search results. It's all FREE to use. ",
    "url": "https://github.com/nashsu/FreeAskInternet",
    "stars": 8514,
    "forks": 898,
    "language": "Python",
    "last_updated": "2024-12-10T07:59:48Z",
    "topics": [],
    "owner": {
      "username": "nashsu",
      "profile_url": "https://github.com/nashsu"
    }
  },
  {
    "name": "RVC-Project/Retrieval-based-Voice-Conversion-WebUI",
    "description": "Easily train a good VC model with voice data <= 10 mins!",
    "url": "https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI",
    "stars": 25111,
    "forks": 3671,
    "language": "Python",
    "last_updated": "2024-12-11T03:18:09Z",
    "topics": [
      "audio-analysis",
      "change",
      "conversational-ai",
      "conversion",
      "converter",
      "retrieval-model",
      "retrieve-data",
      "rvc",
      "so-vits-svc",
      "sovits",
      "vc",
      "vits",
      "voice",
      "voice-conversion",
      "voice-converter",
      "voiceconversion"
    ],
    "owner": {
      "username": "RVC-Project",
      "profile_url": "https://github.com/RVC-Project"
    }
  },
  {
    "name": "systemdesign42/system-design",
    "description": "A resource to help you pass system design interview and become good at work \ud83d\udc47",
    "url": "https://github.com/systemdesign42/system-design",
    "stars": 13414,
    "forks": 1349,
    "language": null,
    "last_updated": "2024-12-11T03:04:29Z",
    "topics": [
      "computer-science",
      "development",
      "distributed-systems",
      "high-level-design",
      "interview-questions",
      "programming",
      "scalability",
      "software-engineering",
      "system-design",
      "system-design-interview"
    ],
    "owner": {
      "username": "systemdesign42",
      "profile_url": "https://github.com/systemdesign42"
    }
  },
  {
    "name": "sdg-1/data-team-handbook",
    "description": null,
    "url": "https://github.com/sdg-1/data-team-handbook",
    "stars": 597,
    "forks": 58,
    "language": null,
    "last_updated": "2024-12-11T04:11:02Z",
    "topics": [],
    "owner": {
      "username": "sdg-1",
      "profile_url": "https://github.com/sdg-1"
    }
  },
  {
    "name": "gispada/nestjs-python-kafka-microservices",
    "description": "Project to experiment with a microservices architecture based on Apache Kafka",
    "url": "https://github.com/gispada/nestjs-python-kafka-microservices",
    "stars": 20,
    "forks": 7,
    "language": "TypeScript",
    "last_updated": "2024-09-27T19:15:23Z",
    "topics": [
      "apache-kafka",
      "microservices",
      "nestjs",
      "python",
      "schema-registry"
    ],
    "owner": {
      "username": "gispada",
      "profile_url": "https://github.com/gispada"
    }
  },
  {
    "name": "All-Hands-AI/OpenHands",
    "description": "\ud83d\ude4c OpenHands: Code Less, Make More",
    "url": "https://github.com/All-Hands-AI/OpenHands",
    "stars": 38255,
    "forks": 4323,
    "language": "Python",
    "last_updated": "2024-12-11T03:52:58Z",
    "topics": [
      "agent",
      "artificial-intelligence",
      "chatgpt",
      "claude-ai",
      "cli",
      "developer-tools",
      "gpt",
      "llm",
      "openai"
    ],
    "owner": {
      "username": "All-Hands-AI",
      "profile_url": "https://github.com/All-Hands-AI"
    }
  },
  {
    "name": "stitionai/devika",
    "description": "Devika is an Agentic AI Software Engineer that can understand high-level human instructions, break them down into steps, research relevant information, and write code to achieve the given objective. Devika aims to be a competitive open-source alternative to Devin by Cognition AI.",
    "url": "https://github.com/stitionai/devika",
    "stars": 18561,
    "forks": 2412,
    "language": "Python",
    "last_updated": "2024-12-11T02:52:25Z",
    "topics": [],
    "owner": {
      "username": "stitionai",
      "profile_url": "https://github.com/stitionai"
    }
  },
  {
    "name": "StevenBlack/hosts",
    "description": "\ud83d\udd12 Consolidating and extending hosts files from several well-curated sources. Optionally pick extensions for porn, social media, and other categories.",
    "url": "https://github.com/StevenBlack/hosts",
    "stars": 27086,
    "forks": 2242,
    "language": "Python",
    "last_updated": "2024-12-11T02:54:01Z",
    "topics": [
      "ad-blocker",
      "anti-virus",
      "curated-sources",
      "gambling-filter",
      "hosts",
      "malware",
      "porn-filter",
      "pornblocker",
      "privacy",
      "protection",
      "python",
      "ransomware",
      "security",
      "social-media-filter",
      "trojans",
      "unified-hosts"
    ],
    "owner": {
      "username": "StevenBlack",
      "profile_url": "https://github.com/StevenBlack"
    }
  },
  {
    "name": "neetcode-gh/leetcode",
    "description": "Leetcode solutions",
    "url": "https://github.com/neetcode-gh/leetcode",
    "stars": 5720,
    "forks": 2334,
    "language": "JavaScript",
    "last_updated": "2024-12-11T03:01:47Z",
    "topics": [],
    "owner": {
      "username": "neetcode-gh",
      "profile_url": "https://github.com/neetcode-gh"
    }
  },
  {
    "name": "jasonppy/VoiceCraft",
    "description": "Zero-Shot Speech Editing and Text-to-Speech in the Wild",
    "url": "https://github.com/jasonppy/VoiceCraft",
    "stars": 7700,
    "forks": 751,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T03:43:57Z",
    "topics": [],
    "owner": {
      "username": "jasonppy",
      "profile_url": "https://github.com/jasonppy"
    }
  },
  {
    "name": "ifnesi/python-kafka-microservices",
    "description": "Implementing an Event Sourcing/CQRS microservices with Apache Kafka",
    "url": "https://github.com/ifnesi/python-kafka-microservices",
    "stars": 47,
    "forks": 19,
    "language": "Python",
    "last_updated": "2024-12-05T08:16:50Z",
    "topics": [
      "confluent",
      "confluent-cloud",
      "kafka",
      "microservices",
      "python"
    ],
    "owner": {
      "username": "ifnesi",
      "profile_url": "https://github.com/ifnesi"
    }
  },
  {
    "name": "lavague-ai/LaVague",
    "description": "Large Action Model framework to develop AI Web Agents",
    "url": "https://github.com/lavague-ai/LaVague",
    "stars": 5543,
    "forks": 510,
    "language": "Python",
    "last_updated": "2024-12-11T04:13:40Z",
    "topics": [
      "ai",
      "browser",
      "large-action-model",
      "llm",
      "oss",
      "rag"
    ],
    "owner": {
      "username": "lavague-ai",
      "profile_url": "https://github.com/lavague-ai"
    }
  },
  {
    "name": "huggingface/safetensors",
    "description": "Simple, safe way to store and distribute tensors",
    "url": "https://github.com/huggingface/safetensors",
    "stars": 2945,
    "forks": 201,
    "language": "Python",
    "last_updated": "2024-12-11T03:21:52Z",
    "topics": [],
    "owner": {
      "username": "huggingface",
      "profile_url": "https://github.com/huggingface"
    }
  },
  {
    "name": "facefusion/facefusion",
    "description": "Industry leading face manipulation platform",
    "url": "https://github.com/facefusion/facefusion",
    "stars": 20141,
    "forks": 3109,
    "language": "Python",
    "last_updated": "2024-12-11T04:07:43Z",
    "topics": [
      "ai",
      "deep-fake",
      "deepfake",
      "face-swap",
      "faceswap",
      "lip-sync",
      "lipsync",
      "webcam"
    ],
    "owner": {
      "username": "facefusion",
      "profile_url": "https://github.com/facefusion"
    }
  },
  {
    "name": "CrunchyData/postgres-operator",
    "description": "Production PostgreSQL for Kubernetes, from high availability Postgres clusters to full-scale database-as-a-service.",
    "url": "https://github.com/CrunchyData/postgres-operator",
    "stars": 3982,
    "forks": 597,
    "language": "Go",
    "last_updated": "2024-12-10T23:29:42Z",
    "topics": [
      "data-infrastructure",
      "database",
      "database-as-a-service",
      "database-management",
      "disaster-recovery",
      "high-availability",
      "kubernetes",
      "kubernetes-operator",
      "operator",
      "pgo",
      "postgres",
      "postgres-operator",
      "postgresql",
      "postgresql-clusters",
      "postgresql-metrics",
      "postgresql-monitoring"
    ],
    "owner": {
      "username": "CrunchyData",
      "profile_url": "https://github.com/CrunchyData"
    }
  },
  {
    "name": "friuns2/BlackFriday-GPTs-Prompts",
    "description": "List of free GPTs that doesn't require plus subscription ",
    "url": "https://github.com/friuns2/BlackFriday-GPTs-Prompts",
    "stars": 5963,
    "forks": 929,
    "language": null,
    "last_updated": "2024-12-11T01:18:12Z",
    "topics": [
      "agents",
      "agi",
      "ai",
      "anthropic",
      "artifacts",
      "awesome",
      "awesome-list",
      "bots",
      "chatbot",
      "chatgpt",
      "claude",
      "exploit",
      "gemini",
      "google",
      "gpt",
      "hack",
      "jailbreak",
      "openai",
      "prompts",
      "spam"
    ],
    "owner": {
      "username": "friuns2",
      "profile_url": "https://github.com/friuns2"
    }
  },
  {
    "name": "jacoblee93/fully-local-pdf-chatbot",
    "description": "Yes, it's another chat over documents implementation... but this one is entirely local!",
    "url": "https://github.com/jacoblee93/fully-local-pdf-chatbot",
    "stars": 1685,
    "forks": 311,
    "language": "TypeScript",
    "last_updated": "2024-12-10T10:28:38Z",
    "topics": [],
    "owner": {
      "username": "jacoblee93",
      "profile_url": "https://github.com/jacoblee93"
    }
  },
  {
    "name": "deepseek-ai/DeepSeek-VL",
    "description": "DeepSeek-VL: Towards Real-World Vision-Language Understanding",
    "url": "https://github.com/deepseek-ai/DeepSeek-VL",
    "stars": 2125,
    "forks": 201,
    "language": "Python",
    "last_updated": "2024-12-10T08:41:54Z",
    "topics": [
      "foundation-models",
      "vision-language-model",
      "vision-language-pretraining"
    ],
    "owner": {
      "username": "deepseek-ai",
      "profile_url": "https://github.com/deepseek-ai"
    }
  },
  {
    "name": "ai-boost/awesome-prompts",
    "description": "Curated list of chatgpt prompts from the top-rated GPTs in the GPTs Store. Prompt Engineering, prompt attack & prompt protect. Advanced Prompt Engineering papers.",
    "url": "https://github.com/ai-boost/awesome-prompts",
    "stars": 5388,
    "forks": 497,
    "language": null,
    "last_updated": "2024-12-11T02:12:18Z",
    "topics": [
      "awesome",
      "awesome-list",
      "chatgpt",
      "gpt4",
      "gpts",
      "gptstore",
      "papers",
      "prompt",
      "prompt-engineering"
    ],
    "owner": {
      "username": "ai-boost",
      "profile_url": "https://github.com/ai-boost"
    }
  },
  {
    "name": "fastapi/full-stack-fastapi-template",
    "description": "Full stack, modern web application template. Using FastAPI, React, SQLModel, PostgreSQL, Docker, GitHub Actions, automatic HTTPS and more.",
    "url": "https://github.com/fastapi/full-stack-fastapi-template",
    "stars": 28290,
    "forks": 5081,
    "language": "TypeScript",
    "last_updated": "2024-12-11T03:56:19Z",
    "topics": [
      "backend",
      "chakra-ui",
      "docker",
      "fastapi",
      "frontend",
      "json",
      "json-schema",
      "jwt",
      "letsencrypt",
      "openapi",
      "postgresql",
      "python",
      "react",
      "sqlmodel",
      "swagger",
      "tanstack-query",
      "tanstack-router",
      "traefik",
      "typescript"
    ],
    "owner": {
      "username": "fastapi",
      "profile_url": "https://github.com/fastapi"
    }
  },
  {
    "name": "milanm/DevOps-Roadmap",
    "description": "DevOps Roadmap for 2024. with learning resources",
    "url": "https://github.com/milanm/DevOps-Roadmap",
    "stars": 13090,
    "forks": 2106,
    "language": null,
    "last_updated": "2024-12-11T01:29:07Z",
    "topics": [
      "aws",
      "azure",
      "computer-science",
      "continous-delivery",
      "continuous-integration",
      "developer-roadmap",
      "devops",
      "devops-roadmap",
      "docker",
      "go",
      "grafana",
      "jira",
      "kubernetes",
      "linux",
      "prometheus",
      "python",
      "roadmap",
      "sre",
      "study-plan"
    ],
    "owner": {
      "username": "milanm",
      "profile_url": "https://github.com/milanm"
    }
  },
  {
    "name": "ototadana/sd-face-editor",
    "description": "Face Editor for Stable Diffusion",
    "url": "https://github.com/ototadana/sd-face-editor",
    "stars": 1032,
    "forks": 86,
    "language": "Python",
    "last_updated": "2024-11-30T18:39:01Z",
    "topics": [
      "stable-diffusion",
      "stable-diffusion-webui"
    ],
    "owner": {
      "username": "ototadana",
      "profile_url": "https://github.com/ototadana"
    }
  },
  {
    "name": "AI-Hypercomputer/maxtext",
    "description": "A simple, performant and scalable Jax LLM!",
    "url": "https://github.com/AI-Hypercomputer/maxtext",
    "stars": 1553,
    "forks": 301,
    "language": "Python",
    "last_updated": "2024-12-10T03:27:57Z",
    "topics": [
      "gpt",
      "large-language-models",
      "llm"
    ],
    "owner": {
      "username": "AI-Hypercomputer",
      "profile_url": "https://github.com/AI-Hypercomputer"
    }
  },
  {
    "name": "Fanghua-Yu/SUPIR",
    "description": "SUPIR aims at developing Practical Algorithms for Photo-Realistic Image Restoration In the Wild. Our new online demo is also released at suppixel.ai.",
    "url": "https://github.com/Fanghua-Yu/SUPIR",
    "stars": 4447,
    "forks": 388,
    "language": "Python",
    "last_updated": "2024-12-10T09:40:04Z",
    "topics": [
      "deep-learning",
      "diffusion-models",
      "llava",
      "pytorch",
      "pytorch-lightning",
      "restoration",
      "sdxl",
      "stable-diffusion",
      "super-resolution"
    ],
    "owner": {
      "username": "Fanghua-Yu",
      "profile_url": "https://github.com/Fanghua-Yu"
    }
  },
  {
    "name": "axolotl-ai-cloud/axolotl",
    "description": "Go ahead and axolotl questions",
    "url": "https://github.com/axolotl-ai-cloud/axolotl",
    "stars": 8063,
    "forks": 891,
    "language": "Python",
    "last_updated": "2024-12-10T21:25:30Z",
    "topics": [],
    "owner": {
      "username": "axolotl-ai-cloud",
      "profile_url": "https://github.com/axolotl-ai-cloud"
    }
  },
  {
    "name": "hatchet-dev/hatchet",
    "description": "A distributed, fault-tolerant task queue",
    "url": "https://github.com/hatchet-dev/hatchet",
    "stars": 4329,
    "forks": 165,
    "language": "Go",
    "last_updated": "2024-12-11T03:05:46Z",
    "topics": [
      "concurrency",
      "dag",
      "distributed",
      "distributed-systems",
      "durable-execution",
      "event-driven",
      "fastapi",
      "golang",
      "nodejs",
      "python",
      "queue",
      "typescript",
      "workflow-engine"
    ],
    "owner": {
      "username": "hatchet-dev",
      "profile_url": "https://github.com/hatchet-dev"
    }
  },
  {
    "name": "zijie0/HumanSystemOptimization",
    "description": "\u5065\u5eb7\u5b66\u4e60\u5230150\u5c81 - \u4eba\u4f53\u7cfb\u7edf\u8c03\u4f18\u4e0d\u5b8c\u5168\u6307\u5357",
    "url": "https://github.com/zijie0/HumanSystemOptimization",
    "stars": 13183,
    "forks": 966,
    "language": null,
    "last_updated": "2024-12-10T15:59:41Z",
    "topics": [],
    "owner": {
      "username": "zijie0",
      "profile_url": "https://github.com/zijie0"
    }
  },
  {
    "name": "Eladlev/AutoPrompt",
    "description": "A framework for prompt tuning using Intent-based Prompt Calibration ",
    "url": "https://github.com/Eladlev/AutoPrompt",
    "stars": 2254,
    "forks": 197,
    "language": "Python",
    "last_updated": "2024-12-11T03:15:43Z",
    "topics": [
      "prompt-engineering",
      "prompt-tuning",
      "synthetic-dataset-generation"
    ],
    "owner": {
      "username": "Eladlev",
      "profile_url": "https://github.com/Eladlev"
    }
  },
  {
    "name": "Lissy93/web-check",
    "description": "\ud83d\udd75\ufe0f\u200d\u2642\ufe0f All-in-one OSINT tool for analysing any website",
    "url": "https://github.com/Lissy93/web-check",
    "stars": 22688,
    "forks": 1747,
    "language": "TypeScript",
    "last_updated": "2024-12-10T21:40:21Z",
    "topics": [
      "osint",
      "privacy",
      "security",
      "security-tools",
      "sysadmin"
    ],
    "owner": {
      "username": "Lissy93",
      "profile_url": "https://github.com/Lissy93"
    }
  },
  {
    "name": "bigcode-project/starcoder2",
    "description": "Home of StarCoder2!",
    "url": "https://github.com/bigcode-project/starcoder2",
    "stars": 1803,
    "forks": 163,
    "language": "Python",
    "last_updated": "2024-12-10T18:47:05Z",
    "topics": [],
    "owner": {
      "username": "bigcode-project",
      "profile_url": "https://github.com/bigcode-project"
    }
  },
  {
    "name": "pydantic/FastUI",
    "description": "Build better UIs faster.",
    "url": "https://github.com/pydantic/FastUI",
    "stars": 8344,
    "forks": 321,
    "language": "Python",
    "last_updated": "2024-12-10T19:52:00Z",
    "topics": [
      "fastapi",
      "pydantic",
      "python",
      "react"
    ],
    "owner": {
      "username": "pydantic",
      "profile_url": "https://github.com/pydantic"
    }
  },
  {
    "name": "naver/dust3r",
    "description": "DUSt3R: Geometric 3D Vision Made Easy",
    "url": "https://github.com/naver/dust3r",
    "stars": 5488,
    "forks": 594,
    "language": "Python",
    "last_updated": "2024-12-11T03:20:11Z",
    "topics": [],
    "owner": {
      "username": "naver",
      "profile_url": "https://github.com/naver"
    }
  },
  {
    "name": "armankhondker/best-leetcode-resources",
    "description": "This repository contains resources for technical coding interviews. ",
    "url": "https://github.com/armankhondker/best-leetcode-resources",
    "stars": 3205,
    "forks": 326,
    "language": null,
    "last_updated": "2024-12-09T14:23:03Z",
    "topics": [
      "algorithms",
      "coding",
      "coding-interview",
      "data-structures",
      "interview-prep",
      "interview-problems",
      "leetcode",
      "leetcode-solutions",
      "software-engineering"
    ],
    "owner": {
      "username": "armankhondker",
      "profile_url": "https://github.com/armankhondker"
    }
  },
  {
    "name": "WongKinYiu/yolov9",
    "description": "Implementation of paper - YOLOv9: Learning What You Want to Learn Using Programmable Gradient Information",
    "url": "https://github.com/WongKinYiu/yolov9",
    "stars": 9046,
    "forks": 1440,
    "language": "Python",
    "last_updated": "2024-12-11T03:41:30Z",
    "topics": [
      "yolov9"
    ],
    "owner": {
      "username": "WongKinYiu",
      "profile_url": "https://github.com/WongKinYiu"
    }
  },
  {
    "name": "FujiwaraChoki/MoneyPrinterV2",
    "description": "Automate the process of making money online.",
    "url": "https://github.com/FujiwaraChoki/MoneyPrinterV2",
    "stars": 2441,
    "forks": 323,
    "language": "Python",
    "last_updated": "2024-12-09T17:10:31Z",
    "topics": [
      "automation",
      "cli",
      "json",
      "money",
      "outreach",
      "python",
      "twitter",
      "youtube"
    ],
    "owner": {
      "username": "FujiwaraChoki",
      "profile_url": "https://github.com/FujiwaraChoki"
    }
  },
  {
    "name": "charlax/professional-programming",
    "description": "A collection of learning resources for curious software engineers",
    "url": "https://github.com/charlax/professional-programming",
    "stars": 46839,
    "forks": 3734,
    "language": "Python",
    "last_updated": "2024-12-11T01:46:30Z",
    "topics": [
      "architecture",
      "computer-science",
      "concepts",
      "documentation",
      "engineer",
      "learning",
      "lessons-learned",
      "professional",
      "programmer",
      "programming-language",
      "read-articles",
      "scalability",
      "software-engineering"
    ],
    "owner": {
      "username": "charlax",
      "profile_url": "https://github.com/charlax"
    }
  },
  {
    "name": "google/magika",
    "description": "Detect file content types with deep learning",
    "url": "https://github.com/google/magika",
    "stars": 8213,
    "forks": 424,
    "language": "Rust",
    "last_updated": "2024-12-11T02:13:22Z",
    "topics": [
      "deep-learning",
      "filetype",
      "keras-classification-models",
      "keras-models",
      "mime-types"
    ],
    "owner": {
      "username": "google",
      "profile_url": "https://github.com/google"
    }
  },
  {
    "name": "iperov/DeepFaceLive",
    "description": "Real-time face swap for PC streaming or video calls",
    "url": "https://github.com/iperov/DeepFaceLive",
    "stars": 27094,
    "forks": 101,
    "language": "Python",
    "last_updated": "2024-12-11T01:22:15Z",
    "topics": [
      "deepfake",
      "faceswap",
      "machine-learning",
      "real-time",
      "streaming",
      "videocall",
      "webcam"
    ],
    "owner": {
      "username": "iperov",
      "profile_url": "https://github.com/iperov"
    }
  },
  {
    "name": "TaskingAI/TaskingAI",
    "description": "The open source platform for AI-native application development.",
    "url": "https://github.com/TaskingAI/TaskingAI",
    "stars": 6243,
    "forks": 321,
    "language": "Python",
    "last_updated": "2024-12-10T13:41:57Z",
    "topics": [
      "agent",
      "ai",
      "ai-native",
      "function-call",
      "generative-ai",
      "gpt",
      "langchain",
      "llm",
      "rag",
      "retrieval-augmented-generation",
      "vector"
    ],
    "owner": {
      "username": "TaskingAI",
      "profile_url": "https://github.com/TaskingAI"
    }
  },
  {
    "name": "goenning/google-indexing-script",
    "description": "Script to get your site indexed on Google in less than 48 hours",
    "url": "https://github.com/goenning/google-indexing-script",
    "stars": 7028,
    "forks": 486,
    "language": "TypeScript",
    "last_updated": "2024-12-10T19:43:04Z",
    "topics": [
      "google",
      "indexing",
      "seo"
    ],
    "owner": {
      "username": "goenning",
      "profile_url": "https://github.com/goenning"
    }
  },
  {
    "name": "AnswerDotAI/RAGatouille",
    "description": "Easily use and train state of the art late-interaction retrieval methods (ColBERT) in any RAG pipeline. Designed for modularity and ease-of-use, backed by research.",
    "url": "https://github.com/AnswerDotAI/RAGatouille",
    "stars": 3113,
    "forks": 211,
    "language": "Python",
    "last_updated": "2024-12-11T02:51:23Z",
    "topics": [],
    "owner": {
      "username": "AnswerDotAI",
      "profile_url": "https://github.com/AnswerDotAI"
    }
  },
  {
    "name": "trimstray/the-book-of-secret-knowledge",
    "description": "A collection of inspiring lists, manuals, cheatsheets, blogs, hacks, one-liners, cli/web tools and more.",
    "url": "https://github.com/trimstray/the-book-of-secret-knowledge",
    "stars": 150928,
    "forks": 9624,
    "language": null,
    "last_updated": "2024-12-11T04:05:32Z",
    "topics": [
      "awesome",
      "awesome-list",
      "bsd",
      "cheatsheets",
      "devops",
      "guidelines",
      "hacking",
      "hacks",
      "howtos",
      "linux",
      "lists",
      "manuals",
      "one-liners",
      "pentesters",
      "resources",
      "search-engines",
      "security",
      "security-researchers",
      "sysops"
    ],
    "owner": {
      "username": "trimstray",
      "profile_url": "https://github.com/trimstray"
    }
  },
  {
    "name": "Codium-ai/AlphaCodium",
    "description": "Official implementation for the paper: \"Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering\"\"",
    "url": "https://github.com/Codium-ai/AlphaCodium",
    "stars": 3692,
    "forks": 276,
    "language": "Python",
    "last_updated": "2024-12-11T03:33:09Z",
    "topics": [
      "broader-impacts",
      "code-generation",
      "flow-engineering",
      "paper-implementations",
      "state-of-the-art"
    ],
    "owner": {
      "username": "Codium-ai",
      "profile_url": "https://github.com/Codium-ai"
    }
  },
  {
    "name": "anshulc55/Jenkins_Upgradev3",
    "description": null,
    "url": "https://github.com/anshulc55/Jenkins_Upgradev3",
    "stars": 110,
    "forks": 2179,
    "language": "C#",
    "last_updated": "2024-12-08T23:35:48Z",
    "topics": [],
    "owner": {
      "username": "anshulc55",
      "profile_url": "https://github.com/anshulc55"
    }
  },
  {
    "name": "microsoft/TaskWeaver",
    "description": "A code-first agent framework for seamlessly planning and executing data analytics tasks. ",
    "url": "https://github.com/microsoft/TaskWeaver",
    "stars": 5386,
    "forks": 694,
    "language": "Python",
    "last_updated": "2024-12-10T21:47:59Z",
    "topics": [
      "agent",
      "ai-agents",
      "code-interpreter",
      "copilot",
      "data-analysis",
      "llm",
      "openai"
    ],
    "owner": {
      "username": "microsoft",
      "profile_url": "https://github.com/microsoft"
    }
  },
  {
    "name": "mingrammer/diagrams",
    "description": ":art: Diagram as Code for prototyping cloud system architectures",
    "url": "https://github.com/mingrammer/diagrams",
    "stars": 39914,
    "forks": 2555,
    "language": "Python",
    "last_updated": "2024-12-11T01:38:57Z",
    "topics": [
      "architecture",
      "diagram",
      "diagram-as-code",
      "graphviz"
    ],
    "owner": {
      "username": "mingrammer",
      "profile_url": "https://github.com/mingrammer"
    }
  },
  {
    "name": "instantX-research/InstantID",
    "description": "InstantID: Zero-shot Identity-Preserving Generation in Seconds \ud83d\udd25",
    "url": "https://github.com/instantX-research/InstantID",
    "stars": 11192,
    "forks": 818,
    "language": "Python",
    "last_updated": "2024-12-11T00:21:17Z",
    "topics": [],
    "owner": {
      "username": "instantX-research",
      "profile_url": "https://github.com/instantX-research"
    }
  },
  {
    "name": "gregorojstersek/resources-to-become-a-great-engineering-leader",
    "description": "List of books, blogs, newsletters and people!",
    "url": "https://github.com/gregorojstersek/resources-to-become-a-great-engineering-leader",
    "stars": 3454,
    "forks": 409,
    "language": null,
    "last_updated": "2024-12-11T03:47:44Z",
    "topics": [],
    "owner": {
      "username": "gregorojstersek",
      "profile_url": "https://github.com/gregorojstersek"
    }
  },
  {
    "name": "TencentARC/PhotoMaker",
    "description": "PhotoMaker [CVPR 2024]",
    "url": "https://github.com/TencentARC/PhotoMaker",
    "stars": 9616,
    "forks": 768,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T21:53:37Z",
    "topics": [],
    "owner": {
      "username": "TencentARC",
      "profile_url": "https://github.com/TencentARC"
    }
  },
  {
    "name": "RVC-Boss/GPT-SoVITS",
    "description": "1 min voice data can also be used to train a good TTS model! (few shot voice cloning)",
    "url": "https://github.com/RVC-Boss/GPT-SoVITS",
    "stars": 36768,
    "forks": 4185,
    "language": "Python",
    "last_updated": "2024-12-11T03:55:46Z",
    "topics": [
      "text-to-speech",
      "tts",
      "vits",
      "voice-clone",
      "voice-cloneai",
      "voice-cloning"
    ],
    "owner": {
      "username": "RVC-Boss",
      "profile_url": "https://github.com/RVC-Boss"
    }
  },
  {
    "name": "netease-youdao/QAnything",
    "description": "Question and Answer based on Anything.",
    "url": "https://github.com/netease-youdao/QAnything",
    "stars": 12024,
    "forks": 1170,
    "language": "Python",
    "last_updated": "2024-12-11T04:04:26Z",
    "topics": [],
    "owner": {
      "username": "netease-youdao",
      "profile_url": "https://github.com/netease-youdao"
    }
  },
  {
    "name": "dataelement/bisheng",
    "description": "BISHENG is an open LLM devops platform for next generation Enterprise AI applications. Powerful and comprehensive features include: GenAI workflow, RAG, Agent, Unified model management, Evaluation, SFT, Dataset Management, Enterprise-level System Management, Observability and more.",
    "url": "https://github.com/dataelement/bisheng",
    "stars": 8996,
    "forks": 1630,
    "language": "Python",
    "last_updated": "2024-12-11T02:46:22Z",
    "topics": [
      "agent",
      "ai",
      "chatbot",
      "enterprise",
      "finetune",
      "genai",
      "gpt",
      "langchian",
      "llama",
      "llm",
      "llmdevops",
      "llmops",
      "ocr",
      "openai",
      "orchestration",
      "python",
      "rag",
      "react",
      "sft",
      "workflow"
    ],
    "owner": {
      "username": "dataelement",
      "profile_url": "https://github.com/dataelement"
    }
  },
  {
    "name": "VikParuchuri/surya",
    "description": "OCR, layout analysis, reading order, table recognition in 90+ languages",
    "url": "https://github.com/VikParuchuri/surya",
    "stars": 14532,
    "forks": 919,
    "language": "Python",
    "last_updated": "2024-12-11T02:55:24Z",
    "topics": [],
    "owner": {
      "username": "VikParuchuri",
      "profile_url": "https://github.com/VikParuchuri"
    }
  },
  {
    "name": "MooreThreads/Moore-AnimateAnyone",
    "description": "Character Animation (AnimateAnyone, Face Reenactment)",
    "url": "https://github.com/MooreThreads/Moore-AnimateAnyone",
    "stars": 3220,
    "forks": 255,
    "language": "Python",
    "last_updated": "2024-12-10T01:16:33Z",
    "topics": [],
    "owner": {
      "username": "MooreThreads",
      "profile_url": "https://github.com/MooreThreads"
    }
  },
  {
    "name": "microsoft/autogen",
    "description": "A programming framework for agentic AI \ud83e\udd16 (PyPi: autogen-agentchat)",
    "url": "https://github.com/microsoft/autogen",
    "stars": 35682,
    "forks": 5157,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T04:06:10Z",
    "topics": [
      "agent-based-framework",
      "agent-oriented-programming",
      "agentic",
      "agentic-agi",
      "chat",
      "chat-application",
      "chatbot",
      "chatgpt",
      "gpt",
      "gpt-35-turbo",
      "gpt-4",
      "llm-agent",
      "llm-framework",
      "llm-inference",
      "llmops"
    ],
    "owner": {
      "username": "microsoft",
      "profile_url": "https://github.com/microsoft"
    }
  },
  {
    "name": "maybe-finance/maybe",
    "description": "The OS for your personal finances",
    "url": "https://github.com/maybe-finance/maybe",
    "stars": 34351,
    "forks": 2462,
    "language": "Ruby",
    "last_updated": "2024-12-11T04:11:58Z",
    "topics": [
      "finance",
      "hotwire",
      "personal-finance",
      "postgresql",
      "ruby",
      "ruby-on-rails",
      "stimulusjs",
      "turbo"
    ],
    "owner": {
      "username": "maybe-finance",
      "profile_url": "https://github.com/maybe-finance"
    }
  },
  {
    "name": "guoqincode/Open-AnimateAnyone",
    "description": "Unofficial Implementation of Animate Anyone",
    "url": "https://github.com/guoqincode/Open-AnimateAnyone",
    "stars": 2958,
    "forks": 239,
    "language": "Python",
    "last_updated": "2024-12-10T09:15:04Z",
    "topics": [],
    "owner": {
      "username": "guoqincode",
      "profile_url": "https://github.com/guoqincode"
    }
  },
  {
    "name": "gunnarmorling/1brc",
    "description": "1\ufe0f\u20e3\ud83d\udc1d\ud83c\udfce\ufe0f The One Billion Row Challenge -- A fun exploration of how quickly 1B rows from a text file can be aggregated with Java",
    "url": "https://github.com/gunnarmorling/1brc",
    "stars": 6521,
    "forks": 1940,
    "language": "Java",
    "last_updated": "2024-12-11T03:39:26Z",
    "topics": [
      "1brc",
      "challenges"
    ],
    "owner": {
      "username": "gunnarmorling",
      "profile_url": "https://github.com/gunnarmorling"
    }
  },
  {
    "name": "Meroser/IPTV",
    "description": "\u6df1\u5ea6\u5b9a\u5236\u5c5e\u4e8e\u81ea\u5df1\u7684EPG\u8282\u76ee\u9884\u544a\u3001\u9ad8\u6e05\u53f0\u6807",
    "url": "https://github.com/Meroser/IPTV",
    "stars": 3855,
    "forks": 589,
    "language": null,
    "last_updated": "2024-12-10T02:32:53Z",
    "topics": [],
    "owner": {
      "username": "Meroser",
      "profile_url": "https://github.com/Meroser"
    }
  },
  {
    "name": "DopplerHQ/awesome-interview-questions",
    "description": ":octocat: A curated awesome list of lists of interview questions. Feel free to contribute! :mortar_board: ",
    "url": "https://github.com/DopplerHQ/awesome-interview-questions",
    "stars": 71878,
    "forks": 8902,
    "language": null,
    "last_updated": "2024-12-11T03:22:06Z",
    "topics": [
      "android-interview-questions",
      "angularjs-interview-questions",
      "awesome",
      "awesome-list",
      "awesomeness",
      "interview-practice",
      "interview-questions",
      "interviewing",
      "javascript",
      "javascript-interview-questions",
      "list",
      "python-interview-questions",
      "rails-interview",
      "ruby"
    ],
    "owner": {
      "username": "DopplerHQ",
      "profile_url": "https://github.com/DopplerHQ"
    }
  },
  {
    "name": "hahwul/DevSecOps",
    "description": "\u267e\ufe0f Collection and Roadmap for everyone who wants DevSecOps. Hope your DevOps are more safe \ud83d\ude0e",
    "url": "https://github.com/hahwul/DevSecOps",
    "stars": 1817,
    "forks": 367,
    "language": "Go",
    "last_updated": "2024-12-10T09:43:17Z",
    "topics": [
      "awesome-list",
      "collections",
      "devops",
      "devsecops",
      "roadmap",
      "security",
      "tools"
    ],
    "owner": {
      "username": "hahwul",
      "profile_url": "https://github.com/hahwul"
    }
  },
  {
    "name": "hiteshchoudhary/chai-backend",
    "description": "A video series on chai aur code youtube channel",
    "url": "https://github.com/hiteshchoudhary/chai-backend",
    "stars": 5439,
    "forks": 813,
    "language": "JavaScript",
    "last_updated": "2024-12-10T20:46:13Z",
    "topics": [],
    "owner": {
      "username": "hiteshchoudhary",
      "profile_url": "https://github.com/hiteshchoudhary"
    }
  },
  {
    "name": "aaamoon/copilot-gpt4-service",
    "description": "Convert Github Copilot to ChatGPT",
    "url": "https://github.com/aaamoon/copilot-gpt4-service",
    "stars": 9084,
    "forks": 838,
    "language": "Go",
    "last_updated": "2024-12-03T23:20:33Z",
    "topics": [
      "chatgpt",
      "copilot",
      "gpt4",
      "openai"
    ],
    "owner": {
      "username": "aaamoon",
      "profile_url": "https://github.com/aaamoon"
    }
  },
  {
    "name": "bleedline/Awesome-gptlike-shellsite",
    "description": "\u6df1\u5165\u63a2\u7d22\u7cbe\u9009\u7684\u5957\u58f3\u7ad9\u548c\u5fc5\u5907API\u8d44\u6e90\u3002\u672c\u6587\u4e3a\u521d\u5b66\u8005\u548c\u7ecf\u9a8c\u4e30\u5bcc\u7684\u8fd0\u8425\u8005\u63d0\u4f9b\u4e00\u7ad9\u5f0f\u6307\u5357\uff0c\u6db5\u76d6\u5e38\u89c1\u95ee\u9898\u89e3\u7b54\u548c\u57fa\u7840\u653b\u7565\uff0c\u52a9\u60a8\u8fc8\u5411\u5957\u58f3\u7ad9\u526f\u4e1a\u6210\u529f\u4e4b\u8def\u3002Dive into a curated selection of shell sites and essential APIs. This article offers a comprehensive guide for both beginners and seasoned operators, covering FAQs and basic strategies to propel you towards success in your shell site side hustle.",
    "url": "https://github.com/bleedline/Awesome-gptlike-shellsite",
    "stars": 2044,
    "forks": 223,
    "language": null,
    "last_updated": "2024-12-06T02:18:12Z",
    "topics": [],
    "owner": {
      "username": "bleedline",
      "profile_url": "https://github.com/bleedline"
    }
  },
  {
    "name": "hiroi-sora/Umi-OCR",
    "description": "OCR software, free and offline. \u5f00\u6e90\u3001\u514d\u8d39\u7684\u79bb\u7ebfOCR\u8f6f\u4ef6\u3002\u652f\u6301\u622a\u5c4f/\u6279\u91cf\u5bfc\u5165\u56fe\u7247\uff0cPDF\u6587\u6863\u8bc6\u522b\uff0c\u6392\u9664\u6c34\u5370/\u9875\u7709\u9875\u811a\uff0c\u626b\u63cf/\u751f\u6210\u4e8c\u7ef4\u7801\u3002\u5185\u7f6e\u591a\u56fd\u8bed\u8a00\u5e93\u3002",
    "url": "https://github.com/hiroi-sora/Umi-OCR",
    "stars": 27855,
    "forks": 2778,
    "language": "Python",
    "last_updated": "2024-12-11T03:21:21Z",
    "topics": [
      "ocr",
      "ocr-python",
      "paddleocr",
      "qml",
      "qt",
      "screenshot",
      "umi-ocr"
    ],
    "owner": {
      "username": "hiroi-sora",
      "profile_url": "https://github.com/hiroi-sora"
    }
  },
  {
    "name": "ali-vilab/dreamtalk",
    "description": "Official implementations for paper: DreamTalk: When Expressive Talking Head Generation Meets Diffusion Probabilistic Models",
    "url": "https://github.com/ali-vilab/dreamtalk",
    "stars": 1637,
    "forks": 200,
    "language": "Python",
    "last_updated": "2024-12-10T05:48:03Z",
    "topics": [
      "audio-visual-learning",
      "face-animation",
      "talking-head",
      "video-generation"
    ],
    "owner": {
      "username": "ali-vilab",
      "profile_url": "https://github.com/ali-vilab"
    }
  },
  {
    "name": "GrowingGit/GitHub-English-Top-Charts",
    "description": "Help you discover excellent English projects and get rid of disturbing by other spoken language.",
    "url": "https://github.com/GrowingGit/GitHub-English-Top-Charts",
    "stars": 2112,
    "forks": 197,
    "language": "Python",
    "last_updated": "2024-11-22T15:10:17Z",
    "topics": [],
    "owner": {
      "username": "GrowingGit",
      "profile_url": "https://github.com/GrowingGit"
    }
  },
  {
    "name": "myshell-ai/OpenVoice",
    "description": "Instant voice cloning by MIT and MyShell.",
    "url": "https://github.com/myshell-ai/OpenVoice",
    "stars": 30038,
    "forks": 2961,
    "language": "Python",
    "last_updated": "2024-12-11T03:26:26Z",
    "topics": [
      "text-to-speech",
      "tts",
      "voice-clone",
      "zero-shot-tts"
    ],
    "owner": {
      "username": "myshell-ai",
      "profile_url": "https://github.com/myshell-ai"
    }
  },
  {
    "name": "tyxsspa/AnyText",
    "description": "Official implementation code of the paper <AnyText: Multilingual Visual Text Generation And Editing>",
    "url": "https://github.com/tyxsspa/AnyText",
    "stars": 4404,
    "forks": 285,
    "language": "Python",
    "last_updated": "2024-12-11T00:58:29Z",
    "topics": [],
    "owner": {
      "username": "tyxsspa",
      "profile_url": "https://github.com/tyxsspa"
    }
  },
  {
    "name": "jordan-cutler/path-to-senior-engineer-handbook",
    "description": "All the resources you need to get to Senior Engineer and beyond",
    "url": "https://github.com/jordan-cutler/path-to-senior-engineer-handbook",
    "stars": 13896,
    "forks": 1253,
    "language": null,
    "last_updated": "2024-12-11T03:32:01Z",
    "topics": [
      "awesome",
      "career",
      "career-growth",
      "path-to-senior",
      "senior-engineer",
      "software-developer"
    ],
    "owner": {
      "username": "jordan-cutler",
      "profile_url": "https://github.com/jordan-cutler"
    }
  },
  {
    "name": "jianchang512/clone-voice",
    "description": "A sound cloning tool with a web interface, using your voice or any sound to record audio / \u4e00\u4e2a\u5e26web\u754c\u9762\u7684\u58f0\u97f3\u514b\u9686\u5de5\u5177\uff0c\u4f7f\u7528\u4f60\u7684\u97f3\u8272\u6216\u4efb\u610f\u58f0\u97f3\u6765\u5f55\u5236\u97f3\u9891",
    "url": "https://github.com/jianchang512/clone-voice",
    "stars": 7738,
    "forks": 799,
    "language": "Python",
    "last_updated": "2024-12-11T02:56:15Z",
    "topics": [
      "clonevoice",
      "speech-analysis",
      "sts",
      "tts",
      "voice-assistant"
    ],
    "owner": {
      "username": "jianchang512",
      "profile_url": "https://github.com/jianchang512"
    }
  },
  {
    "name": "iusztinpaul/hands-on-llms",
    "description": "\ud83e\udd96 \ud835\udddf\ud835\uddf2\ud835\uddee\ud835\uddff\ud835\uddfb about \ud835\udddf\ud835\udddf\ud835\udde0\ud835\ude00, \ud835\udddf\ud835\udddf\ud835\udde0\ud835\udde2\ud835\uddfd\ud835\ude00, and \ud835\ude03\ud835\uddf2\ud835\uddf0\ud835\ude01\ud835\uddfc\ud835\uddff \ud835\uddd7\ud835\uddd5\ud835\ude00 for free by designing, training, and deploying a real-time financial advisor LLM system ~ \ud835\ude34\ud835\ude30\ud835\ude36\ud835\ude33\ud835\ude24\ud835\ude26 \ud835\ude24\ud835\ude30\ud835\ude25\ud835\ude26 + \ud835\ude37\ud835\ude2a\ud835\ude25\ud835\ude26\ud835\ude30 & \ud835\ude33\ud835\ude26\ud835\ude22\ud835\ude25\ud835\ude2a\ud835\ude2f\ud835\ude28 \ud835\ude2e\ud835\ude22\ud835\ude35\ud835\ude26\ud835\ude33\ud835\ude2a\ud835\ude22\ud835\ude2d\ud835\ude34",
    "url": "https://github.com/iusztinpaul/hands-on-llms",
    "stars": 3146,
    "forks": 488,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T15:55:47Z",
    "topics": [
      "3-pipeline-design",
      "aws",
      "beam",
      "bytewax",
      "cicd",
      "comet-ml",
      "docker",
      "fine-tuning",
      "generative-ai",
      "huggingface",
      "langchain",
      "llmops",
      "llms",
      "mlops",
      "qdrant",
      "qlora",
      "streaming",
      "transformers"
    ],
    "owner": {
      "username": "iusztinpaul",
      "profile_url": "https://github.com/iusztinpaul"
    }
  },
  {
    "name": "Coder-World04/Complete-System-Design",
    "description": "This repository contains everything you need to become proficient in System Design",
    "url": "https://github.com/Coder-World04/Complete-System-Design",
    "stars": 4026,
    "forks": 523,
    "language": null,
    "last_updated": "2024-12-10T14:53:54Z",
    "topics": [],
    "owner": {
      "username": "Coder-World04",
      "profile_url": "https://github.com/Coder-World04"
    }
  },
  {
    "name": "kilimchoi/engineering-blogs",
    "description": "A curated list of engineering blogs",
    "url": "https://github.com/kilimchoi/engineering-blogs",
    "stars": 31856,
    "forks": 1642,
    "language": "Ruby",
    "last_updated": "2024-12-11T01:41:53Z",
    "topics": [
      "engineering-blogs",
      "lists",
      "programming-blogs",
      "software-development",
      "tech"
    ],
    "owner": {
      "username": "kilimchoi",
      "profile_url": "https://github.com/kilimchoi"
    }
  },
  {
    "name": "mnotgod96/AppAgent",
    "description": "AppAgent: Multimodal Agents as Smartphone Users, an LLM-based multimodal agent framework designed to operate smartphone apps.",
    "url": "https://github.com/mnotgod96/AppAgent",
    "stars": 5221,
    "forks": 564,
    "language": "Python",
    "last_updated": "2024-12-11T03:03:59Z",
    "topics": [
      "agent",
      "chatgpt",
      "generative-ai",
      "gpt4",
      "gpt4v",
      "llm"
    ],
    "owner": {
      "username": "mnotgod96",
      "profile_url": "https://github.com/mnotgod96"
    }
  },
  {
    "name": "Pythagora-io/gpt-pilot",
    "description": "The first real AI developer",
    "url": "https://github.com/Pythagora-io/gpt-pilot",
    "stars": 32030,
    "forks": 3232,
    "language": "Python",
    "last_updated": "2024-12-11T02:21:41Z",
    "topics": [
      "ai",
      "codegen",
      "coding-assistant",
      "developer-tools",
      "gpt-4",
      "research-project"
    ],
    "owner": {
      "username": "Pythagora-io",
      "profile_url": "https://github.com/Pythagora-io"
    }
  },
  {
    "name": "cumulo-autumn/StreamDiffusion",
    "description": "StreamDiffusion: A Pipeline-Level Solution for Real-Time Interactive Generation",
    "url": "https://github.com/cumulo-autumn/StreamDiffusion",
    "stars": 9784,
    "forks": 706,
    "language": "Python",
    "last_updated": "2024-12-10T07:02:20Z",
    "topics": [],
    "owner": {
      "username": "cumulo-autumn",
      "profile_url": "https://github.com/cumulo-autumn"
    }
  },
  {
    "name": "jlevy/the-art-of-command-line",
    "description": "Master the command line, in one page",
    "url": "https://github.com/jlevy/the-art-of-command-line",
    "stars": 153979,
    "forks": 14580,
    "language": null,
    "last_updated": "2024-12-11T03:25:44Z",
    "topics": [
      "bash",
      "documentation",
      "linux",
      "macos",
      "unix",
      "windows"
    ],
    "owner": {
      "username": "jlevy",
      "profile_url": "https://github.com/jlevy"
    }
  },
  {
    "name": "ali-vilab/VGen",
    "description": "Official repo for VGen: a holistic video generation ecosystem for video generation building on diffusion models",
    "url": "https://github.com/ali-vilab/VGen",
    "stars": 2998,
    "forks": 265,
    "language": "Python",
    "last_updated": "2024-12-10T11:35:04Z",
    "topics": [
      "diffusion-models",
      "video-synthesis"
    ],
    "owner": {
      "username": "ali-vilab",
      "profile_url": "https://github.com/ali-vilab"
    }
  },
  {
    "name": "onyx-dot-app/onyx",
    "description": "Gen-AI Chat for Teams - Think ChatGPT if it had access to your team's unique knowledge.",
    "url": "https://github.com/onyx-dot-app/onyx",
    "stars": 10882,
    "forks": 1383,
    "language": "Python",
    "last_updated": "2024-12-11T03:58:50Z",
    "topics": [
      "ai-chat",
      "chatgpt",
      "enterprise-search",
      "gen-ai",
      "information-retrieval",
      "nextjs",
      "python",
      "rag"
    ],
    "owner": {
      "username": "onyx-dot-app",
      "profile_url": "https://github.com/onyx-dot-app"
    }
  },
  {
    "name": "ruanyf/weekly",
    "description": "\u79d1\u6280\u7231\u597d\u8005\u5468\u520a\uff0c\u6bcf\u5468\u4e94\u53d1\u5e03",
    "url": "https://github.com/ruanyf/weekly",
    "stars": 49481,
    "forks": 2945,
    "language": null,
    "last_updated": "2024-12-11T04:03:58Z",
    "topics": [],
    "owner": {
      "username": "ruanyf",
      "profile_url": "https://github.com/ruanyf"
    }
  },
  {
    "name": "bytedance/ImageDream",
    "description": "The code releasing for https://image-dream.github.io/",
    "url": "https://github.com/bytedance/ImageDream",
    "stars": 749,
    "forks": 34,
    "language": "Python",
    "last_updated": "2024-12-10T02:39:56Z",
    "topics": [
      "research"
    ],
    "owner": {
      "username": "bytedance",
      "profile_url": "https://github.com/bytedance"
    }
  },
  {
    "name": "bleedline/aimoneyhunter",
    "description": "ai\u526f\u4e1a\u8d5a\u94b1\u5927\u96c6\u5408\uff0c\u6559\u4f60\u5982\u4f55\u5229\u7528ai\u505a\u4e00\u4e9b\u526f\u4e1a\u9879\u76ee\uff0c\u8d5a\u53d6\u66f4\u591a\u989d\u5916\u6536\u76ca\u3002The Ultimate Guide to Making Money with AI Side Hustles: Learn how to leverage AI for some cool side gigs and rake in some extra cash. Check out the English version for more insights.",
    "url": "https://github.com/bleedline/aimoneyhunter",
    "stars": 13826,
    "forks": 1258,
    "language": null,
    "last_updated": "2024-12-11T03:51:07Z",
    "topics": [],
    "owner": {
      "username": "bleedline",
      "profile_url": "https://github.com/bleedline"
    }
  },
  {
    "name": "swisskyrepo/PayloadsAllTheThings",
    "description": "A list of useful payloads and bypass for Web Application Security and Pentest/CTF",
    "url": "https://github.com/swisskyrepo/PayloadsAllTheThings",
    "stars": 61863,
    "forks": 14764,
    "language": "Python",
    "last_updated": "2024-12-11T02:51:47Z",
    "topics": [
      "bounty",
      "bugbounty",
      "bypass",
      "cheatsheet",
      "enumeration",
      "hacking",
      "hacktoberfest",
      "methodology",
      "payload",
      "payloads",
      "penetration-testing",
      "pentest",
      "privilege-escalation",
      "redteam",
      "security",
      "vulnerability",
      "web-application"
    ],
    "owner": {
      "username": "swisskyrepo",
      "profile_url": "https://github.com/swisskyrepo"
    }
  },
  {
    "name": "sweepai/sweep",
    "description": "Sweep: open-source AI-powered Software Developer for small features and bug fixes.",
    "url": "https://github.com/sweepai/sweep",
    "stars": 7473,
    "forks": 432,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T02:34:05Z",
    "topics": [
      "ai",
      "ai-developer",
      "ai-softwar",
      "ai-software",
      "code-assistant",
      "code-search",
      "developer-tools",
      "github-app",
      "gpt-4"
    ],
    "owner": {
      "username": "sweepai",
      "profile_url": "https://github.com/sweepai"
    }
  },
  {
    "name": "cby-chen/Kubernetes",
    "description": "kubernetes (k8s) \u4e8c\u8fdb\u5236\u9ad8\u53ef\u7528\u5b89\u88c5\uff0cBinary installation of kubernetes (k8s)  --- \u5f00\u6e90\u4e0d\u6613\uff0c\u5e2e\u5fd9\u70b9\u4e2astar\uff0c\u8c22\u8c22\u4e86\ud83c\udf39",
    "url": "https://github.com/cby-chen/Kubernetes",
    "stars": 932,
    "forks": 326,
    "language": "Shell",
    "last_updated": "2024-12-10T07:36:10Z",
    "topics": [
      "binary",
      "calico",
      "centos",
      "containerd",
      "coredns",
      "dashboard",
      "docker",
      "etcd",
      "etcd-cluster",
      "ingress",
      "install",
      "ipv4",
      "ipv6",
      "ipvs",
      "k8s",
      "kernel",
      "kernel-module",
      "kubernetes",
      "metrics-server",
      "ubuntu"
    ],
    "owner": {
      "username": "cby-chen",
      "profile_url": "https://github.com/cby-chen"
    }
  },
  {
    "name": "alifiroozi80/ansible-infrastructure",
    "description": "Deploy a whole infrastructure with Ansible!",
    "url": "https://github.com/alifiroozi80/ansible-infrastructure",
    "stars": 16,
    "forks": 6,
    "language": null,
    "last_updated": "2024-03-24T13:29:36Z",
    "topics": [
      "ansible",
      "haproxy",
      "jenkins",
      "kubernetes",
      "mattermost",
      "teleport",
      "vpn"
    ],
    "owner": {
      "username": "alifiroozi80",
      "profile_url": "https://github.com/alifiroozi80"
    }
  },
  {
    "name": "cookeem/kubeadm-ha",
    "description": "\u901a\u8fc7kubeadm\u5b89\u88c5kubernetes\u9ad8\u53ef\u7528\u96c6\u7fa4\uff0c\u4f7f\u7528docker/containerd\u5bb9\u5668\u8fd0\u884c\u65f6\uff0c\u9002\u7528v1.24.x\u4ee5\u4e0a\u7248\u672c",
    "url": "https://github.com/cookeem/kubeadm-ha",
    "stars": 678,
    "forks": 275,
    "language": null,
    "last_updated": "2024-11-11T01:53:11Z",
    "topics": [
      "cluster",
      "containerd",
      "ha",
      "high-availability",
      "istio",
      "keepalived",
      "kubeadm",
      "kubernetes",
      "nginx",
      "prometheus",
      "traefik"
    ],
    "owner": {
      "username": "cookeem",
      "profile_url": "https://github.com/cookeem"
    }
  },
  {
    "name": "meta-llama/PurpleLlama",
    "description": "Set of tools to assess and improve LLM security.",
    "url": "https://github.com/meta-llama/PurpleLlama",
    "stars": 2783,
    "forks": 455,
    "language": "Python",
    "last_updated": "2024-12-10T13:49:04Z",
    "topics": [],
    "owner": {
      "username": "meta-llama",
      "profile_url": "https://github.com/meta-llama"
    }
  },
  {
    "name": "microsoft/kubernetes-learning-path",
    "description": "https://azure.microsoft.com/en-us/resources/kubernetes-learning-path/",
    "url": "https://github.com/microsoft/kubernetes-learning-path",
    "stars": 377,
    "forks": 129,
    "language": null,
    "last_updated": "2024-12-05T06:58:56Z",
    "topics": [],
    "owner": {
      "username": "microsoft",
      "profile_url": "https://github.com/microsoft"
    }
  },
  {
    "name": "diegolnasc/kubernetes-best-practices",
    "description": "A cookbook with the best practices to working with kubernetes.",
    "url": "https://github.com/diegolnasc/kubernetes-best-practices",
    "stars": 1431,
    "forks": 76,
    "language": null,
    "last_updated": "2024-12-06T15:44:34Z",
    "topics": [
      "container",
      "documentation",
      "kubernetes"
    ],
    "owner": {
      "username": "diegolnasc",
      "profile_url": "https://github.com/diegolnasc"
    }
  },
  {
    "name": "learnk8s/kubernetes-production-best-practices",
    "description": "A checklist of Kubernetes best practices to help you release to production",
    "url": "https://github.com/learnk8s/kubernetes-production-best-practices",
    "stars": 1077,
    "forks": 210,
    "language": null,
    "last_updated": "2024-12-10T20:25:48Z",
    "topics": [
      "best-practices",
      "kubernetes"
    ],
    "owner": {
      "username": "learnk8s",
      "profile_url": "https://github.com/learnk8s"
    }
  },
  {
    "name": "LouisShark/chatgpt_system_prompt",
    "description": "A collection of GPT system prompts and various prompt injection/leaking knowledge.",
    "url": "https://github.com/LouisShark/chatgpt_system_prompt",
    "stars": 8360,
    "forks": 1218,
    "language": "HTML",
    "last_updated": "2024-12-11T03:43:43Z",
    "topics": [
      "gpt",
      "prompt",
      "prompt-engineering"
    ],
    "owner": {
      "username": "LouisShark",
      "profile_url": "https://github.com/LouisShark"
    }
  },
  {
    "name": "florinpop17/app-ideas",
    "description": "A Collection of application ideas which can be used to improve your coding skills.",
    "url": "https://github.com/florinpop17/app-ideas",
    "stars": 81203,
    "forks": 9610,
    "language": null,
    "last_updated": "2024-12-11T02:55:43Z",
    "topics": [
      "applications",
      "coding",
      "codingchallenges",
      "css",
      "hacktoberfest",
      "html",
      "ideas",
      "javascript",
      "practice"
    ],
    "owner": {
      "username": "florinpop17",
      "profile_url": "https://github.com/florinpop17"
    }
  },
  {
    "name": "linexjlin/GPTs",
    "description": "leaked prompts of GPTs",
    "url": "https://github.com/linexjlin/GPTs",
    "stars": 28953,
    "forks": 3925,
    "language": null,
    "last_updated": "2024-12-11T02:18:21Z",
    "topics": [],
    "owner": {
      "username": "linexjlin",
      "profile_url": "https://github.com/linexjlin"
    }
  },
  {
    "name": "protectai/ai-exploits",
    "description": "A collection of real world AI/ML exploits for responsibly disclosed vulnerabilities ",
    "url": "https://github.com/protectai/ai-exploits",
    "stars": 1452,
    "forks": 115,
    "language": "Python",
    "last_updated": "2024-12-09T04:47:02Z",
    "topics": [],
    "owner": {
      "username": "protectai",
      "profile_url": "https://github.com/protectai"
    }
  },
  {
    "name": "abi/screenshot-to-code",
    "description": "Drop in a screenshot and convert it to clean code (HTML/Tailwind/React/Vue)",
    "url": "https://github.com/abi/screenshot-to-code",
    "stars": 65241,
    "forks": 7941,
    "language": "Python",
    "last_updated": "2024-12-11T03:58:17Z",
    "topics": [],
    "owner": {
      "username": "abi",
      "profile_url": "https://github.com/abi"
    }
  },
  {
    "name": "disler/multi-agent-postgres-data-analytics",
    "description": "The way we interact with our data is changing.",
    "url": "https://github.com/disler/multi-agent-postgres-data-analytics",
    "stars": 792,
    "forks": 156,
    "language": "Python",
    "last_updated": "2024-12-10T20:42:48Z",
    "topics": [],
    "owner": {
      "username": "disler",
      "profile_url": "https://github.com/disler"
    }
  },
  {
    "name": "chenzomi12/AISystem",
    "description": "AISystem \u4e3b\u8981\u662f\u6307AI\u7cfb\u7edf\uff0c\u5305\u62ecAI\u82af\u7247\u3001AI\u7f16\u8bd1\u5668\u3001AI\u63a8\u7406\u548c\u8bad\u7ec3\u6846\u67b6\u7b49AI\u5168\u6808\u5e95\u5c42\u6280\u672f",
    "url": "https://github.com/chenzomi12/AISystem",
    "stars": 11522,
    "forks": 1666,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T03:47:21Z",
    "topics": [
      "ai",
      "aiinfra",
      "aisys",
      "dlsys",
      "mlsys"
    ],
    "owner": {
      "username": "chenzomi12",
      "profile_url": "https://github.com/chenzomi12"
    }
  },
  {
    "name": "Anil-matcha/Awesome-GPT-Store",
    "description": "Custom GPT Store - A collection of major GPTS available in public",
    "url": "https://github.com/Anil-matcha/Awesome-GPT-Store",
    "stars": 1448,
    "forks": 161,
    "language": null,
    "last_updated": "2024-12-10T20:56:32Z",
    "topics": [
      "agentgpt",
      "ai-agents",
      "awesome-gpt-store",
      "awesome-gpts",
      "awesome-list",
      "chatgpt",
      "chatgpt-api",
      "chatgpt-plugins",
      "customgpt",
      "gpt-4",
      "gpt-store",
      "gpts",
      "gptshowcas",
      "gptslist",
      "gptstore"
    ],
    "owner": {
      "username": "Anil-matcha",
      "profile_url": "https://github.com/Anil-matcha"
    }
  },
  {
    "name": "taranjeet/awesome-gpts",
    "description": "Collection of all the GPTs created by the community",
    "url": "https://github.com/taranjeet/awesome-gpts",
    "stars": 1258,
    "forks": 85,
    "language": null,
    "last_updated": "2024-12-09T13:47:35Z",
    "topics": [
      "awesome",
      "awesome-list",
      "chatgpt",
      "gpts",
      "gptstore",
      "lists",
      "resources"
    ],
    "owner": {
      "username": "taranjeet",
      "profile_url": "https://github.com/taranjeet"
    }
  },
  {
    "name": "SawyerHood/draw-a-ui",
    "description": "Draw a mockup and generate html for it",
    "url": "https://github.com/SawyerHood/draw-a-ui",
    "stars": 13320,
    "forks": 1604,
    "language": "TypeScript",
    "last_updated": "2024-12-11T01:46:56Z",
    "topics": [
      "ai",
      "gpt",
      "openai",
      "react",
      "typescript"
    ],
    "owner": {
      "username": "SawyerHood",
      "profile_url": "https://github.com/SawyerHood"
    }
  },
  {
    "name": "Decron/Whitebox-Code-GPT",
    "description": "Repository of instructions for Programming-specific GPT models",
    "url": "https://github.com/Decron/Whitebox-Code-GPT",
    "stars": 206,
    "forks": 20,
    "language": "Dart",
    "last_updated": "2024-12-09T05:18:35Z",
    "topics": [
      "ai",
      "chatbot",
      "flutter",
      "gpt",
      "llm",
      "programming-languages",
      "python",
      "tools"
    ],
    "owner": {
      "username": "Decron",
      "profile_url": "https://github.com/Decron"
    }
  },
  {
    "name": "stas00/ml-engineering",
    "description": "Machine Learning Engineering Open Book",
    "url": "https://github.com/stas00/ml-engineering",
    "stars": 11957,
    "forks": 726,
    "language": "Python",
    "last_updated": "2024-12-11T02:30:08Z",
    "topics": [
      "ai",
      "large-language-models",
      "llm",
      "machine-learning",
      "machine-learning-engineering",
      "mlops",
      "pytorch",
      "scalability",
      "slurm",
      "transformers"
    ],
    "owner": {
      "username": "stas00",
      "profile_url": "https://github.com/stas00"
    }
  },
  {
    "name": "gto76/python-cheatsheet",
    "description": "Comprehensive Python Cheatsheet",
    "url": "https://github.com/gto76/python-cheatsheet",
    "stars": 36596,
    "forks": 6481,
    "language": "Python",
    "last_updated": "2024-12-11T00:45:11Z",
    "topics": [
      "cheatsheet",
      "python",
      "python-cheatsheet",
      "reference"
    ],
    "owner": {
      "username": "gto76",
      "profile_url": "https://github.com/gto76"
    }
  },
  {
    "name": "iam-veeramalla/Docker-Zero-to-Hero",
    "description": "Repo to learn Docker with examples. Contributions are most welcome.",
    "url": "https://github.com/iam-veeramalla/Docker-Zero-to-Hero",
    "stars": 4079,
    "forks": 8216,
    "language": null,
    "last_updated": "2024-12-10T18:50:18Z",
    "topics": [],
    "owner": {
      "username": "iam-veeramalla",
      "profile_url": "https://github.com/iam-veeramalla"
    }
  },
  {
    "name": "g1879/DrissionPage",
    "description": "Python based web automation tool. Powerful and elegant.",
    "url": "https://github.com/g1879/DrissionPage",
    "stars": 8450,
    "forks": 794,
    "language": "Python",
    "last_updated": "2024-12-11T03:38:39Z",
    "topics": [
      "automation-framework",
      "python",
      "web-automation"
    ],
    "owner": {
      "username": "g1879",
      "profile_url": "https://github.com/g1879"
    }
  },
  {
    "name": "tairov/llama2.mojo",
    "description": "Inference Llama 2 in one file of pure \ud83d\udd25",
    "url": "https://github.com/tairov/llama2.mojo",
    "stars": 2105,
    "forks": 142,
    "language": "Mojo",
    "last_updated": "2024-12-10T05:55:00Z",
    "topics": [
      "inference",
      "llama",
      "llama2",
      "modular",
      "mojo",
      "parallelize",
      "performance",
      "simd",
      "tensor",
      "transformer-architecture",
      "vectorization"
    ],
    "owner": {
      "username": "tairov",
      "profile_url": "https://github.com/tairov"
    }
  },
  {
    "name": "OpenBMB/ChatDev",
    "description": "Create Customized Software using Natural Language Idea (through LLM-powered Multi-Agent Collaboration)",
    "url": "https://github.com/OpenBMB/ChatDev",
    "stars": 25785,
    "forks": 3238,
    "language": "Shell",
    "last_updated": "2024-12-11T03:12:33Z",
    "topics": [],
    "owner": {
      "username": "OpenBMB",
      "profile_url": "https://github.com/OpenBMB"
    }
  },
  {
    "name": "yangshun/tech-interview-handbook",
    "description": "\ud83d\udcaf Curated coding interview preparation materials for busy software engineers",
    "url": "https://github.com/yangshun/tech-interview-handbook",
    "stars": 119900,
    "forks": 14794,
    "language": "TypeScript",
    "last_updated": "2024-12-11T03:47:39Z",
    "topics": [
      "algorithm",
      "algorithm-interview",
      "algorithm-interview-questions",
      "algorithms",
      "behavioral-interviews",
      "coding-interviews",
      "interview-practice",
      "interview-preparation",
      "interview-questions",
      "system-design"
    ],
    "owner": {
      "username": "yangshun",
      "profile_url": "https://github.com/yangshun"
    }
  },
  {
    "name": "ByteByteGoHq/system-design-101",
    "description": "Explain complex systems using visuals and simple terms. Help you prepare for system design interviews.",
    "url": "https://github.com/ByteByteGoHq/system-design-101",
    "stars": 64925,
    "forks": 6863,
    "language": null,
    "last_updated": "2024-12-11T03:29:47Z",
    "topics": [
      "aws",
      "cloud-computing",
      "coding-interviews",
      "computer-science",
      "interview-questions",
      "software-architecture",
      "software-development",
      "software-engineering",
      "system-design",
      "system-design-interview"
    ],
    "owner": {
      "username": "ByteByteGoHq",
      "profile_url": "https://github.com/ByteByteGoHq"
    }
  },
  {
    "name": "doocs/leetcode",
    "description": "\ud83d\udd25LeetCode solutions in any programming language | \u591a\u79cd\u7f16\u7a0b\u8bed\u8a00\u5b9e\u73b0 LeetCode\u3001\u300a\u5251\u6307 Offer\uff08\u7b2c 2 \u7248\uff09\u300b\u3001\u300a\u7a0b\u5e8f\u5458\u9762\u8bd5\u91d1\u5178\uff08\u7b2c 6 \u7248\uff09\u300b\u9898\u89e3",
    "url": "https://github.com/doocs/leetcode",
    "stars": 32060,
    "forks": 7698,
    "language": "Java",
    "last_updated": "2024-12-11T03:54:31Z",
    "topics": [
      "algorithms",
      "cpp",
      "csharp",
      "golang",
      "java",
      "javascript",
      "leetcode",
      "python3"
    ],
    "owner": {
      "username": "doocs",
      "profile_url": "https://github.com/doocs"
    }
  },
  {
    "name": "kamyu104/LeetCode-Solutions",
    "description": "\ud83c\udfcb\ufe0f Python / Modern C++ Solutions of All 3384 LeetCode Problems (Weekly Update)",
    "url": "https://github.com/kamyu104/LeetCode-Solutions",
    "stars": 4748,
    "forks": 1569,
    "language": "C++",
    "last_updated": "2024-12-10T21:40:25Z",
    "topics": [
      "algorithm",
      "algorithms",
      "cpp",
      "cpp11",
      "data-structure",
      "interview-practice",
      "interview-preparation",
      "interview-questions",
      "leetcode",
      "leetcode-cpp",
      "leetcode-python",
      "leetcode-solutions",
      "modern-cpp",
      "python"
    ],
    "owner": {
      "username": "kamyu104",
      "profile_url": "https://github.com/kamyu104"
    }
  },
  {
    "name": "iam-veeramalla/aws-devops-zero-to-hero",
    "description": "AWS zero to hero repo for devops engineers to learn AWS in 30 Days. This repo includes projects, presentations, interview questions and real time examples.",
    "url": "https://github.com/iam-veeramalla/aws-devops-zero-to-hero",
    "stars": 7011,
    "forks": 9448,
    "language": "Python",
    "last_updated": "2024-12-10T22:28:25Z",
    "topics": [],
    "owner": {
      "username": "iam-veeramalla",
      "profile_url": "https://github.com/iam-veeramalla"
    }
  },
  {
    "name": "karan/Projects-Solutions",
    "description": ":pager: Links to others' solutions to Projects (https://github.com/karan/Projects/)",
    "url": "https://github.com/karan/Projects-Solutions",
    "stars": 4167,
    "forks": 1290,
    "language": null,
    "last_updated": "2024-12-07T14:12:13Z",
    "topics": [],
    "owner": {
      "username": "karan",
      "profile_url": "https://github.com/karan"
    }
  },
  {
    "name": "practical-tutorials/project-based-learning",
    "description": "Curated list of project-based tutorials",
    "url": "https://github.com/practical-tutorials/project-based-learning",
    "stars": 206735,
    "forks": 26978,
    "language": null,
    "last_updated": "2024-12-11T03:59:58Z",
    "topics": [
      "beginner-project",
      "cpp",
      "golang",
      "javascript",
      "project",
      "python",
      "tutorial",
      "webdevelopment"
    ],
    "owner": {
      "username": "practical-tutorials",
      "profile_url": "https://github.com/practical-tutorials"
    }
  },
  {
    "name": "AMAI-GmbH/AI-Expert-Roadmap",
    "description": "Roadmap to becoming an Artificial Intelligence Expert in 2022",
    "url": "https://github.com/AMAI-GmbH/AI-Expert-Roadmap",
    "stars": 29298,
    "forks": 2493,
    "language": "JavaScript",
    "last_updated": "2024-12-11T02:42:47Z",
    "topics": [
      "ai",
      "ai-roadmap",
      "artificial-intelligence",
      "data-analysis",
      "data-science",
      "deep-learning",
      "machine-learning",
      "neural-network",
      "roadmap",
      "study-plan"
    ],
    "owner": {
      "username": "AMAI-GmbH",
      "profile_url": "https://github.com/AMAI-GmbH"
    }
  },
  {
    "name": "noisetorch/NoiseTorch",
    "description": "Real-time microphone noise suppression on Linux.",
    "url": "https://github.com/noisetorch/NoiseTorch",
    "stars": 9398,
    "forks": 233,
    "language": "Go",
    "last_updated": "2024-12-10T03:33:52Z",
    "topics": [
      "hacktoberfest",
      "hacktoberfest2023",
      "linux",
      "noise-reduction",
      "noise-suppression",
      "pulseaudio",
      "voice",
      "voice-activated",
      "voice-activity-detection"
    ],
    "owner": {
      "username": "noisetorch",
      "profile_url": "https://github.com/noisetorch"
    }
  },
  {
    "name": "Ebazhanov/linkedin-skill-assessments-quizzes",
    "description": "Full reference of LinkedIn answers 2024 for skill assessments (aws-lambda, rest-api, javascript, react, git, html, jquery, mongodb, java, Go, python, machine-learning, power-point) linkedin excel test l\u00f6sungen, linkedin machine learning test LinkedIn test questions and answers ",
    "url": "https://github.com/Ebazhanov/linkedin-skill-assessments-quizzes",
    "stars": 28528,
    "forks": 13330,
    "language": null,
    "last_updated": "2024-12-10T21:46:38Z",
    "topics": [
      "answers",
      "assessment",
      "english",
      "exam",
      "france",
      "german",
      "golang",
      "hacktoberfest",
      "hacktoberfest2020",
      "hacktoberfest2021",
      "hacktoberfest2022",
      "hacktoberfest2023",
      "hacktoberfest2024",
      "linkedin",
      "linkedin-questions",
      "quiz",
      "quiz-questions",
      "skills"
    ],
    "owner": {
      "username": "Ebazhanov",
      "profile_url": "https://github.com/Ebazhanov"
    }
  },
  {
    "name": "jupyter-naas/awesome-notebooks",
    "description": "Data & AI Notebook templates catalog organized by tools, following the IMO (input, model, output) framework for easy usage and discovery..",
    "url": "https://github.com/jupyter-naas/awesome-notebooks",
    "stars": 2727,
    "forks": 452,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T08:51:19Z",
    "topics": [
      "awesome",
      "awesome-list",
      "hacktoberfest",
      "hacktoberfest2023",
      "jupyter",
      "jupyter-notebook",
      "jupyterlab",
      "naas",
      "notebooks-templates",
      "opensource",
      "python",
      "templates"
    ],
    "owner": {
      "username": "jupyter-naas",
      "profile_url": "https://github.com/jupyter-naas"
    }
  },
  {
    "name": "archinetai/audio-ai-timeline",
    "description": "A timeline of the latest AI models for audio generation, starting in 2023!",
    "url": "https://github.com/archinetai/audio-ai-timeline",
    "stars": 1894,
    "forks": 70,
    "language": null,
    "last_updated": "2024-12-10T20:21:52Z",
    "topics": [
      "artificial-intelligence",
      "audio-generation",
      "machine-learning"
    ],
    "owner": {
      "username": "archinetai",
      "profile_url": "https://github.com/archinetai"
    }
  },
  {
    "name": "novuhq/novu",
    "description": "Open-Source Notification Platform. Embeddable Notification Center, E-mail, Push and Slack Integrations.",
    "url": "https://github.com/novuhq/novu",
    "stars": 35546,
    "forks": 3917,
    "language": "TypeScript",
    "last_updated": "2024-12-11T02:22:49Z",
    "topics": [
      "communication",
      "css",
      "email",
      "hacktoberfest",
      "html",
      "javascript",
      "nodejs",
      "notification-center",
      "notifications",
      "push-notifications",
      "react",
      "reactjs",
      "sms",
      "transactional",
      "typescript"
    ],
    "owner": {
      "username": "novuhq",
      "profile_url": "https://github.com/novuhq"
    }
  },
  {
    "name": "shivammehta25/Matcha-TTS",
    "description": "[ICASSP 2024] \ud83c\udf75 Matcha-TTS: A fast TTS architecture with conditional flow matching",
    "url": "https://github.com/shivammehta25/Matcha-TTS",
    "stars": 763,
    "forks": 99,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T15:03:23Z",
    "topics": [
      "deep-learning",
      "diffusion-model",
      "diffusion-models",
      "flow-matching",
      "machine-learning",
      "non-autoregressive",
      "probabilistic",
      "probabilistic-machine-learning",
      "text-to-speech",
      "tts",
      "tts-api",
      "tts-engines"
    ],
    "owner": {
      "username": "shivammehta25",
      "profile_url": "https://github.com/shivammehta25"
    }
  },
  {
    "name": "tldraw/tldraw",
    "description": "whiteboard / infinite canvas SDK",
    "url": "https://github.com/tldraw/tldraw",
    "stars": 36239,
    "forks": 2236,
    "language": "TypeScript",
    "last_updated": "2024-12-11T03:49:49Z",
    "topics": [
      "canvas",
      "collaboration",
      "design",
      "diagram",
      "drawing",
      "infinite",
      "multiplayer",
      "react",
      "sketch",
      "sync",
      "whiteboard"
    ],
    "owner": {
      "username": "tldraw",
      "profile_url": "https://github.com/tldraw"
    }
  },
  {
    "name": "yoheinakajima/instagraph",
    "description": "Converts text input or URL into knowledge graph and displays",
    "url": "https://github.com/yoheinakajima/instagraph",
    "stars": 3482,
    "forks": 290,
    "language": "Python",
    "last_updated": "2024-12-11T01:32:06Z",
    "topics": [],
    "owner": {
      "username": "yoheinakajima",
      "profile_url": "https://github.com/yoheinakajima"
    }
  },
  {
    "name": "mylxsw/aidea-server",
    "description": "AIdea \u662f\u4e00\u6b3e\u652f\u6301 GPT  \u4ee5\u53ca\u56fd\u4ea7\u5927\u8bed\u8a00\u6a21\u578b\u901a\u4e49\u5343\u95ee\u3001\u6587\u5fc3\u4e00\u8a00\u7b49\uff0c\u652f\u6301 Stable Diffusion \u6587\u751f\u56fe\u3001\u56fe\u751f\u56fe\u3001 SDXL1.0\u3001\u8d85\u5206\u8fa8\u7387\u3001\u56fe\u7247\u4e0a\u8272\u7684\u5168\u80fd\u578b APP\u3002",
    "url": "https://github.com/mylxsw/aidea-server",
    "stars": 1587,
    "forks": 436,
    "language": "Go",
    "last_updated": "2024-12-10T11:55:08Z",
    "topics": [
      "ai",
      "chatgpt",
      "gpt",
      "llm",
      "stable-diffusion"
    ],
    "owner": {
      "username": "mylxsw",
      "profile_url": "https://github.com/mylxsw"
    }
  },
  {
    "name": "DataTalksClub/machine-learning-zoomcamp",
    "description": "Learn ML engineering for free in 4 months!",
    "url": "https://github.com/DataTalksClub/machine-learning-zoomcamp",
    "stars": 9664,
    "forks": 2281,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T22:50:20Z",
    "topics": [],
    "owner": {
      "username": "DataTalksClub",
      "profile_url": "https://github.com/DataTalksClub"
    }
  },
  {
    "name": "mylxsw/aidea",
    "description": "AIdea \u662f\u4e00\u6b3e\u652f\u6301 GPT  \u4ee5\u53ca\u56fd\u4ea7\u5927\u8bed\u8a00\u6a21\u578b\u901a\u4e49\u5343\u95ee\u3001\u6587\u5fc3\u4e00\u8a00\u7b49\uff0c\u652f\u6301 Stable Diffusion \u6587\u751f\u56fe\u3001\u56fe\u751f\u56fe\u3001 SDXL1.0\u3001\u8d85\u5206\u8fa8\u7387\u3001\u56fe\u7247\u4e0a\u8272\u7684\u5168\u80fd\u578b APP\u3002",
    "url": "https://github.com/mylxsw/aidea",
    "stars": 6550,
    "forks": 974,
    "language": "Dart",
    "last_updated": "2024-12-10T12:49:11Z",
    "topics": [
      "ai",
      "chatbot",
      "flutter",
      "gpt",
      "gpt-4",
      "stable-diffusion",
      "tongyiqianwen",
      "wenxinyiyan"
    ],
    "owner": {
      "username": "mylxsw",
      "profile_url": "https://github.com/mylxsw"
    }
  },
  {
    "name": "krahets/hello-algo",
    "description": "\u300aHello \u7b97\u6cd5\u300b\uff1a\u52a8\u753b\u56fe\u89e3\u3001\u4e00\u952e\u8fd0\u884c\u7684\u6570\u636e\u7ed3\u6784\u4e0e\u7b97\u6cd5\u6559\u7a0b\u3002\u652f\u6301 Python, Java, C++, C, C#, JS, Go, Swift, Rust, Ruby, Kotlin, TS, Dart \u4ee3\u7801\u3002\u7b80\u4f53\u7248\u548c\u7e41\u4f53\u7248\u540c\u6b65\u66f4\u65b0\uff0cEnglish version ongoing",
    "url": "https://github.com/krahets/hello-algo",
    "stars": 102932,
    "forks": 12904,
    "language": "Java",
    "last_updated": "2024-12-11T04:13:02Z",
    "topics": [
      "algo",
      "algorithm",
      "algorithms",
      "book",
      "data-structure",
      "data-structures",
      "data-structures-and-algorithms",
      "dsa",
      "education",
      "leetcode",
      "programming"
    ],
    "owner": {
      "username": "krahets",
      "profile_url": "https://github.com/krahets"
    }
  },
  {
    "name": "w-okada/voice-changer",
    "description": "\u30ea\u30a2\u30eb\u30bf\u30a4\u30e0\u30dc\u30a4\u30b9\u30c1\u30a7\u30f3\u30b8\u30e3\u30fc Realtime Voice Changer",
    "url": "https://github.com/w-okada/voice-changer",
    "stars": 16692,
    "forks": 1817,
    "language": "Python",
    "last_updated": "2024-12-11T03:32:25Z",
    "topics": [],
    "owner": {
      "username": "w-okada",
      "profile_url": "https://github.com/w-okada"
    }
  },
  {
    "name": "Z4nzu/hackingtool",
    "description": "ALL IN ONE Hacking Tool For Hackers",
    "url": "https://github.com/Z4nzu/hackingtool",
    "stars": 50954,
    "forks": 5470,
    "language": "Python",
    "last_updated": "2024-12-11T02:03:33Z",
    "topics": [
      "allinonehackingtool",
      "besthackingtool",
      "ctf-tools",
      "ddos-attack-tool",
      "hacker",
      "hacking",
      "linux",
      "password-attack",
      "steganography",
      "web-attack",
      "wireless-attack",
      "xss-attacks",
      "xss-detection"
    ],
    "owner": {
      "username": "Z4nzu",
      "profile_url": "https://github.com/Z4nzu"
    }
  },
  {
    "name": "OpenInterpreter/open-interpreter",
    "description": "A natural language interface for computers",
    "url": "https://github.com/OpenInterpreter/open-interpreter",
    "stars": 57350,
    "forks": 4922,
    "language": "Python",
    "last_updated": "2024-12-11T02:54:16Z",
    "topics": [
      "chatgpt",
      "gpt-4",
      "interpreter",
      "javascript",
      "nodejs",
      "python"
    ],
    "owner": {
      "username": "OpenInterpreter",
      "profile_url": "https://github.com/OpenInterpreter"
    }
  },
  {
    "name": "srbhr/Resume-Matcher",
    "description": "Resume Matcher is an open source, free tool to improve your resume. It works by using language models to compare and rank resumes with job descriptions. ",
    "url": "https://github.com/srbhr/Resume-Matcher",
    "stars": 5308,
    "forks": 2281,
    "language": "Python",
    "last_updated": "2024-12-11T03:57:00Z",
    "topics": [
      "applicant-tracking-system",
      "ats",
      "hacktoberfest",
      "machine-learning",
      "natural-language-processing",
      "nextjs",
      "python",
      "resume",
      "resume-builder",
      "resume-parser",
      "text-similarity",
      "typescript",
      "vector-search",
      "word-embeddings"
    ],
    "owner": {
      "username": "srbhr",
      "profile_url": "https://github.com/srbhr"
    }
  },
  {
    "name": "AI-Prompt-Genius/AI-Prompt-Genius",
    "description": "Curate a custom library of AI Prompts",
    "url": "https://github.com/AI-Prompt-Genius/AI-Prompt-Genius",
    "stars": 1108,
    "forks": 163,
    "language": "JavaScript",
    "last_updated": "2024-12-10T05:04:10Z",
    "topics": [
      "ai",
      "browser-extension",
      "chatgpt",
      "chrome-extension"
    ],
    "owner": {
      "username": "AI-Prompt-Genius",
      "profile_url": "https://github.com/AI-Prompt-Genius"
    }
  },
  {
    "name": "sindresorhus/awesome-chatgpt",
    "description": "\ud83e\udd16 Awesome list for ChatGPT \u2014 an artificial intelligence chatbot developed by OpenAI",
    "url": "https://github.com/sindresorhus/awesome-chatgpt",
    "stars": 5206,
    "forks": 317,
    "language": null,
    "last_updated": "2024-12-10T19:13:14Z",
    "topics": [
      "ai",
      "artificial-intelligence",
      "awesome",
      "awesome-list",
      "chatgpt",
      "gpt",
      "gpt-3",
      "gpt-4",
      "openai"
    ],
    "owner": {
      "username": "sindresorhus",
      "profile_url": "https://github.com/sindresorhus"
    }
  },
  {
    "name": "dair-ai/ML-Papers-Explained",
    "description": "Explanation to key concepts in ML",
    "url": "https://github.com/dair-ai/ML-Papers-Explained",
    "stars": 7347,
    "forks": 576,
    "language": null,
    "last_updated": "2024-12-10T04:33:01Z",
    "topics": [],
    "owner": {
      "username": "dair-ai",
      "profile_url": "https://github.com/dair-ai"
    }
  },
  {
    "name": "labuladong/fucking-algorithm",
    "description": "\u5237\u7b97\u6cd5\u5168\u9760\u5957\u8def\uff0c\u8ba4\u51c6 labuladong \u5c31\u591f\u4e86\uff01English version supported! Crack LeetCode, not only how, but also why. ",
    "url": "https://github.com/labuladong/fucking-algorithm",
    "stars": 126114,
    "forks": 23245,
    "language": "Markdown",
    "last_updated": "2024-12-11T03:21:57Z",
    "topics": [
      "algorithms",
      "computer-science",
      "data-structures",
      "dynamic-programming",
      "dynamic-programming-algorithm",
      "interview-questions",
      "kmp",
      "leetcode"
    ],
    "owner": {
      "username": "labuladong",
      "profile_url": "https://github.com/labuladong"
    }
  },
  {
    "name": "jzhang38/TinyLlama",
    "description": "The TinyLlama project is an open endeavor to pretrain a 1.1B Llama model on 3 trillion tokens.",
    "url": "https://github.com/jzhang38/TinyLlama",
    "stars": 8000,
    "forks": 473,
    "language": "Python",
    "last_updated": "2024-12-11T03:52:50Z",
    "topics": [],
    "owner": {
      "username": "jzhang38",
      "profile_url": "https://github.com/jzhang38"
    }
  },
  {
    "name": "cloudcommunity/Free-Certifications",
    "description": "A curated list of free courses & certifications.",
    "url": "https://github.com/cloudcommunity/Free-Certifications",
    "stars": 27251,
    "forks": 2028,
    "language": null,
    "last_updated": "2024-12-11T00:56:08Z",
    "topics": [
      "awesome",
      "awesome-list",
      "awesome-lists",
      "certification",
      "certifications",
      "exams",
      "free",
      "free-certification",
      "free-certifications",
      "free-coupon",
      "free-coupons",
      "free-course",
      "free-courses",
      "free-learning",
      "free-voucher",
      "free-vouchers",
      "freebie",
      "freebies",
      "hacktoberfest",
      "learning"
    ],
    "owner": {
      "username": "cloudcommunity",
      "profile_url": "https://github.com/cloudcommunity"
    }
  },
  {
    "name": "langgptai/wonderful-prompts",
    "description": "\ud83d\udd25\u4e2d\u6587 prompt \u7cbe\u9009\ud83d\udd25\uff0cChatGPT \u4f7f\u7528\u6307\u5357\uff0c\u63d0\u5347 ChatGPT \u53ef\u73a9\u6027\u548c\u53ef\u7528\u6027\uff01\ud83d\ude80",
    "url": "https://github.com/langgptai/wonderful-prompts",
    "stars": 3436,
    "forks": 303,
    "language": null,
    "last_updated": "2024-12-11T02:36:01Z",
    "topics": [
      "chatgpt",
      "chatgpt3",
      "gpt3-prompts",
      "gpt3-turbo",
      "gpt35",
      "gpt4",
      "openai",
      "prompt-engineering",
      "prompts"
    ],
    "owner": {
      "username": "langgptai",
      "profile_url": "https://github.com/langgptai"
    }
  },
  {
    "name": "shroominic/codeinterpreter-api",
    "description": "\ud83d\udc7e Open source implementation of the ChatGPT Code Interpreter",
    "url": "https://github.com/shroominic/codeinterpreter-api",
    "stars": 3798,
    "forks": 405,
    "language": "Python",
    "last_updated": "2024-12-10T07:04:48Z",
    "topics": [
      "chatgpt",
      "chatgpt-code-generation",
      "code-interpreter",
      "codeinterpreter",
      "langchain",
      "llm-agent"
    ],
    "owner": {
      "username": "shroominic",
      "profile_url": "https://github.com/shroominic"
    }
  },
  {
    "name": "hpcaitech/ColossalAI",
    "description": "Making large AI models cheaper, faster and more accessible",
    "url": "https://github.com/hpcaitech/ColossalAI",
    "stars": 38893,
    "forks": 4351,
    "language": "Python",
    "last_updated": "2024-12-11T03:48:05Z",
    "topics": [
      "ai",
      "big-model",
      "data-parallelism",
      "deep-learning",
      "distributed-computing",
      "foundation-models",
      "heterogeneous-training",
      "hpc",
      "inference",
      "large-scale",
      "model-parallelism",
      "pipeline-parallelism"
    ],
    "owner": {
      "username": "hpcaitech",
      "profile_url": "https://github.com/hpcaitech"
    }
  },
  {
    "name": "fighting41love/funNLP",
    "description": "\u4e2d\u82f1\u6587\u654f\u611f\u8bcd\u3001\u8bed\u8a00\u68c0\u6d4b\u3001\u4e2d\u5916\u624b\u673a/\u7535\u8bdd\u5f52\u5c5e\u5730/\u8fd0\u8425\u5546\u67e5\u8be2\u3001\u540d\u5b57\u63a8\u65ad\u6027\u522b\u3001\u624b\u673a\u53f7\u62bd\u53d6\u3001\u8eab\u4efd\u8bc1\u62bd\u53d6\u3001\u90ae\u7bb1\u62bd\u53d6\u3001\u4e2d\u65e5\u6587\u4eba\u540d\u5e93\u3001\u4e2d\u6587\u7f29\u5199\u5e93\u3001\u62c6\u5b57\u8bcd\u5178\u3001\u8bcd\u6c47\u60c5\u611f\u503c\u3001\u505c\u7528\u8bcd\u3001\u53cd\u52a8\u8bcd\u8868\u3001\u66b4\u6050\u8bcd\u8868\u3001\u7e41\u7b80\u4f53\u8f6c\u6362\u3001\u82f1\u6587\u6a21\u62df\u4e2d\u6587\u53d1\u97f3\u3001\u6c6a\u5cf0\u6b4c\u8bcd\u751f\u6210\u5668\u3001\u804c\u4e1a\u540d\u79f0\u8bcd\u5e93\u3001\u540c\u4e49\u8bcd\u5e93\u3001\u53cd\u4e49\u8bcd\u5e93\u3001\u5426\u5b9a\u8bcd\u5e93\u3001\u6c7d\u8f66\u54c1\u724c\u8bcd\u5e93\u3001\u6c7d\u8f66\u96f6\u4ef6\u8bcd\u5e93\u3001\u8fde\u7eed\u82f1\u6587\u5207\u5272\u3001\u5404\u79cd\u4e2d\u6587\u8bcd\u5411\u91cf\u3001\u516c\u53f8\u540d\u5b57\u5927\u5168\u3001\u53e4\u8bd7\u8bcd\u5e93\u3001IT\u8bcd\u5e93\u3001\u8d22\u7ecf\u8bcd\u5e93\u3001\u6210\u8bed\u8bcd\u5e93\u3001\u5730\u540d\u8bcd\u5e93\u3001\u5386\u53f2\u540d\u4eba\u8bcd\u5e93\u3001\u8bd7\u8bcd\u8bcd\u5e93\u3001\u533b\u5b66\u8bcd\u5e93\u3001\u996e\u98df\u8bcd\u5e93\u3001\u6cd5\u5f8b\u8bcd\u5e93\u3001\u6c7d\u8f66\u8bcd\u5e93\u3001\u52a8\u7269\u8bcd\u5e93\u3001\u4e2d\u6587\u804a\u5929\u8bed\u6599\u3001\u4e2d\u6587\u8c23\u8a00\u6570\u636e\u3001\u767e\u5ea6\u4e2d\u6587\u95ee\u7b54\u6570\u636e\u96c6\u3001\u53e5\u5b50\u76f8\u4f3c\u5ea6\u5339\u914d\u7b97\u6cd5\u96c6\u5408\u3001bert\u8d44\u6e90\u3001\u6587\u672c\u751f\u6210&\u6458\u8981\u76f8\u5173\u5de5\u5177\u3001cocoNLP\u4fe1\u606f\u62bd\u53d6\u5de5\u5177\u3001\u56fd\u5185\u7535\u8bdd\u53f7\u7801\u6b63\u5219\u5339\u914d\u3001\u6e05\u534e\u5927\u5b66XLORE:\u4e2d\u82f1\u6587\u8de8\u8bed\u8a00\u767e\u79d1\u77e5\u8bc6\u56fe\u8c31\u3001\u6e05\u534e\u5927\u5b66\u4eba\u5de5\u667a\u80fd\u6280\u672f\u7cfb\u5217\u62a5\u544a\u3001\u81ea\u7136\u8bed\u8a00\u751f\u6210\u3001NLU\u592a\u96be\u4e86\u7cfb\u5217\u3001\u81ea\u52a8\u5bf9\u8054\u6570\u636e\u53ca\u673a\u5668\u4eba\u3001\u7528\u6237\u540d\u9ed1\u540d\u5355\u5217\u8868\u3001\u7f6a\u540d\u6cd5\u52a1\u540d\u8bcd\u53ca\u5206\u7c7b\u6a21\u578b\u3001\u5fae\u4fe1\u516c\u4f17\u53f7\u8bed\u6599\u3001cs224n\u6df1\u5ea6\u5b66\u4e60\u81ea\u7136\u8bed\u8a00\u5904\u7406\u8bfe\u7a0b\u3001\u4e2d\u6587\u624b\u5199\u6c49\u5b57\u8bc6\u522b\u3001\u4e2d\u6587\u81ea\u7136\u8bed\u8a00\u5904\u7406 \u8bed\u6599/\u6570\u636e\u96c6\u3001\u53d8\u91cf\u547d\u540d\u795e\u5668\u3001\u5206\u8bcd\u8bed\u6599\u5e93+\u4ee3\u7801\u3001\u4efb\u52a1\u578b\u5bf9\u8bdd\u82f1\u6587\u6570\u636e\u96c6\u3001ASR \u8bed\u97f3\u6570\u636e\u96c6 + \u57fa\u4e8e\u6df1\u5ea6\u5b66\u4e60\u7684\u4e2d\u6587\u8bed\u97f3\u8bc6\u522b\u7cfb\u7edf\u3001\u7b11\u58f0\u68c0\u6d4b\u5668\u3001Microsoft\u591a\u8bed\u8a00\u6570\u5b57/\u5355\u4f4d/\u5982\u65e5\u671f\u65f6\u95f4\u8bc6\u522b\u5305\u3001\u4e2d\u534e\u65b0\u534e\u5b57\u5178\u6570\u636e\u5e93\u53caapi(\u5305\u62ec\u5e38\u7528\u6b47\u540e\u8bed\u3001\u6210\u8bed\u3001\u8bcd\u8bed\u548c\u6c49\u5b57)\u3001\u6587\u6863\u56fe\u8c31\u81ea\u52a8\u751f\u6210\u3001SpaCy \u4e2d\u6587\u6a21\u578b\u3001Common Voice\u8bed\u97f3\u8bc6\u522b\u6570\u636e\u96c6\u65b0\u7248\u3001\u795e\u7ecf\u7f51\u7edc\u5173\u7cfb\u62bd\u53d6\u3001\u57fa\u4e8ebert\u7684\u547d\u540d\u5b9e\u4f53\u8bc6\u522b\u3001\u5173\u952e\u8bcd(Keyphrase)\u62bd\u53d6\u5305pke\u3001\u57fa\u4e8e\u533b\u7597\u9886\u57df\u77e5\u8bc6\u56fe\u8c31\u7684\u95ee\u7b54\u7cfb\u7edf\u3001\u57fa\u4e8e\u4f9d\u5b58\u53e5\u6cd5\u4e0e\u8bed\u4e49\u89d2\u8272\u6807\u6ce8\u7684\u4e8b\u4ef6\u4e09\u5143\u7ec4\u62bd\u53d6\u3001\u4f9d\u5b58\u53e5\u6cd5\u5206\u67904\u4e07\u53e5\u9ad8\u8d28\u91cf\u6807\u6ce8\u6570\u636e\u3001cnocr\uff1a\u7528\u6765\u505a\u4e2d\u6587OCR\u7684Python3\u5305\u3001\u4e2d\u6587\u4eba\u7269\u5173\u7cfb\u77e5\u8bc6\u56fe\u8c31\u9879\u76ee\u3001\u4e2d\u6587nlp\u7ade\u8d5b\u9879\u76ee\u53ca\u4ee3\u7801\u6c47\u603b\u3001\u4e2d\u6587\u5b57\u7b26\u6570\u636e\u3001speech-aligner: \u4ece\u201c\u4eba\u58f0\u8bed\u97f3\u201d\u53ca\u5176\u201c\u8bed\u8a00\u6587\u672c\u201d\u4ea7\u751f\u97f3\u7d20\u7ea7\u522b\u65f6\u95f4\u5bf9\u9f50\u6807\u6ce8\u7684\u5de5\u5177\u3001AmpliGraph: \u77e5\u8bc6\u56fe\u8c31\u8868\u793a\u5b66\u4e60(Python)\u5e93\uff1a\u77e5\u8bc6\u56fe\u8c31\u6982\u5ff5\u94fe\u63a5\u9884\u6d4b\u3001Scattertext \u6587\u672c\u53ef\u89c6\u5316(python)\u3001\u8bed\u8a00/\u77e5\u8bc6\u8868\u793a\u5de5\u5177\uff1aBERT & ERNIE\u3001\u4e2d\u6587\u5bf9\u6bd4\u82f1\u6587\u81ea\u7136\u8bed\u8a00\u5904\u7406NLP\u7684\u533a\u522b\u7efc\u8ff0\u3001Synonyms\u4e2d\u6587\u8fd1\u4e49\u8bcd\u5de5\u5177\u5305\u3001HarvestText\u9886\u57df\u81ea\u9002\u5e94\u6587\u672c\u6316\u6398\u5de5\u5177\uff08\u65b0\u8bcd\u53d1\u73b0-\u60c5\u611f\u5206\u6790-\u5b9e\u4f53\u94fe\u63a5\u7b49\uff09\u3001word2word\uff1a(Python)\u65b9\u4fbf\u6613\u7528\u7684\u591a\u8bed\u8a00\u8bcd-\u8bcd\u5bf9\u96c6\uff1a62\u79cd\u8bed\u8a00/3,564\u4e2a\u591a\u8bed\u8a00\u5bf9\u3001\u8bed\u97f3\u8bc6\u522b\u8bed\u6599\u751f\u6210\u5de5\u5177\uff1a\u4ece\u5177\u6709\u97f3\u9891/\u5b57\u5e55\u7684\u5728\u7ebf\u89c6\u9891\u521b\u5efa\u81ea\u52a8\u8bed\u97f3\u8bc6\u522b(ASR)\u8bed\u6599\u5e93\u3001\u6784\u5efa\u533b\u7597\u5b9e\u4f53\u8bc6\u522b\u7684\u6a21\u578b\uff08\u5305\u542b\u8bcd\u5178\u548c\u8bed\u6599\u6807\u6ce8\uff09\u3001\u5355\u6587\u6863\u975e\u76d1\u7763\u7684\u5173\u952e\u8bcd\u62bd\u53d6\u3001Kashgari\u4e2d\u4f7f\u7528gpt-2\u8bed\u8a00\u6a21\u578b\u3001\u5f00\u6e90\u7684\u91d1\u878d\u6295\u8d44\u6570\u636e\u63d0\u53d6\u5de5\u5177\u3001\u6587\u672c\u81ea\u52a8\u6458\u8981\u5e93TextTeaser: \u4ec5\u652f\u6301\u82f1\u6587\u3001\u4eba\u6c11\u65e5\u62a5\u8bed\u6599\u5904\u7406\u5de5\u5177\u96c6\u3001\u4e00\u4e9b\u5173\u4e8e\u81ea\u7136\u8bed\u8a00\u7684\u57fa\u672c\u6a21\u578b\u3001\u57fa\u4e8e14W\u6b4c\u66f2\u77e5\u8bc6\u5e93\u7684\u95ee\u7b54\u5c1d\u8bd5--\u529f\u80fd\u5305\u62ec\u6b4c\u8bcd\u63a5\u9f99and\u5df2\u77e5\u6b4c\u8bcd\u627e\u6b4c\u66f2\u4ee5\u53ca\u6b4c\u66f2\u6b4c\u624b\u6b4c\u8bcd\u4e09\u89d2\u5173\u7cfb\u7684\u95ee\u7b54\u3001\u57fa\u4e8eSiamese bilstm\u6a21\u578b\u7684\u76f8\u4f3c\u53e5\u5b50\u5224\u5b9a\u6a21\u578b\u5e76\u63d0\u4f9b\u8bad\u7ec3\u6570\u636e\u96c6\u548c\u6d4b\u8bd5\u6570\u636e\u96c6\u3001\u7528Transformer\u7f16\u89e3\u7801\u6a21\u578b\u5b9e\u73b0\u7684\u6839\u636eHacker News\u6587\u7ae0\u6807\u9898\u81ea\u52a8\u751f\u6210\u8bc4\u8bba\u3001\u7528BERT\u8fdb\u884c\u5e8f\u5217\u6807\u8bb0\u548c\u6587\u672c\u5206\u7c7b\u7684\u6a21\u677f\u4ee3\u7801\u3001LitBank\uff1aNLP\u6570\u636e\u96c6\u2014\u2014\u652f\u6301\u81ea\u7136\u8bed\u8a00\u5904\u7406\u548c\u8ba1\u7b97\u4eba\u6587\u5b66\u79d1\u4efb\u52a1\u7684100\u90e8\u5e26\u6807\u8bb0\u82f1\u6587\u5c0f\u8bf4\u8bed\u6599\u3001\u767e\u5ea6\u5f00\u6e90\u7684\u57fa\u51c6\u4fe1\u606f\u62bd\u53d6\u7cfb\u7edf\u3001\u865a\u5047\u65b0\u95fb\u6570\u636e\u96c6\u3001Facebook: LAMA\u8bed\u8a00\u6a21\u578b\u5206\u6790\uff0c\u63d0\u4f9bTransformer-XL/BERT/ELMo/GPT\u9884\u8bad\u7ec3\u8bed\u8a00\u6a21\u578b\u7684\u7edf\u4e00\u8bbf\u95ee\u63a5\u53e3\u3001CommonsenseQA\uff1a\u9762\u5411\u5e38\u8bc6\u7684\u82f1\u6587QA\u6311\u6218\u3001\u4e2d\u6587\u77e5\u8bc6\u56fe\u8c31\u8d44\u6599\u3001\u6570\u636e\u53ca\u5de5\u5177\u3001\u5404\u5927\u516c\u53f8\u5185\u90e8\u91cc\u5927\u725b\u5206\u4eab\u7684\u6280\u672f\u6587\u6863 PDF \u6216\u8005 PPT\u3001\u81ea\u7136\u8bed\u8a00\u751f\u6210SQL\u8bed\u53e5\uff08\u82f1\u6587\uff09\u3001\u4e2d\u6587NLP\u6570\u636e\u589e\u5f3a\uff08EDA\uff09\u5de5\u5177\u3001\u82f1\u6587NLP\u6570\u636e\u589e\u5f3a\u5de5\u5177 \u3001\u57fa\u4e8e\u533b\u836f\u77e5\u8bc6\u56fe\u8c31\u7684\u667a\u80fd\u95ee\u7b54\u7cfb\u7edf\u3001\u4eac\u4e1c\u5546\u54c1\u77e5\u8bc6\u56fe\u8c31\u3001\u57fa\u4e8emongodb\u5b58\u50a8\u7684\u519b\u4e8b\u9886\u57df\u77e5\u8bc6\u56fe\u8c31\u95ee\u7b54\u9879\u76ee\u3001\u57fa\u4e8e\u8fdc\u76d1\u7763\u7684\u4e2d\u6587\u5173\u7cfb\u62bd\u53d6\u3001\u8bed\u97f3\u60c5\u611f\u5206\u6790\u3001\u4e2d\u6587ULMFiT-\u60c5\u611f\u5206\u6790-\u6587\u672c\u5206\u7c7b-\u8bed\u6599\u53ca\u6a21\u578b\u3001\u4e00\u4e2a\u62cd\u7167\u505a\u9898\u7a0b\u5e8f\u3001\u4e16\u754c\u5404\u56fd\u5927\u89c4\u6a21\u4eba\u540d\u5e93\u3001\u4e00\u4e2a\u5229\u7528\u6709\u8da3\u4e2d\u6587\u8bed\u6599\u5e93 qingyun \u8bad\u7ec3\u51fa\u6765\u7684\u4e2d\u6587\u804a\u5929\u673a\u5668\u4eba\u3001\u4e2d\u6587\u804a\u5929\u673a\u5668\u4ebaseqGAN\u3001\u7701\u5e02\u533a\u9547\u884c\u653f\u533a\u5212\u6570\u636e\u5e26\u62fc\u97f3\u6807\u6ce8\u3001\u6559\u80b2\u884c\u4e1a\u65b0\u95fb\u8bed\u6599\u5e93\u5305\u542b\u81ea\u52a8\u6587\u6458\u529f\u80fd\u3001\u5f00\u653e\u4e86\u5bf9\u8bdd\u673a\u5668\u4eba-\u77e5\u8bc6\u56fe\u8c31-\u8bed\u4e49\u7406\u89e3-\u81ea\u7136\u8bed\u8a00\u5904\u7406\u5de5\u5177\u53ca\u6570\u636e\u3001\u4e2d\u6587\u77e5\u8bc6\u56fe\u8c31\uff1a\u57fa\u4e8e\u767e\u5ea6\u767e\u79d1\u4e2d\u6587\u9875\u9762-\u62bd\u53d6\u4e09\u5143\u7ec4\u4fe1\u606f-\u6784\u5efa\u4e2d\u6587\u77e5\u8bc6\u56fe\u8c31\u3001masr: \u4e2d\u6587\u8bed\u97f3\u8bc6\u522b-\u63d0\u4f9b\u9884\u8bad\u7ec3\u6a21\u578b-\u9ad8\u8bc6\u522b\u7387\u3001Python\u97f3\u9891\u6570\u636e\u589e\u5e7f\u5e93\u3001\u4e2d\u6587\u5168\u8bcd\u8986\u76d6BERT\u53ca\u4e24\u4efd\u9605\u8bfb\u7406\u89e3\u6570\u636e\u3001ConvLab\uff1a\u5f00\u6e90\u591a\u57df\u7aef\u5230\u7aef\u5bf9\u8bdd\u7cfb\u7edf\u5e73\u53f0\u3001\u4e2d\u6587\u81ea\u7136\u8bed\u8a00\u5904\u7406\u6570\u636e\u96c6\u3001\u57fa\u4e8e\u6700\u65b0\u7248\u672crasa\u642d\u5efa\u7684\u5bf9\u8bdd\u7cfb\u7edf\u3001\u57fa\u4e8eTensorFlow\u548cBERT\u7684\u7ba1\u9053\u5f0f\u5b9e\u4f53\u53ca\u5173\u7cfb\u62bd\u53d6\u3001\u4e00\u4e2a\u5c0f\u578b\u7684\u8bc1\u5238\u77e5\u8bc6\u56fe\u8c31/\u77e5\u8bc6\u5e93\u3001\u590d\u76d8\u6240\u6709NLP\u6bd4\u8d5b\u7684TOP\u65b9\u6848\u3001OpenCLaP\uff1a\u591a\u9886\u57df\u5f00\u6e90\u4e2d\u6587\u9884\u8bad\u7ec3\u8bed\u8a00\u6a21\u578b\u4ed3\u5e93\u3001UER\uff1a\u57fa\u4e8e\u4e0d\u540c\u8bed\u6599+\u7f16\u7801\u5668+\u76ee\u6807\u4efb\u52a1\u7684\u4e2d\u6587\u9884\u8bad\u7ec3\u6a21\u578b\u4ed3\u5e93\u3001\u4e2d\u6587\u81ea\u7136\u8bed\u8a00\u5904\u7406\u5411\u91cf\u5408\u96c6\u3001\u57fa\u4e8e\u91d1\u878d-\u53f8\u6cd5\u9886\u57df(\u517c\u6709\u95f2\u804a\u6027\u8d28)\u7684\u804a\u5929\u673a\u5668\u4eba\u3001g2pC\uff1a\u57fa\u4e8e\u4e0a\u4e0b\u6587\u7684\u6c49\u8bed\u8bfb\u97f3\u81ea\u52a8\u6807\u8bb0\u6a21\u5757\u3001Zincbase \u77e5\u8bc6\u56fe\u8c31\u6784\u5efa\u5de5\u5177\u5305\u3001\u8bd7\u6b4c\u8d28\u91cf\u8bc4\u4ef7/\u7ec6\u7c92\u5ea6\u60c5\u611f\u8bd7\u6b4c\u8bed\u6599\u5e93\u3001\u5feb\u901f\u8f6c\u5316\u300c\u4e2d\u6587\u6570\u5b57\u300d\u548c\u300c\u963f\u62c9\u4f2f\u6570\u5b57\u300d\u3001\u767e\u5ea6\u77e5\u9053\u95ee\u7b54\u8bed\u6599\u5e93\u3001\u57fa\u4e8e\u77e5\u8bc6\u56fe\u8c31\u7684\u95ee\u7b54\u7cfb\u7edf\u3001jieba_fast \u52a0\u901f\u7248\u7684jieba\u3001\u6b63\u5219\u8868\u8fbe\u5f0f\u6559\u7a0b\u3001\u4e2d\u6587\u9605\u8bfb\u7406\u89e3\u6570\u636e\u96c6\u3001\u57fa\u4e8eBERT\u7b49\u6700\u65b0\u8bed\u8a00\u6a21\u578b\u7684\u62bd\u53d6\u5f0f\u6458\u8981\u63d0\u53d6\u3001Python\u5229\u7528\u6df1\u5ea6\u5b66\u4e60\u8fdb\u884c\u6587\u672c\u6458\u8981\u7684\u7efc\u5408\u6307\u5357\u3001\u77e5\u8bc6\u56fe\u8c31\u6df1\u5ea6\u5b66\u4e60\u76f8\u5173\u8d44\u6599\u6574\u7406\u3001\u7ef4\u57fa\u5927\u89c4\u6a21\u5e73\u884c\u6587\u672c\u8bed\u6599\u3001StanfordNLP 0.2.0\uff1a\u7eafPython\u7248\u81ea\u7136\u8bed\u8a00\u5904\u7406\u5305\u3001NeuralNLP-NeuralClassifier\uff1a\u817e\u8baf\u5f00\u6e90\u6df1\u5ea6\u5b66\u4e60\u6587\u672c\u5206\u7c7b\u5de5\u5177\u3001\u7aef\u5230\u7aef\u7684\u5c01\u95ed\u57df\u5bf9\u8bdd\u7cfb\u7edf\u3001\u4e2d\u6587\u547d\u540d\u5b9e\u4f53\u8bc6\u522b\uff1aNeuroNER vs. BertNER\u3001\u65b0\u95fb\u4e8b\u4ef6\u7ebf\u7d22\u62bd\u53d6\u30012019\u5e74\u767e\u5ea6\u7684\u4e09\u5143\u7ec4\u62bd\u53d6\u6bd4\u8d5b\uff1a\u201c\u79d1\u5b66\u7a7a\u95f4\u961f\u201d\u6e90\u7801\u3001\u57fa\u4e8e\u4f9d\u5b58\u53e5\u6cd5\u7684\u5f00\u653e\u57df\u6587\u672c\u77e5\u8bc6\u4e09\u5143\u7ec4\u62bd\u53d6\u548c\u77e5\u8bc6\u5e93\u6784\u5efa\u3001\u4e2d\u6587\u7684GPT2\u8bad\u7ec3\u4ee3\u7801\u3001ML-NLP - \u673a\u5668\u5b66\u4e60(Machine Learning)NLP\u9762\u8bd5\u4e2d\u5e38\u8003\u5230\u7684\u77e5\u8bc6\u70b9\u548c\u4ee3\u7801\u5b9e\u73b0\u3001nlp4han:\u4e2d\u6587\u81ea\u7136\u8bed\u8a00\u5904\u7406\u5de5\u5177\u96c6(\u65ad\u53e5/\u5206\u8bcd/\u8bcd\u6027\u6807\u6ce8/\u7ec4\u5757/\u53e5\u6cd5\u5206\u6790/\u8bed\u4e49\u5206\u6790/NER/N\u5143\u8bed\u6cd5/HMM/\u4ee3\u8bcd\u6d88\u89e3/\u60c5\u611f\u5206\u6790/\u62fc\u5199\u68c0\u67e5\u3001XLM\uff1aFacebook\u7684\u8de8\u8bed\u8a00\u9884\u8bad\u7ec3\u8bed\u8a00\u6a21\u578b\u3001\u7528\u57fa\u4e8eBERT\u7684\u5fae\u8c03\u548c\u7279\u5f81\u63d0\u53d6\u65b9\u6cd5\u6765\u8fdb\u884c\u77e5\u8bc6\u56fe\u8c31\u767e\u5ea6\u767e\u79d1\u4eba\u7269\u8bcd\u6761\u5c5e\u6027\u62bd\u53d6\u3001\u4e2d\u6587\u81ea\u7136\u8bed\u8a00\u5904\u7406\u76f8\u5173\u7684\u5f00\u653e\u4efb\u52a1-\u6570\u636e\u96c6-\u5f53\u524d\u6700\u4f73\u7ed3\u679c\u3001CoupletAI - \u57fa\u4e8eCNN+Bi-LSTM+Attention \u7684\u81ea\u52a8\u5bf9\u5bf9\u8054\u7cfb\u7edf\u3001\u62bd\u8c61\u77e5\u8bc6\u56fe\u8c31\u3001MiningZhiDaoQACorpus - 580\u4e07\u767e\u5ea6\u77e5\u9053\u95ee\u7b54\u6570\u636e\u6316\u6398\u9879\u76ee\u3001brat rapid annotation tool: \u5e8f\u5217\u6807\u6ce8\u5de5\u5177\u3001\u5927\u89c4\u6a21\u4e2d\u6587\u77e5\u8bc6\u56fe\u8c31\u6570\u636e\uff1a1.4\u4ebf\u5b9e\u4f53\u3001\u6570\u636e\u589e\u5f3a\u5728\u673a\u5668\u7ffb\u8bd1\u53ca\u5176\u4ed6nlp\u4efb\u52a1\u4e2d\u7684\u5e94\u7528\u53ca\u6548\u679c\u3001allennlp\u9605\u8bfb\u7406\u89e3:\u652f\u6301\u591a\u79cd\u6570\u636e\u548c\u6a21\u578b\u3001PDF\u8868\u683c\u6570\u636e\u63d0\u53d6\u5de5\u5177 \u3001 Graphbrain\uff1aAI\u5f00\u6e90\u8f6f\u4ef6\u5e93\u548c\u79d1\u7814\u5de5\u5177\uff0c\u76ee\u7684\u662f\u4fc3\u8fdb\u81ea\u52a8\u610f\u4e49\u63d0\u53d6\u548c\u6587\u672c\u7406\u89e3\u4ee5\u53ca\u77e5\u8bc6\u7684\u63a2\u7d22\u548c\u63a8\u65ad\u3001\u7b80\u5386\u81ea\u52a8\u7b5b\u9009\u7cfb\u7edf\u3001\u57fa\u4e8e\u547d\u540d\u5b9e\u4f53\u8bc6\u522b\u7684\u7b80\u5386\u81ea\u52a8\u6458\u8981\u3001\u4e2d\u6587\u8bed\u8a00\u7406\u89e3\u6d4b\u8bc4\u57fa\u51c6\uff0c\u5305\u62ec\u4ee3\u8868\u6027\u7684\u6570\u636e\u96c6&\u57fa\u51c6\u6a21\u578b&\u8bed\u6599\u5e93&\u6392\u884c\u699c\u3001\u6811\u6d1e OCR \u6587\u5b57\u8bc6\u522b \u3001\u4ece\u5305\u542b\u8868\u683c\u7684\u626b\u63cf\u56fe\u7247\u4e2d\u8bc6\u522b\u8868\u683c\u548c\u6587\u5b57\u3001\u8bed\u58f0\u8fc1\u79fb\u3001Python\u53e3\u8bed\u81ea\u7136\u8bed\u8a00\u5904\u7406\u5de5\u5177\u96c6(\u82f1\u6587)\u3001 similarity\uff1a\u76f8\u4f3c\u5ea6\u8ba1\u7b97\u5de5\u5177\u5305\uff0cjava\u7f16\u5199\u3001\u6d77\u91cf\u4e2d\u6587\u9884\u8bad\u7ec3ALBERT\u6a21\u578b \u3001Transformers 2.0 \u3001\u57fa\u4e8e\u5927\u89c4\u6a21\u97f3\u9891\u6570\u636e\u96c6Audioset\u7684\u97f3\u9891\u589e\u5f3a \u3001Poplar\uff1a\u7f51\u9875\u7248\u81ea\u7136\u8bed\u8a00\u6807\u6ce8\u5de5\u5177\u3001\u56fe\u7247\u6587\u5b57\u53bb\u9664\uff0c\u53ef\u7528\u4e8e\u6f2b\u753b\u7ffb\u8bd1 \u3001186\u79cd\u8bed\u8a00\u7684\u6570\u5b57\u53eb\u6cd5\u5e93\u3001Amazon\u53d1\u5e03\u57fa\u4e8e\u77e5\u8bc6\u7684\u4eba-\u4eba\u5f00\u653e\u9886\u57df\u5bf9\u8bdd\u6570\u636e\u96c6 \u3001\u4e2d\u6587\u6587\u672c\u7ea0\u9519\u6a21\u5757\u4ee3\u7801\u3001\u7e41\u7b80\u4f53\u8f6c\u6362 \u3001 Python\u5b9e\u73b0\u7684\u591a\u79cd\u6587\u672c\u53ef\u8bfb\u6027\u8bc4\u4ef7\u6307\u6807\u3001\u7c7b\u4f3c\u4e8e\u4eba\u540d/\u5730\u540d/\u7ec4\u7ec7\u673a\u6784\u540d\u7684\u547d\u540d\u4f53\u8bc6\u522b\u6570\u636e\u96c6 \u3001\u4e1c\u5357\u5927\u5b66\u300a\u77e5\u8bc6\u56fe\u8c31\u300b\u7814\u7a76\u751f\u8bfe\u7a0b(\u8d44\u6599)\u3001. \u82f1\u6587\u62fc\u5199\u68c0\u67e5\u5e93 \u3001 wwsearch\u662f\u4f01\u4e1a\u5fae\u4fe1\u540e\u53f0\u81ea\u7814\u7684\u5168\u6587\u68c0\u7d22\u5f15\u64ce\u3001CHAMELEON\uff1a\u6df1\u5ea6\u5b66\u4e60\u65b0\u95fb\u63a8\u8350\u7cfb\u7edf\u5143\u67b6\u6784 \u3001 8\u7bc7\u8bba\u6587\u68b3\u7406BERT\u76f8\u5173\u6a21\u578b\u8fdb\u5c55\u4e0e\u53cd\u601d\u3001DocSearch\uff1a\u514d\u8d39\u6587\u6863\u641c\u7d22\u5f15\u64ce\u3001 LIDA\uff1a\u8f7b\u91cf\u4ea4\u4e92\u5f0f\u5bf9\u8bdd\u6807\u6ce8\u5de5\u5177 \u3001aili - the fastest in-memory index in the East \u4e1c\u534a\u7403\u6700\u5feb\u5e76\u53d1\u7d22\u5f15 \u3001\u77e5\u8bc6\u56fe\u8c31\u8f66\u97f3\u5de5\u4f5c\u9879\u76ee\u3001\u81ea\u7136\u8bed\u8a00\u751f\u6210\u8d44\u6e90\u5927\u5168 \u3001\u4e2d\u65e5\u97e9\u5206\u8bcd\u5e93mecab\u7684Python\u63a5\u53e3\u5e93\u3001\u4e2d\u6587\u6587\u672c\u6458\u8981/\u5173\u952e\u8bcd\u63d0\u53d6\u3001\u6c49\u5b57\u5b57\u7b26\u7279\u5f81\u63d0\u53d6\u5668 (featurizer)\uff0c\u63d0\u53d6\u6c49\u5b57\u7684\u7279\u5f81\uff08\u53d1\u97f3\u7279\u5f81\u3001\u5b57\u5f62\u7279\u5f81\uff09\u7528\u505a\u6df1\u5ea6\u5b66\u4e60\u7684\u7279\u5f81\u3001\u4e2d\u6587\u751f\u6210\u4efb\u52a1\u57fa\u51c6\u6d4b\u8bc4 \u3001\u4e2d\u6587\u7f29\u5199\u6570\u636e\u96c6\u3001\u4e2d\u6587\u4efb\u52a1\u57fa\u51c6\u6d4b\u8bc4 - \u4ee3\u8868\u6027\u7684\u6570\u636e\u96c6-\u57fa\u51c6(\u9884\u8bad\u7ec3)\u6a21\u578b-\u8bed\u6599\u5e93-baseline-\u5de5\u5177\u5305-\u6392\u884c\u699c\u3001PySS3\uff1a\u9762\u5411\u53ef\u89e3\u91caAI\u7684SS3\u6587\u672c\u5206\u7c7b\u5668\u673a\u5668\u53ef\u89c6\u5316\u5de5\u5177 \u3001\u4e2d\u6587NLP\u6570\u636e\u96c6\u5217\u8868\u3001COPE - \u683c\u5f8b\u8bd7\u7f16\u8f91\u7a0b\u5e8f\u3001doccano\uff1a\u57fa\u4e8e\u7f51\u9875\u7684\u5f00\u6e90\u534f\u540c\u591a\u8bed\u8a00\u6587\u672c\u6807\u6ce8\u5de5\u5177 \u3001PreNLP\uff1a\u81ea\u7136\u8bed\u8a00\u9884\u5904\u7406\u5e93\u3001\u7b80\u5355\u7684\u7b80\u5386\u89e3\u6790\u5668\uff0c\u7528\u6765\u4ece\u7b80\u5386\u4e2d\u63d0\u53d6\u5173\u952e\u4fe1\u606f\u3001\u7528\u4e8e\u4e2d\u6587\u95f2\u804a\u7684GPT2\u6a21\u578b\uff1aGPT2-chitchat\u3001\u57fa\u4e8e\u68c0\u7d22\u804a\u5929\u673a\u5668\u4eba\u591a\u8f6e\u54cd\u5e94\u9009\u62e9\u76f8\u5173\u8d44\u6e90\u5217\u8868(Leaderboards\u3001Datasets\u3001Papers)\u3001(Colab)\u62bd\u8c61\u6587\u672c\u6458\u8981\u5b9e\u73b0\u96c6\u9526(\u6559\u7a0b \u3001\u8bcd\u8bed\u62fc\u97f3\u6570\u636e\u3001\u9ad8\u6548\u6a21\u7cca\u641c\u7d22\u5de5\u5177\u3001NLP\u6570\u636e\u589e\u5e7f\u8d44\u6e90\u96c6\u3001\u5fae\u8f6f\u5bf9\u8bdd\u673a\u5668\u4eba\u6846\u67b6 \u3001 GitHub Typo Corpus\uff1a\u5927\u89c4\u6a21GitHub\u591a\u8bed\u8a00\u62fc\u5199\u9519\u8bef/\u8bed\u6cd5\u9519\u8bef\u6570\u636e\u96c6\u3001TextCluster\uff1a\u77ed\u6587\u672c\u805a\u7c7b\u9884\u5904\u7406\u6a21\u5757 Short text cluster\u3001\u9762\u5411\u8bed\u97f3\u8bc6\u522b\u7684\u4e2d\u6587\u6587\u672c\u89c4\u8303\u5316\u3001BLINK\uff1a\u6700\u5148\u8fdb\u7684\u5b9e\u4f53\u94fe\u63a5\u5e93\u3001BertPunc\uff1a\u57fa\u4e8eBERT\u7684\u6700\u5148\u8fdb\u6807\u70b9\u4fee\u590d\u6a21\u578b\u3001Tokenizer\uff1a\u5feb\u901f\u3001\u53ef\u5b9a\u5236\u7684\u6587\u672c\u8bcd\u6761\u5316\u5e93\u3001\u4e2d\u6587\u8bed\u8a00\u7406\u89e3\u6d4b\u8bc4\u57fa\u51c6\uff0c\u5305\u62ec\u4ee3\u8868\u6027\u7684\u6570\u636e\u96c6\u3001\u57fa\u51c6(\u9884\u8bad\u7ec3)\u6a21\u578b\u3001\u8bed\u6599\u5e93\u3001\u6392\u884c\u699c\u3001spaCy \u533b\u5b66\u6587\u672c\u6316\u6398\u4e0e\u4fe1\u606f\u63d0\u53d6 \u3001 NLP\u4efb\u52a1\u793a\u4f8b\u9879\u76ee\u4ee3\u7801\u96c6\u3001 python\u62fc\u5199\u68c0\u67e5\u5e93\u3001chatbot-list - \u884c\u4e1a\u5185\u5173\u4e8e\u667a\u80fd\u5ba2\u670d\u3001\u804a\u5929\u673a\u5668\u4eba\u7684\u5e94\u7528\u548c\u67b6\u6784\u3001\u7b97\u6cd5\u5206\u4eab\u548c\u4ecb\u7ecd\u3001\u8bed\u97f3\u8d28\u91cf\u8bc4\u4ef7\u6307\u6807(MOSNet, BSSEval, STOI, PESQ, SRMR)\u3001 \u7528138GB\u8bed\u6599\u8bad\u7ec3\u7684\u6cd5\u6587RoBERTa\u9884\u8bad\u7ec3\u8bed\u8a00\u6a21\u578b \u3001BERT-NER-Pytorch\uff1a\u4e09\u79cd\u4e0d\u540c\u6a21\u5f0f\u7684BERT\u4e2d\u6587NER\u5b9e\u9a8c\u3001\u65e0\u9053\u8bcd\u5178 - \u6709\u9053\u8bcd\u5178\u7684\u547d\u4ee4\u884c\u7248\u672c\uff0c\u652f\u6301\u82f1\u6c49\u4e92\u67e5\u548c\u5728\u7ebf\u67e5\u8be2\u30012019\u5e74NLP\u4eae\u70b9\u56de\u987e\u3001 Chinese medical dialogue data \u4e2d\u6587\u533b\u7597\u5bf9\u8bdd\u6570\u636e\u96c6 \u3001\u6700\u597d\u7684\u6c49\u5b57\u6570\u5b57(\u4e2d\u6587\u6570\u5b57)-\u963f\u62c9\u4f2f\u6570\u5b57\u8f6c\u6362\u5de5\u5177\u3001 \u57fa\u4e8e\u767e\u79d1\u77e5\u8bc6\u5e93\u7684\u4e2d\u6587\u8bcd\u8bed\u591a\u8bcd\u4e49/\u4e49\u9879\u83b7\u53d6\u4e0e\u7279\u5b9a\u53e5\u5b50\u8bcd\u8bed\u8bed\u4e49\u6d88\u6b67\u3001awesome-nlp-sentiment-analysis - \u60c5\u611f\u5206\u6790\u3001\u60c5\u7eea\u539f\u56e0\u8bc6\u522b\u3001\u8bc4\u4ef7\u5bf9\u8c61\u548c\u8bc4\u4ef7\u8bcd\u62bd\u53d6\u3001LineFlow\uff1a\u9762\u5411\u6240\u6709\u6df1\u5ea6\u5b66\u4e60\u6846\u67b6\u7684NLP\u6570\u636e\u9ad8\u6548\u52a0\u8f7d\u5668\u3001\u4e2d\u6587\u533b\u5b66NLP\u516c\u5f00\u8d44\u6e90\u6574\u7406 \u3001MedQuAD\uff1a(\u82f1\u6587)\u533b\u5b66\u95ee\u7b54\u6570\u636e\u96c6\u3001\u5c06\u81ea\u7136\u8bed\u8a00\u6570\u5b57\u4e32\u89e3\u6790\u8f6c\u6362\u4e3a\u6574\u6570\u548c\u6d6e\u70b9\u6570\u3001Transfer Learning in Natural Language Processing (NLP) \u3001\u9762\u5411\u8bed\u97f3\u8bc6\u522b\u7684\u4e2d\u6587/\u82f1\u6587\u53d1\u97f3\u8f9e\u5178\u3001Tokenizers\uff1a\u6ce8\u91cd\u6027\u80fd\u4e0e\u591a\u529f\u80fd\u6027\u7684\u6700\u5148\u8fdb\u5206\u8bcd\u5668\u3001CLUENER \u7ec6\u7c92\u5ea6\u547d\u540d\u5b9e\u4f53\u8bc6\u522b Fine Grained Named Entity Recognition\u3001 \u57fa\u4e8eBERT\u7684\u4e2d\u6587\u547d\u540d\u5b9e\u4f53\u8bc6\u522b\u3001\u4e2d\u6587\u8c23\u8a00\u6570\u636e\u5e93\u3001NLP\u6570\u636e\u96c6/\u57fa\u51c6\u4efb\u52a1\u5927\u5217\u8868\u3001nlp\u76f8\u5173\u7684\u4e00\u4e9b\u8bba\u6587\u53ca\u4ee3\u7801, \u5305\u62ec\u4e3b\u9898\u6a21\u578b\u3001\u8bcd\u5411\u91cf(Word Embedding)\u3001\u547d\u540d\u5b9e\u4f53\u8bc6\u522b(NER)\u3001\u6587\u672c\u5206\u7c7b(Text Classificatin)\u3001\u6587\u672c\u751f\u6210(Text Generation)\u3001\u6587\u672c\u76f8\u4f3c\u6027(Text Similarity)\u8ba1\u7b97\u7b49\uff0c\u6d89\u53ca\u5230\u5404\u79cd\u4e0enlp\u76f8\u5173\u7684\u7b97\u6cd5\uff0c\u57fa\u4e8ekeras\u548ctensorflow \u3001Python\u6587\u672c\u6316\u6398/NLP\u5b9e\u6218\u793a\u4f8b\u3001 Blackstone\uff1a\u9762\u5411\u975e\u7ed3\u6784\u5316\u6cd5\u5f8b\u6587\u672c\u7684spaCy pipeline\u548cNLP\u6a21\u578b\u901a\u8fc7\u540c\u4e49\u8bcd\u66ff\u6362\u5b9e\u73b0\u6587\u672c\u201c\u53d8\u8138\u201d \u3001\u4e2d\u6587 \u9884\u8bad\u7ec3 ELECTREA \u6a21\u578b: \u57fa\u4e8e\u5bf9\u6297\u5b66\u4e60 pretrain Chinese Model \u3001albert-chinese-ner - \u7528\u9884\u8bad\u7ec3\u8bed\u8a00\u6a21\u578bALBERT\u505a\u4e2d\u6587NER \u3001\u57fa\u4e8eGPT2\u7684\u7279\u5b9a\u4e3b\u9898\u6587\u672c\u751f\u6210/\u6587\u672c\u589e\u5e7f\u3001\u5f00\u6e90\u9884\u8bad\u7ec3\u8bed\u8a00\u6a21\u578b\u5408\u96c6\u3001\u591a\u8bed\u8a00\u53e5\u5411\u91cf\u5305\u3001\u7f16\u7801\u3001\u6807\u8bb0\u548c\u5b9e\u73b0\uff1a\u4e00\u79cd\u53ef\u63a7\u9ad8\u6548\u7684\u6587\u672c\u751f\u6210\u65b9\u6cd5\u3001 \u82f1\u6587\u810f\u8bdd\u5927\u5217\u8868 \u3001attnvis\uff1aGPT2\u3001BERT\u7b49transformer\u8bed\u8a00\u6a21\u578b\u6ce8\u610f\u529b\u4ea4\u4e92\u53ef\u89c6\u5316\u3001CoVoST\uff1aFacebook\u53d1\u5e03\u7684\u591a\u8bed\u79cd\u8bed\u97f3-\u6587\u672c\u7ffb\u8bd1\u8bed\u6599\u5e93\uff0c\u5305\u62ec11\u79cd\u8bed\u8a00(\u6cd5\u8bed\u3001\u5fb7\u8bed\u3001\u8377\u5170\u8bed\u3001\u4fc4\u8bed\u3001\u897f\u73ed\u7259\u8bed\u3001\u610f\u5927\u5229\u8bed\u3001\u571f\u8033\u5176\u8bed\u3001\u6ce2\u65af\u8bed\u3001\u745e\u5178\u8bed\u3001\u8499\u53e4\u8bed\u548c\u4e2d\u6587)\u7684\u8bed\u97f3\u3001\u6587\u5b57\u8f6c\u5f55\u53ca\u82f1\u6587\u8bd1\u6587\u3001Jiagu\u81ea\u7136\u8bed\u8a00\u5904\u7406\u5de5\u5177 - \u4ee5BiLSTM\u7b49\u6a21\u578b\u4e3a\u57fa\u7840\uff0c\u63d0\u4f9b\u77e5\u8bc6\u56fe\u8c31\u5173\u7cfb\u62bd\u53d6 \u4e2d\u6587\u5206\u8bcd \u8bcd\u6027\u6807\u6ce8 \u547d\u540d\u5b9e\u4f53\u8bc6\u522b \u60c5\u611f\u5206\u6790 \u65b0\u8bcd\u53d1\u73b0 \u5173\u952e\u8bcd \u6587\u672c\u6458\u8981 \u6587\u672c\u805a\u7c7b\u7b49\u529f\u80fd\u3001\u7528unet\u5b9e\u73b0\u5bf9\u6587\u6863\u8868\u683c\u7684\u81ea\u52a8\u68c0\u6d4b\uff0c\u8868\u683c\u91cd\u5efa\u3001NLP\u4e8b\u4ef6\u63d0\u53d6\u6587\u732e\u8d44\u6e90\u5217\u8868 \u3001 \u91d1\u878d\u9886\u57df\u81ea\u7136\u8bed\u8a00\u5904\u7406\u7814\u7a76\u8d44\u6e90\u5927\u5217\u8868\u3001CLUEDatasetSearch - \u4e2d\u82f1\u6587NLP\u6570\u636e\u96c6\uff1a\u641c\u7d22\u6240\u6709\u4e2d\u6587NLP\u6570\u636e\u96c6\uff0c\u9644\u5e38\u7528\u82f1\u6587NLP\u6570\u636e\u96c6 \u3001medical_NER - \u4e2d\u6587\u533b\u5b66\u77e5\u8bc6\u56fe\u8c31\u547d\u540d\u5b9e\u4f53\u8bc6\u522b \u3001(\u54c8\u4f5b)\u8bb2\u56e0\u679c\u63a8\u7406\u7684\u514d\u8d39\u4e66\u3001\u77e5\u8bc6\u56fe\u8c31\u76f8\u5173\u5b66\u4e60\u8d44\u6599/\u6570\u636e\u96c6/\u5de5\u5177\u8d44\u6e90\u5927\u5217\u8868\u3001Forte\uff1a\u7075\u6d3b\u5f3a\u5927\u7684\u81ea\u7136\u8bed\u8a00\u5904\u7406pipeline\u5de5\u5177\u96c6 \u3001Python\u5b57\u7b26\u4e32\u76f8\u4f3c\u6027\u7b97\u6cd5\u5e93\u3001PyLaia\uff1a\u9762\u5411\u624b\u5199\u6587\u6863\u5206\u6790\u7684\u6df1\u5ea6\u5b66\u4e60\u5de5\u5177\u5305\u3001TextFooler\uff1a\u9488\u5bf9\u6587\u672c\u5206\u7c7b/\u63a8\u7406\u7684\u5bf9\u6297\u6587\u672c\u751f\u6210\u6a21\u5757\u3001Haystack\uff1a\u7075\u6d3b\u3001\u5f3a\u5927\u7684\u53ef\u6269\u5c55\u95ee\u7b54(QA)\u6846\u67b6\u3001\u4e2d\u6587\u5173\u952e\u77ed\u8bed\u62bd\u53d6\u5de5\u5177",
    "url": "https://github.com/fighting41love/funNLP",
    "stars": 69742,
    "forks": 14565,
    "language": "Python",
    "last_updated": "2024-12-11T03:53:59Z",
    "topics": [],
    "owner": {
      "username": "fighting41love",
      "profile_url": "https://github.com/fighting41love"
    }
  },
  {
    "name": "AUTOMATIC1111/stable-diffusion-webui",
    "description": "Stable Diffusion web UI",
    "url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui",
    "stars": 144211,
    "forks": 27087,
    "language": "Python",
    "last_updated": "2024-12-11T03:49:22Z",
    "topics": [
      "ai",
      "ai-art",
      "deep-learning",
      "diffusion",
      "gradio",
      "image-generation",
      "image2image",
      "img2img",
      "pytorch",
      "stable-diffusion",
      "text2image",
      "torch",
      "txt2img",
      "unstable",
      "upscaling",
      "web"
    ],
    "owner": {
      "username": "AUTOMATIC1111",
      "profile_url": "https://github.com/AUTOMATIC1111"
    }
  },
  {
    "name": "iam-veeramalla/terraform-zero-to-hero",
    "description": "Master Terraform in 7 days using this Zero to Hero course.",
    "url": "https://github.com/iam-veeramalla/terraform-zero-to-hero",
    "stars": 2517,
    "forks": 10565,
    "language": "HCL",
    "last_updated": "2024-12-10T14:38:24Z",
    "topics": [],
    "owner": {
      "username": "iam-veeramalla",
      "profile_url": "https://github.com/iam-veeramalla"
    }
  },
  {
    "name": "codecrafters-io/build-your-own-x",
    "description": "Master programming by recreating your favorite technologies from scratch.",
    "url": "https://github.com/codecrafters-io/build-your-own-x",
    "stars": 316828,
    "forks": 29384,
    "language": "Markdown",
    "last_updated": "2024-12-11T04:13:12Z",
    "topics": [
      "awesome-list",
      "free",
      "programming",
      "tutorial-code",
      "tutorial-exercises",
      "tutorials"
    ],
    "owner": {
      "username": "codecrafters-io",
      "profile_url": "https://github.com/codecrafters-io"
    }
  },
  {
    "name": "hehonghui/awesome-english-ebooks",
    "description": "\u7ecf\u6d4e\u5b66\u4eba(\u542b\u97f3\u9891)\u3001\u7ebd\u7ea6\u5ba2\u3001\u536b\u62a5\u3001\u8fde\u7ebf\u3001\u5927\u897f\u6d0b\u6708\u520a\u7b49\u82f1\u8bed\u6742\u5fd7\u514d\u8d39\u4e0b\u8f7d,\u652f\u6301epub\u3001mobi\u3001pdf\u683c\u5f0f, \u6bcf\u5468\u66f4\u65b0",
    "url": "https://github.com/hehonghui/awesome-english-ebooks",
    "stars": 22369,
    "forks": 1753,
    "language": "CSS",
    "last_updated": "2024-12-11T02:43:09Z",
    "topics": [
      "download",
      "ebooks",
      "economist",
      "economist-ebooks",
      "new-yorker",
      "pdf"
    ],
    "owner": {
      "username": "hehonghui",
      "profile_url": "https://github.com/hehonghui"
    }
  },
  {
    "name": "TheAlgorithms/Python",
    "description": "All Algorithms implemented in Python",
    "url": "https://github.com/TheAlgorithms/Python",
    "stars": 195441,
    "forks": 45920,
    "language": "Python",
    "last_updated": "2024-12-11T03:59:00Z",
    "topics": [
      "algorithm",
      "algorithm-competitions",
      "algorithms-implemented",
      "algos",
      "community-driven",
      "education",
      "hacktoberfest",
      "interview",
      "learn",
      "practice",
      "python",
      "searches",
      "sorting-algorithms",
      "sorts"
    ],
    "owner": {
      "username": "TheAlgorithms",
      "profile_url": "https://github.com/TheAlgorithms"
    }
  },
  {
    "name": "p0p4k/vits2_pytorch",
    "description": "unofficial vits2-TTS implementation in pytorch",
    "url": "https://github.com/p0p4k/vits2_pytorch",
    "stars": 495,
    "forks": 92,
    "language": "Python",
    "last_updated": "2024-12-08T09:20:18Z",
    "topics": [
      "deep-learning",
      "pytorch",
      "text-to-speech",
      "tts",
      "vits2"
    ],
    "owner": {
      "username": "p0p4k",
      "profile_url": "https://github.com/p0p4k"
    }
  },
  {
    "name": "yezz123/authx",
    "description": "Ready-to-use and customizable Authentications and Oauth2 management for FastAPI \u2728",
    "url": "https://github.com/yezz123/authx",
    "stars": 837,
    "forks": 50,
    "language": "Python",
    "last_updated": "2024-12-08T02:48:15Z",
    "topics": [
      "authentification",
      "authorization",
      "backend",
      "fastapi",
      "jwt",
      "pydantic",
      "python",
      "starlette"
    ],
    "owner": {
      "username": "yezz123",
      "profile_url": "https://github.com/yezz123"
    }
  },
  {
    "name": "Buuntu/fastapi-react",
    "description": "\ud83d\ude80   Cookiecutter Template for FastAPI + React Projects.  Using PostgreSQL, SQLAlchemy, and Docker",
    "url": "https://github.com/Buuntu/fastapi-react",
    "stars": 2252,
    "forks": 351,
    "language": "Python",
    "last_updated": "2024-12-10T03:19:44Z",
    "topics": [
      "boilerplate",
      "cookiecutter",
      "docker",
      "fastapi",
      "full-stack",
      "jwt",
      "nginx",
      "oauth2",
      "postgres",
      "react",
      "react-admin",
      "sqlalchemy",
      "typescript"
    ],
    "owner": {
      "username": "Buuntu",
      "profile_url": "https://github.com/Buuntu"
    }
  },
  {
    "name": "Kludex/awesome-fastapi-projects",
    "description": "List of FastAPI projects! :sunglasses: :rocket: ",
    "url": "https://github.com/Kludex/awesome-fastapi-projects",
    "stars": 1380,
    "forks": 118,
    "language": "TypeScript",
    "last_updated": "2024-12-10T23:22:10Z",
    "topics": [
      "fastapi"
    ],
    "owner": {
      "username": "Kludex",
      "profile_url": "https://github.com/Kludex"
    }
  },
  {
    "name": "s3rius/FastAPI-template",
    "description": "Feature rich robust FastAPI template.",
    "url": "https://github.com/s3rius/FastAPI-template",
    "stars": 2037,
    "forks": 176,
    "language": "Python",
    "last_updated": "2024-12-10T17:15:56Z",
    "topics": [
      "aerich",
      "alembic",
      "asynchronous",
      "asyncio",
      "cookiecutter",
      "cookiecutter-python3",
      "cookiecutter-template",
      "fastapi",
      "fastapi-boilerplate",
      "fastapi-template",
      "graphql",
      "opentelemetry",
      "ormar",
      "prometheus",
      "python3",
      "sentry",
      "sqlalchemy-orm",
      "strawberry-graphql",
      "tortoise-orm"
    ],
    "owner": {
      "username": "s3rius",
      "profile_url": "https://github.com/s3rius"
    }
  },
  {
    "name": "binhnguyennus/awesome-scalability",
    "description": "The Patterns of Scalable, Reliable, and Performant Large-Scale Systems",
    "url": "https://github.com/binhnguyennus/awesome-scalability",
    "stars": 59391,
    "forks": 6082,
    "language": null,
    "last_updated": "2024-12-11T04:09:10Z",
    "topics": [
      "architecture",
      "awesome",
      "awesome-list",
      "backend",
      "big-data",
      "computer-science",
      "design-patterns",
      "devops",
      "distributed-systems",
      "interview",
      "interview-practice",
      "interview-questions",
      "lists",
      "machine-learning",
      "programming",
      "resources",
      "scalability",
      "system",
      "system-design",
      "web-development"
    ],
    "owner": {
      "username": "binhnguyennus",
      "profile_url": "https://github.com/binhnguyennus"
    }
  },
  {
    "name": "synesthesiam/opentts",
    "description": "Open Text to Speech Server",
    "url": "https://github.com/synesthesiam/opentts",
    "stars": 964,
    "forks": 136,
    "language": "Python",
    "last_updated": "2024-12-06T23:27:53Z",
    "topics": [],
    "owner": {
      "username": "synesthesiam",
      "profile_url": "https://github.com/synesthesiam"
    }
  },
  {
    "name": "lllyasviel/Fooocus",
    "description": "Focus on prompting and generating",
    "url": "https://github.com/lllyasviel/Fooocus",
    "stars": 41901,
    "forks": 6013,
    "language": "Python",
    "last_updated": "2024-12-11T02:31:59Z",
    "topics": [],
    "owner": {
      "username": "lllyasviel",
      "profile_url": "https://github.com/lllyasviel"
    }
  },
  {
    "name": "RayVentura/ShortGPT",
    "description": "\ud83d\ude80\ud83c\udfac ShortGPT - Experimental AI framework for youtube shorts / tiktok channel automation",
    "url": "https://github.com/RayVentura/ShortGPT",
    "stars": 5895,
    "forks": 744,
    "language": "Python",
    "last_updated": "2024-12-11T02:26:25Z",
    "topics": [
      "ai",
      "artificial-intelligence",
      "automation",
      "autonomous-agents",
      "content",
      "gpt-4",
      "openai",
      "python",
      "video",
      "video-editing"
    ],
    "owner": {
      "username": "RayVentura",
      "profile_url": "https://github.com/RayVentura"
    }
  },
  {
    "name": "Audio-AGI/AudioSep",
    "description": "Official implementation of \"Separate Anything You Describe\"",
    "url": "https://github.com/Audio-AGI/AudioSep",
    "stars": 1649,
    "forks": 118,
    "language": "Python",
    "last_updated": "2024-12-11T00:21:11Z",
    "topics": [],
    "owner": {
      "username": "Audio-AGI",
      "profile_url": "https://github.com/Audio-AGI"
    }
  },
  {
    "name": "lakahaga/dc-comix-tts",
    "description": "Implementation of DCComix TTS: An End-to-End Expressive TTS with Discrete Code Collaborated with Mixer",
    "url": "https://github.com/lakahaga/dc-comix-tts",
    "stars": 76,
    "forks": 8,
    "language": "Python",
    "last_updated": "2024-11-28T15:15:17Z",
    "topics": [],
    "owner": {
      "username": "lakahaga",
      "profile_url": "https://github.com/lakahaga"
    }
  },
  {
    "name": "b04901014/MQTTS",
    "description": null,
    "url": "https://github.com/b04901014/MQTTS",
    "stars": 254,
    "forks": 36,
    "language": "Python",
    "last_updated": "2024-10-28T05:46:21Z",
    "topics": [],
    "owner": {
      "username": "b04901014",
      "profile_url": "https://github.com/b04901014"
    }
  },
  {
    "name": "modelscope/FunASR",
    "description": "A Fundamental End-to-End Speech Recognition Toolkit and Open Source SOTA Pretrained Models, Supporting Speech Recognition, Voice Activity Detection, Text Post-processing etc.",
    "url": "https://github.com/modelscope/FunASR",
    "stars": 7268,
    "forks": 778,
    "language": "Python",
    "last_updated": "2024-12-11T03:30:46Z",
    "topics": [
      "audio-visual-speech-recognition",
      "conformer",
      "dfsmn",
      "paraformer",
      "pretrained-model",
      "punctuation",
      "pytorch",
      "rnnt",
      "speaker-diarization",
      "speech-recognition",
      "speechgpt",
      "speechllm",
      "vad",
      "voice-activity-detection",
      "whisper"
    ],
    "owner": {
      "username": "modelscope",
      "profile_url": "https://github.com/modelscope"
    }
  },
  {
    "name": "lazyprogrammer/machine_learning_examples",
    "description": "A collection of machine learning examples and tutorials.",
    "url": "https://github.com/lazyprogrammer/machine_learning_examples",
    "stars": 8421,
    "forks": 6348,
    "language": "Python",
    "last_updated": "2024-12-10T14:55:52Z",
    "topics": [
      "data-science",
      "deep-learning",
      "machine-learning",
      "natural-language-processing",
      "python",
      "reinforcement-learning"
    ],
    "owner": {
      "username": "lazyprogrammer",
      "profile_url": "https://github.com/lazyprogrammer"
    }
  },
  {
    "name": "gorse-io/gorse",
    "description": "Gorse open source recommender system engine",
    "url": "https://github.com/gorse-io/gorse",
    "stars": 8646,
    "forks": 793,
    "language": "Go",
    "last_updated": "2024-12-11T02:36:23Z",
    "topics": [
      "collaborative-filtering",
      "go",
      "knn",
      "machine-learning",
      "recommender-system"
    ],
    "owner": {
      "username": "gorse-io",
      "profile_url": "https://github.com/gorse-io"
    }
  },
  {
    "name": "TencentARC/GFPGAN",
    "description": "GFPGAN aims at developing Practical Algorithms for Real-world Face Restoration.",
    "url": "https://github.com/TencentARC/GFPGAN",
    "stars": 35999,
    "forks": 5966,
    "language": "Python",
    "last_updated": "2024-12-11T02:42:45Z",
    "topics": [
      "deep-learning",
      "face-restoration",
      "gan",
      "gfpgan",
      "image-restoration",
      "pytorch",
      "super-resolution"
    ],
    "owner": {
      "username": "TencentARC",
      "profile_url": "https://github.com/TencentARC"
    }
  },
  {
    "name": "labmlai/annotated_deep_learning_paper_implementations",
    "description": "\ud83e\uddd1\u200d\ud83c\udfeb 60+ Implementations/tutorials of deep learning papers with side-by-side notes \ud83d\udcdd; including transformers (original, xl, switch, feedback, vit, ...), optimizers (adam, adabelief, sophia, ...), gans(cyclegan, stylegan2, ...), \ud83c\udfae reinforcement learning (ppo, dqn), capsnet, distillation, ... \ud83e\udde0",
    "url": "https://github.com/labmlai/annotated_deep_learning_paper_implementations",
    "stars": 57041,
    "forks": 5834,
    "language": "Python",
    "last_updated": "2024-12-11T04:00:15Z",
    "topics": [
      "attention",
      "deep-learning",
      "deep-learning-tutorial",
      "gan",
      "literate-programming",
      "lora",
      "machine-learning",
      "neural-networks",
      "optimizers",
      "pytorch",
      "reinforcement-learning",
      "transformer",
      "transformers"
    ],
    "owner": {
      "username": "labmlai",
      "profile_url": "https://github.com/labmlai"
    }
  },
  {
    "name": "Shaunwei/RealChar",
    "description": "\ud83c\udf99\ufe0f\ud83e\udd16Create, Customize and Talk to your AI Character/Companion in Realtime (All in One Codebase!). Have a natural seamless conversation with AI everywhere (mobile, web and terminal) using LLM OpenAI GPT3.5/4, Anthropic Claude2, Chroma Vector DB, Whisper Speech2Text, ElevenLabs Text2Speech\ud83c\udf99\ufe0f\ud83e\udd16",
    "url": "https://github.com/Shaunwei/RealChar",
    "stars": 6045,
    "forks": 738,
    "language": "JavaScript",
    "last_updated": "2024-12-11T02:18:44Z",
    "topics": [],
    "owner": {
      "username": "Shaunwei",
      "profile_url": "https://github.com/Shaunwei"
    }
  },
  {
    "name": "guoyww/AnimateDiff",
    "description": "Official implementation of AnimateDiff.",
    "url": "https://github.com/guoyww/AnimateDiff",
    "stars": 10698,
    "forks": 876,
    "language": "Python",
    "last_updated": "2024-12-11T02:01:31Z",
    "topics": [],
    "owner": {
      "username": "guoyww",
      "profile_url": "https://github.com/guoyww"
    }
  },
  {
    "name": "bazingagin/npc_gzip",
    "description": "Code for Paper: \u201cLow-Resource\u201d Text Classification: A Parameter-Free Classification Method with Compressors",
    "url": "https://github.com/bazingagin/npc_gzip",
    "stars": 1768,
    "forks": 157,
    "language": "Python",
    "last_updated": "2024-12-07T11:00:17Z",
    "topics": [],
    "owner": {
      "username": "bazingagin",
      "profile_url": "https://github.com/bazingagin"
    }
  },
  {
    "name": "EbookFoundation/free-programming-books",
    "description": ":books: Freely available programming books",
    "url": "https://github.com/EbookFoundation/free-programming-books",
    "stars": 341170,
    "forks": 61942,
    "language": "HTML",
    "last_updated": "2024-12-11T03:46:53Z",
    "topics": [
      "books",
      "education",
      "hacktoberfest",
      "list",
      "resource"
    ],
    "owner": {
      "username": "EbookFoundation",
      "profile_url": "https://github.com/EbookFoundation"
    }
  },
  {
    "name": "kenjihiranabe/The-Art-of-Linear-Algebra",
    "description": "Graphic notes on Gilbert Strang's \"Linear Algebra for Everyone\"",
    "url": "https://github.com/kenjihiranabe/The-Art-of-Linear-Algebra",
    "stars": 18180,
    "forks": 2203,
    "language": "PostScript",
    "last_updated": "2024-12-11T00:47:35Z",
    "topics": [],
    "owner": {
      "username": "kenjihiranabe",
      "profile_url": "https://github.com/kenjihiranabe"
    }
  },
  {
    "name": "databricks-academy/large-language-models",
    "description": "Notebooks for Large Language Models (LLMs) Specialization",
    "url": "https://github.com/databricks-academy/large-language-models",
    "stars": 768,
    "forks": 419,
    "language": "Python",
    "last_updated": "2024-12-10T02:32:01Z",
    "topics": [],
    "owner": {
      "username": "databricks-academy",
      "profile_url": "https://github.com/databricks-academy"
    }
  },
  {
    "name": "cedrickchee/awesome-wireguard",
    "description": "A curated list of WireGuard tools, projects, and resources.",
    "url": "https://github.com/cedrickchee/awesome-wireguard",
    "stars": 1048,
    "forks": 60,
    "language": null,
    "last_updated": "2024-12-10T19:00:31Z",
    "topics": [
      "awesome",
      "awesome-list",
      "curated-list",
      "mesh-network",
      "vpn",
      "wireguard"
    ],
    "owner": {
      "username": "cedrickchee",
      "profile_url": "https://github.com/cedrickchee"
    }
  },
  {
    "name": "XingangPan/DragGAN",
    "description": "Official Code for DragGAN (SIGGRAPH 2023)",
    "url": "https://github.com/XingangPan/DragGAN",
    "stars": 35780,
    "forks": 3447,
    "language": "Python",
    "last_updated": "2024-12-11T02:43:16Z",
    "topics": [
      "artificial-intelligence",
      "generative-adversarial-network",
      "generative-models",
      "image-manipulation"
    ],
    "owner": {
      "username": "XingangPan",
      "profile_url": "https://github.com/XingangPan"
    }
  },
  {
    "name": "AI4Finance-Foundation/FinGPT",
    "description": "FinGPT: Open-Source Financial Large Language Models!  Revolutionize \ud83d\udd25    We release the trained model on HuggingFace.",
    "url": "https://github.com/AI4Finance-Foundation/FinGPT",
    "stars": 14318,
    "forks": 1973,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T04:13:19Z",
    "topics": [
      "chatgpt",
      "finance",
      "fingpt",
      "fintech",
      "large-language-models",
      "machine-learning",
      "nlp",
      "prompt-engineering",
      "pytorch",
      "reinforcement-learning",
      "robo-advisor",
      "sentiment-analysis",
      "technical-analysis"
    ],
    "owner": {
      "username": "AI4Finance-Foundation",
      "profile_url": "https://github.com/AI4Finance-Foundation"
    }
  },
  {
    "name": "gpt-engineer-org/gpt-engineer",
    "description": "Platform to experiment with the AI Software Engineer. Terminal based. NOTE: Very different from https://gptengineer.app",
    "url": "https://github.com/gpt-engineer-org/gpt-engineer",
    "stars": 52611,
    "forks": 6842,
    "language": "Python",
    "last_updated": "2024-12-11T03:20:59Z",
    "topics": [
      "ai",
      "autonomous-agent",
      "code-generation",
      "codebase-generation",
      "codegen",
      "coding-assistant",
      "gpt-4",
      "gpt-engineer",
      "openai",
      "python"
    ],
    "owner": {
      "username": "gpt-engineer-org",
      "profile_url": "https://github.com/gpt-engineer-org"
    }
  },
  {
    "name": "jihoo-kim/awesome-RecSys",
    "description": "A curated list of awesome Recommender System (Books, Conferences, Researchers, Papers, Github Repositories, Useful Sites, Youtube Videos)",
    "url": "https://github.com/jihoo-kim/awesome-RecSys",
    "stars": 796,
    "forks": 121,
    "language": null,
    "last_updated": "2024-12-08T11:01:56Z",
    "topics": [],
    "owner": {
      "username": "jihoo-kim",
      "profile_url": "https://github.com/jihoo-kim"
    }
  },
  {
    "name": "ading2210/poe-api",
    "description": "[UNMAINTAINED] A reverse engineered Python API wrapper for Quora's Poe, which provides free access to ChatGPT, GPT-4, and Claude.",
    "url": "https://github.com/ading2210/poe-api",
    "stars": 2506,
    "forks": 316,
    "language": "Python",
    "last_updated": "2024-12-09T04:47:06Z",
    "topics": [
      "chatgpt",
      "graphql",
      "library",
      "poe",
      "python",
      "quora"
    ],
    "owner": {
      "username": "ading2210",
      "profile_url": "https://github.com/ading2210"
    }
  },
  {
    "name": "NaiboWang/EasySpider",
    "description": "A visual no-code/code-free web crawler/spider\u6613\u91c7\u96c6\uff1a\u4e00\u4e2a\u53ef\u89c6\u5316\u6d4f\u89c8\u5668\u81ea\u52a8\u5316\u6d4b\u8bd5/\u6570\u636e\u91c7\u96c6/\u722c\u866b\u8f6f\u4ef6\uff0c\u53ef\u4ee5\u65e0\u4ee3\u7801\u56fe\u5f62\u5316\u7684\u8bbe\u8ba1\u548c\u6267\u884c\u722c\u866b\u4efb\u52a1\u3002\u522b\u540d\uff1aServiceWrapper\u9762\u5411Web\u5e94\u7528\u7684\u667a\u80fd\u5316\u670d\u52a1\u5c01\u88c5\u7cfb\u7edf\u3002",
    "url": "https://github.com/NaiboWang/EasySpider",
    "stars": 36430,
    "forks": 4457,
    "language": "JavaScript",
    "last_updated": "2024-12-11T04:00:25Z",
    "topics": [
      "batch-processing",
      "batch-script",
      "code-free",
      "crawler",
      "data-collection",
      "frontend",
      "gui",
      "html",
      "input-parameters",
      "layman",
      "parameters",
      "robotics",
      "rpa",
      "scraper",
      "spider",
      "visual",
      "visualization",
      "visualprogramming",
      "web",
      "www"
    ],
    "owner": {
      "username": "NaiboWang",
      "profile_url": "https://github.com/NaiboWang"
    }
  },
  {
    "name": "DataTalksClub/project-of-the-week",
    "description": "Learn by doing: DIY project groups at DataTalks.Club ",
    "url": "https://github.com/DataTalksClub/project-of-the-week",
    "stars": 382,
    "forks": 85,
    "language": null,
    "last_updated": "2024-12-10T02:57:00Z",
    "topics": [],
    "owner": {
      "username": "DataTalksClub",
      "profile_url": "https://github.com/DataTalksClub"
    }
  },
  {
    "name": "OpenGVLab/DragGAN",
    "description": "Unofficial Implementation of DragGAN - \"Drag Your GAN: Interactive Point-based Manipulation on the Generative Image Manifold\" \uff08DragGAN \u5168\u529f\u80fd\u5b9e\u73b0\uff0c\u5728\u7ebfDemo\uff0c\u672c\u5730\u90e8\u7f72\u8bd5\u7528\uff0c\u4ee3\u7801\u3001\u6a21\u578b\u5df2\u5168\u90e8\u5f00\u6e90\uff0c\u652f\u6301Windows, macOS, Linux\uff09",
    "url": "https://github.com/OpenGVLab/DragGAN",
    "stars": 4998,
    "forks": 491,
    "language": "Python",
    "last_updated": "2024-12-09T08:00:56Z",
    "topics": [
      "draggan",
      "gradio-interface",
      "image-editing",
      "image-generation",
      "interngpt"
    ],
    "owner": {
      "username": "OpenGVLab",
      "profile_url": "https://github.com/OpenGVLab"
    }
  },
  {
    "name": "OpenGVLab/InternGPT",
    "description": "InternGPT (iGPT) is an open source demo platform where you can easily showcase your AI models. Now it supports DragGAN, ChatGPT, ImageBind, multimodal chat like GPT-4, SAM, interactive image editing, etc. Try it at igpt.opengvlab.com (\u652f\u6301DragGAN\u3001ChatGPT\u3001ImageBind\u3001SAM\u7684\u5728\u7ebfDemo\u7cfb\u7edf)",
    "url": "https://github.com/OpenGVLab/InternGPT",
    "stars": 3208,
    "forks": 232,
    "language": "Python",
    "last_updated": "2024-12-11T04:12:29Z",
    "topics": [
      "chatgpt",
      "click",
      "draggan",
      "foundation-model",
      "gpt",
      "gpt-4",
      "gradio",
      "husky",
      "image-captioning",
      "imagebind",
      "internimage",
      "langchain",
      "llama",
      "llm",
      "multimodal",
      "sam",
      "segment-anything",
      "vicuna",
      "video-generation",
      "vqa"
    ],
    "owner": {
      "username": "OpenGVLab",
      "profile_url": "https://github.com/OpenGVLab"
    }
  },
  {
    "name": "Takaaki-Saeki/zm-text-tts",
    "description": "[IJCAI'23] Learning to Speak from Text for Low-Resource TTS",
    "url": "https://github.com/Takaaki-Saeki/zm-text-tts",
    "stars": 64,
    "forks": 2,
    "language": "Python",
    "last_updated": "2024-09-17T08:39:15Z",
    "topics": [],
    "owner": {
      "username": "Takaaki-Saeki",
      "profile_url": "https://github.com/Takaaki-Saeki"
    }
  },
  {
    "name": "tinygrad/tinygrad",
    "description": "You like pytorch? You like micrograd? You love tinygrad! \u2764\ufe0f ",
    "url": "https://github.com/tinygrad/tinygrad",
    "stars": 27142,
    "forks": 3013,
    "language": "Python",
    "last_updated": "2024-12-11T03:46:16Z",
    "topics": [],
    "owner": {
      "username": "tinygrad",
      "profile_url": "https://github.com/tinygrad"
    }
  },
  {
    "name": "cedrickchee/awesome-ml-model-compression",
    "description": "Awesome machine learning model compression research papers, quantization, tools, and learning material.",
    "url": "https://github.com/cedrickchee/awesome-ml-model-compression",
    "stars": 493,
    "forks": 63,
    "language": null,
    "last_updated": "2024-11-24T09:50:16Z",
    "topics": [
      "awesome-list",
      "machine-learning",
      "model-compression",
      "neural-networks",
      "pruning",
      "quantization"
    ],
    "owner": {
      "username": "cedrickchee",
      "profile_url": "https://github.com/cedrickchee"
    }
  },
  {
    "name": "graviraja/100-Days-of-NLP",
    "description": null,
    "url": "https://github.com/graviraja/100-Days-of-NLP",
    "stars": 320,
    "forks": 113,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-06T13:37:44Z",
    "topics": [
      "100daysofcode",
      "100daysofmlcode",
      "100daysofnlp",
      "deep-learning",
      "deep-neural-networks",
      "machine-learning",
      "natural-language-processing",
      "nlp",
      "pytorch"
    ],
    "owner": {
      "username": "graviraja",
      "profile_url": "https://github.com/graviraja"
    }
  },
  {
    "name": "graviraja/MLOps-Basics",
    "description": null,
    "url": "https://github.com/graviraja/MLOps-Basics",
    "stars": 6108,
    "forks": 1027,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T16:10:38Z",
    "topics": [],
    "owner": {
      "username": "graviraja",
      "profile_url": "https://github.com/graviraja"
    }
  },
  {
    "name": "danielbeach/data-engineering-practice",
    "description": "Data Engineering Practice Problems",
    "url": "https://github.com/danielbeach/data-engineering-practice",
    "stars": 1776,
    "forks": 500,
    "language": "Python",
    "last_updated": "2024-12-10T02:29:36Z",
    "topics": [],
    "owner": {
      "username": "danielbeach",
      "profile_url": "https://github.com/danielbeach"
    }
  },
  {
    "name": "samadhankadam/Hadoop-Ebook",
    "description": null,
    "url": "https://github.com/samadhankadam/Hadoop-Ebook",
    "stars": 126,
    "forks": 0,
    "language": null,
    "last_updated": "2024-01-09T13:17:32Z",
    "topics": [],
    "owner": {
      "username": "samadhankadam",
      "profile_url": "https://github.com/samadhankadam"
    }
  },
  {
    "name": "eugeneyan/applied-ml",
    "description": "\ud83d\udcda Papers & tech blogs by companies sharing their work on data science & machine learning in production.",
    "url": "https://github.com/eugeneyan/applied-ml",
    "stars": 27399,
    "forks": 3696,
    "language": null,
    "last_updated": "2024-12-11T02:52:26Z",
    "topics": [
      "applied-data-science",
      "applied-machine-learning",
      "computer-vision",
      "data-discovery",
      "data-engineering",
      "data-quality",
      "data-science",
      "deep-learning",
      "machine-learning",
      "natural-language-processing",
      "production",
      "recsys",
      "reinforcement-learning",
      "search"
    ],
    "owner": {
      "username": "eugeneyan",
      "profile_url": "https://github.com/eugeneyan"
    }
  },
  {
    "name": "chiphuyen/dmls-book",
    "description": "Summaries and resources for Designing Machine Learning Systems book (Chip Huyen, O'Reilly 2022)",
    "url": "https://github.com/chiphuyen/dmls-book",
    "stars": 2346,
    "forks": 347,
    "language": null,
    "last_updated": "2024-12-11T02:10:57Z",
    "topics": [],
    "owner": {
      "username": "chiphuyen",
      "profile_url": "https://github.com/chiphuyen"
    }
  },
  {
    "name": "ad-freiburg/whitespace-correction",
    "description": "Fast whitespace correction with Transformers",
    "url": "https://github.com/ad-freiburg/whitespace-correction",
    "stars": 15,
    "forks": 0,
    "language": "Python",
    "last_updated": "2024-11-23T21:11:48Z",
    "topics": [],
    "owner": {
      "username": "ad-freiburg",
      "profile_url": "https://github.com/ad-freiburg"
    }
  },
  {
    "name": "behitek/social-scraper",
    "description": "Vietnamese text data crawler scripts for various sites (including Youtube, Facebook, 4rum, news, ...)",
    "url": "https://github.com/behitek/social-scraper",
    "stars": 75,
    "forks": 45,
    "language": "Python",
    "last_updated": "2024-11-17T18:47:32Z",
    "topics": [
      "crawler",
      "crawlers",
      "crawling-framework",
      "instagram",
      "requests",
      "scraper",
      "scraping-websites",
      "selenium-python",
      "youtube"
    ],
    "owner": {
      "username": "behitek",
      "profile_url": "https://github.com/behitek"
    }
  },
  {
    "name": "qdrant/qdrant",
    "description": "Qdrant - High-performance, massive-scale Vector Database and Vector Search Engine for the next generation of AI. Also available in the cloud https://cloud.qdrant.io/",
    "url": "https://github.com/qdrant/qdrant",
    "stars": 20924,
    "forks": 1437,
    "language": "Rust",
    "last_updated": "2024-12-11T03:33:51Z",
    "topics": [
      "approximate-nearest-neighbor-search",
      "embeddings-similarity",
      "hacktoberfest",
      "hnsw",
      "image-search",
      "knn-algorithm",
      "machine-learning",
      "matching",
      "mlops",
      "nearest-neighbor-search",
      "neural-network",
      "neural-search",
      "recommender-system",
      "search",
      "search-engine",
      "search-engines",
      "similarity-search",
      "vector-database",
      "vector-search",
      "vector-search-engine"
    ],
    "owner": {
      "username": "qdrant",
      "profile_url": "https://github.com/qdrant"
    }
  },
  {
    "name": "Avik-Jain/100-Days-Of-ML-Code",
    "description": "100 Days of ML Coding",
    "url": "https://github.com/Avik-Jain/100-Days-Of-ML-Code",
    "stars": 45749,
    "forks": 10664,
    "language": null,
    "last_updated": "2024-12-11T04:02:42Z",
    "topics": [
      "100-days-of-code-log",
      "100daysofcode",
      "deep-learning",
      "implementation",
      "infographics",
      "linear-algebra",
      "linear-regression",
      "logistic-regression",
      "machine-learning",
      "machine-learning-algorithms",
      "naive-bayes-classifier",
      "python",
      "scikit-learn",
      "siraj-raval",
      "siraj-raval-challenge",
      "support-vector-machines",
      "svm",
      "tutorial"
    ],
    "owner": {
      "username": "Avik-Jain",
      "profile_url": "https://github.com/Avik-Jain"
    }
  },
  {
    "name": "hailoc12/docbao_crawler",
    "description": "Framework qu\u00e9t d\u1eef li\u1ec7u tr\u00ean Internet h\u1ed7 tr\u1ee3 render javascript v\u00e0 qu\u00e9t \u0111a nhi\u1ec7m",
    "url": "https://github.com/hailoc12/docbao_crawler",
    "stars": 47,
    "forks": 29,
    "language": "Python",
    "last_updated": "2024-09-02T17:07:23Z",
    "topics": [],
    "owner": {
      "username": "hailoc12",
      "profile_url": "https://github.com/hailoc12"
    }
  },
  {
    "name": "telexyz/vi",
    "description": "X\u00e2y d\u1ef1ng t\u1eadp d\u1eef li\u1ec7u 500GB (20% done) v\u0103n b\u1ea3n ti\u1ebfng Vi\u1ec7t \u0111\u1ec3 hu\u1ea5n luy\u1ec7n m\u00f4 h\u00ecnh ng\u00f4n ng\u1eef l\u1edbn",
    "url": "https://github.com/telexyz/vi",
    "stars": 25,
    "forks": 2,
    "language": "Python",
    "last_updated": "2024-04-17T16:39:34Z",
    "topics": [],
    "owner": {
      "username": "telexyz",
      "profile_url": "https://github.com/telexyz"
    }
  },
  {
    "name": "bigcode-project/starcoder",
    "description": "Home of StarCoder: fine-tuning & inference!",
    "url": "https://github.com/bigcode-project/starcoder",
    "stars": 7339,
    "forks": 522,
    "language": "Python",
    "last_updated": "2024-12-10T18:03:55Z",
    "topics": [],
    "owner": {
      "username": "bigcode-project",
      "profile_url": "https://github.com/bigcode-project"
    }
  },
  {
    "name": "veeral-patel/how-to-secure-anything",
    "description": "How to systematically secure anything: a repository about security engineering",
    "url": "https://github.com/veeral-patel/how-to-secure-anything",
    "stars": 9955,
    "forks": 687,
    "language": null,
    "last_updated": "2024-12-09T15:55:57Z",
    "topics": [
      "secure-design",
      "secure-systems",
      "security",
      "security-architecture",
      "security-assurance",
      "security-engineering",
      "threat-modeling"
    ],
    "owner": {
      "username": "veeral-patel",
      "profile_url": "https://github.com/veeral-patel"
    }
  },
  {
    "name": "puncsky/system-design-and-architecture",
    "description": "Learn how to design large-scale systems. Prep for the system design interview.",
    "url": "https://github.com/puncsky/system-design-and-architecture",
    "stars": 2614,
    "forks": 588,
    "language": "Makefile",
    "last_updated": "2024-12-10T14:53:52Z",
    "topics": [
      "architecture",
      "design",
      "design-patterns",
      "design-system",
      "development",
      "interview",
      "interview-practice",
      "interview-questions",
      "system-design",
      "web"
    ],
    "owner": {
      "username": "puncsky",
      "profile_url": "https://github.com/puncsky"
    }
  },
  {
    "name": "karanpratapsingh/system-design",
    "description": "Learn how to design systems at scale and prepare for system design interviews",
    "url": "https://github.com/karanpratapsingh/system-design",
    "stars": 33186,
    "forks": 3662,
    "language": null,
    "last_updated": "2024-12-11T02:59:10Z",
    "topics": [
      "architecture",
      "distributed-systems",
      "engineering",
      "interview",
      "interview-preparation",
      "microservices",
      "scalability",
      "system-design",
      "system-design-interview",
      "tech"
    ],
    "owner": {
      "username": "karanpratapsingh",
      "profile_url": "https://github.com/karanpratapsingh"
    }
  },
  {
    "name": "bregman-arie/devops-exercises",
    "description": "Linux, Jenkins, AWS, SRE, Prometheus, Docker, Python, Ansible, Git, Kubernetes, Terraform, OpenStack, SQL, NoSQL, Azure, GCP, DNS, Elastic, Network, Virtualization. DevOps Interview Questions",
    "url": "https://github.com/bregman-arie/devops-exercises",
    "stars": 66956,
    "forks": 14956,
    "language": "Python",
    "last_updated": "2024-12-11T04:01:56Z",
    "topics": [
      "ansible",
      "aws",
      "azure",
      "coding",
      "containers",
      "devops",
      "docker",
      "git",
      "interview",
      "interview-questions",
      "kubernetes",
      "linux",
      "openstack",
      "production-engineer",
      "prometheus",
      "python",
      "sql",
      "sre",
      "terraform"
    ],
    "owner": {
      "username": "bregman-arie",
      "profile_url": "https://github.com/bregman-arie"
    }
  },
  {
    "name": "donnemartin/system-design-primer",
    "description": "Learn how to design large-scale systems. Prep for the system design interview.  Includes Anki flashcards.",
    "url": "https://github.com/donnemartin/system-design-primer",
    "stars": 278865,
    "forks": 46669,
    "language": "Python",
    "last_updated": "2024-12-11T03:57:47Z",
    "topics": [
      "design",
      "design-patterns",
      "design-system",
      "development",
      "interview",
      "interview-practice",
      "interview-questions",
      "programming",
      "python",
      "system",
      "web",
      "web-application",
      "webapp"
    ],
    "owner": {
      "username": "donnemartin",
      "profile_url": "https://github.com/donnemartin"
    }
  },
  {
    "name": "OBenner/data-engineering-interview-questions",
    "description": "More than 2000+ Data engineer interview questions.",
    "url": "https://github.com/OBenner/data-engineering-interview-questions",
    "stars": 1177,
    "forks": 420,
    "language": null,
    "last_updated": "2024-12-11T03:41:00Z",
    "topics": [
      "airflow",
      "avro",
      "aws",
      "azure",
      "cassandra",
      "data-engineering",
      "data-structures",
      "flink",
      "flume",
      "hadoop",
      "hadoop-hdfs",
      "hbase",
      "hive",
      "impala",
      "interview",
      "interview-questions",
      "kafka",
      "nifi",
      "spark",
      "sql"
    ],
    "owner": {
      "username": "OBenner",
      "profile_url": "https://github.com/OBenner"
    }
  },
  {
    "name": "igorbarinov/awesome-data-engineering",
    "description": "A curated list of data engineering tools for software developers",
    "url": "https://github.com/igorbarinov/awesome-data-engineering",
    "stars": 6876,
    "forks": 1237,
    "language": null,
    "last_updated": "2024-12-10T19:15:49Z",
    "topics": [
      "awesome",
      "awesome-list"
    ],
    "owner": {
      "username": "igorbarinov",
      "profile_url": "https://github.com/igorbarinov"
    }
  },
  {
    "name": "AIGC-Audio/AudioGPT",
    "description": "AudioGPT: Understanding and Generating Speech, Music, Sound, and Talking Head",
    "url": "https://github.com/AIGC-Audio/AudioGPT",
    "stars": 10059,
    "forks": 867,
    "language": "Python",
    "last_updated": "2024-12-10T07:31:01Z",
    "topics": [
      "audio",
      "gpt",
      "music",
      "sound",
      "speech",
      "talking-head"
    ],
    "owner": {
      "username": "AIGC-Audio",
      "profile_url": "https://github.com/AIGC-Audio"
    }
  },
  {
    "name": "EthicalML/awesome-production-machine-learning",
    "description": "A curated list of awesome open source libraries to deploy, monitor, version and scale your machine learning",
    "url": "https://github.com/EthicalML/awesome-production-machine-learning",
    "stars": 17696,
    "forks": 2257,
    "language": null,
    "last_updated": "2024-12-10T13:39:03Z",
    "topics": [
      "awesome",
      "awesome-list",
      "data-mining",
      "deep-learning",
      "explainability",
      "interpretability",
      "large-scale-machine-learning",
      "large-scale-ml",
      "machine-learning",
      "machine-learning-operations",
      "ml-operations",
      "ml-ops",
      "mlops",
      "privacy-preserving",
      "privacy-preserving-machine-learning",
      "privacy-preserving-ml",
      "production-machine-learning",
      "production-ml",
      "responsible-ai"
    ],
    "owner": {
      "username": "EthicalML",
      "profile_url": "https://github.com/EthicalML"
    }
  },
  {
    "name": "reworkd/AgentGPT",
    "description": "\ud83e\udd16 Assemble, configure, and deploy autonomous AI Agents in your browser.",
    "url": "https://github.com/reworkd/AgentGPT",
    "stars": 32008,
    "forks": 9254,
    "language": "TypeScript",
    "last_updated": "2024-12-11T03:11:18Z",
    "topics": [
      "agent",
      "agentgpt",
      "agi",
      "autogpt",
      "baby-agi",
      "gpt",
      "langchain",
      "next",
      "openai",
      "t3",
      "t3-stack"
    ],
    "owner": {
      "username": "reworkd",
      "profile_url": "https://github.com/reworkd"
    }
  },
  {
    "name": "f/awesome-chatgpt-prompts",
    "description": "This repo includes ChatGPT prompt curation to use ChatGPT better.",
    "url": "https://github.com/f/awesome-chatgpt-prompts",
    "stars": 113867,
    "forks": 15540,
    "language": "HTML",
    "last_updated": "2024-12-11T03:44:19Z",
    "topics": [
      "bots",
      "chatbot",
      "chatgpt",
      "chatgpt-api",
      "language"
    ],
    "owner": {
      "username": "f",
      "profile_url": "https://github.com/f"
    }
  },
  {
    "name": "tatsu-lab/stanford_alpaca",
    "description": "Code and documentation to train Stanford's Alpaca models, and generate the data.",
    "url": "https://github.com/tatsu-lab/stanford_alpaca",
    "stars": 29641,
    "forks": 4056,
    "language": "Python",
    "last_updated": "2024-12-11T02:40:27Z",
    "topics": [
      "deep-learning",
      "instruction-following",
      "language-model"
    ],
    "owner": {
      "username": "tatsu-lab",
      "profile_url": "https://github.com/tatsu-lab"
    }
  },
  {
    "name": "sukun1045/music_basic_theory",
    "description": null,
    "url": "https://github.com/sukun1045/music_basic_theory",
    "stars": 7,
    "forks": 0,
    "language": null,
    "last_updated": "2023-04-12T02:53:21Z",
    "topics": [],
    "owner": {
      "username": "sukun1045",
      "profile_url": "https://github.com/sukun1045"
    }
  },
  {
    "name": "geekyutao/Inpaint-Anything",
    "description": "Inpaint anything using Segment Anything and inpainting models.",
    "url": "https://github.com/geekyutao/Inpaint-Anything",
    "stars": 6681,
    "forks": 560,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T02:45:38Z",
    "topics": [],
    "owner": {
      "username": "geekyutao",
      "profile_url": "https://github.com/geekyutao"
    }
  },
  {
    "name": "oobabooga/text-generation-webui",
    "description": "A Gradio web UI for Large Language Models.",
    "url": "https://github.com/oobabooga/text-generation-webui",
    "stars": 41046,
    "forks": 5346,
    "language": "Python",
    "last_updated": "2024-12-11T04:12:10Z",
    "topics": [],
    "owner": {
      "username": "oobabooga",
      "profile_url": "https://github.com/oobabooga"
    }
  },
  {
    "name": "run-llama/llama_index",
    "description": "LlamaIndex is a data framework for your LLM applications",
    "url": "https://github.com/run-llama/llama_index",
    "stars": 37260,
    "forks": 5344,
    "language": "Python",
    "last_updated": "2024-12-11T03:37:27Z",
    "topics": [
      "agents",
      "application",
      "data",
      "fine-tuning",
      "framework",
      "llamaindex",
      "llm",
      "multi-agents",
      "rag",
      "vector-database"
    ],
    "owner": {
      "username": "run-llama",
      "profile_url": "https://github.com/run-llama"
    }
  },
  {
    "name": "Significant-Gravitas/AutoGPT",
    "description": "AutoGPT is the vision of accessible AI for everyone, to use and to build on. Our mission is to provide the tools, so that you can focus on what matters.",
    "url": "https://github.com/Significant-Gravitas/AutoGPT",
    "stars": 169049,
    "forks": 44527,
    "language": "Python",
    "last_updated": "2024-12-11T04:08:02Z",
    "topics": [
      "ai",
      "artificial-intelligence",
      "autonomous-agents",
      "gpt-4",
      "openai",
      "python"
    ],
    "owner": {
      "username": "Significant-Gravitas",
      "profile_url": "https://github.com/Significant-Gravitas"
    }
  },
  {
    "name": "ga642381/Speech-Prompts-Adapters",
    "description": "This Repository surveys the paper focusing on Prompting and Adapters for Speech Processing. ",
    "url": "https://github.com/ga642381/Speech-Prompts-Adapters",
    "stars": 105,
    "forks": 5,
    "language": null,
    "last_updated": "2024-12-04T02:07:51Z",
    "topics": [
      "adapter",
      "awesome-list",
      "papers",
      "parameter-efficient-learning",
      "prompt",
      "reprogramming",
      "speech"
    ],
    "owner": {
      "username": "ga642381",
      "profile_url": "https://github.com/ga642381"
    }
  },
  {
    "name": "dair-ai/ML-Papers-of-the-Week",
    "description": "\ud83d\udd25Highlighting the top ML papers every week.",
    "url": "https://github.com/dair-ai/ML-Papers-of-the-Week",
    "stars": 10385,
    "forks": 613,
    "language": null,
    "last_updated": "2024-12-11T03:48:40Z",
    "topics": [
      "ai",
      "data-science",
      "deeplearning",
      "machine-learning",
      "nlp"
    ],
    "owner": {
      "username": "dair-ai",
      "profile_url": "https://github.com/dair-ai"
    }
  },
  {
    "name": "Ayush7-BIT/Google-Facilitator-Program-Solutions",
    "description": null,
    "url": "https://github.com/Ayush7-BIT/Google-Facilitator-Program-Solutions",
    "stars": 145,
    "forks": 467,
    "language": null,
    "last_updated": "2024-12-09T07:02:13Z",
    "topics": [],
    "owner": {
      "username": "Ayush7-BIT",
      "profile_url": "https://github.com/Ayush7-BIT"
    }
  },
  {
    "name": "OpenGVLab/LLaMA-Adapter",
    "description": "[ICLR 2024] Fine-tuning LLaMA to follow Instructions within 1 Hour and 1.2M Parameters",
    "url": "https://github.com/OpenGVLab/LLaMA-Adapter",
    "stars": 5772,
    "forks": 374,
    "language": "Python",
    "last_updated": "2024-12-11T03:10:35Z",
    "topics": [],
    "owner": {
      "username": "OpenGVLab",
      "profile_url": "https://github.com/OpenGVLab"
    }
  },
  {
    "name": "telexyz/GPT4VN",
    "description": "Ai c\u0169ng c\u00f3 th\u1ec3 t\u1ef1 t\u1ea1o chatbot b\u1eb1ng hu\u1ea5n luy\u1ec7n ch\u1ec9 d\u1eabn, v\u1edbi 12G GPU (RTX 3060) v\u00e0 kho\u1ea3ng v\u00e0i ch\u1ee5c MB d\u1eef li\u1ec7u",
    "url": "https://github.com/telexyz/GPT4VN",
    "stars": 111,
    "forks": 36,
    "language": "Python",
    "last_updated": "2024-10-11T06:13:19Z",
    "topics": [],
    "owner": {
      "username": "telexyz",
      "profile_url": "https://github.com/telexyz"
    }
  },
  {
    "name": "bbbestb/KeXueShangWang_Google_Facebook_Twitter_VPN_VPS_Proxy",
    "description": "\u79d1\u5b66\u4e0a\u7f51\ud83d\udfe2\ud83d\udfe2\u79d1\u5b66\u4e0a\u7f51\ud83d\udd34\ud83d\udd34\u79d1\u5b66\u4e0a\u7f51\ud83d\udfe1\ud83d\udfe1\u79d1\u5b66\u4e0a\u7f51",
    "url": "https://github.com/bbbestb/KeXueShangWang_Google_Facebook_Twitter_VPN_VPS_Proxy",
    "stars": 626,
    "forks": 78,
    "language": "Python",
    "last_updated": "2024-12-09T18:35:37Z",
    "topics": [
      "kexue",
      "shangwang",
      "vpn"
    ],
    "owner": {
      "username": "bbbestb",
      "profile_url": "https://github.com/bbbestb"
    }
  },
  {
    "name": "Voice-Lab/VoiceLab",
    "description": "Automated Reproducible Acoustical Analysis",
    "url": "https://github.com/Voice-Lab/VoiceLab",
    "stars": 145,
    "forks": 18,
    "language": "Python",
    "last_updated": "2024-12-04T01:53:43Z",
    "topics": [
      "acoustic-analysis",
      "open-science",
      "python",
      "python3",
      "speech-processing",
      "voice-analysis",
      "voice-manipulation"
    ],
    "owner": {
      "username": "Voice-Lab",
      "profile_url": "https://github.com/Voice-Lab"
    }
  },
  {
    "name": "NafisiAslH/KnowledgeSharing",
    "description": null,
    "url": "https://github.com/NafisiAslH/KnowledgeSharing",
    "stars": 1114,
    "forks": 274,
    "language": "Python",
    "last_updated": "2024-12-09T01:44:39Z",
    "topics": [],
    "owner": {
      "username": "NafisiAslH",
      "profile_url": "https://github.com/NafisiAslH"
    }
  },
  {
    "name": "getcursor/cursor",
    "description": "The AI Code Editor",
    "url": "https://github.com/getcursor/cursor",
    "stars": 25980,
    "forks": 1612,
    "language": null,
    "last_updated": "2024-12-11T04:09:59Z",
    "topics": [],
    "owner": {
      "username": "getcursor",
      "profile_url": "https://github.com/getcursor"
    }
  },
  {
    "name": "showlab/Tune-A-Video",
    "description": "[ICCV 2023] Tune-A-Video: One-Shot Tuning of Image Diffusion Models for Text-to-Video Generation",
    "url": "https://github.com/showlab/Tune-A-Video",
    "stars": 4272,
    "forks": 385,
    "language": "Python",
    "last_updated": "2024-12-10T17:53:07Z",
    "topics": [],
    "owner": {
      "username": "showlab",
      "profile_url": "https://github.com/showlab"
    }
  },
  {
    "name": "Kinyugo/msanii",
    "description": "A novel diffusion-based model for synthesizing long-context, high-fidelity music efficiently.",
    "url": "https://github.com/Kinyugo/msanii",
    "stars": 194,
    "forks": 10,
    "language": "Python",
    "last_updated": "2024-09-05T07:42:18Z",
    "topics": [],
    "owner": {
      "username": "Kinyugo",
      "profile_url": "https://github.com/Kinyugo"
    }
  },
  {
    "name": "lucidrains/gigagan-pytorch",
    "description": "Implementation of GigaGAN, new SOTA GAN out of Adobe. Culmination of nearly a decade of research into GANs",
    "url": "https://github.com/lucidrains/gigagan-pytorch",
    "stars": 1841,
    "forks": 108,
    "language": "Python",
    "last_updated": "2024-12-02T01:57:32Z",
    "topics": [
      "artificial-intelligence",
      "deep-learning",
      "generative-adversarial-network"
    ],
    "owner": {
      "username": "lucidrains",
      "profile_url": "https://github.com/lucidrains"
    }
  },
  {
    "name": "developershomes/SparkETL",
    "description": "Spark all the ETL Pipelines",
    "url": "https://github.com/developershomes/SparkETL",
    "stars": 32,
    "forks": 19,
    "language": "Jupyter Notebook",
    "last_updated": "2024-10-28T13:50:36Z",
    "topics": [],
    "owner": {
      "username": "developershomes",
      "profile_url": "https://github.com/developershomes"
    }
  },
  {
    "name": "alanchn31/Data-Engineering-Projects",
    "description": "Personal Data Engineering Projects",
    "url": "https://github.com/alanchn31/Data-Engineering-Projects",
    "stars": 871,
    "forks": 191,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-09T21:39:53Z",
    "topics": [
      "airflow",
      "aws-redshift",
      "cassandra",
      "data-engineering",
      "data-engineering-nanodegree",
      "data-lake",
      "data-modeling",
      "data-warehouse",
      "ingest-data",
      "mongodb",
      "postgres",
      "scrapy",
      "spark",
      "star-schema"
    ],
    "owner": {
      "username": "alanchn31",
      "profile_url": "https://github.com/alanchn31"
    }
  },
  {
    "name": "ggerganov/llama.cpp",
    "description": "LLM inference in C/C++",
    "url": "https://github.com/ggerganov/llama.cpp",
    "stars": 69058,
    "forks": 9919,
    "language": "C++",
    "last_updated": "2024-12-11T03:45:13Z",
    "topics": [
      "ggml",
      "llama"
    ],
    "owner": {
      "username": "ggerganov",
      "profile_url": "https://github.com/ggerganov"
    }
  },
  {
    "name": "christianversloot/machine-learning-articles",
    "description": "\ud83e\udde0\ud83d\udcac Articles I wrote about machine learning, archived from MachineCurve.com.",
    "url": "https://github.com/christianversloot/machine-learning-articles",
    "stars": 3463,
    "forks": 740,
    "language": null,
    "last_updated": "2024-12-09T14:13:30Z",
    "topics": [
      "albert",
      "bert",
      "clustering",
      "convolutional-neural-networks",
      "dbscan",
      "deep-learning",
      "gan",
      "gans",
      "gpt",
      "huggingface-transformers",
      "keras",
      "keras-tensorflow",
      "machine-learning",
      "neural-networks",
      "pytorch",
      "pytorch-implementation",
      "pytorch-tutorial",
      "scikit-learn",
      "tensorflow",
      "transformers"
    ],
    "owner": {
      "username": "christianversloot",
      "profile_url": "https://github.com/christianversloot"
    }
  },
  {
    "name": "chenfei-wu/TaskMatrix",
    "description": null,
    "url": "https://github.com/chenfei-wu/TaskMatrix",
    "stars": 34558,
    "forks": 3318,
    "language": "Python",
    "last_updated": "2024-12-11T03:29:06Z",
    "topics": [],
    "owner": {
      "username": "chenfei-wu",
      "profile_url": "https://github.com/chenfei-wu"
    }
  },
  {
    "name": "liusongxiang/Large-Audio-Models",
    "description": "Keep track of big models in audio domain, including speech, singing, music etc.",
    "url": "https://github.com/liusongxiang/Large-Audio-Models",
    "stars": 463,
    "forks": 28,
    "language": null,
    "last_updated": "2024-12-04T13:16:49Z",
    "topics": [],
    "owner": {
      "username": "liusongxiang",
      "profile_url": "https://github.com/liusongxiang"
    }
  },
  {
    "name": "lucidrains/PaLM-rlhf-pytorch",
    "description": "Implementation of RLHF (Reinforcement Learning with Human Feedback) on top of the PaLM architecture. Basically ChatGPT but with PaLM",
    "url": "https://github.com/lucidrains/PaLM-rlhf-pytorch",
    "stars": 7723,
    "forks": 670,
    "language": "Python",
    "last_updated": "2024-12-10T11:37:51Z",
    "topics": [
      "artificial-intelligence",
      "attention-mechanisms",
      "deep-learning",
      "human-feedback",
      "reinforcement-learning",
      "transformers"
    ],
    "owner": {
      "username": "lucidrains",
      "profile_url": "https://github.com/lucidrains"
    }
  },
  {
    "name": "meilisearch/meilisearch-python",
    "description": "Python wrapper for the Meilisearch API",
    "url": "https://github.com/meilisearch/meilisearch-python",
    "stars": 466,
    "forks": 86,
    "language": "Python",
    "last_updated": "2024-12-06T09:52:22Z",
    "topics": [
      "client",
      "meilisearch",
      "sdk"
    ],
    "owner": {
      "username": "meilisearch",
      "profile_url": "https://github.com/meilisearch"
    }
  },
  {
    "name": "visenger/awesome-mlops",
    "description": "A curated list of references for MLOps ",
    "url": "https://github.com/visenger/awesome-mlops",
    "stars": 12662,
    "forks": 1896,
    "language": null,
    "last_updated": "2024-12-10T15:18:47Z",
    "topics": [
      "ai",
      "data-science",
      "devops",
      "engineering",
      "federated-learning",
      "machine-learning",
      "ml",
      "mlops",
      "software-engineering"
    ],
    "owner": {
      "username": "visenger",
      "profile_url": "https://github.com/visenger"
    }
  },
  {
    "name": "dair-ai/Prompt-Engineering-Guide",
    "description": "\ud83d\udc19 Guides, papers, lecture, notebooks and resources for prompt engineering",
    "url": "https://github.com/dair-ai/Prompt-Engineering-Guide",
    "stars": 50963,
    "forks": 4947,
    "language": "MDX",
    "last_updated": "2024-12-11T03:55:00Z",
    "topics": [
      "chatgpt",
      "deep-learning",
      "generative-ai",
      "language-model",
      "openai",
      "prompt-engineering"
    ],
    "owner": {
      "username": "dair-ai",
      "profile_url": "https://github.com/dair-ai"
    }
  },
  {
    "name": "awesome-spark/awesome-spark",
    "description": "A curated list of awesome Apache Spark packages and resources.",
    "url": "https://github.com/awesome-spark/awesome-spark",
    "stars": 1732,
    "forks": 331,
    "language": "Shell",
    "last_updated": "2024-12-09T22:26:05Z",
    "topics": [
      "apache-spark",
      "awesome",
      "pyspark",
      "sparkr"
    ],
    "owner": {
      "username": "awesome-spark",
      "profile_url": "https://github.com/awesome-spark"
    }
  },
  {
    "name": "ali-vilab/composer",
    "description": "Official implementation of \"Composer: Creative and Controllable Image Synthesis with Composable Conditions\"",
    "url": "https://github.com/ali-vilab/composer",
    "stars": 1545,
    "forks": 48,
    "language": null,
    "last_updated": "2024-12-08T14:19:06Z",
    "topics": [],
    "owner": {
      "username": "ali-vilab",
      "profile_url": "https://github.com/ali-vilab"
    }
  },
  {
    "name": "amazon-science/mm-cot",
    "description": "Official implementation for \"Multimodal Chain-of-Thought Reasoning in Language Models\" (stay tuned and more will be updated)",
    "url": "https://github.com/amazon-science/mm-cot",
    "stars": 3830,
    "forks": 315,
    "language": "Python",
    "last_updated": "2024-12-11T03:00:12Z",
    "topics": [],
    "owner": {
      "username": "amazon-science",
      "profile_url": "https://github.com/amazon-science"
    }
  },
  {
    "name": "PlayVoice/lora-svc",
    "description": "singing voice change based on whisper, and lora for singing voice clone",
    "url": "https://github.com/PlayVoice/lora-svc",
    "stars": 631,
    "forks": 78,
    "language": "Python",
    "last_updated": "2024-11-30T18:31:59Z",
    "topics": [
      "lora",
      "singing-voice-conversion",
      "speech-to-sing",
      "uni-svc",
      "vits",
      "vits-svc",
      "voice-change",
      "voice-cloning",
      "voice-conversion",
      "whisper"
    ],
    "owner": {
      "username": "PlayVoice",
      "profile_url": "https://github.com/PlayVoice"
    }
  },
  {
    "name": "haoheliu/AudioLDM",
    "description": "AudioLDM: Generate speech, sound effects, music and beyond, with text.",
    "url": "https://github.com/haoheliu/AudioLDM",
    "stars": 2479,
    "forks": 225,
    "language": "Python",
    "last_updated": "2024-12-10T20:56:07Z",
    "topics": [
      "audio-generation"
    ],
    "owner": {
      "username": "haoheliu",
      "profile_url": "https://github.com/haoheliu"
    }
  },
  {
    "name": "data-engineering-community/data-engineering-wiki",
    "description": "The best place to learn data engineering. Built and maintained by the data engineering community.",
    "url": "https://github.com/data-engineering-community/data-engineering-wiki",
    "stars": 1462,
    "forks": 155,
    "language": "CSS",
    "last_updated": "2024-12-10T21:36:53Z",
    "topics": [
      "data",
      "data-engineer",
      "data-engineering",
      "data-modeling",
      "data-pipelines",
      "database",
      "etl",
      "sql"
    ],
    "owner": {
      "username": "data-engineering-community",
      "profile_url": "https://github.com/data-engineering-community"
    }
  },
  {
    "name": "adilkhash/Data-Engineering-HowTo",
    "description": "A list of useful resources to learn Data Engineering from scratch",
    "url": "https://github.com/adilkhash/Data-Engineering-HowTo",
    "stars": 3557,
    "forks": 508,
    "language": null,
    "last_updated": "2024-12-11T03:11:22Z",
    "topics": [
      "cloud-providers",
      "data-engineering",
      "data-pipeline",
      "distributed-systems",
      "scala"
    ],
    "owner": {
      "username": "adilkhash",
      "profile_url": "https://github.com/adilkhash"
    }
  },
  {
    "name": "GokuMohandas/mlops-course",
    "description": "Learn how to design, develop, deploy and iterate on production-grade ML applications.",
    "url": "https://github.com/GokuMohandas/mlops-course",
    "stars": 2984,
    "forks": 516,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-09T21:50:00Z",
    "topics": [
      "data-engineering",
      "data-quality",
      "data-science",
      "deep-learning",
      "distributed-ml",
      "llms",
      "machine-learning",
      "mlops",
      "natural-language-processing",
      "python",
      "pytorch",
      "ray"
    ],
    "owner": {
      "username": "GokuMohandas",
      "profile_url": "https://github.com/GokuMohandas"
    }
  },
  {
    "name": "google-research/tuning_playbook",
    "description": "A playbook for systematically maximizing the performance of deep learning models.",
    "url": "https://github.com/google-research/tuning_playbook",
    "stars": 27508,
    "forks": 2281,
    "language": null,
    "last_updated": "2024-12-11T02:15:30Z",
    "topics": [],
    "owner": {
      "username": "google-research",
      "profile_url": "https://github.com/google-research"
    }
  },
  {
    "name": "ant-design/ant-design",
    "description": "An enterprise-class UI design language and React UI library",
    "url": "https://github.com/ant-design/ant-design",
    "stars": 92814,
    "forks": 50226,
    "language": "TypeScript",
    "last_updated": "2024-12-11T03:56:28Z",
    "topics": [
      "ant-design",
      "antd",
      "design-systems",
      "react",
      "typescript",
      "ui-kit",
      "ui-library"
    ],
    "owner": {
      "username": "ant-design",
      "profile_url": "https://github.com/ant-design"
    }
  },
  {
    "name": "PyExplained/Autotune-using-Python",
    "description": null,
    "url": "https://github.com/PyExplained/Autotune-using-Python",
    "stars": 12,
    "forks": 0,
    "language": "Python",
    "last_updated": "2024-06-17T13:41:59Z",
    "topics": [],
    "owner": {
      "username": "PyExplained",
      "profile_url": "https://github.com/PyExplained"
    }
  },
  {
    "name": "LinXueyuanStdio/chatgpt-review-rebuttal-extension",
    "description": "ChatGPT - Review & Rebuttal: A browser extension for generating reviews and rebuttals, powered by ChatGPT. \u5229\u7528 ChatGPT \u751f\u6210\u5ba1\u7a3f\u610f\u89c1\u548c\u56de\u590d\u7684\u6d4f\u89c8\u5668\u63d2\u4ef6",
    "url": "https://github.com/LinXueyuanStdio/chatgpt-review-rebuttal-extension",
    "stars": 249,
    "forks": 8,
    "language": "TypeScript",
    "last_updated": "2024-08-01T01:58:09Z",
    "topics": [
      "chatgpt",
      "chorme",
      "chorme-extension",
      "edge",
      "firefox",
      "openreview",
      "rebuttal",
      "review"
    ],
    "owner": {
      "username": "LinXueyuanStdio",
      "profile_url": "https://github.com/LinXueyuanStdio"
    }
  },
  {
    "name": "lifeiteng/vall-e",
    "description": "PyTorch implementation of VALL-E(Zero-Shot Text-To-Speech), Reproduced Demo https://lifeiteng.github.io/valle/index.html",
    "url": "https://github.com/lifeiteng/vall-e",
    "stars": 2060,
    "forks": 319,
    "language": "Python",
    "last_updated": "2024-12-10T03:39:46Z",
    "topics": [
      "chatgpt",
      "in-context-learning",
      "large-language-models",
      "text-to-speech",
      "tts",
      "vall-e",
      "valle"
    ],
    "owner": {
      "username": "lifeiteng",
      "profile_url": "https://github.com/lifeiteng"
    }
  },
  {
    "name": "DataTalksClub/awesome-data-podcasts",
    "description": "A list of awesome data podcasts",
    "url": "https://github.com/DataTalksClub/awesome-data-podcasts",
    "stars": 369,
    "forks": 56,
    "language": null,
    "last_updated": "2024-12-04T13:51:11Z",
    "topics": [],
    "owner": {
      "username": "DataTalksClub",
      "profile_url": "https://github.com/DataTalksClub"
    }
  },
  {
    "name": "EthicalML/awesome-artificial-intelligence-regulation",
    "description": "This repository aims to map the ecosystem of artificial intelligence guidelines, principles, codes of ethics, standards, regulation and beyond.",
    "url": "https://github.com/EthicalML/awesome-artificial-intelligence-regulation",
    "stars": 1276,
    "forks": 169,
    "language": null,
    "last_updated": "2024-12-10T21:58:27Z",
    "topics": [
      "ai",
      "ai-ethics",
      "ai-guidelines",
      "ai-policy",
      "data-ethics",
      "data-protection",
      "ethical-ai",
      "ethics-frameworks",
      "guidelines",
      "institute-for-ethical-ai",
      "machine-learning",
      "machine-learning-guidelines",
      "principles",
      "privacy",
      "regulation"
    ],
    "owner": {
      "username": "EthicalML",
      "profile_url": "https://github.com/EthicalML"
    }
  },
  {
    "name": "JusperLee/TDANet",
    "description": "An efficient speech separation method",
    "url": "https://github.com/JusperLee/TDANet",
    "stars": 268,
    "forks": 30,
    "language": "Python",
    "last_updated": "2024-12-11T03:27:41Z",
    "topics": [],
    "owner": {
      "username": "JusperLee",
      "profile_url": "https://github.com/JusperLee"
    }
  },
  {
    "name": "fathyb/carbonyl",
    "description": "Chromium running inside your terminal",
    "url": "https://github.com/fathyb/carbonyl",
    "stars": 14775,
    "forks": 288,
    "language": "Rust",
    "last_updated": "2024-12-11T01:36:55Z",
    "topics": [
      "browser",
      "chromium",
      "terminal"
    ],
    "owner": {
      "username": "fathyb",
      "profile_url": "https://github.com/fathyb"
    }
  },
  {
    "name": "interactiveaudiolab/penn",
    "description": "Pitch Estimating Neural Networks (PENN)",
    "url": "https://github.com/interactiveaudiolab/penn",
    "stars": 236,
    "forks": 22,
    "language": "Python",
    "last_updated": "2024-12-02T22:02:04Z",
    "topics": [
      "frequency",
      "music",
      "periodicity",
      "pitch",
      "speech",
      "voicing"
    ],
    "owner": {
      "username": "interactiveaudiolab",
      "profile_url": "https://github.com/interactiveaudiolab"
    }
  },
  {
    "name": "slp-rl/aero",
    "description": "This repo contains the official PyTorch implementation of \"Audio Super Resolution in the Spectral Domain\" (ICASSP 2023)",
    "url": "https://github.com/slp-rl/aero",
    "stars": 207,
    "forks": 27,
    "language": "Python",
    "last_updated": "2024-11-26T03:25:31Z",
    "topics": [
      "audio",
      "audio-processing",
      "audio-super-resolution",
      "bandwidth-extension",
      "machine-learning",
      "pytorch",
      "speech-synthesis"
    ],
    "owner": {
      "username": "slp-rl",
      "profile_url": "https://github.com/slp-rl"
    }
  },
  {
    "name": "TooTouch/DUAD",
    "description": "Unofficial Implementation for Deep Unsupervised Anomaly Detection (DUAD)",
    "url": "https://github.com/TooTouch/DUAD",
    "stars": 3,
    "forks": 0,
    "language": "Python",
    "last_updated": "2023-01-17T01:40:10Z",
    "topics": [],
    "owner": {
      "username": "TooTouch",
      "profile_url": "https://github.com/TooTouch"
    }
  },
  {
    "name": "apache/druid",
    "description": "Apache Druid: a high performance real-time analytics database.",
    "url": "https://github.com/apache/druid",
    "stars": 13542,
    "forks": 3709,
    "language": "Java",
    "last_updated": "2024-12-10T19:44:03Z",
    "topics": [
      "druid"
    ],
    "owner": {
      "username": "apache",
      "profile_url": "https://github.com/apache"
    }
  },
  {
    "name": "JuanCrg90/Clean-Code-Notes",
    "description": "My notes of Clean Code book",
    "url": "https://github.com/JuanCrg90/Clean-Code-Notes",
    "stars": 5891,
    "forks": 819,
    "language": null,
    "last_updated": "2024-12-06T08:47:44Z",
    "topics": [
      "book",
      "clean-code",
      "notes"
    ],
    "owner": {
      "username": "JuanCrg90",
      "profile_url": "https://github.com/JuanCrg90"
    }
  },
  {
    "name": "chq1155/A-Survey-on-Generative-Diffusion-Model",
    "description": null,
    "url": "https://github.com/chq1155/A-Survey-on-Generative-Diffusion-Model",
    "stars": 922,
    "forks": 60,
    "language": null,
    "last_updated": "2024-12-07T03:05:08Z",
    "topics": [],
    "owner": {
      "username": "chq1155",
      "profile_url": "https://github.com/chq1155"
    }
  },
  {
    "name": "matplotlib/cheatsheets",
    "description": "Official Matplotlib cheat sheets",
    "url": "https://github.com/matplotlib/cheatsheets",
    "stars": 7380,
    "forks": 896,
    "language": "Python",
    "last_updated": "2024-12-11T01:40:30Z",
    "topics": [
      "cheatsheet",
      "matplotlib",
      "python"
    ],
    "owner": {
      "username": "matplotlib",
      "profile_url": "https://github.com/matplotlib"
    }
  },
  {
    "name": "rougier/scientific-visualization-book",
    "description": "An open access book on scientific visualization using python and matplotlib",
    "url": "https://github.com/rougier/scientific-visualization-book",
    "stars": 10734,
    "forks": 993,
    "language": "Python",
    "last_updated": "2024-12-10T12:51:23Z",
    "topics": [
      "book",
      "dataviz",
      "matplotlib",
      "numpy",
      "open-access",
      "plotting",
      "python",
      "scientific-publications"
    ],
    "owner": {
      "username": "rougier",
      "profile_url": "https://github.com/rougier"
    }
  },
  {
    "name": "alibaba-damo-academy/SpokenNLP",
    "description": "A wide variety of research projects developed by the SpokenNLP team of Speech Lab, Alibaba Group.",
    "url": "https://github.com/alibaba-damo-academy/SpokenNLP",
    "stars": 110,
    "forks": 11,
    "language": "Python",
    "last_updated": "2024-11-24T03:13:50Z",
    "topics": [
      "deep-learning",
      "machine-learning",
      "natural-language-processing",
      "nlp",
      "python",
      "pytorch"
    ],
    "owner": {
      "username": "alibaba-damo-academy",
      "profile_url": "https://github.com/alibaba-damo-academy"
    }
  },
  {
    "name": "facebookresearch/xformers",
    "description": "Hackable and optimized Transformers building blocks, supporting a composable construction.",
    "url": "https://github.com/facebookresearch/xformers",
    "stars": 8759,
    "forks": 629,
    "language": "Python",
    "last_updated": "2024-12-10T14:03:32Z",
    "topics": [],
    "owner": {
      "username": "facebookresearch",
      "profile_url": "https://github.com/facebookresearch"
    }
  },
  {
    "name": "mli/paper-reading",
    "description": "\u6df1\u5ea6\u5b66\u4e60\u7ecf\u5178\u3001\u65b0\u8bba\u6587\u9010\u6bb5\u7cbe\u8bfb",
    "url": "https://github.com/mli/paper-reading",
    "stars": 27446,
    "forks": 2463,
    "language": null,
    "last_updated": "2024-12-11T03:00:58Z",
    "topics": [
      "deep-learning",
      "paper",
      "reading-list"
    ],
    "owner": {
      "username": "mli",
      "profile_url": "https://github.com/mli"
    }
  },
  {
    "name": "facebookresearch/detr",
    "description": "End-to-End Object Detection with Transformers",
    "url": "https://github.com/facebookresearch/detr",
    "stars": 13733,
    "forks": 2476,
    "language": "Python",
    "last_updated": "2024-12-11T03:21:12Z",
    "topics": [],
    "owner": {
      "username": "facebookresearch",
      "profile_url": "https://github.com/facebookresearch"
    }
  },
  {
    "name": "karpathy/nanoGPT",
    "description": "The simplest, fastest repository for training/finetuning medium-sized GPTs.",
    "url": "https://github.com/karpathy/nanoGPT",
    "stars": 37808,
    "forks": 6038,
    "language": "Python",
    "last_updated": "2024-12-11T04:08:30Z",
    "topics": [],
    "owner": {
      "username": "karpathy",
      "profile_url": "https://github.com/karpathy"
    }
  },
  {
    "name": "ming024/ming024.github.io",
    "description": null,
    "url": "https://github.com/ming024/ming024.github.io",
    "stars": 1,
    "forks": 0,
    "language": "HTML",
    "last_updated": "2024-09-23T20:23:05Z",
    "topics": [],
    "owner": {
      "username": "ming024",
      "profile_url": "https://github.com/ming024"
    }
  },
  {
    "name": "PaddlePaddle/PaddleOCR",
    "description": "Awesome multilingual OCR toolkits based on PaddlePaddle (practical ultra lightweight OCR system, support 80+ languages recognition, provide data annotation and synthesis tools, support training and deployment among server, mobile, embedded and IoT devices)",
    "url": "https://github.com/PaddlePaddle/PaddleOCR",
    "stars": 44929,
    "forks": 7875,
    "language": "Python",
    "last_updated": "2024-12-11T04:13:46Z",
    "topics": [
      "chineseocr",
      "crnn",
      "db",
      "ocr",
      "ocrlite"
    ],
    "owner": {
      "username": "PaddlePaddle",
      "profile_url": "https://github.com/PaddlePaddle"
    }
  },
  {
    "name": "kaylode/vietnamese-ocr-toolbox",
    "description": "A toolbox for Vietnamese Optical Character Recognition.",
    "url": "https://github.com/kaylode/vietnamese-ocr-toolbox",
    "stars": 106,
    "forks": 29,
    "language": "C++",
    "last_updated": "2024-12-10T03:55:08Z",
    "topics": [
      "character-recognition",
      "idcard-ocr",
      "invoices",
      "object-detection",
      "ocr",
      "text-detection",
      "toolbox",
      "vietnamese-ocr"
    ],
    "owner": {
      "username": "kaylode",
      "profile_url": "https://github.com/kaylode"
    }
  },
  {
    "name": "mhadidg/software-architecture-books",
    "description": "A comprehensive list of books on Software Architecture.",
    "url": "https://github.com/mhadidg/software-architecture-books",
    "stars": 9914,
    "forks": 790,
    "language": null,
    "last_updated": "2024-12-10T13:41:56Z",
    "topics": [
      "architecture",
      "awesome",
      "awesome-list",
      "books",
      "goodreads",
      "software-architecture",
      "software-design",
      "software-engineering"
    ],
    "owner": {
      "username": "mhadidg",
      "profile_url": "https://github.com/mhadidg"
    }
  },
  {
    "name": "GoogleCloudPlatform/ml-design-patterns",
    "description": "Source code accompanying O'Reilly book: Machine Learning Design Patterns",
    "url": "https://github.com/GoogleCloudPlatform/ml-design-patterns",
    "stars": 1905,
    "forks": 534,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T13:09:25Z",
    "topics": [],
    "owner": {
      "username": "GoogleCloudPlatform",
      "profile_url": "https://github.com/GoogleCloudPlatform"
    }
  },
  {
    "name": "microsoft/CLAP",
    "description": "Learning audio concepts from natural language supervision",
    "url": "https://github.com/microsoft/CLAP",
    "stars": 498,
    "forks": 38,
    "language": "Python",
    "last_updated": "2024-12-09T05:28:34Z",
    "topics": [],
    "owner": {
      "username": "microsoft",
      "profile_url": "https://github.com/microsoft"
    }
  },
  {
    "name": "abhishek-ch/around-dataengineering",
    "description": "A Data Engineering & Machine Learning Knowledge Hub",
    "url": "https://github.com/abhishek-ch/around-dataengineering",
    "stars": 1118,
    "forks": 225,
    "language": "Python",
    "last_updated": "2024-11-19T16:57:37Z",
    "topics": [
      "airflow",
      "data-engineering",
      "datascience",
      "devops",
      "infrastructure",
      "machine-learning",
      "mlops",
      "spark"
    ],
    "owner": {
      "username": "abhishek-ch",
      "profile_url": "https://github.com/abhishek-ch"
    }
  },
  {
    "name": "xiaobai1217/Awesome-Video-Datasets",
    "description": "Video datasets",
    "url": "https://github.com/xiaobai1217/Awesome-Video-Datasets",
    "stars": 1240,
    "forks": 95,
    "language": null,
    "last_updated": "2024-12-10T16:43:49Z",
    "topics": [],
    "owner": {
      "username": "xiaobai1217",
      "profile_url": "https://github.com/xiaobai1217"
    }
  },
  {
    "name": "khanld/ASR-Wav2vec-Finetune",
    "description": ":zap: Finetune Wa2vec 2.0 For Speech Recognition",
    "url": "https://github.com/khanld/ASR-Wav2vec-Finetune",
    "stars": 118,
    "forks": 24,
    "language": "Python",
    "last_updated": "2024-12-11T00:43:54Z",
    "topics": [
      "asr",
      "finetune-wav2vec",
      "huggingface",
      "pytorch",
      "speech-recognition",
      "speech-to-text",
      "vietnamese-speech-recognition",
      "wav2vec2"
    ],
    "owner": {
      "username": "khanld",
      "profile_url": "https://github.com/khanld"
    }
  },
  {
    "name": "microsoft/NeuralSpeech",
    "description": null,
    "url": "https://github.com/microsoft/NeuralSpeech",
    "stars": 1398,
    "forks": 182,
    "language": "Python",
    "last_updated": "2024-12-10T03:09:00Z",
    "topics": [],
    "owner": {
      "username": "microsoft",
      "profile_url": "https://github.com/microsoft"
    }
  },
  {
    "name": "binhvq/news-corpus",
    "description": "Corpus ti\u1ebfng vi\u1ec7t",
    "url": "https://github.com/binhvq/news-corpus",
    "stars": 350,
    "forks": 70,
    "language": null,
    "last_updated": "2024-12-09T12:32:42Z",
    "topics": [],
    "owner": {
      "username": "binhvq",
      "profile_url": "https://github.com/binhvq"
    }
  },
  {
    "name": "hyunwoongko/kocrawl",
    "description": "Collection of useful Korean crawlers",
    "url": "https://github.com/hyunwoongko/kocrawl",
    "stars": 87,
    "forks": 22,
    "language": "Python",
    "last_updated": "2024-07-18T01:33:46Z",
    "topics": [],
    "owner": {
      "username": "hyunwoongko",
      "profile_url": "https://github.com/hyunwoongko"
    }
  },
  {
    "name": "openai/tiktoken",
    "description": "tiktoken is a fast BPE tokeniser for use with OpenAI's models.",
    "url": "https://github.com/openai/tiktoken",
    "stars": 12631,
    "forks": 864,
    "language": "Python",
    "last_updated": "2024-12-11T03:50:40Z",
    "topics": [],
    "owner": {
      "username": "openai",
      "profile_url": "https://github.com/openai"
    }
  },
  {
    "name": "Rongjiehuang/GenerSpeech",
    "description": "PyTorch Implementation of GenerSpeech (NeurIPS'22): a text-to-speech model towards zero-shot style transfer of OOD custom voice.",
    "url": "https://github.com/Rongjiehuang/GenerSpeech",
    "stars": 320,
    "forks": 45,
    "language": "Python",
    "last_updated": "2024-11-17T09:06:27Z",
    "topics": [
      "domain-generalization",
      "neurips-2022",
      "speech-synthesis",
      "style-transfer",
      "text-to-speech",
      "tts"
    ],
    "owner": {
      "username": "Rongjiehuang",
      "profile_url": "https://github.com/Rongjiehuang"
    }
  },
  {
    "name": "Zhendong-Wang/Diffusion-GAN",
    "description": "Official PyTorch implementation for paper: Diffusion-GAN: Training GANs with Diffusion",
    "url": "https://github.com/Zhendong-Wang/Diffusion-GAN",
    "stars": 628,
    "forks": 68,
    "language": "Python",
    "last_updated": "2024-12-10T09:34:56Z",
    "topics": [],
    "owner": {
      "username": "Zhendong-Wang",
      "profile_url": "https://github.com/Zhendong-Wang"
    }
  },
  {
    "name": "haoheliu/voicefixer",
    "description": "General Speech Restoration",
    "url": "https://github.com/haoheliu/voicefixer",
    "stars": 1055,
    "forks": 132,
    "language": "Python",
    "last_updated": "2024-12-10T23:57:36Z",
    "topics": [
      "declipping",
      "denoise",
      "dereverberation",
      "mel",
      "speech",
      "speech-analysis",
      "speech-enhancement",
      "speech-processing",
      "speech-synthesis",
      "super-resolution",
      "tts",
      "vocoder"
    ],
    "owner": {
      "username": "haoheliu",
      "profile_url": "https://github.com/haoheliu"
    }
  },
  {
    "name": "hcy71o/AutoVocoder",
    "description": "Autovocoder: Fast Waveform Generation from a Learned Speech Representation using Differentiable Digital Signal Processing",
    "url": "https://github.com/hcy71o/AutoVocoder",
    "stars": 68,
    "forks": 13,
    "language": "Python",
    "last_updated": "2024-11-03T16:33:20Z",
    "topics": [
      "speech-synthesis",
      "tts",
      "vocoder",
      "waveform-generator"
    ],
    "owner": {
      "username": "hcy71o",
      "profile_url": "https://github.com/hcy71o"
    }
  },
  {
    "name": "salesforce/botsim",
    "description": " BotSIM - a data-efficient end-to-end Bot SIMulation toolkit for evaluation, diagnosis, and improvement of commercial chatbots",
    "url": "https://github.com/salesforce/botsim",
    "stars": 114,
    "forks": 8,
    "language": "Jupyter Notebook",
    "last_updated": "2024-11-28T20:41:14Z",
    "topics": [
      "bot-testing",
      "chatbot",
      "dialog-simulator",
      "dialogflow-chatbot",
      "dialogue-systems",
      "liveagent",
      "paraphrase-generation",
      "salesforce-bot",
      "task-oriented-dialogue",
      "testing"
    ],
    "owner": {
      "username": "salesforce",
      "profile_url": "https://github.com/salesforce"
    }
  },
  {
    "name": "decfrr/Text-to-sound-Synthesis-Prompt2Prompt",
    "description": null,
    "url": "https://github.com/decfrr/Text-to-sound-Synthesis-Prompt2Prompt",
    "stars": 8,
    "forks": 0,
    "language": "Python",
    "last_updated": "2024-03-13T06:06:11Z",
    "topics": [],
    "owner": {
      "username": "decfrr",
      "profile_url": "https://github.com/decfrr"
    }
  },
  {
    "name": "ilaria-manco/song-describer",
    "description": "Song Describer is a data collection platform for annotating music with textual descriptions.",
    "url": "https://github.com/ilaria-manco/song-describer",
    "stars": 57,
    "forks": 5,
    "language": "Python",
    "last_updated": "2024-12-03T16:12:25Z",
    "topics": [
      "annotations",
      "audio-captioning",
      "data-collection",
      "music-dataset"
    ],
    "owner": {
      "username": "ilaria-manco",
      "profile_url": "https://github.com/ilaria-manco"
    }
  },
  {
    "name": "ggerganov/whisper.cpp",
    "description": "Port of OpenAI's Whisper model in C/C++",
    "url": "https://github.com/ggerganov/whisper.cpp",
    "stars": 36166,
    "forks": 3699,
    "language": "C++",
    "last_updated": "2024-12-11T03:16:45Z",
    "topics": [
      "inference",
      "openai",
      "speech-recognition",
      "speech-to-text",
      "transformer",
      "whisper"
    ],
    "owner": {
      "username": "ggerganov",
      "profile_url": "https://github.com/ggerganov"
    }
  },
  {
    "name": "amazon-science/esci-data",
    "description": "Shopping Queries Dataset: A Large-Scale ESCI Benchmark for Improving Product Search",
    "url": "https://github.com/amazon-science/esci-data",
    "stars": 256,
    "forks": 54,
    "language": "Python",
    "last_updated": "2024-12-10T05:36:57Z",
    "topics": [],
    "owner": {
      "username": "amazon-science",
      "profile_url": "https://github.com/amazon-science"
    }
  },
  {
    "name": "ubisoft/ubisoft-laforge-daft-exprt",
    "description": "PyTorch Implementation of Daft-Exprt: Robust Prosody Transfer Across Speakers for Expressive Speech Synthesis",
    "url": "https://github.com/ubisoft/ubisoft-laforge-daft-exprt",
    "stars": 126,
    "forks": 23,
    "language": "Python",
    "last_updated": "2024-11-25T07:59:59Z",
    "topics": [
      "affine-transformations",
      "expressive-spee",
      "expressive-speech-synthesis",
      "prosody",
      "prosody-transfer",
      "pytorch",
      "self-attention",
      "speech-synthesis",
      "style",
      "style-transfer",
      "text-to-speech",
      "tts"
    ],
    "owner": {
      "username": "ubisoft",
      "profile_url": "https://github.com/ubisoft"
    }
  },
  {
    "name": "undertheseanlp/NLP-Vietnamese-progress",
    "description": "Repository to track the progress in Vietnamese Natural Language Processing, including the datasets and the current state-of-the-art for the most common Vietnamese NLP tasks.",
    "url": "https://github.com/undertheseanlp/NLP-Vietnamese-progress",
    "stars": 348,
    "forks": 74,
    "language": null,
    "last_updated": "2024-11-26T05:12:00Z",
    "topics": [
      "nlp",
      "vietnamese-nlp"
    ],
    "owner": {
      "username": "undertheseanlp",
      "profile_url": "https://github.com/undertheseanlp"
    }
  },
  {
    "name": "otto-de/recsys-dataset",
    "description": "\ud83d\udecd A real-world e-commerce dataset for session-based recommender systems research.",
    "url": "https://github.com/otto-de/recsys-dataset",
    "stars": 316,
    "forks": 47,
    "language": "Python",
    "last_updated": "2024-12-02T18:28:22Z",
    "topics": [
      "benchmark",
      "dataset",
      "e-commerce",
      "kaggle",
      "machine-learning",
      "multi-objective-optimization",
      "otto",
      "recommendation-system",
      "recommendations",
      "recommender-system",
      "recsys",
      "session-based"
    ],
    "owner": {
      "username": "otto-de",
      "profile_url": "https://github.com/otto-de"
    }
  },
  {
    "name": "maum-ai/phaseaug",
    "description": "ICASSP 2023 Accepted",
    "url": "https://github.com/maum-ai/phaseaug",
    "stars": 190,
    "forks": 14,
    "language": "Python",
    "last_updated": "2024-10-26T21:48:03Z",
    "topics": [
      "gan",
      "speech-synthesis",
      "vocoder"
    ],
    "owner": {
      "username": "maum-ai",
      "profile_url": "https://github.com/maum-ai"
    }
  },
  {
    "name": "Shihara-Dilshan/John-Keells-App-Revamp",
    "description": "John keells mobile app revamp using React Native and Flask with MongoDB.",
    "url": "https://github.com/Shihara-Dilshan/John-Keells-App-Revamp",
    "stars": 25,
    "forks": 12,
    "language": "JavaScript",
    "last_updated": "2024-11-06T15:58:27Z",
    "topics": [
      "animatable",
      "context-api",
      "drawer-navigation",
      "flask",
      "javascript",
      "mongodb",
      "mongoengine",
      "python",
      "react-native"
    ],
    "owner": {
      "username": "Shihara-Dilshan",
      "profile_url": "https://github.com/Shihara-Dilshan"
    }
  },
  {
    "name": "hhguo/MSMC-TTS",
    "description": "Official Implement of Multi-Stage Multi-Codebook (MSMC) TTS",
    "url": "https://github.com/hhguo/MSMC-TTS",
    "stars": 162,
    "forks": 15,
    "language": "Python",
    "last_updated": "2024-10-05T03:25:44Z",
    "topics": [
      "deep-learning",
      "gan",
      "speech-synthesis",
      "text-to-speech",
      "tts",
      "vocoder",
      "vq-vae",
      "vqgan"
    ],
    "owner": {
      "username": "hhguo",
      "profile_url": "https://github.com/hhguo"
    }
  },
  {
    "name": "MubertAI/Mubert-Text-to-Music",
    "description": "A simple notebook demonstrating prompt-based music generation via Mubert API",
    "url": "https://github.com/MubertAI/Mubert-Text-to-Music",
    "stars": 2737,
    "forks": 241,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-06T06:34:11Z",
    "topics": [],
    "owner": {
      "username": "MubertAI",
      "profile_url": "https://github.com/MubertAI"
    }
  },
  {
    "name": "MasayaKawamura/MB-iSTFT-VITS",
    "description": "Lightweight and High-Fidelity End-to-End Text-to-Speech with Multi-Band Generation and Inverse Short-Time Fourier Transform",
    "url": "https://github.com/MasayaKawamura/MB-iSTFT-VITS",
    "stars": 424,
    "forks": 65,
    "language": "Python",
    "last_updated": "2024-12-04T03:07:27Z",
    "topics": [],
    "owner": {
      "username": "MasayaKawamura",
      "profile_url": "https://github.com/MasayaKawamura"
    }
  },
  {
    "name": "ttslr/Ai-TTS",
    "description": "[InterSpeech'2023] Explicit Intensity Control for Accented Text-to-speech",
    "url": "https://github.com/ttslr/Ai-TTS",
    "stars": 3,
    "forks": 1,
    "language": "HTML",
    "last_updated": "2024-09-24T06:05:05Z",
    "topics": [],
    "owner": {
      "username": "ttslr",
      "profile_url": "https://github.com/ttslr"
    }
  },
  {
    "name": "miccio-dk/NISQA",
    "description": "NISQA - Non-Intrusive Speech Quality and TTS Naturalness Assessment",
    "url": "https://github.com/miccio-dk/NISQA",
    "stars": 16,
    "forks": 0,
    "language": "Python",
    "last_updated": "2024-01-04T17:07:35Z",
    "topics": [],
    "owner": {
      "username": "miccio-dk",
      "profile_url": "https://github.com/miccio-dk"
    }
  },
  {
    "name": "sony/DiffRoll",
    "description": "PyTorch implementation of DiffRoll, a diffusion-based generative automatic music transcription (AMT) model",
    "url": "https://github.com/sony/DiffRoll",
    "stars": 71,
    "forks": 11,
    "language": "Jupyter Notebook",
    "last_updated": "2024-10-13T13:04:34Z",
    "topics": [
      "automatic-music-transcription",
      "deep-generative-model",
      "diffusion",
      "generative-model",
      "inpainting",
      "machine-learning",
      "music-generation",
      "pytorch"
    ],
    "owner": {
      "username": "sony",
      "profile_url": "https://github.com/sony"
    }
  },
  {
    "name": "KevinMIN95/StyleSpeech",
    "description": "Official implementation of Meta-StyleSpeech and StyleSpeech",
    "url": "https://github.com/KevinMIN95/StyleSpeech",
    "stars": 241,
    "forks": 38,
    "language": "Python",
    "last_updated": "2024-10-18T06:05:34Z",
    "topics": [
      "meta-learning",
      "meta-stylespeech",
      "neural-tts",
      "official",
      "speech",
      "speech-synthesis",
      "stylespeech",
      "text-to-speech",
      "tts"
    ],
    "owner": {
      "username": "KevinMIN95",
      "profile_url": "https://github.com/KevinMIN95"
    }
  },
  {
    "name": "automl/TabPFN",
    "description": "Official implementation of the TabPFN paper (https://arxiv.org/abs/2207.01848) and the tabpfn package.",
    "url": "https://github.com/automl/TabPFN",
    "stars": 1239,
    "forks": 112,
    "language": "Python",
    "last_updated": "2024-12-10T20:37:34Z",
    "topics": [],
    "owner": {
      "username": "automl",
      "profile_url": "https://github.com/automl"
    }
  },
  {
    "name": "DataTalksClub/data-engineering-zoomcamp",
    "description": "Free Data Engineering course! ",
    "url": "https://github.com/DataTalksClub/data-engineering-zoomcamp",
    "stars": 25525,
    "forks": 5462,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T04:12:51Z",
    "topics": [
      "data-engineering",
      "dbt",
      "docker",
      "kafka",
      "prefect",
      "spark"
    ],
    "owner": {
      "username": "DataTalksClub",
      "profile_url": "https://github.com/DataTalksClub"
    }
  },
  {
    "name": "huawei-noah/Speech-Backbones",
    "description": "This is the main repository of open-sourced speech technology by Huawei Noah's Ark Lab.",
    "url": "https://github.com/huawei-noah/Speech-Backbones",
    "stars": 566,
    "forks": 121,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-03T03:20:33Z",
    "topics": [
      "speech-processing",
      "speech-recognition",
      "speech-synthesis"
    ],
    "owner": {
      "username": "huawei-noah",
      "profile_url": "https://github.com/huawei-noah"
    }
  },
  {
    "name": "vkothapally/Subband-Beamformer",
    "description": null,
    "url": "https://github.com/vkothapally/Subband-Beamformer",
    "stars": 31,
    "forks": 4,
    "language": "HTML",
    "last_updated": "2024-01-25T00:37:26Z",
    "topics": [],
    "owner": {
      "username": "vkothapally",
      "profile_url": "https://github.com/vkothapally"
    }
  },
  {
    "name": "boost-devs/ai-tech-interview",
    "description": "\ud83d\udc69\u200d\ud83d\udcbb\ud83d\udc68\u200d\ud83d\udcbb AI \uc5d4\uc9c0\ub2c8\uc5b4 \uae30\uc220 \uba74\uc811 \uc2a4\ud130\ub514 (\u2b50\ufe0f 1k+)",
    "url": "https://github.com/boost-devs/ai-tech-interview",
    "stars": 1897,
    "forks": 454,
    "language": null,
    "last_updated": "2024-12-10T01:04:52Z",
    "topics": [
      "artificial-intelligence",
      "computer-science",
      "python",
      "study",
      "tech-interview"
    ],
    "owner": {
      "username": "boost-devs",
      "profile_url": "https://github.com/boost-devs"
    }
  },
  {
    "name": "ArtifexSoftware/pdf2docx",
    "description": "Open source Python library for converting PDF to DOCX.",
    "url": "https://github.com/ArtifexSoftware/pdf2docx",
    "stars": 2644,
    "forks": 388,
    "language": "Python",
    "last_updated": "2024-12-10T13:42:08Z",
    "topics": [
      "docx",
      "extract-table",
      "pdf-converter",
      "pdf-to-word",
      "pymupdf"
    ],
    "owner": {
      "username": "ArtifexSoftware",
      "profile_url": "https://github.com/ArtifexSoftware"
    }
  },
  {
    "name": "lkwq007/stablediffusion-infinity",
    "description": "Outpainting with Stable Diffusion on an infinite canvas",
    "url": "https://github.com/lkwq007/stablediffusion-infinity",
    "stars": 3857,
    "forks": 303,
    "language": "Python",
    "last_updated": "2024-12-05T16:54:21Z",
    "topics": [
      "gui",
      "inpainting",
      "outpainting",
      "stable-diffusion",
      "stablediffusion"
    ],
    "owner": {
      "username": "lkwq007",
      "profile_url": "https://github.com/lkwq007"
    }
  },
  {
    "name": "wenet-e2e/wetts",
    "description": "Production First and Production Ready End-to-End Text-to-Speech Toolkit",
    "url": "https://github.com/wenet-e2e/wetts",
    "stars": 376,
    "forks": 60,
    "language": "Python",
    "last_updated": "2024-12-05T01:41:12Z",
    "topics": [],
    "owner": {
      "username": "wenet-e2e",
      "profile_url": "https://github.com/wenet-e2e"
    }
  },
  {
    "name": "yuan1615/AdaVocoder",
    "description": "Adaptive Vocoder for Custom Voice",
    "url": "https://github.com/yuan1615/AdaVocoder",
    "stars": 59,
    "forks": 10,
    "language": "Python",
    "last_updated": "2024-11-20T10:02:10Z",
    "topics": [],
    "owner": {
      "username": "yuan1615",
      "profile_url": "https://github.com/yuan1615"
    }
  },
  {
    "name": "Zain-Jiang/Dict-TTS",
    "description": null,
    "url": "https://github.com/Zain-Jiang/Dict-TTS",
    "stars": 131,
    "forks": 10,
    "language": "Python",
    "last_updated": "2024-06-28T03:13:32Z",
    "topics": [],
    "owner": {
      "username": "Zain-Jiang",
      "profile_url": "https://github.com/Zain-Jiang"
    }
  },
  {
    "name": "openai/whisper",
    "description": "Robust Speech Recognition via Large-Scale Weak Supervision",
    "url": "https://github.com/openai/whisper",
    "stars": 72597,
    "forks": 8660,
    "language": "Python",
    "last_updated": "2024-12-11T04:12:21Z",
    "topics": [],
    "owner": {
      "username": "openai",
      "profile_url": "https://github.com/openai"
    }
  },
  {
    "name": "chenkui164/FastASR",
    "description": "\u8fd9\u662f\u4e00\u4e2a\u7528C++\u5b9e\u73b0ASR\u63a8\u7406\u7684\u9879\u76ee\uff0c\u5b83\u4f9d\u8d56\u5f88\u5c11\uff0c\u5b89\u88c5\u4e5f\u5f88\u7b80\u5355\uff0c\u63a8\u7406\u901f\u5ea6\u5f88\u5feb\uff0c\u5728\u6811\u8393\u6d3e4B\u7b49ARM\u5e73\u53f0\u4e5f\u53ef\u4ee5\u6d41\u7545\u7684\u8fd0\u884c\u3002 \u652f\u6301\u7684\u6a21\u578b\u662f\u7531Google\u7684Transformer\u6a21\u578b\u4e2d\u4f18\u5316\u800c\u6765\uff0c\u6570\u636e\u96c6\u662f\u5f00\u6e90wenetspeech(10000+\u5c0f\u65f6)\u6216\u963f\u91cc\u79c1\u6709\u6570\u636e\u96c6(60000+\u5c0f\u65f6)\uff0c \u6240\u4ee5\u8bc6\u522b\u6548\u679c\u4e5f\u5f88\u597d\uff0c\u53ef\u4ee5\u5ab2\u7f8e\u8bb8\u591a\u5546\u7528\u7684ASR\u8f6f\u4ef6\u3002",
    "url": "https://github.com/chenkui164/FastASR",
    "stars": 490,
    "forks": 76,
    "language": "C",
    "last_updated": "2024-12-05T02:55:03Z",
    "topics": [
      "speech-recognition"
    ],
    "owner": {
      "username": "chenkui164",
      "profile_url": "https://github.com/chenkui164"
    }
  },
  {
    "name": "MelissaChen15/control-vc",
    "description": "This is the implementation for \"ControlVC: Zero-Shot Voice Conversion with Time-Varying Controls on Pitch and Rhythm\"",
    "url": "https://github.com/MelissaChen15/control-vc",
    "stars": 128,
    "forks": 17,
    "language": "Python",
    "last_updated": "2024-11-08T03:49:24Z",
    "topics": [],
    "owner": {
      "username": "MelissaChen15",
      "profile_url": "https://github.com/MelissaChen15"
    }
  },
  {
    "name": "microsoft/SpeechT5",
    "description": "Unified-Modal Speech-Text Pre-Training for Spoken Language Processing",
    "url": "https://github.com/microsoft/SpeechT5",
    "stars": 1233,
    "forks": 114,
    "language": "Python",
    "last_updated": "2024-12-10T11:07:22Z",
    "topics": [
      "speech-pretraining",
      "speech-recognition",
      "speech-synthesis",
      "speech-text-pretraining",
      "speech-translation",
      "speech2c",
      "speechlm",
      "speecht5",
      "speechut",
      "vallex",
      "vatlm"
    ],
    "owner": {
      "username": "microsoft",
      "profile_url": "https://github.com/microsoft"
    }
  },
  {
    "name": "tts-tutorial/book",
    "description": null,
    "url": "https://github.com/tts-tutorial/book",
    "stars": 63,
    "forks": 1,
    "language": null,
    "last_updated": "2024-11-23T02:55:07Z",
    "topics": [],
    "owner": {
      "username": "tts-tutorial",
      "profile_url": "https://github.com/tts-tutorial"
    }
  },
  {
    "name": "eloimoliner/gramophone_noise_synth",
    "description": "Realistic gramophone noise synthesis using a diffusion model",
    "url": "https://github.com/eloimoliner/gramophone_noise_synth",
    "stars": 18,
    "forks": 4,
    "language": "Jupyter Notebook",
    "last_updated": "2024-10-17T21:42:32Z",
    "topics": [],
    "owner": {
      "username": "eloimoliner",
      "profile_url": "https://github.com/eloimoliner"
    }
  },
  {
    "name": "wolfgarbe/SymSpell",
    "description": "SymSpell: 1 million times faster spelling correction & fuzzy search through Symmetric Delete spelling correction algorithm",
    "url": "https://github.com/wolfgarbe/SymSpell",
    "stars": 3162,
    "forks": 298,
    "language": "C#",
    "last_updated": "2024-12-10T02:35:50Z",
    "topics": [
      "approximate-string-matching",
      "chinese-text-segmentation",
      "chinese-word-segmentation",
      "damerau-levenshtein",
      "edit-distance",
      "fuzzy-matching",
      "fuzzy-search",
      "levenshtein",
      "levenshtein-distance",
      "spell-check",
      "spellcheck",
      "spelling",
      "spelling-correction",
      "symspell",
      "text-segmentation",
      "word-segmentation"
    ],
    "owner": {
      "username": "wolfgarbe",
      "profile_url": "https://github.com/wolfgarbe"
    }
  },
  {
    "name": "vovanphuc/smartmenu",
    "description": "Top 1 Quy Nhon AI Hackathon 2022 Challenge Smart Menu",
    "url": "https://github.com/vovanphuc/smartmenu",
    "stars": 31,
    "forks": 15,
    "language": "Python",
    "last_updated": "2024-10-18T21:03:01Z",
    "topics": [],
    "owner": {
      "username": "vovanphuc",
      "profile_url": "https://github.com/vovanphuc"
    }
  },
  {
    "name": "CompVis/stable-diffusion",
    "description": "A latent text-to-image diffusion model",
    "url": "https://github.com/CompVis/stable-diffusion",
    "stars": 68691,
    "forks": 10203,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T03:31:41Z",
    "topics": [],
    "owner": {
      "username": "CompVis",
      "profile_url": "https://github.com/CompVis"
    }
  },
  {
    "name": "magenta/music-spectrogram-diffusion",
    "description": null,
    "url": "https://github.com/magenta/music-spectrogram-diffusion",
    "stars": 385,
    "forks": 27,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-09T01:17:03Z",
    "topics": [],
    "owner": {
      "username": "magenta",
      "profile_url": "https://github.com/magenta"
    }
  },
  {
    "name": "TensorSpeech/TensorFlowTTS",
    "description": ":stuck_out_tongue_closed_eyes: TensorFlowTTS: Real-Time State-of-the-art Speech Synthesis for Tensorflow 2 (supported including English, French, Korean, Chinese, German and Easy to adapt for other languages)",
    "url": "https://github.com/TensorSpeech/TensorFlowTTS",
    "stars": 3852,
    "forks": 814,
    "language": "Python",
    "last_updated": "2024-12-09T15:25:08Z",
    "topics": [
      "chinese-tts",
      "fastspeech",
      "fastspeech2",
      "german-tts",
      "japanese-tts",
      "korea-tts",
      "melgan",
      "mobile-tts",
      "multi-speaker-tts",
      "multiband-melgan",
      "parallel-wavegan",
      "real-time",
      "speech-synthesis",
      "tacotron2",
      "tensorflow2",
      "text-to-speech",
      "tflite",
      "tts",
      "vocoder",
      "zh-tts"
    ],
    "owner": {
      "username": "TensorSpeech",
      "profile_url": "https://github.com/TensorSpeech"
    }
  },
  {
    "name": "Music-and-Culture-Technology-Lab/omnizart",
    "description": "Omniscient Mozart, being able to transcribe everything in the music, including vocal, drum, chord, beat, instruments, and more.",
    "url": "https://github.com/Music-and-Culture-Technology-Lab/omnizart",
    "stars": 1647,
    "forks": 102,
    "language": "Python",
    "last_updated": "2024-12-09T23:07:26Z",
    "topics": [
      "beat-tracking",
      "chord",
      "drum-transcription",
      "music-information-retrieval",
      "music-transcription",
      "vocal"
    ],
    "owner": {
      "username": "Music-and-Culture-Technology-Lab",
      "profile_url": "https://github.com/Music-and-Culture-Technology-Lab"
    }
  },
  {
    "name": "CMsmartvoice/One-Shot-Voice-Cloning",
    "description": ":relaxed: One Shot Voice Cloning base on Unet-TTS",
    "url": "https://github.com/CMsmartvoice/One-Shot-Voice-Cloning",
    "stars": 238,
    "forks": 40,
    "language": "Jupyter Notebook",
    "last_updated": "2024-11-30T16:23:11Z",
    "topics": [
      "one-shot",
      "style-transfer",
      "tts",
      "voice-cloning"
    ],
    "owner": {
      "username": "CMsmartvoice",
      "profile_url": "https://github.com/CMsmartvoice"
    }
  },
  {
    "name": "MiniXC/LightningFastSpeech2",
    "description": null,
    "url": "https://github.com/MiniXC/LightningFastSpeech2",
    "stars": 56,
    "forks": 4,
    "language": "Python",
    "last_updated": "2024-01-04T17:03:51Z",
    "topics": [],
    "owner": {
      "username": "MiniXC",
      "profile_url": "https://github.com/MiniXC"
    }
  },
  {
    "name": "lucidrains/audiolm-pytorch",
    "description": "Implementation of AudioLM, a SOTA Language Modeling Approach to Audio Generation out of Google Research, in Pytorch",
    "url": "https://github.com/lucidrains/audiolm-pytorch",
    "stars": 2455,
    "forks": 266,
    "language": "Python",
    "last_updated": "2024-12-09T19:08:35Z",
    "topics": [
      "artificial-intelligence",
      "attention-mechanisms",
      "audio-synthesis",
      "deep-learning",
      "transformers"
    ],
    "owner": {
      "username": "lucidrains",
      "profile_url": "https://github.com/lucidrains"
    }
  },
  {
    "name": "maum-ai/assem-vc",
    "description": "Official Code for Assem-VC @ICASSP2022",
    "url": "https://github.com/maum-ai/assem-vc",
    "stars": 265,
    "forks": 38,
    "language": "Jupyter Notebook",
    "last_updated": "2024-09-01T05:19:08Z",
    "topics": [
      "deep-learning",
      "pytorch",
      "speech-synthesis",
      "voice-conversion"
    ],
    "owner": {
      "username": "maum-ai",
      "profile_url": "https://github.com/maum-ai"
    }
  },
  {
    "name": "keonlee9420/Expressive-FastSpeech2",
    "description": "PyTorch Implementation of Non-autoregressive Expressive (emotional, conversational) TTS based on FastSpeech2, supporting English, Korean, and your own languages.",
    "url": "https://github.com/keonlee9420/Expressive-FastSpeech2",
    "stars": 291,
    "forks": 47,
    "language": "Python",
    "last_updated": "2024-12-03T15:26:26Z",
    "topics": [
      "conversational-speech-synthesis",
      "conversational-tts",
      "emotional-speech-synthesis",
      "emotional-tts",
      "expressive-speech-synthesis",
      "expressive-tts",
      "korean-speech-synthesis",
      "korean-tts",
      "non-autoregressive",
      "speech-synthesis",
      "text-to-speech",
      "tts"
    ],
    "owner": {
      "username": "keonlee9420",
      "profile_url": "https://github.com/keonlee9420"
    }
  },
  {
    "name": "CZ26/CycleTransGAN-EVC",
    "description": "CycleTransGAN-EVC: A CycleGAN-based Emotional Voice Conversion Model with Transformer",
    "url": "https://github.com/CZ26/CycleTransGAN-EVC",
    "stars": 31,
    "forks": 6,
    "language": "Python",
    "last_updated": "2024-01-08T01:49:35Z",
    "topics": [],
    "owner": {
      "username": "CZ26",
      "profile_url": "https://github.com/CZ26"
    }
  },
  {
    "name": "yl4579/StarGANv2-VC",
    "description": "StarGANv2-VC: A Diverse, Unsupervised, Non-parallel Framework for Natural-Sounding Voice Conversion",
    "url": "https://github.com/yl4579/StarGANv2-VC",
    "stars": 488,
    "forks": 108,
    "language": "Python",
    "last_updated": "2024-12-10T02:56:10Z",
    "topics": [
      "deep-learning",
      "gan",
      "interspeech2021",
      "speech",
      "speech-synthesis",
      "stargan-v2",
      "voice-conversion"
    ],
    "owner": {
      "username": "yl4579",
      "profile_url": "https://github.com/yl4579"
    }
  },
  {
    "name": "AlanBaade/MAE-AST-Public",
    "description": "Public Code for the paper MAE-AST: Masked Autoencoding Audio Spectrogram Transformer",
    "url": "https://github.com/AlanBaade/MAE-AST-Public",
    "stars": 84,
    "forks": 5,
    "language": "Python",
    "last_updated": "2024-11-27T13:14:55Z",
    "topics": [],
    "owner": {
      "username": "AlanBaade",
      "profile_url": "https://github.com/AlanBaade"
    }
  },
  {
    "name": "yangdongchao/Text-to-sound-Synthesis",
    "description": "The source code of our paper \"Diffsound: discrete diffusion model for text-to-sound generation\"",
    "url": "https://github.com/yangdongchao/Text-to-sound-Synthesis",
    "stars": 351,
    "forks": 33,
    "language": "Python",
    "last_updated": "2024-12-04T04:47:15Z",
    "topics": [],
    "owner": {
      "username": "yangdongchao",
      "profile_url": "https://github.com/yangdongchao"
    }
  },
  {
    "name": "Rongjiehuang/ProDiff",
    "description": "PyTorch Implementation of ProDiff (ACM-MM'22) with a Extremely-Fast diffusion speech synthesis pipeline",
    "url": "https://github.com/Rongjiehuang/ProDiff",
    "stars": 434,
    "forks": 55,
    "language": "Python",
    "last_updated": "2024-12-07T13:21:20Z",
    "topics": [
      "diffusion-models",
      "speech-synthesis",
      "text-to-speech"
    ],
    "owner": {
      "username": "Rongjiehuang",
      "profile_url": "https://github.com/Rongjiehuang"
    }
  },
  {
    "name": "asigalov61/Tegridy-MIDI-Dataset",
    "description": "Tegridy MIDI Dataset for precise and effective Music AI models creation.",
    "url": "https://github.com/asigalov61/Tegridy-MIDI-Dataset",
    "stars": 162,
    "forks": 14,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-08T01:58:27Z",
    "topics": [
      "artificial-intelligence",
      "dataset",
      "datasets",
      "karaoke",
      "midi",
      "midi-converter",
      "midi-files",
      "midi-parser",
      "midi-seeds",
      "midis-datasets",
      "multi-track",
      "musenet",
      "music",
      "music-ai",
      "music-clip",
      "music-composition",
      "music-generation",
      "music-library",
      "rock-trios",
      "tegridy"
    ],
    "owner": {
      "username": "asigalov61",
      "profile_url": "https://github.com/asigalov61"
    }
  },
  {
    "name": "mjhydri/Singing-Vocal-Beat-Tracking",
    "description": "This repo contains the source code of the first deep learning-base singing voice beat tracking system. It leverages WavLM and DistilHuBERT pre-trained speech models to create vocal embeddings and trains linear multi-head self-attention layers on top of them to extract vocal beat activations. Then, it uses HMM decoder to infer signing beats and tempo. ",
    "url": "https://github.com/mjhydri/Singing-Vocal-Beat-Tracking",
    "stars": 27,
    "forks": 4,
    "language": "Python",
    "last_updated": "2024-09-21T02:26:36Z",
    "topics": [
      "beat-tracking",
      "hubert",
      "linear-transformer",
      "music",
      "music-information-retrieval",
      "self-supervised",
      "singing-voice",
      "wavlm"
    ],
    "owner": {
      "username": "mjhydri",
      "profile_url": "https://github.com/mjhydri"
    }
  },
  {
    "name": "sophiefy/Sovits",
    "description": "An unofficial implementation of the combination of Soft-VC and  VITS",
    "url": "https://github.com/sophiefy/Sovits",
    "stars": 458,
    "forks": 51,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-05T21:08:50Z",
    "topics": [],
    "owner": {
      "username": "sophiefy",
      "profile_url": "https://github.com/sophiefy"
    }
  },
  {
    "name": "facebookresearch/meshtalk",
    "description": "Code for MeshTalk: 3D Face Animation from Speech using Cross-Modality Disentanglement",
    "url": "https://github.com/facebookresearch/meshtalk",
    "stars": 371,
    "forks": 56,
    "language": "Python",
    "last_updated": "2024-12-10T13:42:10Z",
    "topics": [],
    "owner": {
      "username": "facebookresearch",
      "profile_url": "https://github.com/facebookresearch"
    }
  },
  {
    "name": "facebookresearch/WavAugment",
    "description": "A library for speech data augmentation in time-domain",
    "url": "https://github.com/facebookresearch/WavAugment",
    "stars": 653,
    "forks": 58,
    "language": "Python",
    "last_updated": "2024-12-03T20:54:52Z",
    "topics": [],
    "owner": {
      "username": "facebookresearch",
      "profile_url": "https://github.com/facebookresearch"
    }
  },
  {
    "name": "Edresson/VoiceSplit",
    "description": "VoiceSplit: Targeted Voice Separation by Speaker-Conditioned Spectrogram",
    "url": "https://github.com/Edresson/VoiceSplit",
    "stars": 228,
    "forks": 32,
    "language": "Python",
    "last_updated": "2024-12-10T01:43:51Z",
    "topics": [],
    "owner": {
      "username": "Edresson",
      "profile_url": "https://github.com/Edresson"
    }
  },
  {
    "name": "guan-yuan/Awesome-Singing-Voice-Synthesis-and-Singing-Voice-Conversion",
    "description": "A paper and project list about the cutting edge Speech Synthesis, Text-to-Speech (TTS), Singing Voice Synthesis (SVS), Voice Conversion (VC), Singing Voice Conversion (SVC), and related interesting works (such as Music Synthesis, Automatic Music Transcription, Automatic MOS Prediction, SSL-based ASR...etc). ",
    "url": "https://github.com/guan-yuan/Awesome-Singing-Voice-Synthesis-and-Singing-Voice-Conversion",
    "stars": 412,
    "forks": 29,
    "language": null,
    "last_updated": "2024-12-02T04:07:32Z",
    "topics": [
      "automatic-music-transcription",
      "diffusion-models",
      "mos-prediction",
      "music",
      "music-generation",
      "music-synthesis",
      "music-transcription",
      "pytorch",
      "singing-synthesis",
      "singing-voice",
      "singing-voice-conversion",
      "singing-voice-synthesis",
      "speech",
      "speech-synthesis",
      "text-to-speech",
      "tts",
      "voice-conversion"
    ],
    "owner": {
      "username": "guan-yuan",
      "profile_url": "https://github.com/guan-yuan"
    }
  },
  {
    "name": "DiegoLeon96/Neural-Speech-Dereverberation",
    "description": "Machine and Deep Learning models for speech dereverberation",
    "url": "https://github.com/DiegoLeon96/Neural-Speech-Dereverberation",
    "stars": 105,
    "forks": 21,
    "language": "Python",
    "last_updated": "2024-10-17T13:20:31Z",
    "topics": [
      "dereverberation",
      "speech",
      "speech-enhancement"
    ],
    "owner": {
      "username": "DiegoLeon96",
      "profile_url": "https://github.com/DiegoLeon96"
    }
  },
  {
    "name": "babe269/performant",
    "description": "A toolset for easy formant extraction and visualization from wav files and TTS models",
    "url": "https://github.com/babe269/performant",
    "stars": 30,
    "forks": 1,
    "language": "Python",
    "last_updated": "2024-10-31T13:40:01Z",
    "topics": [],
    "owner": {
      "username": "babe269",
      "profile_url": "https://github.com/babe269"
    }
  },
  {
    "name": "gordicaleksa/stable_diffusion_playground",
    "description": "Playing around with stable diffusion. Generated images are reproducible because I save the metadata and latent information. You can generate and then later interpolate between the images of your choice.",
    "url": "https://github.com/gordicaleksa/stable_diffusion_playground",
    "stars": 209,
    "forks": 24,
    "language": "Python",
    "last_updated": "2024-09-20T12:15:48Z",
    "topics": [
      "diffusion-models",
      "image-generation",
      "latent-diffusion-models",
      "stable-diffusion",
      "stable-diffusion-tutorial"
    ],
    "owner": {
      "username": "gordicaleksa",
      "profile_url": "https://github.com/gordicaleksa"
    }
  },
  {
    "name": "howard1337/S2VC",
    "description": null,
    "url": "https://github.com/howard1337/S2VC",
    "stars": 97,
    "forks": 17,
    "language": "Python",
    "last_updated": "2024-12-09T15:35:16Z",
    "topics": [],
    "owner": {
      "username": "howard1337",
      "profile_url": "https://github.com/howard1337"
    }
  },
  {
    "name": "Jackson-Kang/MFARunner",
    "description": "A simple tool to easily use Montreal Forced Aligner. Also provide alignment(TextGrid) retrieved from ESD.",
    "url": "https://github.com/Jackson-Kang/MFARunner",
    "stars": 44,
    "forks": 4,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-02T11:50:22Z",
    "topics": [],
    "owner": {
      "username": "Jackson-Kang",
      "profile_url": "https://github.com/Jackson-Kang"
    }
  },
  {
    "name": "ldzhangyx/BART-fusion",
    "description": "The code repository for our paper \"Interpreting Song Lyrics with a Music-Informed Pre-trained Language Model\".",
    "url": "https://github.com/ldzhangyx/BART-fusion",
    "stars": 22,
    "forks": 0,
    "language": "Python",
    "last_updated": "2023-05-04T07:53:10Z",
    "topics": [],
    "owner": {
      "username": "ldzhangyx",
      "profile_url": "https://github.com/ldzhangyx"
    }
  },
  {
    "name": "v-nhandt21/MusicVoiceConversion",
    "description": "Sing any popular song with your voice",
    "url": "https://github.com/v-nhandt21/MusicVoiceConversion",
    "stars": 11,
    "forks": 1,
    "language": "Python",
    "last_updated": "2024-11-13T09:46:15Z",
    "topics": [],
    "owner": {
      "username": "v-nhandt21",
      "profile_url": "https://github.com/v-nhandt21"
    }
  },
  {
    "name": "v-nhandt21/Viphoneme",
    "description": "Vi_G2P or ViG2P: G2P package for Vietnamese: based on vPhon and phonology knowledge to convert Raw text - Graphoneme to IPA",
    "url": "https://github.com/v-nhandt21/Viphoneme",
    "stars": 71,
    "forks": 16,
    "language": "Python",
    "last_updated": "2024-11-18T09:01:39Z",
    "topics": [
      "g2p",
      "vig2p"
    ],
    "owner": {
      "username": "v-nhandt21",
      "profile_url": "https://github.com/v-nhandt21"
    }
  },
  {
    "name": "diff-usion/Awesome-Diffusion-Models",
    "description": " A collection of resources and papers on Diffusion Models",
    "url": "https://github.com/diff-usion/Awesome-Diffusion-Models",
    "stars": 11214,
    "forks": 950,
    "language": "HTML",
    "last_updated": "2024-12-11T03:28:29Z",
    "topics": [
      "artificial-intelligence",
      "diffusion-models",
      "generative-model",
      "machine-learning",
      "score-based",
      "score-matching"
    ],
    "owner": {
      "username": "diff-usion",
      "profile_url": "https://github.com/diff-usion"
    }
  },
  {
    "name": "choiHkk/CVAEJETS",
    "description": "Conditional Variational Auto-Encoder with Jointly Training FastSpeech2(+Conformer) and HiFi-GAN for End to End Text to Speech",
    "url": "https://github.com/choiHkk/CVAEJETS",
    "stars": 46,
    "forks": 7,
    "language": "Jupyter Notebook",
    "last_updated": "2024-07-30T06:58:44Z",
    "topics": [],
    "owner": {
      "username": "choiHkk",
      "profile_url": "https://github.com/choiHkk"
    }
  },
  {
    "name": "archinetai/audio-diffusion-pytorch",
    "description": "Audio generation using diffusion models, in PyTorch.",
    "url": "https://github.com/archinetai/audio-diffusion-pytorch",
    "stars": 1975,
    "forks": 168,
    "language": "Python",
    "last_updated": "2024-12-10T23:30:36Z",
    "topics": [
      "artificial-intelligence",
      "audio-generation",
      "deep-learning",
      "denoising-diffusion"
    ],
    "owner": {
      "username": "archinetai",
      "profile_url": "https://github.com/archinetai"
    }
  },
  {
    "name": "KunZhou9646/Mixed_Emotions",
    "description": null,
    "url": "https://github.com/KunZhou9646/Mixed_Emotions",
    "stars": 112,
    "forks": 11,
    "language": "Python",
    "last_updated": "2024-12-10T06:46:44Z",
    "topics": [],
    "owner": {
      "username": "KunZhou9646",
      "profile_url": "https://github.com/KunZhou9646"
    }
  },
  {
    "name": "bootphon/phonemizer",
    "description": "Simple text to phones converter for multiple languages",
    "url": "https://github.com/bootphon/phonemizer",
    "stars": 1245,
    "forks": 175,
    "language": "Python",
    "last_updated": "2024-12-10T12:08:54Z",
    "topics": [],
    "owner": {
      "username": "bootphon",
      "profile_url": "https://github.com/bootphon"
    }
  },
  {
    "name": "microsoft/UniVL",
    "description": "An official implementation for \" UniVL: A Unified Video and Language Pre-Training Model for Multimodal Understanding and Generation\"",
    "url": "https://github.com/microsoft/UniVL",
    "stars": 340,
    "forks": 53,
    "language": "Python",
    "last_updated": "2024-12-09T08:48:17Z",
    "topics": [
      "alignment",
      "caption",
      "caption-task",
      "coin",
      "joint",
      "localization",
      "msrvtt",
      "multimodal-sentiment-analysis",
      "multimodality",
      "pretrain",
      "pretraining",
      "retrieval-task",
      "segmentation",
      "video",
      "video-language",
      "video-text",
      "video-text-retrieval",
      "youcookii"
    ],
    "owner": {
      "username": "microsoft",
      "profile_url": "https://github.com/microsoft"
    }
  },
  {
    "name": "YatingMusic/ddsp-singing-vocoders",
    "description": "Official implementation of SawSing (ISMIR'22)",
    "url": "https://github.com/YatingMusic/ddsp-singing-vocoders",
    "stars": 254,
    "forks": 37,
    "language": "Python",
    "last_updated": "2024-11-03T15:02:04Z",
    "topics": [
      "ismir",
      "singing-synthesis",
      "singing-voice",
      "vocoders"
    ],
    "owner": {
      "username": "YatingMusic",
      "profile_url": "https://github.com/YatingMusic"
    }
  },
  {
    "name": "lucasjinreal/yolov7_d2",
    "description": "\ud83d\udd25\ud83d\udd25\ud83d\udd25\ud83d\udd25 (Earlier YOLOv7 not official one) YOLO with Transformers and Instance Segmentation, with TensorRT acceleration! \ud83d\udd25\ud83d\udd25\ud83d\udd25",
    "url": "https://github.com/lucasjinreal/yolov7_d2",
    "stars": 3126,
    "forks": 481,
    "language": "Python",
    "last_updated": "2024-12-11T03:42:10Z",
    "topics": [
      "detection",
      "detextron2",
      "detr",
      "face",
      "instance-segmentation",
      "object-detection",
      "onnx",
      "tensorrt",
      "transformers",
      "yolo",
      "yolov6",
      "yolov7",
      "yolox"
    ],
    "owner": {
      "username": "lucasjinreal",
      "profile_url": "https://github.com/lucasjinreal"
    }
  },
  {
    "name": "rishikksh20/AudioMAE-pytorch",
    "description": "Unofficial PyTorch implementation of Masked Autoencoders that Listen",
    "url": "https://github.com/rishikksh20/AudioMAE-pytorch",
    "stars": 65,
    "forks": 6,
    "language": "Python",
    "last_updated": "2024-12-09T05:37:58Z",
    "topics": [
      "autoencoder",
      "masked-autoencoder",
      "self-supervised-learning",
      "speech",
      "speech-synthesis",
      "tts"
    ],
    "owner": {
      "username": "rishikksh20",
      "profile_url": "https://github.com/rishikksh20"
    }
  },
  {
    "name": "mycrazycracy/speaker-embedding-with-phonetic-information",
    "description": "The code for the Interspeech paper \"Speaker Embedding Extraction with Phonetic Information\"",
    "url": "https://github.com/mycrazycracy/speaker-embedding-with-phonetic-information",
    "stars": 43,
    "forks": 23,
    "language": "Shell",
    "last_updated": "2024-08-04T04:44:26Z",
    "topics": [],
    "owner": {
      "username": "mycrazycracy",
      "profile_url": "https://github.com/mycrazycracy"
    }
  },
  {
    "name": "KrishnaDN/BERTphone",
    "description": "Implementation of the paper \"BERTphone: Phonetically-aware Encoder Representations for Utterance-level Speaker and Language Recognition\"",
    "url": "https://github.com/KrishnaDN/BERTphone",
    "stars": 17,
    "forks": 5,
    "language": "Python",
    "last_updated": "2023-09-01T08:43:25Z",
    "topics": [
      "language-identification",
      "machine-learning",
      "pytorch",
      "speaker-identification",
      "speech-recognition",
      "unsupervised-learning"
    ],
    "owner": {
      "username": "KrishnaDN",
      "profile_url": "https://github.com/KrishnaDN"
    }
  },
  {
    "name": "mjhydri/BeatNet",
    "description": "BeatNet is state-of-the-art (Real-Time) and Offline joint music beat, downbeat, tempo, and meter tracking system using CRNN and particle filtering.  (ISMIR 2021's paper implementation).",
    "url": "https://github.com/mjhydri/BeatNet",
    "stars": 340,
    "forks": 56,
    "language": "Python",
    "last_updated": "2024-12-10T08:36:26Z",
    "topics": [
      "beat-tracking",
      "beatnet",
      "crnn-network",
      "dnn-beat-tracking",
      "downbeat-tracking",
      "joint-model",
      "meter-detection",
      "online-time-signature-detection",
      "particle-filtering",
      "pytorch",
      "real-time",
      "real-time-beat-tracker",
      "real-time-downbeat-tracker",
      "real-time-tempo",
      "state-of-the-art"
    ],
    "owner": {
      "username": "mjhydri",
      "profile_url": "https://github.com/mjhydri"
    }
  },
  {
    "name": "speechbrain/speechbrain",
    "description": "A PyTorch-based Speech Toolkit",
    "url": "https://github.com/speechbrain/speechbrain",
    "stars": 9038,
    "forks": 1412,
    "language": "Python",
    "last_updated": "2024-12-11T02:58:48Z",
    "topics": [
      "asr",
      "audio",
      "audio-processing",
      "deep-learning",
      "huggingface",
      "language-model",
      "pytorch",
      "speaker-diarization",
      "speaker-recognition",
      "speaker-verification",
      "speech-enhancement",
      "speech-processing",
      "speech-recognition",
      "speech-separation",
      "speech-to-text",
      "speech-toolkit",
      "speechrecognition",
      "spoken-language-understanding",
      "transformers",
      "voice-recognition"
    ],
    "owner": {
      "username": "speechbrain",
      "profile_url": "https://github.com/speechbrain"
    }
  },
  {
    "name": "GANtastic3/MaskCycleGAN-VC",
    "description": "Implementation of Kaneko et al.'s MaskCycleGAN-VC model for non-parallel voice conversion.",
    "url": "https://github.com/GANtastic3/MaskCycleGAN-VC",
    "stars": 113,
    "forks": 32,
    "language": "Python",
    "last_updated": "2024-12-05T13:59:16Z",
    "topics": [],
    "owner": {
      "username": "GANtastic3",
      "profile_url": "https://github.com/GANtastic3"
    }
  },
  {
    "name": "nguyenvulebinh/spoken-norm",
    "description": "Transformation spoken text to written text",
    "url": "https://github.com/nguyenvulebinh/spoken-norm",
    "stars": 29,
    "forks": 4,
    "language": "Python",
    "last_updated": "2024-12-09T08:55:40Z",
    "topics": [],
    "owner": {
      "username": "nguyenvulebinh",
      "profile_url": "https://github.com/nguyenvulebinh"
    }
  },
  {
    "name": "chomeyama/HN-UnifiedSourceFilterGAN",
    "description": null,
    "url": "https://github.com/chomeyama/HN-UnifiedSourceFilterGAN",
    "stars": 87,
    "forks": 18,
    "language": "Python",
    "last_updated": "2024-08-09T11:27:00Z",
    "topics": [],
    "owner": {
      "username": "chomeyama",
      "profile_url": "https://github.com/chomeyama"
    }
  },
  {
    "name": "duongna21/bartflax",
    "description": "Pre-training script for BART in JAX/Flax",
    "url": "https://github.com/duongna21/bartflax",
    "stars": 37,
    "forks": 1,
    "language": "Python",
    "last_updated": "2024-09-18T18:28:16Z",
    "topics": [],
    "owner": {
      "username": "duongna21",
      "profile_url": "https://github.com/duongna21"
    }
  },
  {
    "name": "waywardgeek/sonic",
    "description": "Simple library to speed up or slow down speech",
    "url": "https://github.com/waywardgeek/sonic",
    "stars": 617,
    "forks": 164,
    "language": "C",
    "last_updated": "2024-12-07T03:25:05Z",
    "topics": [],
    "owner": {
      "username": "waywardgeek",
      "profile_url": "https://github.com/waywardgeek"
    }
  },
  {
    "name": "neillu23/CDiffuSE",
    "description": "Conditional Diffusion Probabilistic Model for Speech Enhancement ",
    "url": "https://github.com/neillu23/CDiffuSE",
    "stars": 217,
    "forks": 34,
    "language": "Python",
    "last_updated": "2024-12-10T03:50:26Z",
    "topics": [],
    "owner": {
      "username": "neillu23",
      "profile_url": "https://github.com/neillu23"
    }
  },
  {
    "name": "fuzhenxin/Style-Transfer-in-Text",
    "description": "Paper List for Style Transfer in Text",
    "url": "https://github.com/fuzhenxin/Style-Transfer-in-Text",
    "stars": 1618,
    "forks": 194,
    "language": null,
    "last_updated": "2024-12-05T03:04:21Z",
    "topics": [
      "natural-language-processing",
      "paper",
      "style-transfer",
      "survey"
    ],
    "owner": {
      "username": "fuzhenxin",
      "profile_url": "https://github.com/fuzhenxin"
    }
  },
  {
    "name": "b04901014/FG-transformer-TTS",
    "description": "Official implementation for the paper Fine-grained style control in transformer-based text-to-speech synthesis. ",
    "url": "https://github.com/b04901014/FG-transformer-TTS",
    "stars": 87,
    "forks": 11,
    "language": "Python",
    "last_updated": "2024-10-28T04:31:00Z",
    "topics": [],
    "owner": {
      "username": "b04901014",
      "profile_url": "https://github.com/b04901014"
    }
  },
  {
    "name": "KunZhou9646/Mixed_Emotions_Demo",
    "description": "This is the demo page of the paper \"Speech Synthesis with Mixed Emotions\".",
    "url": "https://github.com/KunZhou9646/Mixed_Emotions_Demo",
    "stars": 2,
    "forks": 0,
    "language": "HTML",
    "last_updated": "2022-07-22T18:00:20Z",
    "topics": [],
    "owner": {
      "username": "KunZhou9646",
      "profile_url": "https://github.com/KunZhou9646"
    }
  },
  {
    "name": "albertfgu/diffwave-sashimi",
    "description": "Implementation of DiffWave and SaShiMi audio generation models",
    "url": "https://github.com/albertfgu/diffwave-sashimi",
    "stars": 118,
    "forks": 14,
    "language": "Python",
    "last_updated": "2024-11-28T11:52:03Z",
    "topics": [],
    "owner": {
      "username": "albertfgu",
      "profile_url": "https://github.com/albertfgu"
    }
  },
  {
    "name": "google/visqol",
    "description": "Perceptual Quality Estimator for speech and audio",
    "url": "https://github.com/google/visqol",
    "stars": 711,
    "forks": 126,
    "language": "C++",
    "last_updated": "2024-12-10T05:43:49Z",
    "topics": [],
    "owner": {
      "username": "google",
      "profile_url": "https://github.com/google"
    }
  },
  {
    "name": "jonatasgrosman/huggingsound",
    "description": "HuggingSound: A toolkit for speech-related tasks based on Hugging Face's tools",
    "url": "https://github.com/jonatasgrosman/huggingsound",
    "stars": 436,
    "forks": 44,
    "language": "Python",
    "last_updated": "2024-12-08T17:10:03Z",
    "topics": [
      "asr",
      "audio",
      "automatic-speech-recognition",
      "speech",
      "speech-recognition",
      "speech-to-text",
      "transformers"
    ],
    "owner": {
      "username": "jonatasgrosman",
      "profile_url": "https://github.com/jonatasgrosman"
    }
  },
  {
    "name": "muqiaoy/eGeMAPS_estimator",
    "description": null,
    "url": "https://github.com/muqiaoy/eGeMAPS_estimator",
    "stars": 22,
    "forks": 3,
    "language": "Python",
    "last_updated": "2024-06-04T07:25:28Z",
    "topics": [],
    "owner": {
      "username": "muqiaoy",
      "profile_url": "https://github.com/muqiaoy"
    }
  },
  {
    "name": "Kyubyong/g2p",
    "description": "g2p: English Grapheme To Phoneme Conversion",
    "url": "https://github.com/Kyubyong/g2p",
    "stars": 821,
    "forks": 128,
    "language": "Python",
    "last_updated": "2024-12-10T21:46:38Z",
    "topics": [
      "cmudict",
      "english-grapheme",
      "g2p",
      "g2p-seq2seq",
      "pronunciation"
    ],
    "owner": {
      "username": "Kyubyong",
      "profile_url": "https://github.com/Kyubyong"
    }
  },
  {
    "name": "rishikksh20/iSTFT-Avocodo-pytorch",
    "description": "Ultrafast GAN  based Vocoder for Text to Speech",
    "url": "https://github.com/rishikksh20/iSTFT-Avocodo-pytorch",
    "stars": 50,
    "forks": 7,
    "language": "Python",
    "last_updated": "2024-07-30T06:54:28Z",
    "topics": [
      "avocodo",
      "gan",
      "hifigan",
      "melgan",
      "speech",
      "speech-synthesis",
      "text-to-speech",
      "tts",
      "vocoder"
    ],
    "owner": {
      "username": "rishikksh20",
      "profile_url": "https://github.com/rishikksh20"
    }
  },
  {
    "name": "NVIDIA/CleanUNet",
    "description": "Official PyTorch Implementation of CleanUNet (ICASSP 2022)",
    "url": "https://github.com/NVIDIA/CleanUNet",
    "stars": 301,
    "forks": 51,
    "language": "Python",
    "last_updated": "2024-12-10T14:52:08Z",
    "topics": [
      "noise-reduction",
      "speech-denoising",
      "speech-enchacement",
      "speech-processing"
    ],
    "owner": {
      "username": "NVIDIA",
      "profile_url": "https://github.com/NVIDIA"
    }
  },
  {
    "name": "patil-suraj/vit-vqgan",
    "description": "JAX implementation ViT-VQGAN",
    "url": "https://github.com/patil-suraj/vit-vqgan",
    "stars": 79,
    "forks": 11,
    "language": "Python",
    "last_updated": "2024-12-08T00:15:29Z",
    "topics": [],
    "owner": {
      "username": "patil-suraj",
      "profile_url": "https://github.com/patil-suraj"
    }
  },
  {
    "name": "lucidrains/vector-quantize-pytorch",
    "description": "Vector (and Scalar) Quantization, in Pytorch",
    "url": "https://github.com/lucidrains/vector-quantize-pytorch",
    "stars": 2722,
    "forks": 219,
    "language": "Python",
    "last_updated": "2024-12-10T18:58:54Z",
    "topics": [
      "artificial-intelligence",
      "deep-learning",
      "pytorch",
      "scalar-quantization",
      "vector-quantization"
    ],
    "owner": {
      "username": "lucidrains",
      "profile_url": "https://github.com/lucidrains"
    }
  },
  {
    "name": "kenders2000/distortionDetection",
    "description": "C++ Program to detect Clipping and other overload based nonlinear distortions in Wav Files",
    "url": "https://github.com/kenders2000/distortionDetection",
    "stars": 30,
    "forks": 5,
    "language": "C",
    "last_updated": "2024-09-23T09:25:01Z",
    "topics": [],
    "owner": {
      "username": "kenders2000",
      "profile_url": "https://github.com/kenders2000"
    }
  },
  {
    "name": "insunhwang89/StyleVC",
    "description": null,
    "url": "https://github.com/insunhwang89/StyleVC",
    "stars": 30,
    "forks": 3,
    "language": "Jupyter Notebook",
    "last_updated": "2024-10-24T06:09:27Z",
    "topics": [],
    "owner": {
      "username": "insunhwang89",
      "profile_url": "https://github.com/insunhwang89"
    }
  },
  {
    "name": "maum-ai/nuwave2",
    "description": "NU-Wave 2: A General Neural Audio Upsampling Model for Various Sampling Rates @ INTERSPEECH 2022",
    "url": "https://github.com/maum-ai/nuwave2",
    "stars": 280,
    "forks": 21,
    "language": "Python",
    "last_updated": "2024-12-05T23:44:02Z",
    "topics": [
      "deep-learning",
      "neural-audio-upsampling",
      "pytorch",
      "super-resolution",
      "upsampling"
    ],
    "owner": {
      "username": "maum-ai",
      "profile_url": "https://github.com/maum-ai"
    }
  },
  {
    "name": "XiangLi1999/Diffusion-LM",
    "description": "Diffusion-LM ",
    "url": "https://github.com/XiangLi1999/Diffusion-LM",
    "stars": 1061,
    "forks": 140,
    "language": "Python",
    "last_updated": "2024-12-05T02:57:48Z",
    "topics": [],
    "owner": {
      "username": "XiangLi1999",
      "profile_url": "https://github.com/XiangLi1999"
    }
  },
  {
    "name": "bzhangGo/st_from_scratch",
    "description": "Revisiting End-to-End Speech-to-Text Translation From Scratch",
    "url": "https://github.com/bzhangGo/st_from_scratch",
    "stars": 12,
    "forks": 4,
    "language": "Python",
    "last_updated": "2024-11-09T09:46:54Z",
    "topics": [
      "end-to-end-speech-translation",
      "speech-to-text-translation",
      "speech-translation",
      "speech-translation-from-scratch"
    ],
    "owner": {
      "username": "bzhangGo",
      "profile_url": "https://github.com/bzhangGo"
    }
  },
  {
    "name": "keonlee9420/DailyTalk",
    "description": "Official repository of DailyTalk: Spoken Dialogue Dataset for Conversational Text-to-Speech, ICASSP 2023",
    "url": "https://github.com/keonlee9420/DailyTalk",
    "stars": 206,
    "forks": 13,
    "language": "Python",
    "last_updated": "2024-12-06T01:08:32Z",
    "topics": [
      "conversational-ai",
      "conversational-data",
      "conversational-tts",
      "dataset",
      "non-autoregressive",
      "pytorch",
      "speech-synthesis",
      "text-to-speech",
      "tts",
      "tts-dataset"
    ],
    "owner": {
      "username": "keonlee9420",
      "profile_url": "https://github.com/keonlee9420"
    }
  },
  {
    "name": "rishikksh20/Avocodo-pytorch",
    "description": "Avocodo: Generative Adversarial Network for Artifact-free Vocoder",
    "url": "https://github.com/rishikksh20/Avocodo-pytorch",
    "stars": 115,
    "forks": 15,
    "language": "Python",
    "last_updated": "2024-06-20T15:34:08Z",
    "topics": [
      "avocodo",
      "gan",
      "generative-adversarial-network",
      "hifi-gan",
      "pytorch",
      "speech-synthesis",
      "text-to-speech",
      "tts",
      "vocoder"
    ],
    "owner": {
      "username": "rishikksh20",
      "profile_url": "https://github.com/rishikksh20"
    }
  },
  {
    "name": "ermongroup/SDEdit",
    "description": "PyTorch implementation for SDEdit: Image Synthesis and Editing with Stochastic Differential Equations",
    "url": "https://github.com/ermongroup/SDEdit",
    "stars": 1019,
    "forks": 92,
    "language": "Python",
    "last_updated": "2024-12-08T11:47:51Z",
    "topics": [
      "controllable-generation",
      "image-editing",
      "image-generation",
      "image-manipulation",
      "pytorch",
      "score-matching"
    ],
    "owner": {
      "username": "ermongroup",
      "profile_url": "https://github.com/ermongroup"
    }
  },
  {
    "name": "auspicious3000/contentvec",
    "description": "speech self-supervised representations",
    "url": "https://github.com/auspicious3000/contentvec",
    "stars": 471,
    "forks": 38,
    "language": "Python",
    "last_updated": "2024-12-04T09:31:39Z",
    "topics": [
      "self-supervised-learning",
      "speech"
    ],
    "owner": {
      "username": "auspicious3000",
      "profile_url": "https://github.com/auspicious3000"
    }
  },
  {
    "name": "facebookresearch/denoised_mdp",
    "description": "Open source code for paper \"Denoised MDPs: Learning World Models Better Than the World Itself\" ",
    "url": "https://github.com/facebookresearch/denoised_mdp",
    "stars": 134,
    "forks": 11,
    "language": "Python",
    "last_updated": "2024-11-27T03:26:04Z",
    "topics": [],
    "owner": {
      "username": "facebookresearch",
      "profile_url": "https://github.com/facebookresearch"
    }
  },
  {
    "name": "NVIDIA/radtts",
    "description": "Provides training, inference and voice conversion recipes for RADTTS and RADTTS++: Flow-based TTS models with Robust Alignment Learning, Diverse Synthesis, and Generative Modeling and Fine-Grained Control over of Low Dimensional (F0 and Energy) Speech Attributes.",
    "url": "https://github.com/NVIDIA/radtts",
    "stars": 283,
    "forks": 40,
    "language": "Roff",
    "last_updated": "2024-10-12T07:20:01Z",
    "topics": [],
    "owner": {
      "username": "NVIDIA",
      "profile_url": "https://github.com/NVIDIA"
    }
  },
  {
    "name": "dunky11/voicesmith",
    "description": "[WIP] VoiceSmith makes training text to speech models easy. ",
    "url": "https://github.com/dunky11/voicesmith",
    "stars": 223,
    "forks": 32,
    "language": "Python",
    "last_updated": "2024-11-22T15:22:24Z",
    "topics": [
      "dataset-manager",
      "delightfultts",
      "preprocessing",
      "speech-synthesis",
      "text-to-speech",
      "toolkit",
      "tts",
      "univnet",
      "voice-cloning"
    ],
    "owner": {
      "username": "dunky11",
      "profile_url": "https://github.com/dunky11"
    }
  },
  {
    "name": "lucidrains/parti-pytorch",
    "description": "Implementation of Parti, Google's pure attention-based text-to-image neural network, in Pytorch",
    "url": "https://github.com/lucidrains/parti-pytorch",
    "stars": 524,
    "forks": 24,
    "language": "Python",
    "last_updated": "2024-11-21T09:42:13Z",
    "topics": [
      "artificial-intelligence",
      "attention-mechanism",
      "deep-learning",
      "text-to-image",
      "transformers"
    ],
    "owner": {
      "username": "lucidrains",
      "profile_url": "https://github.com/lucidrains"
    }
  },
  {
    "name": "alshedivat/al-folio",
    "description": "A beautiful, simple, clean, and responsive Jekyll theme for academics",
    "url": "https://github.com/alshedivat/al-folio",
    "stars": 11500,
    "forks": 11316,
    "language": "HTML",
    "last_updated": "2024-12-11T02:45:55Z",
    "topics": [
      "academic",
      "academic-website",
      "github-pages",
      "hacktoberfest",
      "jekyll",
      "jekyll-blog",
      "jekyll-theme",
      "personal-website",
      "portfolio-website",
      "theme"
    ],
    "owner": {
      "username": "alshedivat",
      "profile_url": "https://github.com/alshedivat"
    }
  },
  {
    "name": "huggingface/diffusers",
    "description": "\ud83e\udd17 Diffusers: State-of-the-art diffusion models for image and audio generation in PyTorch and FLAX.",
    "url": "https://github.com/huggingface/diffusers",
    "stars": 26568,
    "forks": 5471,
    "language": "Python",
    "last_updated": "2024-12-11T03:33:02Z",
    "topics": [
      "deep-learning",
      "diffusion",
      "flax",
      "hacktoberfest",
      "image-generation",
      "image2image",
      "jax",
      "latent-diffusion-models",
      "pytorch",
      "score-based-generative-modeling",
      "stable-diffusion",
      "stable-diffusion-diffusers",
      "text2image"
    ],
    "owner": {
      "username": "huggingface",
      "profile_url": "https://github.com/huggingface"
    }
  },
  {
    "name": "mit-han-lab/mcunet",
    "description": "[NeurIPS 2020] MCUNet: Tiny Deep Learning on IoT Devices; [NeurIPS 2021] MCUNetV2: Memory-Efficient Patch-based Inference for Tiny Deep Learning",
    "url": "https://github.com/mit-han-lab/mcunet",
    "stars": 491,
    "forks": 82,
    "language": "Python",
    "last_updated": "2024-12-10T14:48:39Z",
    "topics": [
      "deep-learning",
      "microncontroller",
      "neural-architecture-search",
      "pytorch",
      "tinyml"
    ],
    "owner": {
      "username": "mit-han-lab",
      "profile_url": "https://github.com/mit-han-lab"
    }
  },
  {
    "name": "kennethleungty/MLOps-Specialization-Notes",
    "description": "Notes for Machine Learning Engineering for Production (MLOps) Specialization course by DeepLearning.AI & Andrew Ng",
    "url": "https://github.com/kennethleungty/MLOps-Specialization-Notes",
    "stars": 351,
    "forks": 152,
    "language": null,
    "last_updated": "2024-12-08T18:33:00Z",
    "topics": [
      "andrew-ng",
      "course",
      "coursera",
      "data-science",
      "deep-learning",
      "deeplearningai",
      "machine-learning",
      "machine-learning-engineering",
      "machine-learning-ops",
      "ml-engineering",
      "ml-engineering-for-production",
      "mlops",
      "notes"
    ],
    "owner": {
      "username": "kennethleungty",
      "profile_url": "https://github.com/kennethleungty"
    }
  },
  {
    "name": "yl4579/PitchExtractor",
    "description": "Deep Neural Pitch Extractor for Voice Conversion and TTS Training",
    "url": "https://github.com/yl4579/PitchExtractor",
    "stars": 120,
    "forks": 30,
    "language": "Python",
    "last_updated": "2024-11-26T13:49:22Z",
    "topics": [
      "pitch-estimation",
      "text-to-speech",
      "voice-conversion"
    ],
    "owner": {
      "username": "yl4579",
      "profile_url": "https://github.com/yl4579"
    }
  },
  {
    "name": "maziarraissi/Applied-Deep-Learning",
    "description": "Applied Deep Learning Course",
    "url": "https://github.com/maziarraissi/Applied-Deep-Learning",
    "stars": 3224,
    "forks": 675,
    "language": null,
    "last_updated": "2024-12-10T20:26:16Z",
    "topics": [],
    "owner": {
      "username": "maziarraissi",
      "profile_url": "https://github.com/maziarraissi"
    }
  },
  {
    "name": "sh-lee-prml/BigVGAN",
    "description": "Unofficial pytorch implementation of BigVGAN: A Universal Neural Vocoder with Large-Scale Training",
    "url": "https://github.com/sh-lee-prml/BigVGAN",
    "stars": 130,
    "forks": 16,
    "language": "Python",
    "last_updated": "2024-07-21T16:33:26Z",
    "topics": [],
    "owner": {
      "username": "sh-lee-prml",
      "profile_url": "https://github.com/sh-lee-prml"
    }
  },
  {
    "name": "johnowhitaker/aiaiart",
    "description": "Course content and resources for the AIAIART course.",
    "url": "https://github.com/johnowhitaker/aiaiart",
    "stars": 567,
    "forks": 47,
    "language": "Jupyter Notebook",
    "last_updated": "2024-11-07T07:34:29Z",
    "topics": [],
    "owner": {
      "username": "johnowhitaker",
      "profile_url": "https://github.com/johnowhitaker"
    }
  },
  {
    "name": "vovanphuc/SimeCSE_Vietnamese",
    "description": "SimeCSE_Vietnamese: Simple Contrastive Learning of Sentence Embeddings with Vietnamese",
    "url": "https://github.com/vovanphuc/SimeCSE_Vietnamese",
    "stars": 19,
    "forks": 1,
    "language": null,
    "last_updated": "2024-09-21T11:30:41Z",
    "topics": [],
    "owner": {
      "username": "vovanphuc",
      "profile_url": "https://github.com/vovanphuc"
    }
  },
  {
    "name": "DatCanCode/sentence-transformers",
    "description": "Sentence Embeddings with BERT & XLNet",
    "url": "https://github.com/DatCanCode/sentence-transformers",
    "stars": 27,
    "forks": 8,
    "language": "Python",
    "last_updated": "2024-09-18T18:27:54Z",
    "topics": [],
    "owner": {
      "username": "DatCanCode",
      "profile_url": "https://github.com/DatCanCode"
    }
  },
  {
    "name": "NVIDIA/BigVGAN",
    "description": "Official PyTorch implementation of BigVGAN (ICLR 2023)",
    "url": "https://github.com/NVIDIA/BigVGAN",
    "stars": 915,
    "forks": 110,
    "language": "Python",
    "last_updated": "2024-12-11T03:38:28Z",
    "topics": [
      "audio-generation",
      "audio-synthesis",
      "music-synthesis",
      "neural-vocoder",
      "singing-voice-synthesis",
      "speech-synthesis"
    ],
    "owner": {
      "username": "NVIDIA",
      "profile_url": "https://github.com/NVIDIA"
    }
  },
  {
    "name": "yl4579/AuxiliaryASR",
    "description": "Joint CTC-S2S Phoneme-level ASR for Voice Conversion and TTS (Text-Mel Alignment)",
    "url": "https://github.com/yl4579/AuxiliaryASR",
    "stars": 112,
    "forks": 36,
    "language": "Python",
    "last_updated": "2024-10-24T08:01:12Z",
    "topics": [
      "asr",
      "text-to-speech",
      "voice-conversion"
    ],
    "owner": {
      "username": "yl4579",
      "profile_url": "https://github.com/yl4579"
    }
  },
  {
    "name": "deepchecks/deepchecks",
    "description": "Deepchecks: Tests for Continuous Validation of ML Models & Data. Deepchecks is a holistic open-source solution for all of your AI & ML validation needs, enabling to thoroughly test your data and models from research to production.",
    "url": "https://github.com/deepchecks/deepchecks",
    "stars": 3642,
    "forks": 255,
    "language": "Python",
    "last_updated": "2024-12-10T22:47:39Z",
    "topics": [
      "data-drift",
      "data-science",
      "data-validation",
      "deep-learning",
      "html-report",
      "jupyter-notebook",
      "machine-learning",
      "ml",
      "mlops",
      "model-monitoring",
      "model-validation",
      "pandas-dataframe",
      "python",
      "pytorch"
    ],
    "owner": {
      "username": "deepchecks",
      "profile_url": "https://github.com/deepchecks"
    }
  },
  {
    "name": "timeseriesAI/tsai",
    "description": "Time series Timeseries Deep Learning Machine Learning Python Pytorch  fastai | State-of-the-art Deep Learning library  for Time Series and Sequences in Pytorch / fastai",
    "url": "https://github.com/timeseriesAI/tsai",
    "stars": 5328,
    "forks": 660,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-10T14:21:36Z",
    "topics": [
      "classification",
      "cnn",
      "deep-learning",
      "fastai",
      "forecasting",
      "inceptiontime",
      "machine-learning",
      "python",
      "pytorch",
      "regression",
      "rnn",
      "rocket",
      "self-supervised",
      "sequential",
      "state-of-the-art",
      "time-series",
      "time-series-analysis",
      "time-series-classification",
      "timeseries",
      "transformer"
    ],
    "owner": {
      "username": "timeseriesAI",
      "profile_url": "https://github.com/timeseriesAI"
    }
  },
  {
    "name": "dnguyenngoc/document-processing",
    "description": "This is project how to build full workflow ocr processing document",
    "url": "https://github.com/dnguyenngoc/document-processing",
    "stars": 5,
    "forks": 1,
    "language": "Python",
    "last_updated": "2024-04-19T20:56:57Z",
    "topics": [
      "ai",
      "celery",
      "deep-learning",
      "fastapi",
      "python",
      "rabbitmq",
      "react",
      "redis",
      "tensorflow"
    ],
    "owner": {
      "username": "dnguyenngoc",
      "profile_url": "https://github.com/dnguyenngoc"
    }
  },
  {
    "name": "dnguyenngoc/real-time-analytic",
    "description": "This repo gives an introduction to setting up streaming analytics using open source technologies",
    "url": "https://github.com/dnguyenngoc/real-time-analytic",
    "stars": 22,
    "forks": 13,
    "language": "Python",
    "last_updated": "2024-09-20T14:21:47Z",
    "topics": [
      "airflow",
      "analytics",
      "druid",
      "kafka",
      "kafka-streams",
      "real-time",
      "superset"
    ],
    "owner": {
      "username": "dnguyenngoc",
      "profile_url": "https://github.com/dnguyenngoc"
    }
  },
  {
    "name": "spotify/klio",
    "description": "Smarter data pipelines for audio.",
    "url": "https://github.com/spotify/klio",
    "stars": 845,
    "forks": 48,
    "language": "Python",
    "last_updated": "2024-12-08T13:16:20Z",
    "topics": [
      "audio-processing",
      "data-pipeline",
      "media-processing",
      "signal-processing"
    ],
    "owner": {
      "username": "spotify",
      "profile_url": "https://github.com/spotify"
    }
  },
  {
    "name": "facebookresearch/BinauralSpeechSynthesis",
    "description": "N/A",
    "url": "https://github.com/facebookresearch/BinauralSpeechSynthesis",
    "stars": 167,
    "forks": 19,
    "language": "Python",
    "last_updated": "2024-12-01T03:39:22Z",
    "topics": [],
    "owner": {
      "username": "facebookresearch",
      "profile_url": "https://github.com/facebookresearch"
    }
  },
  {
    "name": "yl4579/StyleTTS",
    "description": "Official Implementation of StyleTTS",
    "url": "https://github.com/yl4579/StyleTTS",
    "stars": 408,
    "forks": 65,
    "language": "Python",
    "last_updated": "2024-12-06T09:09:07Z",
    "topics": [
      "deep-learning",
      "pytorch",
      "speech-synthesis",
      "text-to-speech",
      "tts"
    ],
    "owner": {
      "username": "yl4579",
      "profile_url": "https://github.com/yl4579"
    }
  },
  {
    "name": "lucidrains/insertion-deletion-ddpm",
    "description": "Implementation of Insertion-deletion Denoising Diffusion Probabilistic Models",
    "url": "https://github.com/lucidrains/insertion-deletion-ddpm",
    "stars": 30,
    "forks": 2,
    "language": null,
    "last_updated": "2024-11-10T11:36:50Z",
    "topics": [
      "artificial-intelligence",
      "deep-learning",
      "denoising-diffusion"
    ],
    "owner": {
      "username": "lucidrains",
      "profile_url": "https://github.com/lucidrains"
    }
  },
  {
    "name": "faroit/awesome-python-scientific-audio",
    "description": " Curated list of python software and packages related to scientific research in audio",
    "url": "https://github.com/faroit/awesome-python-scientific-audio",
    "stars": 1583,
    "forks": 170,
    "language": null,
    "last_updated": "2024-12-09T08:29:28Z",
    "topics": [
      "audio",
      "awesome-list",
      "python"
    ],
    "owner": {
      "username": "faroit",
      "profile_url": "https://github.com/faroit"
    }
  },
  {
    "name": "SpeechResearch/speechresearch.github.io",
    "description": null,
    "url": "https://github.com/SpeechResearch/speechresearch.github.io",
    "stars": 43,
    "forks": 5,
    "language": "HTML",
    "last_updated": "2024-11-09T17:19:31Z",
    "topics": [],
    "owner": {
      "username": "SpeechResearch",
      "profile_url": "https://github.com/SpeechResearch"
    }
  },
  {
    "name": "facebookresearch/dlrm",
    "description": "An implementation of a deep learning recommendation model (DLRM)",
    "url": "https://github.com/facebookresearch/dlrm",
    "stars": 3787,
    "forks": 844,
    "language": "Python",
    "last_updated": "2024-12-10T08:22:53Z",
    "topics": [],
    "owner": {
      "username": "facebookresearch",
      "profile_url": "https://github.com/facebookresearch"
    }
  },
  {
    "name": "Rongjiehuang/FastDiff",
    "description": "PyTorch Implementation of FastDiff (IJCAI'22)",
    "url": "https://github.com/Rongjiehuang/FastDiff",
    "stars": 409,
    "forks": 64,
    "language": "Python",
    "last_updated": "2024-12-03T12:43:43Z",
    "topics": [
      "ijcai2022",
      "neural-vocoder",
      "speech-synthesis",
      "text-to-speech",
      "vocoder"
    ],
    "owner": {
      "username": "Rongjiehuang",
      "profile_url": "https://github.com/Rongjiehuang"
    }
  },
  {
    "name": "pytorch/torchrec",
    "description": "Pytorch domain library for recommendation systems",
    "url": "https://github.com/pytorch/torchrec",
    "stars": 1967,
    "forks": 449,
    "language": "Python",
    "last_updated": "2024-12-11T02:50:26Z",
    "topics": [
      "cuda",
      "deep-learning",
      "gpu",
      "pytorch",
      "recommendation-system",
      "recommender-system",
      "sharding"
    ],
    "owner": {
      "username": "pytorch",
      "profile_url": "https://github.com/pytorch"
    }
  },
  {
    "name": "Spijkervet/CLMR",
    "description": "Official PyTorch implementation of Contrastive Learning of Musical Representations",
    "url": "https://github.com/Spijkervet/CLMR",
    "stars": 311,
    "forks": 48,
    "language": "Python",
    "last_updated": "2024-12-04T02:36:40Z",
    "topics": [
      "contrastive-learning",
      "music-classification",
      "music-information-retrieval",
      "self-supervised-learning"
    ],
    "owner": {
      "username": "Spijkervet",
      "profile_url": "https://github.com/Spijkervet"
    }
  },
  {
    "name": "sevagh/pitch-detection",
    "description": "autocorrelation-based O(NlogN) pitch detection",
    "url": "https://github.com/sevagh/pitch-detection",
    "stars": 581,
    "forks": 68,
    "language": "C++",
    "last_updated": "2024-12-02T08:31:48Z",
    "topics": [
      "autocorrelation",
      "dsp",
      "fft",
      "mpm",
      "pitch-detection",
      "pitch-estimation",
      "pitch-tracking",
      "pyin",
      "yin"
    ],
    "owner": {
      "username": "sevagh",
      "profile_url": "https://github.com/sevagh"
    }
  },
  {
    "name": "yerfor/SyntaSpeech",
    "description": "SyntaSpeech: Syntax-aware Generative Adversarial Text-to-Speech; IJCAI 2022; Official code",
    "url": "https://github.com/yerfor/SyntaSpeech",
    "stars": 198,
    "forks": 31,
    "language": "Python",
    "last_updated": "2024-11-29T03:06:57Z",
    "topics": [
      "gan",
      "pytorch",
      "speech-synthesis",
      "tts"
    ],
    "owner": {
      "username": "yerfor",
      "profile_url": "https://github.com/yerfor"
    }
  },
  {
    "name": "thuhcsi/Crystal",
    "description": "Crystal - C++ implementation of a unified framework for multilingual TTS synthesis engine  with SSML specification as interface.",
    "url": "https://github.com/thuhcsi/Crystal",
    "stars": 227,
    "forks": 68,
    "language": "C++",
    "last_updated": "2024-12-05T17:47:58Z",
    "topics": [
      "crystal-tts-engine",
      "speech-synthesis",
      "text-to-speech",
      "tts"
    ],
    "owner": {
      "username": "thuhcsi",
      "profile_url": "https://github.com/thuhcsi"
    }
  },
  {
    "name": "Kyubyong/mtp",
    "description": "Multi-lingual Text Processing",
    "url": "https://github.com/Kyubyong/mtp",
    "stars": 96,
    "forks": 12,
    "language": null,
    "last_updated": "2024-12-09T10:49:02Z",
    "topics": [
      "text-processing"
    ],
    "owner": {
      "username": "Kyubyong",
      "profile_url": "https://github.com/Kyubyong"
    }
  },
  {
    "name": "bshall/acoustic-model",
    "description": "Acoustic models for: A Comparison of Discrete and Soft Speech Units for Improved Voice Conversion",
    "url": "https://github.com/bshall/acoustic-model",
    "stars": 101,
    "forks": 25,
    "language": "Python",
    "last_updated": "2024-12-09T04:37:10Z",
    "topics": [
      "pytorch",
      "representation-learning",
      "speech",
      "voice-conversion"
    ],
    "owner": {
      "username": "bshall",
      "profile_url": "https://github.com/bshall"
    }
  },
  {
    "name": "unilight/LDNet",
    "description": "Official implementation of the paper: \"LDNet: Unified Listener Dependent Modeling in MOS Prediction for Synthetic Speech\"",
    "url": "https://github.com/unilight/LDNet",
    "stars": 61,
    "forks": 10,
    "language": "Python",
    "last_updated": "2024-09-05T09:33:44Z",
    "topics": [
      "mbnet",
      "mobilenetv3",
      "mos-prediction",
      "mosnet",
      "pytorch",
      "vcc2018",
      "voicemos"
    ],
    "owner": {
      "username": "unilight",
      "profile_url": "https://github.com/unilight"
    }
  },
  {
    "name": "keonlee9420/Comprehensive-E2E-TTS",
    "description": "A Non-Autoregressive End-to-End Text-to-Speech (text-to-wav), supporting a family of SOTA unsupervised duration modelings. This project grows with the research community, aiming to achieve the ultimate E2E-TTS",
    "url": "https://github.com/keonlee9420/Comprehensive-E2E-TTS",
    "stars": 145,
    "forks": 19,
    "language": "Python",
    "last_updated": "2024-11-25T03:46:24Z",
    "topics": [
      "deep-learning",
      "end-to-end",
      "fastspeech2",
      "hifi-gan",
      "jets",
      "multi-speaker",
      "neural-tts",
      "non-ar",
      "non-autoregressive",
      "pytorch",
      "single-speaker",
      "sota",
      "speech-synthesis",
      "text-to-speech",
      "text-to-wav",
      "tts",
      "ultimate-tts",
      "unsupervised"
    ],
    "owner": {
      "username": "keonlee9420",
      "profile_url": "https://github.com/keonlee9420"
    }
  },
  {
    "name": "s3prl/s3prl",
    "description": "Self-Supervised Speech Pre-training and Representation Learning Toolkit",
    "url": "https://github.com/s3prl/s3prl",
    "stars": 2280,
    "forks": 486,
    "language": "Python",
    "last_updated": "2024-12-10T09:39:09Z",
    "topics": [
      "apc",
      "cpc",
      "data2vec",
      "decoar",
      "decoar2",
      "distilhubert",
      "hubert",
      "mockingjay",
      "pase",
      "representation-learning",
      "self-supervised-learning",
      "speech-pretraining",
      "speech-representation",
      "tera",
      "unispeech-sat",
      "vq-apc",
      "vq-wav2vec",
      "wav2vec",
      "wav2vec2",
      "wavlm"
    ],
    "owner": {
      "username": "s3prl",
      "profile_url": "https://github.com/s3prl"
    }
  },
  {
    "name": "keonlee9420/Cross-Speaker-Emotion-Transfer",
    "description": "PyTorch Implementation of ByteDance's Cross-speaker Emotion Transfer Based on Speaker Condition Layer Normalization and Semi-Supervised Training in Text-To-Speech",
    "url": "https://github.com/keonlee9420/Cross-Speaker-Emotion-Transfer",
    "stars": 187,
    "forks": 27,
    "language": "Python",
    "last_updated": "2024-10-22T10:21:24Z",
    "topics": [
      "conditional-layer-normalization",
      "cross-speaker",
      "deep-neural-networks",
      "emotion-transfer",
      "generative-model",
      "global-style-tokens",
      "neural-tts",
      "non-ar",
      "non-autoregressive",
      "parallel-tacotron",
      "pytorch",
      "semi-supervised-learning",
      "speech-synthesis",
      "text-to-speech",
      "tts"
    ],
    "owner": {
      "username": "keonlee9420",
      "profile_url": "https://github.com/keonlee9420"
    }
  },
  {
    "name": "revsic/torch-tacotron",
    "description": "PyTorch implementation of Tacotron, 2017.",
    "url": "https://github.com/revsic/torch-tacotron",
    "stars": 1,
    "forks": 0,
    "language": "Python",
    "last_updated": "2022-05-04T01:49:31Z",
    "topics": [],
    "owner": {
      "username": "revsic",
      "profile_url": "https://github.com/revsic"
    }
  },
  {
    "name": "aliutkus/speechmetrics",
    "description": "A wrapper around speech quality metrics MOSNet, BSSEval, STOI, PESQ, SRMR, SISDR",
    "url": "https://github.com/aliutkus/speechmetrics",
    "stars": 913,
    "forks": 155,
    "language": "Python",
    "last_updated": "2024-12-10T23:20:36Z",
    "topics": [],
    "owner": {
      "username": "aliutkus",
      "profile_url": "https://github.com/aliutkus"
    }
  },
  {
    "name": "Labmem-Zhouyx/CDFSE_FastSpeech2",
    "description": "The Official Implementation of \u201cContent-Dependent Fine-Grained Speaker Embedding for Zero-Shot Speaker Adaptation in Text-to-Speech Synthesis\u201d",
    "url": "https://github.com/Labmem-Zhouyx/CDFSE_FastSpeech2",
    "stars": 81,
    "forks": 12,
    "language": "Python",
    "last_updated": "2024-10-28T03:13:47Z",
    "topics": [
      "pytorch-implementation",
      "speaker",
      "tts"
    ],
    "owner": {
      "username": "Labmem-Zhouyx",
      "profile_url": "https://github.com/Labmem-Zhouyx"
    }
  },
  {
    "name": "polvanrijn/VoiceMe",
    "description": "Repository for the paper: VoiceMe: Personalized voice generation in TTS",
    "url": "https://github.com/polvanrijn/VoiceMe",
    "stars": 126,
    "forks": 21,
    "language": "Python",
    "last_updated": "2024-11-21T07:36:55Z",
    "topics": [],
    "owner": {
      "username": "polvanrijn",
      "profile_url": "https://github.com/polvanrijn"
    }
  },
  {
    "name": "stylegan-human/StyleGAN-Human",
    "description": "StyleGAN-Human: A Data-Centric Odyssey of Human Generation",
    "url": "https://github.com/stylegan-human/StyleGAN-Human",
    "stars": 1152,
    "forks": 145,
    "language": "Python",
    "last_updated": "2024-12-08T15:31:45Z",
    "topics": [],
    "owner": {
      "username": "stylegan-human",
      "profile_url": "https://github.com/stylegan-human"
    }
  },
  {
    "name": "neonbjb/tortoise-tts",
    "description": "A multi-voice TTS system trained with an emphasis on quality",
    "url": "https://github.com/neonbjb/tortoise-tts",
    "stars": 13351,
    "forks": 1849,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-11T02:24:13Z",
    "topics": [],
    "owner": {
      "username": "neonbjb",
      "profile_url": "https://github.com/neonbjb"
    }
  },
  {
    "name": "kan-bayashi/ParallelWaveGAN",
    "description": "Unofficial Parallel WaveGAN (+ MelGAN & Multi-band MelGAN & HiFi-GAN & StyleMelGAN) with Pytorch",
    "url": "https://github.com/kan-bayashi/ParallelWaveGAN",
    "stars": 1577,
    "forks": 343,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-08T03:18:27Z",
    "topics": [
      "hifigan",
      "melgan",
      "neural-vocoder",
      "parallel-wavenet",
      "pytorch",
      "realtime",
      "speech-synthesis",
      "style-melgan",
      "text-to-speech",
      "tts",
      "vocoder",
      "wavenet"
    ],
    "owner": {
      "username": "kan-bayashi",
      "profile_url": "https://github.com/kan-bayashi"
    }
  },
  {
    "name": "zsl24/Mel-GAN-Voice-Conversion-Demo",
    "description": "A Demo for real-time voice conversion based on Mel-GAN",
    "url": "https://github.com/zsl24/Mel-GAN-Voice-Conversion-Demo",
    "stars": 12,
    "forks": 1,
    "language": "Python",
    "last_updated": "2023-06-05T13:41:03Z",
    "topics": [
      "deep-learning",
      "speech-synthesis",
      "voice-conversion"
    ],
    "owner": {
      "username": "zsl24",
      "profile_url": "https://github.com/zsl24"
    }
  },
  {
    "name": "siddiquelatif/URDU-Dataset",
    "description": "Urdu Language Speech Emotional Corpus  ",
    "url": "https://github.com/siddiquelatif/URDU-Dataset",
    "stars": 44,
    "forks": 11,
    "language": null,
    "last_updated": "2024-10-31T12:02:30Z",
    "topics": [
      "emotion",
      "recognition",
      "speech",
      "urdu"
    ],
    "owner": {
      "username": "siddiquelatif",
      "profile_url": "https://github.com/siddiquelatif"
    }
  },
  {
    "name": "MeidanGR/SpeechEmotionRecognition_Realtime",
    "description": "Speech Emotion Recognition (SER) in real-time, using Deep Neural Networks (DNN) of Long Short Memory Term (LSTM).",
    "url": "https://github.com/MeidanGR/SpeechEmotionRecognition_Realtime",
    "stars": 94,
    "forks": 21,
    "language": "Jupyter Notebook",
    "last_updated": "2024-12-09T19:23:27Z",
    "topics": [
      "algorithm",
      "deep-learning",
      "keras",
      "librosa",
      "lstm",
      "pandas",
      "python"
    ],
    "owner": {
      "username": "MeidanGR",
      "profile_url": "https://github.com/MeidanGR"
    }
  },
  {
    "name": "cnlinxi/tpse_tacotron2",
    "description": "TPSE-GST Tacotron2",
    "url": "https://github.com/cnlinxi/tpse_tacotron2",
    "stars": 14,
    "forks": 5,
    "language": "Python",
    "last_updated": "2024-08-14T02:19:34Z",
    "topics": [],
    "owner": {
      "username": "cnlinxi",
      "profile_url": "https://github.com/cnlinxi"
    }
  },
  {
    "name": "brentspell/hifi-gan-bwe",
    "description": "Unofficial implementation of HiFi-GAN+ from the paper \"Bandwidth Extension is All You Need\" by Su, et al.",
    "url": "https://github.com/brentspell/hifi-gan-bwe",
    "stars": 206,
    "forks": 26,
    "language": "Python",
    "last_updated": "2024-11-13T03:19:07Z",
    "topics": [],
    "owner": {
      "username": "brentspell",
      "profile_url": "https://github.com/brentspell"
    }
  },
  {
    "name": "kahne/SpeechTransProgress",
    "description": "Tracking the progress in end-to-end speech translation",
    "url": "https://github.com/kahne/SpeechTransProgress",
    "stars": 255,
    "forks": 25,
    "language": null,
    "last_updated": "2024-11-25T03:24:19Z",
    "topics": [
      "artificial-intelligence",
      "machine-translation",
      "natural-language-generation",
      "natural-language-processing",
      "speech-processing",
      "speech-translation",
      "spoken-language-processing",
      "spoken-language-translation"
    ],
    "owner": {
      "username": "kahne",
      "profile_url": "https://github.com/kahne"
    }
  },
  {
    "name": "Yoshifumi-Nakano/visual-text-to-speech",
    "description": "visual-text to speech",
    "url": "https://github.com/Yoshifumi-Nakano/visual-text-to-speech",
    "stars": 14,
    "forks": 2,
    "language": "Python",
    "last_updated": "2024-12-04T08:45:24Z",
    "topics": [],
    "owner": {
      "username": "Yoshifumi-Nakano",
      "profile_url": "https://github.com/Yoshifumi-Nakano"
    }
  },
  {
    "name": "Wendison/VQMIVC",
    "description": "Official implementation of VQMIVC: One-shot (any-to-any) Voice Conversion @ Interspeech 2021 + Online playing demo!",
    "url": "https://github.com/Wendison/VQMIVC",
    "stars": 340,
    "forks": 55,
    "language": "Jupyter Notebook",
    "last_updated": "2024-11-11T05:59:52Z",
    "topics": [
      "disentanglement-learning",
      "one-shot",
      "speech",
      "speech-generation",
      "voice-conversion"
    ],
    "owner": {
      "username": "Wendison",
      "profile_url": "https://github.com/Wendison"
    }
  },
  {
    "name": "liusongxiang/ppg-vc",
    "description": "PPG-Based Voice Conversion",
    "url": "https://github.com/liusongxiang/ppg-vc",
    "stars": 329,
    "forks": 72,
    "language": "Python",
    "last_updated": "2024-11-20T02:23:47Z",
    "topics": [
      "conformer",
      "one-shot",
      "phonetic-posteriorgram",
      "ppg",
      "ppg-vc",
      "speech-synthesis",
      "voice-conversion"
    ],
    "owner": {
      "username": "liusongxiang",
      "profile_url": "https://github.com/liusongxiang"
    }
  },
  {
    "name": "liusongxiang/StarGAN-Voice-Conversion",
    "description": "This is a pytorch implementation of the paper: StarGAN-VC: Non-parallel many-to-many voice conversion with star generative adversarial networks  ",
    "url": "https://github.com/liusongxiang/StarGAN-Voice-Conversion",
    "stars": 515,
    "forks": 93,
    "language": "Python",
    "last_updated": "2024-11-19T07:37:23Z",
    "topics": [
      "pytorch-implementation",
      "stargan",
      "voice-conversion"
    ],
    "owner": {
      "username": "liusongxiang",
      "profile_url": "https://github.com/liusongxiang"
    }
  },
  {
    "name": "thuhcsi/IJCAI2019-DRL4SER",
    "description": "The python implementation for paper \"Towards Discriminative Representation Learning for Speech Emotion Recognition\" in IJCAI-2019",
    "url": "https://github.com/thuhcsi/IJCAI2019-DRL4SER",
    "stars": 22,
    "forks": 5,
    "language": "Python",
    "last_updated": "2022-12-09T12:29:25Z",
    "topics": [],
    "owner": {
      "username": "thuhcsi",
      "profile_url": "https://github.com/thuhcsi"
    }
  },
  {
    "name": "thuhcsi/icassp2021-emotion-tts",
    "description": "Please visit: https://thuhcsi.github.io/icassp2021-emotion-tts/",
    "url": "https://github.com/thuhcsi/icassp2021-emotion-tts",
    "stars": 34,
    "forks": 13,
    "language": "Python",
    "last_updated": "2024-11-05T10:05:27Z",
    "topics": [],
    "owner": {
      "username": "thuhcsi",
      "profile_url": "https://github.com/thuhcsi"
    }
  },
  {
    "name": "CorentinJ/Real-Time-Voice-Cloning",
    "description": "Clone a voice in 5 seconds to generate arbitrary speech in real-time",
    "url": "https://github.com/CorentinJ/Real-Time-Voice-Cloning",
    "stars": 52938,
    "forks": 8813,
    "language": "Python",
    "last_updated": "2024-12-11T02:39:50Z",
    "topics": [
      "deep-learning",
      "python",
      "pytorch",
      "tensorflow",
      "tts",
      "voice-cloning"
    ],
    "owner": {
      "username": "CorentinJ",
      "profile_url": "https://github.com/CorentinJ"
    }
  },
  {
    "name": "facebookresearch/speech-resynthesis",
    "description": "An official reimplementation of the method described in the INTERSPEECH 2021 paper - Speech Resynthesis from Discrete Disentangled Self-Supervised Representations.",
    "url": "https://github.com/facebookresearch/speech-resynthesis",
    "stars": 392,
    "forks": 55,
    "language": "Python",
    "last_updated": "2024-11-24T09:00:25Z",
    "topics": [],
    "owner": {
      "username": "facebookresearch",
      "profile_url": "https://github.com/facebookresearch"
    }
  },
  {
    "name": "hs-oh-prml/FastSpeech-GST-Korea",
    "description": null,
    "url": "https://github.com/hs-oh-prml/FastSpeech-GST-Korea",
    "stars": 3,
    "forks": 0,
    "language": "Python",
    "last_updated": "2023-04-01T02:02:24Z",
    "topics": [],
    "owner": {
      "username": "hs-oh-prml",
      "profile_url": "https://github.com/hs-oh-prml"
    }
  },
  {
    "name": "hs-oh-prml/EmotionControllableTextToSpeech",
    "description": null,
    "url": "https://github.com/hs-oh-prml/EmotionControllableTextToSpeech",
    "stars": 21,
    "forks": 4,
    "language": "HTML",
    "last_updated": "2024-11-13T03:07:14Z",
    "topics": [],
    "owner": {
      "username": "hs-oh-prml",
      "profile_url": "https://github.com/hs-oh-prml"
    }
  },
  {
    "name": "KinglittleQ/GST-Tacotron",
    "description": " A PyTorch implementation of Style Tokens: Unsupervised Style Modeling, Control and Transfer in End-to-End Speech Synthesis",
    "url": "https://github.com/KinglittleQ/GST-Tacotron",
    "stars": 364,
    "forks": 71,
    "language": "Python",
    "last_updated": "2024-12-09T08:06:18Z",
    "topics": [
      "gst-tacotron",
      "pytorch",
      "tacotron",
      "tts"
    ],
    "owner": {
      "username": "KinglittleQ",
      "profile_url": "https://github.com/KinglittleQ"
    }
  },
  {
    "name": "rarefin/TTS_VAE",
    "description": "Text to Speech Synthesis based on controllable latent representation",
    "url": "https://github.com/rarefin/TTS_VAE",
    "stars": 14,
    "forks": 3,
    "language": "Python",
    "last_updated": "2022-06-15T05:16:45Z",
    "topics": [],
    "owner": {
      "username": "rarefin",
      "profile_url": "https://github.com/rarefin"
    }
  },
  {
    "name": "AzamRabiee/Emotional-TTS",
    "description": "Korean Emotional End-to-End Neural Speech synthesizer, ML4audio, NIPS2017",
    "url": "https://github.com/AzamRabiee/Emotional-TTS",
    "stars": 72,
    "forks": 13,
    "language": null,
    "last_updated": "2024-11-13T03:03:58Z",
    "topics": [],
    "owner": {
      "username": "AzamRabiee",
      "profile_url": "https://github.com/AzamRabiee"
    }
  },
  {
    "name": "ujscjj/DPTNet",
    "description": null,
    "url": "https://github.com/ujscjj/DPTNet",
    "stars": 106,
    "forks": 24,
    "language": "Python",
    "last_updated": "2024-11-29T03:00:01Z",
    "topics": [],
    "owner": {
      "username": "ujscjj",
      "profile_url": "https://github.com/ujscjj"
    }
  },
  {
    "name": "NVIDIA/mellotron",
    "description": "Mellotron: a multispeaker voice synthesis model based on Tacotron 2 GST that can make a voice emote and sing without emotive or singing training data",
    "url": "https://github.com/NVIDIA/mellotron",
    "stars": 855,
    "forks": 182,
    "language": "Jupyter Notebook",
    "last_updated": "2024-11-15T07:02:23Z",
    "topics": [],
    "owner": {
      "username": "NVIDIA",
      "profile_url": "https://github.com/NVIDIA"
    }
  },
  {
    "name": "espnet/espnet",
    "description": "End-to-End Speech Processing Toolkit",
    "url": "https://github.com/espnet/espnet",
    "stars": 8579,
    "forks": 2195,
    "language": "Python",
    "last_updated": "2024-12-11T03:39:00Z",
    "topics": [
      "chainer",
      "deep-learning",
      "end-to-end",
      "kaldi",
      "machine-translation",
      "pytorch",
      "singing-voice-synthesis",
      "speaker-diarization",
      "speech-enhancement",
      "speech-recognition",
      "speech-separation",
      "speech-synthesis",
      "speech-translation",
      "spoken-language-understanding",
      "text-to-speech",
      "voice-conversion"
    ],
    "owner": {
      "username": "espnet",
      "profile_url": "https://github.com/espnet"
    }
  },
  {
    "name": "ConferencingSpeech/ConferencingSpeech2022",
    "description": "Non-intrusive Objective Speech Quality Assessment (NISQA) Challenge in Online Conferencing Applications",
    "url": "https://github.com/ConferencingSpeech/ConferencingSpeech2022",
    "stars": 43,
    "forks": 7,
    "language": "Python",
    "last_updated": "2024-11-19T04:22:11Z",
    "topics": [],
    "owner": {
      "username": "ConferencingSpeech",
      "profile_url": "https://github.com/ConferencingSpeech"
    }
  },
  {
    "name": "ttslr/MonTTS",
    "description": null,
    "url": "https://github.com/ttslr/MonTTS",
    "stars": 13,
    "forks": 4,
    "language": "Python",
    "last_updated": "2023-06-02T10:55:48Z",
    "topics": [],
    "owner": {
      "username": "ttslr",
      "profile_url": "https://github.com/ttslr"
    }
  },
  {
    "name": "jxzhanggg/nonparaSeq2seqVC_code",
    "description": "Implementation code of non-parallel sequence-to-sequence VC",
    "url": "https://github.com/jxzhanggg/nonparaSeq2seqVC_code",
    "stars": 250,
    "forks": 56,
    "language": "Python",
    "last_updated": "2024-10-24T06:21:52Z",
    "topics": [
      "deep-learning",
      "pytorch-implementation",
      "text-to-speech",
      "voice-conversion"
    ],
    "owner": {
      "username": "jxzhanggg",
      "profile_url": "https://github.com/jxzhanggg"
    }
  },
  {
    "name": "KunZhou9646/Speaker-independent-emotional-voice-conversion-based-on-conditional-VAW-GAN-and-CWT",
    "description": "This is the implementation of our Interspeech 2020 paper \"Converting anyone's emotion: towards speaker-independent emotional voice conversion\".",
    "url": "https://github.com/KunZhou9646/Speaker-independent-emotional-voice-conversion-based-on-conditional-VAW-GAN-and-CWT",
    "stars": 88,
    "forks": 13,
    "language": "Python",
    "last_updated": "2024-11-26T02:26:56Z",
    "topics": [],
    "owner": {
      "username": "KunZhou9646",
      "profile_url": "https://github.com/KunZhou9646"
    }
  },
  {
    "name": "ttslr/StrengthNet",
    "description": "[INTERSPEECH'2022] Accurate Emotion Strength Assessment for Seen and Unseen Speech Based on Data-Driven Deep Learning",
    "url": "https://github.com/ttslr/StrengthNet",
    "stars": 79,
    "forks": 11,
    "language": "Python",
    "last_updated": "2024-09-28T07:17:43Z",
    "topics": [],
    "owner": {
      "username": "ttslr",
      "profile_url": "https://github.com/ttslr"
    }
  },
  {
    "name": "KunZhou9646/Emovox",
    "description": "This is the implementation of the paper \"Emotion Intensity and its Control for Emotional Voice Conversion\".",
    "url": "https://github.com/KunZhou9646/Emovox",
    "stars": 82,
    "forks": 11,
    "language": "Python",
    "last_updated": "2024-11-26T05:18:32Z",
    "topics": [],
    "owner": {
      "username": "KunZhou9646",
      "profile_url": "https://github.com/KunZhou9646"
    }
  },
  {
    "name": "WelkinYang/Learn2Sing2.0",
    "description": "Diffusion and Mutual Information-Based Target Speaker SVS by Learning from Singing Teacher",
    "url": "https://github.com/WelkinYang/Learn2Sing2.0",
    "stars": 177,
    "forks": 26,
    "language": "JavaScript",
    "last_updated": "2024-11-08T13:35:07Z",
    "topics": [
      "singing-voice",
      "singing-voice-synthesis",
      "tts"
    ],
    "owner": {
      "username": "WelkinYang",
      "profile_url": "https://github.com/WelkinYang"
    }
  },
  {
    "name": "ruizhecao96/CMGAN",
    "description": "Conformer-based Metric GAN for speech enhancement",
    "url": "https://github.com/ruizhecao96/CMGAN",
    "stars": 320,
    "forks": 61,
    "language": "Python",
    "last_updated": "2024-12-10T08:56:00Z",
    "topics": [],
    "owner": {
      "username": "ruizhecao96",
      "profile_url": "https://github.com/ruizhecao96"
    }
  },
  {
    "name": "heraclex12/vietpunc",
    "description": "Vietnamese Punctuation Prediction using Pretrained Language Models",
    "url": "https://github.com/heraclex12/vietpunc",
    "stars": 13,
    "forks": 6,
    "language": "Jupyter Notebook",
    "last_updated": "2024-07-30T23:08:41Z",
    "topics": [
      "punctuation-restoration",
      "transformer",
      "vietnamese"
    ],
    "owner": {
      "username": "heraclex12",
      "profile_url": "https://github.com/heraclex12"
    }
  },
  {
    "name": "Takaaki-Saeki/ssl_speech_restoration",
    "description": "SelfRemaster: SSL Speech Restoration",
    "url": "https://github.com/Takaaki-Saeki/ssl_speech_restoration",
    "stars": 87,
    "forks": 8,
    "language": "Python",
    "last_updated": "2024-11-22T17:47:21Z",
    "topics": [
      "pytorch",
      "self-supervised-learning",
      "speech-enhancement",
      "speech-synthesis"
    ],
    "owner": {
      "username": "Takaaki-Saeki",
      "profile_url": "https://github.com/Takaaki-Saeki"
    }
  },
  {
    "name": "yuguochencuc/SF-Net",
    "description": "The implementation of \"Optimizing Shoulder to Shoulder: A Coordinated Sub-Band Fusion Model for Real-Time Full-Band Speech Enhancement\"",
    "url": "https://github.com/yuguochencuc/SF-Net",
    "stars": 51,
    "forks": 9,
    "language": "Python",
    "last_updated": "2024-09-30T14:18:40Z",
    "topics": [],
    "owner": {
      "username": "yuguochencuc",
      "profile_url": "https://github.com/yuguochencuc"
    }
  },
  {
    "name": "sangyun884/Diffusion-Models-Seminar",
    "description": null,
    "url": "https://github.com/sangyun884/Diffusion-Models-Seminar",
    "stars": 127,
    "forks": 6,
    "language": null,
    "last_updated": "2024-10-14T23:20:22Z",
    "topics": [
      "diffusion-models",
      "generative-model",
      "score-based-generative-modeling",
      "score-based-generative-models",
      "score-based-models"
    ],
    "owner": {
      "username": "sangyun884",
      "profile_url": "https://github.com/sangyun884"
    }
  },
  {
    "name": "tencent-ailab/bddm",
    "description": "BDDM: Bilateral Denoising Diffusion Models for Fast and High-Quality Speech Synthesis",
    "url": "https://github.com/tencent-ailab/bddm",
    "stars": 224,
    "forks": 30,
    "language": "Python",
    "last_updated": "2024-12-07T07:39:16Z",
    "topics": [],
    "owner": {
      "username": "tencent-ailab",
      "profile_url": "https://github.com/tencent-ailab"
    }
  },
  {
    "name": "rishikksh20/HiFiplusplus-pytorch",
    "description": "HiFi++: a Unified Framework for Neural Vocoding, Bandwidth Extension and Speech Enhancement",
    "url": "https://github.com/rishikksh20/HiFiplusplus-pytorch",
    "stars": 154,
    "forks": 19,
    "language": "Python",
    "last_updated": "2024-11-28T21:54:06Z",
    "topics": [],
    "owner": {
      "username": "rishikksh20",
      "profile_url": "https://github.com/rishikksh20"
    }
  },
  {
    "name": "MoonInTheRiver/NeuralSVB",
    "description": "Learning the Beauty in Songs: Neural Singing Voice Beautifier; ACL 2022 (Main conference); Official code",
    "url": "https://github.com/MoonInTheRiver/NeuralSVB",
    "stars": 426,
    "forks": 51,
    "language": "Python",
    "last_updated": "2024-12-02T08:36:13Z",
    "topics": [
      "acl2022",
      "gan",
      "singing-synthesis",
      "singing-voice",
      "singing-voice-conversion",
      "singing-voice-synthesis"
    ],
    "owner": {
      "username": "MoonInTheRiver",
      "profile_url": "https://github.com/MoonInTheRiver"
    }
  },
  {
    "name": "NTT123/vietTTS",
    "description": "Vietnamese Text to Speech library",
    "url": "https://github.com/NTT123/vietTTS",
    "stars": 202,
    "forks": 91,
    "language": "Python",
    "last_updated": "2024-12-07T14:48:58Z",
    "topics": [
      "deep-learning",
      "hifi-gan",
      "tacotron",
      "text-to-speech",
      "tts-engines",
      "vietnam",
      "vietnamese",
      "vocoder"
    ],
    "owner": {
      "username": "NTT123",
      "profile_url": "https://github.com/NTT123"
    }
  }
]
```
