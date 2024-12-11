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