import React, { useEffect } from "react";
// import "../assets/vendor/bootstrap/css/bootstrap.min.css";
// import "../assets/css/main.css";
// import "../assets/css/variables.css";

import "../assets/js/main.js";

import Aos from "aos";
import "aos/dist/aos.css";

const WelcomeSection = () => {
  useEffect(() => {
    Aos.init({ once: false });
    Aos.refresh();
  }, []);

  return (
    <section
      id="hero-fullscreen"
      className="hero-fullscreen d-flex align-items-center"
    >
      <div
        className="container d-flex flex-column align-items-center position-relative"
        data-aos="zoom-out"
      >
        <h2 className="text-center">
          Selamat Datang di <span>LARA</span>
        </h2>
        <p style={{ textAlign: "center" }}>
          Sebuah Chatbot Konsultasi Hukum Perkawinan.
        </p>
        <div className="d-flex">
          <a href="#chat" className="btn-get-started scrollto">
            Mulai
          </a>
        </div>
      </div>
    </section>
  );
};

export default WelcomeSection;
