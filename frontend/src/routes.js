import Dashboard from "layouts/dashboard";
import Tables from "layouts/tables";
import Profile from "layouts/profile";
import SignIn from "layouts/authentication/sign-in";
import SignUp from "layouts/authentication/sign-up";

// Icon imports
import DashboardIcon from "@mui/icons-material/Dashboard";
import TableChartIcon from "@mui/icons-material/TableChart";
import PersonIcon from "@mui/icons-material/Person";
import LoginIcon from "@mui/icons-material/Login";
import AppRegistrationIcon from "@mui/icons-material/AppRegistration";

const routes = [
  {
    type: "collapse",
    name: "Dashboard",
    key: "dashboard",
    icon: <DashboardIcon />,
    route: "/dashboard",
    component: Dashboard,
  },
  {
    type: "collapse",
    name: "Aulas",
    key: "tables",
    icon: <TableChartIcon />,
    route: "/tables",
    component: Tables,
  },
  {
    type: "collapse",
    name: "Perfil",
    key: "profile",
    icon: <PersonIcon />,
    route: "/profile",
    component: Profile,
  },
  {
    type: "collapse",
    name: "Iniciar Sesión",
    key: "sign-in",
    icon: <LoginIcon />,
    route: "/authentication/sign-in",
    component: SignIn,
  },
  {
    type: "collapse",
    name: "Registrarse",
    key: "sign-up",
    icon: <AppRegistrationIcon />,
    route: "/authentication/sign-up",
    component: SignUp,
  },
];

export default routes;
