import React, { useState } from "react";
import axios from "axios";

function FileUpload({ setFiles }) {
  const [file, setFile] = useState(null);

  const onFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const onSubmit = (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    axios
      .post("http://http://127.0.0.1:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log("File uploaded successfully");
        setFiles(response.data); // 親コンポーネントから渡されたsetFilesを使ってファイルリストを更新
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
      });
  };

  return (
    <form onSubmit={onSubmit}>
      <input type="file" onChange={onFileChange} />
      <button type="submit">Upload</button>
    </form>
  );
}

export default FileUpload;