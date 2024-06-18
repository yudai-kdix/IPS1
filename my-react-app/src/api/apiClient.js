// src/api/apiClient.js
import axios from "axios";
import { API_URL } from "../config/development";

const apiClient = axios.create({
  baseURL: API_URL,
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("authToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;


// // データを送信する関数
// const sendData = async (data) => {
//   try {
//     const response = await apiClient.post("/data", data);
//     console.log(response.data);
//   } catch (error) {
//     console.error(error);
//   }
// };