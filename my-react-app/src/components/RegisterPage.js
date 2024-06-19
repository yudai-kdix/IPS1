import { Button, Container, TextField, Typography } from "@mui/material";
import axios from "axios";
import React, { useState } from "react";
import { API_URL } from "../config/development";

function RegisterPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    try {
      const response = await axios.post(
        API_URL + "/signup",
        {
          username: username,
          password: password,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      // const response = await axios.post(API_URL + "/signup", {
      //   username: username,
      //   password: password,
      // });
      console.log(response.data); // レスポンスを処理
      alert("Registration successful");
    } catch (error) {
      alert("Registration failed");
      console.error(error);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Typography component="h1" variant="h5">
        新規登録
      </Typography>
      <TextField
        variant="outlined"
        margin="normal"
        required
        fullWidth
        label="ユーザーネーム"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        autoFocus
      />
      <TextField
        variant="outlined"
        margin="normal"
        required
        fullWidth
        label="パスワード"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <Button
        type="button"
        fullWidth
        variant="contained"
        color="primary"
        onClick={handleRegister}
      >
        登録
      </Button>
    </Container>
  );
}

export default RegisterPage;
