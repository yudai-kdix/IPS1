import { Button, Drawer, List, ListItem, ListItemText } from "@mui/material";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // 追加
import TopBar from "./TopBar";


const Sidebar = ({ open, toggleDrawer }) => {
  const navigate = useNavigate(); // useNavigateフックを使用

  const menuItems = [
    { text: "Home", path: "/" }, // Homeページへのパスを"/"とする
    { text: "Login", path: "/login" }, // Loginページへのパスを"/login"とする
    { text: "Register", path: "/register" }, // Registerページへのパスを"/register"とする
    { text: "Upload", path: "/upload" }, // Uploadページへのパスを"/upload"とする
    {text: "FaceList", path: "/faces"}
  ];

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
              {menuItems.map((item) => (
                <ListItem
                  button
                  key={item.text}
                  onClick={() => navigate(item.path)}
                >
                  {" "}
                  {/* クリック時にnavigateを使用してページ遷移 */}
                  <Button fullWidth>
                    <ListItemText primary={item.text} />
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
