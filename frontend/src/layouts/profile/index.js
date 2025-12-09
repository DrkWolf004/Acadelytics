/**
=========================================================
* Material Dashboard 2 React - v2.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2023 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

import { useEffect, useState } from "react";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import { useAuth } from "context/AuthContext";
import { userAPI } from "services/api";

import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";

function Overview() {
  const { user: authUser } = useAuth();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        // Si tienes el ID del usuario en el contexto, úsalo
        if (authUser?.id) {
          const data = await userAPI.getUser(authUser.id);
          setUserData(data.data || data);
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
        // Usar datos del contexto si la llamada falla
        setUserData(authUser);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [authUser]);

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox mb={2} />
      <MDBox py={3}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <MDBox
                mx={2}
                mt={-3}
                py={3}
                px={2}
                variant="gradient"
                bgColor="info"
                borderRadius="lg"
                coloredShadow="info"
              >
                <MDTypography variant="h6" color="white">
                  Mi Perfil
                </MDTypography>
              </MDBox>
              <MDBox pt={3} pb={3} px={3}>
                {loading ? (
                  <MDTypography variant="body2" color="textSecondary">
                    Cargando perfil...
                  </MDTypography>
                ) : userData ? (
                  <Grid container spacing={2}>
                    <Grid item xs={12}>
                      <MDBox mb={2}>
                        <MDTypography variant="button" color="textSecondary">
                          Nombre
                        </MDTypography>
                        <MDTypography variant="h6">{userData.nombre || "N/A"}</MDTypography>
                      </MDBox>
                    </Grid>
                    <Grid item xs={12}>
                      <MDBox mb={2}>
                        <MDTypography variant="button" color="textSecondary">
                          Apellidos
                        </MDTypography>
                        <MDTypography variant="h6">{userData.apellidos || "N/A"}</MDTypography>
                      </MDBox>
                    </Grid>
                    <Grid item xs={12}>
                      <MDBox mb={2}>
                        <MDTypography variant="button" color="textSecondary">
                          Correo
                        </MDTypography>
                        <MDTypography variant="h6">{userData.correo || "N/A"}</MDTypography>
                      </MDBox>
                    </Grid>
                    {userData.role && (
                      <Grid item xs={12}>
                        <MDBox mb={2}>
                          <MDTypography variant="button" color="textSecondary">
                            Rol
                          </MDTypography>
                          <MDTypography variant="h6">{userData.role || "N/A"}</MDTypography>
                        </MDBox>
                      </Grid>
                    )}
                  </Grid>
                ) : (
                  <MDTypography variant="body2" color="textSecondary">
                    No se pudieron cargar los datos del perfil.
                  </MDTypography>
                )}
              </MDBox>
            </Card>
          </Grid>
        </Grid>
      </MDBox>
      <Footer />
    </DashboardLayout>
  );
}

export default Overview;
