// src/components/Reddit/index.jsx

import React, { useState, useEffect, useMemo } from 'react';
import { Search, ChevronDown, ChevronUp, MessageCircle, ThumbsUp, Calendar, Link as LinkIcon, User } from 'lucide-react';

const Reddit = () => {
  const [posts, setPosts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedPost, setExpandedPost] = useState(null);
  const [showType, setShowType] = useState('saved'); // 'saved' or 'upvoted'
  const [sortBy, setSortBy] = useState('date'); // 'date', 'score', 'comments'
  const [metadata, setMetadata] = useState(null);

  useEffect(() => {
    // In a real app, you might want to handle loading and error states
    const fetchData = async () => {
      try {
        const data = await import('../../data/reddit/reddit_content.json');
        setPosts(data[showType] || []);
        setMetadata(data.metadata);
      } catch (error) {
        console.error('Error loading Reddit data:', error);
      }
    };
    fetchData();
  }, [showType]);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const formatScore = (score) => {
    if (score >= 1000) {
      return `${(score / 1000).toFixed(1)}k`;
    }
    return score.toString();
  };

  // Search and sort functionality
  const filteredPosts = useMemo(() => {
    let filtered = [...posts];

    // Apply search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(post => 
        post.title.toLowerCase().includes(term) ||
        post.text?.toLowerCase().includes(term) ||
        post.author.toLowerCase().includes(term) ||
        post.subreddit.toLowerCase().includes(term)
      );
    }

    // Apply sorting
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return new Date(b.created_utc) - new Date(a.created_utc);
        case 'score':
          return b.score - a.score;
        case 'comments':
          return (b.comments?.length || 0) - (a.comments?.length || 0);
        default:
          return 0;
      }
    });

    return filtered;
  }, [posts, searchTerm, sortBy]);

  const renderComments = (comments) => {
    if (!comments || comments.length === 0) return null;

    return (
      <div className="ml-4 space-y-3 border-l-2 border-gray-200 pl-4">
        {comments.map(comment => (
          <div key={comment.id} className="text-sm">
            <div className="flex items-center space-x-2 text-xs text-gray-500">
              <User className="w-4 h-4" />
              <span>{comment.author}</span>
              {comment.is_submitter && (
                <span className="bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full text-xs">OP</span>
              )}
              <span>•</span>
              <span>{formatScore(comment.score)} points</span>
            </div>
            <p className="mt-1 text-gray-700">{comment.text}</p>
            {comment.replies && comment.replies.length > 0 && (
              renderComments(comment.replies)
            )}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z" />
              </svg>
            </div>
            <h1 className="text-2xl font-bold text-gray-900">Reddit Content</h1>
          </div>

          {metadata && (
            <div className="text-sm text-gray-500">
              Last updated: {formatDate(metadata.last_updated)}
            </div>
          )}
        </div>

        {/* Controls */}
        <div className="mb-6 space-y-4">
          {/* Search and type selector */}
          <div className="flex space-x-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search posts..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              />
            </div>
            <select
              value={showType}
              onChange={(e) => setShowType(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            >
              <option value="saved">Saved ({metadata?.total_saved || 0})</option>
              <option value="upvoted">Upvoted ({metadata?.total_upvoted || 0})</option>
            </select>
          </div>

          {/* Sort controls */}
          <div className="flex space-x-4">
            <button
              onClick={() => setSortBy('date')}
              className={`px-4 py-2 rounded-md ${
                sortBy === 'date' ? 'bg-orange-100 text-orange-700' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Calendar className="w-4 h-4 inline-block mr-2" />
              Date
            </button>
            <button
              onClick={() => setSortBy('score')}
              className={`px-4 py-2 rounded-md ${
                sortBy === 'score' ? 'bg-orange-100 text-orange-700' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <ThumbsUp className="w-4 h-4 inline-block mr-2" />
              Score
            </button>
            <button
              onClick={() => setSortBy('comments')}
              className={`px-4 py-2 rounded-md ${
                sortBy === 'comments' ? 'bg-orange-100 text-orange-700' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <MessageCircle className="w-4 h-4 inline-block mr-2" />
              Comments
            </button>
          </div>
        </div>

        {/* Posts */}
        <div className="space-y-4">
          {filteredPosts.map((post) => (
            <div 
              key={post.id}
              className="border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors"
            >
              <div className="flex justify-between items-start mb-2">
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-500">r/{post.subreddit}</span>
                  <span className="text-xs text-gray-400">• by {post.author}</span>
                </div>
                <span className="text-xs text-gray-400">{formatDate(post.created_utc)}</span>
              </div>

              <h2 className="text-lg font-semibold text-gray-900 mb-2">
                <a 
                  href={post.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-blue-600 flex items-center"
                >
                  {post.title}
                  <LinkIcon className="w-4 h-4 ml-2 inline-block text-gray-400" />
                </a>
              </h2>

              {post.text && (
                <p className={`text-gray-600 mb-3 ${
                  expandedPost === post.id ? '' : 'line-clamp-3'
                }`}>
                  {post.text}
                </p>
              )}

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4 text-sm text-gray-500">
                  <span className="flex items-center space-x-1">
                    <ThumbsUp className="w-4 h-4" />
                    <span>{formatScore(post.score)}</span>
                  </span>
                  <span className="flex items-center space-x-1">
                    <MessageCircle className="w-4 h-4" />
                    <span>{post.comments?.length || 0}</span>
                  </span>
                </div>

                {(post.text?.length > 100 || post.comments?.length > 0) && (
                  <button
                    onClick={() => setExpandedPost(expandedPost === post.id ? null : post.id)}
                    className="text-sm text-orange-500 hover:text-orange-600 flex items-center space-x-1"
                  >
                    <span>{expandedPost === post.id ? 'Show less' : 'Show more'}</span>
                    {expandedPost === post.id ? (
                      <ChevronUp className="w-4 h-4" />
                    ) : (
                      <ChevronDown className="w-4 h-4" />
                    )}
                  </button>
                )}
              </div>

              {/* Expanded content */}
              {expandedPost === post.id && post.comments && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <h3 className="text-lg font-semibold mb-4">Comments</h3>
                  {renderComments(post.comments)}
                </div>
              )}
            </div>
          ))}
        </div>

        {filteredPosts.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            No posts found matching your search.
          </div>
        )}
      </div>
    </div>
  );
};

export default Reddit;