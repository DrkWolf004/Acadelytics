import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "context/AuthContext";
import { authAPI, setToken } from "services/api";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import MDInput from "components/MDInput";
import MDButton from "components/MDButton";
import BasicLayout from "layouts/authentication/components/BasicLayout";
import bgImage from "assets/images/bg-sign-in-basic.jpeg";

function SignIn() {
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await authAPI.login(correo, password);
      if (response.token) {
        setToken(response.token);
        login(response.token, response);
        navigate("/dashboard");
      }
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <BasicLayout image={bgImage}>
      <MDBox display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <MDBox width="100%" maxWidth="400px" p={3} boxShadow={3} borderRadius="lg">
          <MDTypography variant="h4" fontWeight="bold" mb={3}>
            Inicia Sesión
          </MDTypography>
          {error && (
            <MDTypography color="error" mb={2} variant="body2">
              {error}
            </MDTypography>
          )}
          <form onSubmit={handleLogin}>
            <MDBox mb={2}>
              <MDInput
                label="Correo"
                type="email"
                value={correo}
                onChange={(e) => setCorreo(e.target.value)}
                fullWidth
                required
              />
            </MDBox>
            <MDBox mb={2}>
              <MDInput
                label="Contraseña"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                fullWidth
                required
              />
            </MDBox>
            <MDButton type="submit" variant="contained" color="info" fullWidth disabled={loading}>
              {loading ? "Cargando..." : "Ingresar"}
            </MDButton>
          </form>
          <MDTypography variant="body2" mt={2} textAlign="center">
            ¿No tienes cuenta?{" "}
            <MDTypography
              component="a"
              href="/authentication/sign-up"
              variant="body2"
              color="info"
              fontWeight="medium"
            >
              Regístrate
            </MDTypography>
          </MDTypography>
        </MDBox>
      </MDBox>
    </BasicLayout>
  );
}

export default SignIn;
