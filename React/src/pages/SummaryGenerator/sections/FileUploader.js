import React, { useState } from "react";
import axios from "axios";
import { useModal } from "react-hooks-use-modal";

// @mui material components
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";

// Material Kit 2 React components
import MKBox from "components/MKBox";
// import MKInput from "components/MKInput";
import MKButton from "components/MKButton";
import MKTypography from "components/MKTypography";
import HorizontalTeamCard from "examples/Cards/TeamCards/HorizontalTeamCard";

function FileUpload() {
  const [selectedFile, setSelectedFile] = useState();
  const [isSelected, setIsSelected] = useState(false);
  const [output, setOutput] = useState([]);
  // const [isFilePicked, setIsFilePicked] = useState(false);

  const [ModalSuccess, closeSuccess] = useModal("root", {
    preventScroll: true,
    closeOnOverlayClick: false,
  });

  const [ModalFail, closeFail] = useModal("root", {
    preventScroll: true,
    closeOnOverlayClick: false,
  });

  const handleChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setIsSelected(true);
    setOutput(event.target.data);
  };

  const UploadFile = (event) => {
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
          console.log(response.data); // the produced summary
          setOutput(response.data);
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
    <MKBox component="section" py={12}>
      <Container>
        <Grid container item justifyContent="center" xs={10} lg={7} mx="auto" textAlign="center">
          <MKTypography variant="h3" mb={1}>
            Upload PDF a file to generate summary
          </MKTypography>
        </Grid>
        <Grid container item xs={12} lg={7} sx={{ mx: "auto" }}>
          <MKBox width="100%" component="form" method="post" autocomplete="off">
            <MKBox p={3}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <MKTypography component="a" fontWeight="regular" color="dark">
                    <input type="file" id="file" name="file" onChange={handleChange} />
                    {isSelected ? (
                      <div>
                        <Grid
                          container
                          item
                          justifyContent="center"
                          xs={10}
                          lg={7}
                          mx="auto"
                          textAlign="center"
                        >
                          <MKTypography variant="h4" mb={1}>
                            File Details
                          </MKTypography>
                        </Grid>
                        <p>Filename: {selectedFile.name}</p>
                        <p>Filetype: {selectedFile.type}</p>
                        <p>Size in bytes: {selectedFile.size}</p>
                        <p>
                          lastModifiedDate: {selectedFile.lastModifiedDate.toLocaleDateString()}
                        </p>
                      </div>
                    ) : (
                      <p>Select a file to show details</p>
                    )}
                  </MKTypography>
                </Grid>
              </Grid>
              <Grid container item justifyContent="center" xs={12} my={2}>
                <MKButton
                  onClick={UploadFile}
                  type="submit"
                  href="#"
                  variant="gradient"
                  color="dark"
                  fullWidth
                >
                  Submit
                </MKButton>
              </Grid>

              <Grid container alignItems="center" py={2}>
                <Grid
                  container
                  item
                  justifyContent="center"
                  xs={10}
                  lg={7}
                  mx="auto"
                  textAlign="center"
                >
                  <MKTypography variant="h4" mb={1}>
                    Summary:
                  </MKTypography>
                </Grid>
                <Grid item xs={12} sm={12}>
                  <MKTypography variant="body2" color="text">
                    {output}
                  </MKTypography>
                </Grid>
              </Grid>
            </MKBox>
          </MKBox>
        </Grid>
      </Container>
      <ModalSuccess>
        <HorizontalTeamCard
          image="https://c.tenor.com/xVfFIHxAzW4AAAAC/success.gif"
          name="Notification"
          position={{ color: "success", label: "Upload Success!" }}
          description=" "
        />
        <MKButton
          onClick={closeSuccess}
          type="submit"
          href="#"
          variant="gradient"
          color="dark"
          fullWidth
        >
          Close
        </MKButton>
      </ModalSuccess>
      <ModalFail>
        <HorizontalTeamCard
          image="https://c.tenor.com/_EOg1bM-P-AAAAAC/fail.gif"
          name="Notification"
          position={{ color: "error", label: "Upload Fail!" }}
          description="Please try agian"
        />
        <MKButton
          onClick={closeFail}
          type="submit"
          href="#"
          variant="gradient"
          color="dark"
          fullWidth
        >
          Close
        </MKButton>
      </ModalFail>
    </MKBox>
  );
}

export default FileUpload;
