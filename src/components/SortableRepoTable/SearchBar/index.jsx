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