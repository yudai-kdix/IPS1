import axios from "axios";
import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  Box,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
} from "@mui/material";

function VideoFrames() {
  const [image, setImage] = useState([]);
  const [loading, setLoading] = useState(true);
  let { id } = useParams();

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:5000/get_frames/${id}`)
      .then((response) => {
        setImage(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching images:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <Box sx={{ p: 2 }}>
        <video id="videoPlayer" style={{ width: "70%" }} controls>
          <source
            src={"http://127.0.0.1:5000/play_video/" + id}
            type="video/mp4"
          />
          Your browser does not support the video tag.
        </video>
        <Typography variant="body1">Loading...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 2 }}>
      <video id="videoPlayer" style={{ width: "70%" }} controls>
        <source
          src={"http://127.0.0.1:5000/uploads/" + id}
          type="video/mp4"
        />
        Your browser does not support the video tag.
      </video>
      <Grid container spacing={2}>
        {imageUrls.map((url, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card sx={{ maxWidth: 345, boxShadow: 3 }}>
              <CardMedia
                component="img"
                height="140"
                image={`http://127.0.0.1:5000${url}`}
                alt={`Frame ${index}`}
              />
              <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                  Frame {index + 1}
                </Typography>
              </CardContent>
              <Link
                href={`/person_name_input/frame_0${index}.jpg`}
                variant="body2"
                color="text.primary"
              >
                View Details
              </Link>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default VideoFrames;
