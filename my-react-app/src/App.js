import CssBaseline from "@mui/material/CssBaseline";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import React from "react";
import { useState } from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import "./App.css";
import FileUpload from "./components/FileUpload";
import PersonNameInput from "./components/PersonNameInput";
import Sidebar from "./components/Sidebar";
import VideoFrames from "./components/SnapshotList";
import TopBar from "./components/TopBar";
import VideoList from "./components/VideoList";
import VideoPlayer from "./components/VideoPlayer";
import VideoStream from "./components/VideoStream";

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
  const [open, setOpen] = useState(false);

  const toggleDrawer = (isOpen) => (event) => {
    if (
      event.type === "keydown" &&
      (event.key === "Tab" || event.key === "Shift")
    ) {
      return;
    }
    setOpen(isOpen);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <TopBar toggleDrawer={toggleDrawer} />
        <div style={{ display: "flex" }}>
          <Sidebar open={open} toggleDrawer={toggleDrawer}  />{" "}
          {/* Sidebarコンポーネントを配置 */}
          <div style={{ flexGrow: 1 }}>
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
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
