import React, { useState, useEffect } from "react";
import axios from "axios";

function VideoPlayer({ filename }) {
  const [videoUrl, setVideoUrl] = useState("");

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:5000/play/${filename}`)
      .then((response) => {
        setVideoUrl(response.data.video_url);
      })
      .catch((error) => {
        console.error("Error fetching video:", error);
      });
  }, [filename]);

  return (
    <div>
      <h1>Video Player</h1>
      <video controls src={videoUrl}>
        Your browser does not support the video tag.
      </video>
    </div>
  );
}

export default VideoPlayer;
