import React, { useState } from "react";
import axios from "axios";

function FileUpload() {
  const [selectedFile, setSelectedFile] = useState();
  const [isSelected, setIsSelected] = useState(false);
  // const [isFilePicked, setIsFilePicked] = useState(false);
  const handleChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setIsSelected(true);
  };

  const Uploadvideo = (event) => {
    const formData = new FormData();
    const uploadfile = document.querySelector("#file");
    formData.append("file", uploadfile.files[0]);
    console.log(uploadfile.files[0]);
    if (uploadfile.files[0]) {
      axios
        .post(`http://localhost:8000/gen_summary/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          // eslint-disable-next-line
          console.log(response);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      alert("File uploaded");
    } else {
      // eslint-disable-next-line
      alert("upload a file");
    }
    // for debugging
    console.log("for debugging");
    console.log(selectedFile.name);
    event.preventDefault();
  };
  return (
    <form>
      <h2>Upload a file</h2>
      <input type="file" id="file" name="file" onChange={handleChange} />
      {isSelected ? (
        <div>
          <h2>File Details</h2>
          <p>Filename: {selectedFile.name}</p>
          <p>Filetype: {selectedFile.type}</p>
          <p>Size in bytes: {selectedFile.size}</p>
          <p>lastModifiedDate:{selectedFile.lastModifiedDate.toLocaleDateString()}</p>
        </div>
      ) : (
        <p>Select a file to show details</p>
      )}
      <div>
        <button type="submit" onClick={Uploadvideo}>
          Submit
        </button>
      </div>
    </form>
  );
}
export default FileUpload;
