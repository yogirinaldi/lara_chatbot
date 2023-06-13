import React from "react";
// import "../assets/vendor/bootstrap/css/bootstrap.min.css";
// import "../assets/css/main.css";
// import "../assets/css/variables.css";

// import "../assets/js/main.js";

const Header = () => {
  return (
    <header id="header" className="header fixed-top" data-scrollto-offset={0}>
      <div className="container-fluid d-flex align-items-center justify-content-center">
        <a
          href="/"
          className="logo d-flex align-items-center scrollto me-auto me-lg-0"
        >
          {/* Uncomment the line below if you also wish to use an image logo */}
          {/* <img src="assets/img/logo.png" alt=""> */}
          <h1>
            LARA<span>.</span>
          </h1>
        </a>
        <nav id="navbar" className="navbar">
          <ul>
            <li>
              <a className="nav-link scrollto" href="#chat">
                Chat
              </a>
            </li>
            <li>
              <a className="nav-link scrollto" href="#team">
                Team
              </a>
            </li>
          </ul>
          <i className="bi bi-list mobile-nav-toggle d-none" />
        </nav>
        {/* .navbar */}
        {/* <a className="btn-getstarted scrollto" href="index.html#about">Get Started</a> */}
      </div>
    </header>
  );
};

export default Header;
