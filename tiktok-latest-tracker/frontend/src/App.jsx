import React, { useState } from 'react';
import SearchBar from './components/SearchBar'; // Assuming SearchBar.jsx is in components
// We will create VideoCard later, for now, just a placeholder for results
// import VideoCard from './components/VideoCard';
import './App.css'; // Optional: if you want to add styles

function App() {
  const [videos, setVideos] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (searchQuery) => {
    setIsLoading(true);
    setError(null);
    setVideos([]); // Clear previous results

    try {
      // The backend runs on port 8000 (as configured in devcontainer.json)
      // Vite's dev server (default 5173) can proxy requests, or we can use full URL.
      // For simplicity in Codespaces, using full URL is often easier initially.
      const response = await fetch(`/api/search?q=${encodeURIComponent(searchQuery)}`);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setVideos(data.results || []); // Assuming backend returns { query: "...", results: [...] }
      if (!data.results || data.results.length === 0) {
        console.log("No results found from backend for query:", searchQuery);
      }

    } catch (err) {
      console.error("Failed to fetch videos:", err);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>TikTok Latest Tracker</h1>
        <SearchBar onSearch={handleSearch} />
      </header>
      <main>
        {isLoading && <p>Loading...</p>}
        {error && <p style={{ color: 'red' }}>Error: {error}</p>}
        <div>
          {videos.length > 0 ? (
            videos.map((video, index) => (
              // Replace with VideoCard component later
              <div key={video.id || index} style={{ border: '1px solid #ccc', margin: '10px', padding: '10px' }}>
                <p><strong>Caption:</strong> {video.caption || 'N/A'}</p>
                <p><strong>URL:</strong> {video.url ? <a href={video.url} target="_blank" rel="noopener noreferrer">{video.url}</a> : 'N/A'}</p>
                <p><em><small>Source: {video.source || 'Unknown'}</small></em></p>
                {video.error && <p style={{color: 'orange'}}>Processing error: {video.error}</p>}
              </div>
            ))
          ) : (
            !isLoading && <p>No videos found. Try a new search.</p>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
