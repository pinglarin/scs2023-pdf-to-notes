// import Grid from "@mui/material/Grid";

// Material Kit 2 React components
import MKBox from "components/MKBox";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import MKTypography from "components/MKTypography";
import MKButton from "components/MKButton";
import HorizontalTeamCard from "examples/Cards/TeamCards/HorizontalTeamCard";
// import MKInput from "components/MKInput";

// Material Kit 2 React examples
import DefaultNavbar from "examples/Navbars/DefaultNavbar";
// import DefaultFooter from "examples/Footers/DefaultFooter";

// Routes
import routes from "routes";
// import footerRoutes from "footer.routes";

// Image
// import bgImage from "assets/images/illustrations/illustration-reset.jpg";

import Timeline from "./PlayerVideo_page/Timeline_part/Timeline";
import Doc from "./PlayerVideo_page/DocReader_part/Doc";
import samplePDF from "./PlayerVideo_page/DocReader_part/Lec04 Image Matting.pdf";
import VideoPlayer from "./PlayerVideo_page/Player_part/VideoMk2";
import "./PlayerVideo_page/Playvideo.css";

function Upload() {
  return (
    <>
      <MKBox position="fixed" top="0.5rem" width="100%">
        <DefaultNavbar
          routes={routes}
          action={{
            type: "external",
            route: "https://www.creative-tim.com/product/material-kit-react",
            label: "free download",
            color: "default",
          }}
          sticky
        />
      </MKBox>
      {/* Headder */}
      <MKBox
        minHeight="75vh"
        width="100%"
        sx={{
          backgroundImage: ({ functions: { linearGradient, rgba }, palette: { gradients } }) =>
            `${linearGradient(
              rgba(gradients.dark.main, 0.6),
              rgba(gradients.dark.state, 0.6)
            )}, url(https://media.discordapp.net/attachments/917582730982723625/936967309866704916/yihao-ren-bai.jpg?width=1440&height=333)`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          display: "grid",
          placeItems: "center",
        }}
      >
        <Container>
          <Grid
            container
            item
            xs={12}
            lg={8}
            justifyContent="center"
            alignItems="center"
            flexDirection="column"
            sx={{ mx: "auto", textAlign: "center" }}
          >
            <MKTypography
              variant="h1"
              color="white"
              sx={({ breakpoints, typography: { size } }) => ({
                [breakpoints.down("md")]: {
                  fontSize: size["3xl"],
                },
              })}
            >
              Uploader Page
            </MKTypography>
            <MKTypography variant="body1" color="white" opacity={0.8} mt={1} mb={3}>
              We&apos;re constantly trying to express ourselves and actualize our dreams. If you
              have the opportunity to play this game
            </MKTypography>
            <MKButton color="default" sx={{ color: ({ palette: { dark } }) => dark.main }}>
              Buy course
            </MKButton>
            <br />
            <HorizontalTeamCard
              image="https://cdn.discordapp.com/attachments/917582730982723625/990506757220630598/FB_IMG_1560130403592.png"
              name="Created by"
              position={{ label: "Teacher A" }}
              description=" "
            />
          </Grid>
        </Container>
      </MKBox>
      <br />
      <br />
      <br />
      <br />
      {/* <div className="PlayerVideo_page">
        <p> Test Video </p>
        <div className="PlayerVideo">
          <VideoPlayer />
        </div>
        <p>Test Timeline</p>
        <Timeline />
        <p>Test Doc Reader</p>
        <div className="Doc">
          <Doc pdf={samplePDF} />
        </div>
      </div> */}
      <Grid container spacing={3} alignItems="center">
        <Grid item xs={12} lg={6}>
          <p> Test Video </p>
          <div className="PlayerVideo">
            <VideoPlayer />
          </div>
          <br />
          <p>Test Doc Reader</p>
          <div className="Doc">
            <Doc pdf={samplePDF} />
          </div>
        </Grid>
        <Grid
          item
          xs={12}
          sm={10}
          md={7}
          lg={6}
          xl={5}
          ml={{ xs: "auto", lg: 6 }}
          mr={{ xs: "auto", lg: 6 }}
        >
          <p>Test Timeline</p>
          <Timeline />
        </Grid>
      </Grid>
      <br />
      <br />
      <br />
      <br />
    </>
  );
}

export default Upload;
