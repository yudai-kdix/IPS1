import React, { useState } from "react";
import { Button, Container, TextField, Typography, Box } from "@mui/material";
import { API_URL } from "../config/development";
import apiClient from "../api/apiClient";

function VideoUpload() {
  const [videoName, setVideoName] = useState("");
  const [videoFile, setVideoFile] = useState(null);

  const handleVideoChange = (event) => {
    setVideoFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!videoFile) {
      alert("Please select a video file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("video", videoFile, videoFile.name);
    formData.append("name", videoName);

    try {
      const response = await apiClient.post(
        API_URL+"/upload_video",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log(response.data);
      alert("Video uploaded successfully");
    } catch (error) {
      console.error("Failed to upload video:", error);
      alert("Failed to upload video.");
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Typography component="h1" variant="h5" gutterBottom>
        Upload Video
      </Typography>
      <TextField
        variant="outlined"
        margin="normal"
        fullWidth
        label="Video Name"
        value={videoName}
        onChange={(e) => setVideoName(e.target.value)}
        autoFocus
      />
      <Box sx={{ marginTop: 2 }}>
        <input
          accept="video/*"
          style={{ display: "none" }}
          id="raised-button-file"
          type="file"
          onChange={handleVideoChange}
        />
        <label htmlFor="raised-button-file">
          <Button variant="outlined" component="span" sx={{ marginRight: 2 }}>
            Choose Video
          </Button>
        </label>
        <Button
          variant="contained"
          color="primary"
          onClick={handleUpload}
          sx={{ marginTop: 2 }}
        >
          Upload
        </Button>
      </Box>
    </Container>
  );
}

export default VideoUpload;
