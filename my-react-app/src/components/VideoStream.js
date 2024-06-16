import React from "react";

function VideoStream({ filename }) {
  const streamUrl = `http://127.0.0.1:5000/video_feed/${filename}`;

  return (
    <div>
      <h1>Live Video Stream</h1>
      <img src={streamUrl} alt="Video Stream" />
    </div>
  );
}

export default VideoStream;
