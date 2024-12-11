import React, { useState, useMemo } from 'react';
import { ArrowUpDown, ArrowUp, ArrowDown, Search, Star, Code, Calendar, RefreshCw } from 'lucide-react';

const SortableRepoTable = ({ initialData }) => {
  const [data, setData] = useState(initialData);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({
    key: 'stars',
    direction: 'desc'
  });

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const sortData = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const filteredAndSortedData = useMemo(() => {
    let filtered = data;
    
    if (searchTerm) {
      filtered = data.filter(repo => 
        repo.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (repo.description && repo.description.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (repo.language && repo.language.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    return [...filtered].sort((a, b) => {
      const { key, direction } = sortConfig;
      
      if (key === 'created_at' || key === 'last_updated') {
        return direction === 'asc' 
          ? new Date(a[key]) - new Date(b[key])
          : new Date(b[key]) - new Date(a[key]);
      }
      
      if (typeof a[key] === 'number') {
        return direction === 'asc' ? a[key] - b[key] : b[key] - a[key];
      }
      
      const aValue = (a[key] || '').toString().toLowerCase();
      const bValue = (b[key] || '').toString().toLowerCase();
      return direction === 'asc'
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue);
    });
  }, [data, searchTerm, sortConfig]);

  const getSortIcon = (key) => {
    if (sortConfig.key !== key) {
      return <ArrowUpDown className="h-4 w-4" />;
    }
    return sortConfig.direction === 'asc' 
      ? <ArrowUp className="h-4 w-4" />
      : <ArrowDown className="h-4 w-4" />;
  };

  const getLanguageColor = (language) => {
    const colors = {
      'JavaScript': 'bg-yellow-200 text-yellow-800',
      'Python': 'bg-blue-200 text-blue-800',
      'Java': 'bg-red-200 text-red-800',
      'TypeScript': 'bg-blue-300 text-blue-900',
      'Ruby': 'bg-red-300 text-red-900',
      'Go': 'bg-cyan-200 text-cyan-800',
      'Rust': 'bg-orange-200 text-orange-800',
      'C++': 'bg-purple-200 text-purple-800',
      'PHP': 'bg-indigo-200 text-indigo-800',
      'Shell': 'bg-gray-200 text-gray-800',
    };
    return colors[language] || 'bg-gray-200 text-gray-800';
  };

  return (
    <div className="w-full bg-white rounded-xl shadow-lg">
      {/* Header */}
      <div className="p-6 border-b">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <h2 className="text-2xl font-bold text-gray-900">Featured Repositories</h2>
          <div className="relative w-full md:w-96">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search repositories..."
              className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-6 border-b">
        <div className="bg-blue-50 p-4 rounded-lg">
          <div className="flex items-center gap-2">
            <Star className="h-5 w-5 text-blue-500" />
            <h3 className="text-sm font-medium text-blue-600">Total Stars</h3>
          </div>
          <p className="text-2xl font-bold text-blue-900 mt-2">
            {data.reduce((acc, repo) => acc + repo.stars, 0).toLocaleString()}
          </p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <div className="flex items-center gap-2">
            <Code className="h-5 w-5 text-green-500" />
            <h3 className="text-sm font-medium text-green-600">Languages</h3>
          </div>
          <p className="text-2xl font-bold text-green-900 mt-2">
            {new Set(data.map(repo => repo.language).filter(Boolean)).size}
          </p>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <div className="flex items-center gap-2">
            <RefreshCw className="h-5 w-5 text-purple-500" />
            <h3 className="text-sm font-medium text-purple-600">Last Updated</h3>
          </div>
          <p className="text-2xl font-bold text-purple-900 mt-2">
            {formatDate(Math.max(...data.map(repo => new Date(repo.last_updated))))}
          </p>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-50">
              <th 
                className="p-4 text-left cursor-pointer hover:bg-gray-100 transition-colors"
                onClick={() => sortData('name')}
              >
                <div className="flex items-center gap-2">
                  Repository {getSortIcon('name')}
                </div>
              </th>
              <th 
                className="p-4 text-left cursor-pointer hover:bg-gray-100 transition-colors"
                onClick={() => sortData('description')}
              >
                <div className="flex items-center gap-2">
                  Description {getSortIcon('description')}
                </div>
              </th>
              <th 
                className="p-4 text-right cursor-pointer hover:bg-gray-100 transition-colors"
                onClick={() => sortData('stars')}
              >
                <div className="flex items-center justify-end gap-2">
                  Stars {getSortIcon('stars')}
                </div>
              </th>
              <th 
                className="p-4 text-left cursor-pointer hover:bg-gray-100 transition-colors"
                onClick={() => sortData('language')}
              >
                <div className="flex items-center gap-2">
                  Language {getSortIcon('language')}
                </div>
              </th>
              <th 
                className="p-4 text-left cursor-pointer hover:bg-gray-100 transition-colors"
                onClick={() => sortData('created_at')}
              >
                <div className="flex items-center gap-2">
                  Created {getSortIcon('created_at')}
                </div>
              </th>
              <th 
                className="p-4 text-left cursor-pointer hover:bg-gray-100 transition-colors"
                onClick={() => sortData('last_updated')}
              >
                <div className="flex items-center gap-2">
                  Last Updated {getSortIcon('last_updated')}
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            {filteredAndSortedData.map((repo, index) => (
              <tr key={index} className="border-t hover:bg-gray-50 transition-colors">
                <td className="p-4">
                  <a 
                    href={repo.url}
                    className="text-blue-600 hover:text-blue-800 font-medium hover:underline"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {repo.name}
                  </a>
                </td>
                <td className="p-4 text-gray-600">{repo.description || 'No description'}</td>
                <td className="p-4 text-right font-medium">{repo.stars.toLocaleString()}</td>
                <td className="p-4">
                  {repo.language && (
                    <span className={`px-2 py-1 rounded-full text-sm font-medium ${getLanguageColor(repo.language)}`}>
                      {repo.language}
                    </span>
                  )}
                </td>
                <td className="p-4 text-gray-600">{formatDate(repo.created_at)}</td>
                <td className="p-4 text-gray-600">{formatDate(repo.last_updated)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {/* No results message */}
        {filteredAndSortedData.length === 0 && (
          <div className="p-8 text-center text-gray-500">
            No repositories found matching your search criteria.
          </div>
        )}
      </div>
      
      {/* Footer */}
      <div className="p-4 border-t text-sm text-gray-500 text-center">
        Showing {filteredAndSortedData.length} of {data.length} repositories
      </div>
    </div>
  );
};

export default SortableRepoTable;
