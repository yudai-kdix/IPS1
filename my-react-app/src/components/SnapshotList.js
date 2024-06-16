import axios from "axios";
import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

function VideoFrames() {
  const [imageUrls, setImageUrls] = useState([]);
  const [loading, setLoading] = useState(true);
  let { filename } = useParams();
  useEffect(() => {

    axios
      .get(`http://127.0.0.1:5000/play/${filename}`)
      .then((response) => {
        setImageUrls(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching images:", error);
        setLoading(false);
      });
  }, []);
  if (loading)
    return (
      <div>
        <h1>Processed Video Frames</h1>
        <video id="videoPlayer" style={{width: '50%' }} controls >
          <source
            src={"http://127.0.0.1:5000/uploads/" + filename}
            type="video/mp4"
          />
          Your browser does not support the video tag.
        </video>
        <p>Loading...</p>
      </div>
    );

  return (
    <div>
      <h1>Processed Video Frames</h1>
      <video id="videoPlayer" style={{ width: "50%" }} controls>
        <source
          src={"http://127.0.0.1:5000/uploads/" + filename}
          type="video/mp4"
        />
        Your browser does not support the video tag.
      </video>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "space-around",
        }}
      >
        {imageUrls.map((url, index) => (
          <Link
            to={`/person_name_input/frame_0${index}.jpg`}
            key={index}
            style={{ width: "30%", margin: "10px" }}
          >
            {" "}
            {/* リンク先を指定 */}
            <img
              key={index}
              src={"http://127.0.0.1:5000" + url}
              alt={`Frame ${index}`}
              style={{ width: "100%", margin: "10px" }}
            />
          </Link>
        ))}
      </div>
    </div>
  );
}

export default VideoFrames;
