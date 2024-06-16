import HomeIcon from "@mui/icons-material/Home";
import SettingsIcon from "@mui/icons-material/Settings";
import VideoLibraryIcon from "@mui/icons-material/VideoLibrary";
import {
  Drawer,
  List,
  ListItem,
  ListItemButton ,
  ListItemIcon,
  ListItemText,
  Typography,
} from "@mui/material";
import React from "react";

function Sidebar() {
  return (
    <Drawer
      variant="permanent"
      anchor="left"
      sx={{ width: 240, flexShrink: 0 }}
    >
      <Typography variant="h6" sx={{ padding: 2 }}>
        YouTube風アプリ
      </Typography>
      <List>
        <ListItem button>
          <ListItemIcon>
            <HomeIcon />
          </ListItemIcon>
          <ListItemText primary="ホーム" />
        </ListItem>
        <ListItem button>
          <ListItemIcon>
            <VideoLibraryIcon />
          </ListItemIcon>
          <ListItemText primary="動画ライブラリ" />
        </ListItem>
        <ListItem button>
          <ListItemIcon>
            <SettingsIcon />
          </ListItemIcon>
          <ListItemText primary="設定" />
        </ListItem>
      </List>
    </Drawer>
  );
}

export default Sidebar;
