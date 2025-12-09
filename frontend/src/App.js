import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import theme from "assets/theme";
import { AuthProvider, useAuth } from "context/AuthContext";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import Sidenav from "examples/Sidenav";
import Configurator from "examples/Configurator";
import Home from "layouts/authentication/home";
import routes from "routes";

function AppContent() {
  const { isAuthenticated } = useAuth();
  const authRoutes = ["/authentication/sign-in", "/authentication/sign-up"];

  const getRoutes = (allRoutes) =>
    allRoutes.map((route) => {
      const isAuthRoute = authRoutes.includes(route.route);
      const Component = route.component;

      if (route.route) {
        return (
          <Route
            exact
            path={route.route}
            element={
              isAuthRoute ? (
                <Component />
              ) : isAuthenticated ? (
                <DashboardLayout>
                  <Component />
                </DashboardLayout>
              ) : (
                <Navigate to="/authentication/sign-in" />
              )
            }
            key={route.key}
          />
        );
      }
      return null;
    });

  return (
    <>
      {isAuthenticated && (
        <Sidenav color="info" brand="Acadelytics" brandName="Acadelytics" routes={routes} />
      )}
      {isAuthenticated && <Configurator />}
      <Routes>
        <Route path="/" element={<Home />} />
        {getRoutes(routes)}
        <Route path="*" element={<Navigate to={isAuthenticated ? "/dashboard" : "/"} />} />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <Router>
      <AuthProvider>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <AppContent />
        </ThemeProvider>
      </AuthProvider>
    </Router>
  );
}
