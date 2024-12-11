// src/components/Analytics/index.jsx
import React, { useMemo, useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, CartesianGrid, LineChart, Line, ResponsiveContainer } from 'recharts';
import { Star, GitFork, Code, Hash, Calendar, Users, Activity, TrendingUp } from 'lucide-react';

// Card component wrapper for consistent styling
const Card = ({ children, className = '' }) => (
  <div className={`bg-white rounded-lg shadow p-6 ${className}`}>
    {children}
  </div>
);

const CardHeader = ({ children }) => (
  <div className="mb-4">{children}</div>
);

const CardTitle = ({ children }) => (
  <h3 className="text-lg font-semibold text-gray-900">{children}</h3>
);

const CardContent = ({ children, className = '' }) => (
  <div className={className}>{children}</div>
);

const Analytics = ({ data }) => {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Stats calculations
  const stats = useMemo(() => {
    const now = new Date();
    const oneMonthAgo = new Date(now.setMonth(now.getMonth() - 1));
    
    const recentActivity = data.filter(repo => 
      new Date(repo.last_updated) >= oneMonthAgo
    ).length;

    const avgStarsPerRepo = data.length > 0 
      ? (data.reduce((sum, repo) => sum + repo.stars, 0) / data.length).toFixed(1)
      : 0;

    return {
      totalRepos: data.length,
      totalStars: data.reduce((sum, repo) => sum + repo.stars, 0),
      totalForks: data.reduce((sum, repo) => sum + repo.forks, 0),
      totalTopics: data.reduce((sum, repo) => sum + repo.topics.length, 0),
      activeRepos: recentActivity,
      avgStarsPerRepo: avgStarsPerRepo
    };
  }, [data]);

  // Language stats calculation
  const languageStats = useMemo(() => {
    const langStats = data.reduce((acc, repo) => {
      if (repo.language) {
        if (!acc[repo.language]) {
          acc[repo.language] = { count: 0, stars: 0, repos: [] };
        }
        acc[repo.language].count += 1;
        acc[repo.language].stars += repo.stars;
        acc[repo.language].repos.push(repo.name);
      }
      return acc;
    }, {});
    
    return Object.entries(langStats)
      .map(([name, { count, stars }]) => ({
        name,
        count,
        stars,
        percentage: (count / data.length * 100).toFixed(1),
        starsPerRepo: (stars / count).toFixed(1)
      }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10);
  }, [data]);

  // Top repositories calculation
  const topRepos = useMemo(() => {
    return [...data]
      .sort((a, b) => b.stars - a.stars)
      .slice(0, 10)
      .map(repo => ({
        name: repo.name.split('/')[1],
        fullName: repo.name,
        stars: repo.stars,
        forks: repo.forks,
        language: repo.language || 'Not specified',
        engagement: ((repo.forks / repo.stars) * 100).toFixed(1),
        topics: repo.topics.length
      }));
  }, [data]);

  // Topics analysis
  const topicsAnalysis = useMemo(() => {
    const topicStats = data.reduce((acc, repo) => {
      repo.topics?.forEach(topic => {
        if (!acc[topic]) {
          acc[topic] = { count: 0, stars: 0, repos: [] };
        }
        acc[topic].count += 1;
        acc[topic].stars += repo.stars;
        acc[topic].repos.push(repo.name);
      });
      return acc;
    }, {});

    return Object.entries(topicStats)
      .map(([name, { count, stars, repos }]) => ({
        name,
        count,
        stars,
        popularity: (stars / count).toFixed(1),
        repoCount: repos.length
      }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 15);
  }, [data]);

  // Activity timeline
  const activityTimeline = useMemo(() => {
    const timeline = data.reduce((acc, repo) => {
      const date = new Date(repo.last_updated);
      const month = date.toLocaleString('default', { month: 'short', year: '2-digit' });
      
      if (!acc[month]) {
        acc[month] = { month, updates: 0, newStars: 0 };
      }
      acc[month].updates += 1;
      return acc;
    }, {});

    return Object.values(timeline)
      .sort((a, b) => new Date(a.month) - new Date(b.month))
      .slice(-6);
  }, [data]);

  const COLORS = [
    '#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8',
    '#82ca9d', '#ffc658', '#8dd1e1', '#a4de6c', '#d0ed57'
  ];

  const formatNumber = (num) => {
    if (num >= 1000000) return `${(num/1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num/1000).toFixed(1)}k`;
    return num.toString();
  };

  if (!isMounted) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <div className="flex items-center space-x-4">
            <Code className="h-6 w-6 text-blue-500" />
            <div>
              <p className="text-sm font-medium text-gray-500">Total Repos</p>
              <h3 className="text-2xl font-bold">{formatNumber(stats.totalRepos)}</h3>
            </div>
          </div>
        </Card>
        
        <Card>
          <div className="flex items-center space-x-4">
            <Star className="h-6 w-6 text-yellow-500" />
            <div>
              <p className="text-sm font-medium text-gray-500">Total Stars</p>
              <h3 className="text-2xl font-bold">{formatNumber(stats.totalStars)}</h3>
              <p className="text-sm text-gray-400">~{stats.avgStarsPerRepo} per repo</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center space-x-4">
            <Activity className="h-6 w-6 text-green-500" />
            <div>
              <p className="text-sm font-medium text-gray-500">Active Repos</p>
              <h3 className="text-2xl font-bold">{stats.activeRepos}</h3>
              <p className="text-sm text-gray-400">Last 30 days</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center space-x-4">
            <Hash className="h-6 w-6 text-purple-500" />
            <div>
              <p className="text-sm font-medium text-gray-500">Topics</p>
              <h3 className="text-2xl font-bold">{formatNumber(stats.totalTopics)}</h3>
              <p className="text-sm text-gray-400">Across all repos</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Repositories */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Top Repositories by Stars</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-96 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={topRepos} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={60} />
                  <YAxis />
                  <Tooltip 
                    content={({ payload, label }) => {
                      if (!payload?.length) return null;
                      const data = payload[0].payload;
                      return (
                        <div className="bg-white p-4 rounded-lg shadow-lg border">
                          <p className="font-bold">{data.fullName}</p>
                          <p className="text-sm text-gray-600">Language: {data.language}</p>
                          <p className="text-sm text-gray-600">Stars: {formatNumber(data.stars)}</p>
                          <p className="text-sm text-gray-600">Forks: {formatNumber(data.forks)}</p>
                          <p className="text-sm text-gray-600">Topics: {data.topics}</p>
                        </div>
                      );
                    }}
                  />
                  <Bar dataKey="stars" fill="#8884d8" name="Stars" />
                  <Bar dataKey="forks" fill="#82ca9d" name="Forks" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Language Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Language Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={languageStats}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    dataKey="count"
                    label={({ name, percentage }) => `${name} (${percentage}%)`}
                  >
                    {languageStats.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    content={({ payload }) => {
                      if (!payload?.length) return null;
                      const data = payload[0].payload;
                      return (
                        <div className="bg-white p-4 rounded-lg shadow-lg border">
                          <p className="font-bold">{data.name}</p>
                          <p className="text-sm text-gray-600">Repos: {data.count}</p>
                          <p className="text-sm text-gray-600">Total Stars: {formatNumber(data.stars)}</p>
                          <p className="text-sm text-gray-600">Stars/Repo: {data.starsPerRepo}</p>
                        </div>
                      );
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Activity Timeline */}
        <Card>
          <CardHeader>
            <CardTitle>Activity Timeline</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart 
                  data={activityTimeline}
                  margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip
                    content={({ payload, label }) => {
                      if (!payload?.length) return null;
                      const data = payload[0].payload;
                      return (
                        <div className="bg-white p-4 rounded-lg shadow-lg border">
                          <p className="font-bold">{data.month}</p>
                          <p className="text-sm text-gray-600">Updates: {data.updates}</p>
                        </div>
                      );
                    }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="updates" 
                    stroke="#8884d8" 
                    strokeWidth={2}
                    dot={{ r: 4 }}
                    activeDot={{ r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Topics Analysis */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Popular Topics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart 
                  data={topicsAnalysis}
                  margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={60} />
                  <YAxis />
                  <Tooltip
                    content={({ payload }) => {
                      if (!payload?.length) return null;
                      const data = payload[0].payload;
                      return (
                        <div className="bg-white p-4 rounded-lg shadow-lg border">
                          <p className="font-bold">{data.name}</p>
                          <p className="text-sm text-gray-600">Repositories: {data.repoCount}</p>
                          <p className="text-sm text-gray-600">Total Stars: {formatNumber(data.stars)}</p>
                          <p className="text-sm text-gray-600">Avg Stars: {data.popularity}</p>
                        </div>
                      );
                    }}
                  />
                  <Bar dataKey="count" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Analytics;