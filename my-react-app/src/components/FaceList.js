import {
    Avatar,
    CircularProgress,
    Container,
    List,
    ListItem,
    ListItemAvatar,
    ListItemText,
} from "@mui/material";
import axios from "axios";
import React, { useEffect, useState } from "react";
import { API_URL } from "../config/development";

const FaceList = () => {
  const [faces, setFaces] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFaces = async () => {
      try {
        const response = await axios.get(API_URL + "/faces"); // エンドポイントを正しいURLに置き換えてください
        console.log(response.data);
        setFaces(response.data);
      } catch (error) {
        console.error("Error fetching faces:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchFaces();
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Container>
      <List>
        {faces.map((face) => (
          <ListItem key={face.id}>
            <ListItemAvatar>
              <Avatar
                src={API_URL +`/face/${face.id}`}
                alt={face.name}
              />
            </ListItemAvatar>
            <ListItemText primary={face.name} />
          </ListItem>
        ))}
      </List>
    </Container>
  );
};

export default FaceList;
