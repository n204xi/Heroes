import React, { useState } from "react";
import { uploadProfilePic } from "../utils/api";

const ProfilePicUpload = ({ character, onUpload }) => {
  const [file, setFile] = useState(null);

  const handleChange = (e) => setFile(e.target.files[0]);
  const handleUpload = async () => {
    if (file) {
      const result = await uploadProfilePic(character, file);
      onUpload(result.profile_pic_url);
    }
  };

  return (
    <div style={{ margin: "10px 0" }}>
      <input type="file" accept="image/*" onChange={handleChange} />
      <button onClick={handleUpload} disabled={!file}>Upload Profile Pic</button>
    </div>
  );
};

export default ProfilePicUpload;