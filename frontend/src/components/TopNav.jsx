import { NavLink } from "react-router-dom";
import { useAuth } from "../context/auth";
import { useUser } from "../context/user";

function NavItem({ to, name, right }) {
  const className = [
    "border-amber-400",
    "py-2 px-4",
    "hover:bg-indigo-800",
    right ? "border-l-2" : "border-r-2"
  ].join(" ")

  const getClassName = ({ isActive }) => (
    isActive ? className + " bg-indigo-800" : className
  );

  return (
    <NavLink to={to} className={getClassName}>
      {name}
    </NavLink>
  );
}

function AuthenticatedNavItems() {
  const user = useUser();

  return (
    <>
      <NavItem to="/chats" name="pony express" />
      <div className="flex-1" />
      <NavItem to="/profile" name={user?.username} right />
    </>
  );
}

function UnauthenticatedNavItems() {
  return (
    <>
      <NavItem to="/" name="pony express" />
      <div className="flex-1" />
      <NavItem to="/login" name="login" right />
    </>
  );
}


function TopNav() {
  const { isLoggedIn } = useAuth();

  return (
    <nav className="flex flex-row border-b-4 border-amber-400">
      {isLoggedIn ?
        <AuthenticatedNavItems /> :
        <UnauthenticatedNavItems />
      }
    </nav>
  );
}

export default TopNav;