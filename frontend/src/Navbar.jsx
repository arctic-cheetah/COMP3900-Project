export default function Navbar() {
  return (
    <nav className='navbar'>
      <img className='logo' src='assets/logo.png' />
      <p className='website-name'>Phishy Links</p>

      <div className='links'>
        <a href='/user'>User</a>
      </div>
    </nav>
  );
}
