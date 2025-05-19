import React, { useRef } from "react";

function FileUpload({ onFileUpload }) {
  const inputRef = useRef();

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileUpload(e.target.files[0]);
      inputRef.current.value = "";
    }
  };

  return (
    <div style={{ margin: "10px 0" }}>
      <input
        type="file"
        accept="image/*,.pdf,.doc,.docx,.txt"
        ref={inputRef}
        onChange={handleChange}
        style={{ display: "none" }}
        id="file-upload"
      />
      <label htmlFor="file-upload" style={{
        background: "#1976d2",
        color: "#fff",
        padding: "8px 16px",
        borderRadius: 6,
        cursor: "pointer"
      }}>
        Upload Image/Document
      </label>
    </div>
  );
}

export default FileUpload;