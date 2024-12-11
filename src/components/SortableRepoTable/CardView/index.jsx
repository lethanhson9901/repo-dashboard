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