import React from 'react';

function VideoCard({ video }) {
  return (
    <div>
      {/* Placeholder for video details */}
      <p>{video ? video.caption : "Loading video..."}</p>
    </div>
  );
}

export default VideoCard;
