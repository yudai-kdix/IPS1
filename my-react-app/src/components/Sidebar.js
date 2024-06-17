import { Button, Drawer, List, ListItem, ListItemText } from "@mui/material";
import React, { useState } from "react";
import TopBar from "./TopBar";

const Sidebar = ({open, toggleDrawer}) => {
  return (
    <>
      <div style={{ paddingTop: "64px" }}>
        <Drawer anchor="left" open={open} onClose={toggleDrawer(false)}>
          <div
            style={{
              width: "250px",
              borderRight: "1px solid #ccc",
              padding: "10px",
            }}
            role="presentation"
            onClick={toggleDrawer(false)}
            onKeyDown={toggleDrawer(false)}
          >
            <List>
              {["Home", "Profile", "Settings"].map((text) => (
                <ListItem key={text}>
                  <Button fullWidth>
                    <ListItemText primary={text} />
                  </Button>
                </ListItem>
              ))}
            </List>
          </div>
        </Drawer>
      </div>
    </>
  );
};

export default Sidebar;
