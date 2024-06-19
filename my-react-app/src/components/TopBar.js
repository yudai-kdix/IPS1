import MenuIcon from "@mui/icons-material/Menu";
import { AppBar, IconButton, Toolbar } from "@mui/material";
import React from "react";

// 独立したAppBarコンポーネント
const TopBar = ({ toggleDrawer }) => {
  return (
    <AppBar position="sticky">
      <Toolbar>
        <IconButton
          onClick={toggleDrawer(true)}
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};

export default TopBar;
