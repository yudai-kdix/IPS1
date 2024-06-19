import {
  Box,
  Card,
  CardContent,
  CardMedia,
  Grid,
  Typography,
} from "@mui/material";
import axios from "axios";
import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

function VideoFrames() {
  const [frames, setFrames] = useState([]);
  const [loading, setLoading] = useState(true);
  let { id } = useParams();

  // useEffect(() => {
  //   axios
  //     .get(`http://127.0.0.1:5000/get_frames/${id}`)
  //     .then((response) => {
  //       setImage(response.data);
  //       setLoading(false);
  //     })
  //     .catch((error) => {
  //       console.error("Error fetching images:", error);
  //       setLoading(false);
  //     });
  // }, []);
  useEffect(() => {
    const fetchFrames = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/get_frames/${id}`
        );
        setLoading(false);
        console.log(response.data);
        setFrames(response.data);
      } catch (error) {
        console.error("Error fetching video frames:", error);
        setLoading(false);
      }
    };
    fetchFrames();
  }, [id]);
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
          src={"http://127.0.0.1:5000/play_video/" + id}
          type="video/mp4"
        />
        Your browser does not support the video tag.
      </video>
      <Grid container spacing={2}>
        {frames.map((frame, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Accordion>
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls={`panel${index}a-content`}
                id={`panel${index}a-header`}
              >
                <Typography>フレーム {index + 1}</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <CardMedia
                  component="img"
                  height="140"
                  src={`data:image/jpeg;base64,${frame}`}
                  alt={`フレーム ${index}`}
                />
              </AccordionDetails>
            </Accordion>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default VideoFrames;
