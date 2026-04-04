import logoIcon from "../assets/logo.png";
import userIcon from "../assets/user.png";

export default function Navbar() {
  return (
    <nav className='navbar'>
      <img className='logo' src={logoIcon} />
      <p className='website-name'>Phishy Links</p>

      <img className='user-photo' src={userIcon} />
    </nav>
  );
}
