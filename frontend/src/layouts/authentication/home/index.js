import { useNavigate } from "react-router-dom";
import { Container, Box, Card, Typography, Button, Grid } from "@mui/material";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import LoginIcon from "@mui/icons-material/Login";
import AppRegistrationIcon from "@mui/icons-material/AppRegistration";

function Home() {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      }}
    >
      <Container maxWidth="md">
        <MDBox mb={4}>
          <MDTypography variant="h2" color="white" textAlign="center" mb={2}>
            Bienvenido a Acadelytics
          </MDTypography>
          <MDTypography variant="h6" color="white" textAlign="center">
            Plataforma de gestión académica
          </MDTypography>
        </MDBox>

        <Grid container spacing={4} justifyContent="center">
          <Grid item xs={12} sm={6}>
            <Card
              sx={{
                height: "100%",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                padding: 3,
                boxShadow: 3,
                transition: "transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out",
                "&:hover": {
                  transform: "translateY(-10px)",
                  boxShadow: 6,
                },
              }}
            >
              <Box sx={{ textAlign: "center", width: "100%" }}>
                <LoginIcon sx={{ fontSize: 60, color: "#667eea", mb: 2 }} />
                <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
                  Iniciar Sesión
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ mb: 3 }}>
                  Accede con tu cuenta para continuar
                </Typography>
                <Button
                  variant="contained"
                  size="large"
                  fullWidth
                  sx={{
                    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    color: "white",
                    fontWeight: 600,
                    padding: "12px",
                    "&:hover": {
                      background: "linear-gradient(135deg, #764ba2 0%, #667eea 100%)",
                    },
                  }}
                  onClick={() => navigate("/authentication/sign-in")}
                >
                  Iniciar Sesión
                </Button>
              </Box>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Card
              sx={{
                height: "100%",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                padding: 3,
                boxShadow: 3,
                transition: "transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out",
                "&:hover": {
                  transform: "translateY(-10px)",
                  boxShadow: 6,
                },
              }}
            >
              <Box sx={{ textAlign: "center", width: "100%" }}>
                <AppRegistrationIcon sx={{ fontSize: 60, color: "#764ba2", mb: 2 }} />
                <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
                  Registrarse
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ mb: 3 }}>
                  Crea una nueva cuenta
                </Typography>
                <Button
                  variant="outlined"
                  size="large"
                  fullWidth
                  sx={{
                    borderColor: "#764ba2",
                    color: "#764ba2",
                    fontWeight: 600,
                    padding: "12px",
                    "&:hover": {
                      background: "rgba(118, 75, 162, 0.1)",
                      borderColor: "#764ba2",
                    },
                  }}
                  onClick={() => navigate("/authentication/sign-up")}
                >
                  Registrarse
                </Button>
              </Box>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default Home;
