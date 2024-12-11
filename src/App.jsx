import React from 'react'
import SortableRepoTable from './components/SortableRepoTable'
import reposData from './data/repos.json'

function App() {
  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <SortableRepoTable initialData={reposData} />
      </div>
    </div>
  )
}

export default App
