// import React, { useState, useRef } from "react";
// import ReactPlayer from "react-player";
// import { Paper, IconButton, Slider, Typography } from "@mui/material";
// import { PlayArrow, Pause} from "@mui/icons-material";

// function VideoPlayer({ id }) {
//   const [playing, setPlaying] = useState(false);
//   const [volume, setVolume] = useState(0.8);
//   const [played, setPlayed] = useState(0);
//   const playerRef = useRef(null);

//   const handlePlayPause = () => {
//     setPlaying(!playing);
//   };

//   const handleVolumeChange = (event, newValue) => {
//     setVolume(parseFloat(newValue));
//   };

//   const handleProgress = (state) => {
//     setPlayed(state.played);
//   };

//   return (
//     <Paper elevation={3} sx={{ width: "70%", padding: "8px" }}>
//       <ReactPlayer
//         ref={playerRef}
//         url={url}
//         width="100%"
//         height="100%"
//         playing={playing}
//         volume={volume}
//         onProgress={handleProgress}
//         controls={true}
//       />
//       <IconButton onClick={handlePlayPause}>
//         {playing ? <Pause /> : <PlayArrow />}
//       </IconButton>
//       <Slider
//         min={0}
//         max={1}
//         step={0.1}
//         value={volume}
//         onChange={handleVolumeChange}
//         aria-labelledby="volume-slider"
//         sx={{ width: "30%" }}
//       />
//       <Typography variant="caption" color="text.secondary">
//         {Math.round(played * 100)}% played
//       </Typography>
//     </Paper>
//   );
// }

// export default VideoPlayer;
