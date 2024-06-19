import { Button, Container, TextField, Typography } from "@mui/material";
import axios from "axios";
import React, { useState } from "react";
import { API_URL } from "../config/development";

function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const response = await axios.post(API_URL + "/login", {
        username: username,
        password: password,
      });
      // レスポンスからトークンを取得しlocalStorageに保存
      localStorage.setItem("authToken", response.data.token);
      alert("Login successful");
    } catch (error) {
      alert("Login failed");
      console.error(error);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Typography component="h1" variant="h5">
        ログイン
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
        onClick={handleLogin}
      >
        ログイン
      </Button>
    </Container>
  );
}

export default LoginPage;
