import React, { useState } from "react";
import axios from "axios";

function PersonNameInput({ filename, faceLocations }) {
  const [names, setNames] = useState({});

  const handleNameChange = (event, faceLocation) => {
    setNames((prev) => ({ ...prev, [faceLocation]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post(
        `http://127.0.0.1:5000/${filename}`,
        {
          ...names,
        }
      );
      console.log("Names saved:", response.data);
      // Optional: Redirect or display a success message
    } catch (error) {
      console.error("Error saving names:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {faceLocations.map((faceLocation, index) => (
        <div key={index}>
          <label>
            Name for {faceLocation}:
            <input
              type="text"
              value={names[faceLocation] || ""}
              onChange={(e) => handleNameChange(e, faceLocation)}
            />
          </label>
        </div>
      ))}
      <button type="submit">Save Names</button>
    </form>
  );
}

export default PersonNameInput;
