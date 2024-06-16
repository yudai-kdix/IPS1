// import React, { useState, useEffect } from "react";
// import axios from "axios";
// import React from "react";


// function VideoList() {
//   const [files, setFiles] = useState([]);

//   useEffect(() => {
//     axios
//       .get("http://127.0.0.1:5000/api/videos")
//       .then((response) => {
//         setFiles(response.data);
//       })
//       .catch((error) => console.error("Error fetching files:", error));
//   }, []);

//   return (
//     <div>
//       <h1>動画ファイルリスト</h1>
//       <ul style={{ textAlign: "left" }}>
//         {files.map((file) => (
//           <li key={file}>
//             <a href={`play/${file}`}>{file}</a>
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// }

// export default VideoList;

import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  CardActionArea,
} from "@mui/material";

function VideoList() {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/api/videos")
      .then((response) => {
        setVideos(response.data);
      })
      .catch((error) => {
        console.error("Error fetching videos:", error);
      });
  }, []);

  return (
    <div>
      <Typography
        variant="h4"
        gutterBottom
        component="div"
        style={{ margin: 20 }}
      >
        動画ファイルリスト
      </Typography>
      <Grid container spacing={2} style={{ padding: 20 }}>
        {videos.map((video, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <CardActionArea href={`play/${video}`}>
              <Card sx={{ maxWidth: 345, minHeight: 200 }}>
                <CardMedia
                  component="img"
                  height="140"
                  image={`http://127.0.0.1:5000/thumbnail/${video}`}
                  alt="動画サムネイル"
                />
                <CardContent>
                  <Typography gutterBottom variant="h5" component="div">
                    {video}
                  </Typography>
                </CardContent>
              </Card>
            </CardActionArea>
          </Grid>
        ))}
      </Grid>
    </div>
  );
}

export default VideoList;