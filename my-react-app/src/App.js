import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import FileUpload from "./components/FileUpload";
import VideoList from "./components/VideoList";
import VideoFrames from "./components/SnapshotList";
import PersonNameInput from "./components/PersonNameInput";
import VideoPlayer from "./components/VideoPlayer";
import VideoStream from "./components/VideoStream";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

const theme = createTheme({
  palette: {
    primary: {
      main: "#556cd6",
    },
    secondary: {
      main: "#19857b",
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<VideoList />} />
            {/* ルートページで動画ファイルのリストを表示 */}
            <Route path="/upload" element={<FileUpload />} />
            {/* ファイルアップロードページ */}
            <Route path="/play/:filename" element={<VideoFrames />} />
            {/* 特定のファイルに対する処理済みフレームを表示 */}
            <Route
              path="/person_name_input/:filename"
              element={<PersonNameInput />}
            />
            {/* 顔データに名前を入力するページ */}
            <Route path="/video/:filename" element={<VideoPlayer />} />
            <Route path="/video_feed/:filename" element={<VideoStream />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
