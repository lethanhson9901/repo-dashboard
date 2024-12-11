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