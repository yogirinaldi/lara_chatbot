import React, { useEffect } from "react";
//import "../assets/vendor/bootstrap/css/bootstrap.min.css";
//import "../assets/css/main.css";
//import "../assets/css/variables.css";
//import "../assets/js/main.js";
import team from "../assets/img/about-bg.png";
import maskot from "../assets/images/lara-mascot.webp";
import Chatbot from "./chatbot/chatbot";

import Aos from "aos";
import "aos/dist/aos.css";

const Main = () => {
  useEffect(() => {
    Aos.init({ once: false });
    Aos.refresh();
  }, []);

  return (
    <main id="main">
      {/* ======= Featured Services Section ======= */}
      {/* End Featured Services Section */}
      {/* ======= About Section ======= */}
      <section id="chat" className="about">
        <div className="container" data-aos="fade-up">
          <div className="section-header">
            <h2>Halo, Saya LARA</h2>
            <p>
              Saya siap membantu memberikan informasi dan solusi mengenai
              perkawinan, hak asuh anak, harta gono-gini dan lainnya.
            </p>
          </div>
          <div
            className="row g-4 g-lg-5"
            data-aos="fade-up"
            data-aos-delay={200}
            style={{ marginTop: "5px" }}
          >
            <div className="col-lg-4">
              <div className="about-img">
                <img src={maskot} className="img-fluid" alt="" />
              </div>
            </div>
            <div className="col-lg-8 no-padding">
              <Chatbot />
            </div>
          </div>
        </div>
      </section>
      {/* End About Section */}

      {/* ======= Team Section ======= */}
      <section id="team" className="team">
        <div className="container" data-aos="fade-up">
          <div className="section-header">
            <h2>Our Team</h2>
            <p>
              Di sini, kami dengan bangga memperkenalkan kepada Anda tim yang
              berdedikasi dan bersemangat yang bertanggung jawab atas kesuksesan
              proyek ini. Kami percaya bahwa kekuatan kami terletak pada
              keragaman bakat dan pengalaman setiap anggota tim kami.
            </p>
          </div>
          <div className="row gy-5">
            <div
              className="col-xl-4 col-md-6 d-flex"
              data-aos="zoom-in"
              data-aos-delay={200}
            >
              <div className="team-member">
                <div className="member-img text-center">
                  <img src={team} className="img-fluid" alt="" />
                </div>
                <div className="member-info">
                  {/* <div className="social">
                    <a href>
                      <i className="bi bi-twitter" />
                    </a>
                    <a href>
                      <i className="bi bi-facebook" />
                    </a>
                    <a href>
                      <i className="bi bi-instagram" />
                    </a>
                    <a href>
                      <i className="bi bi-linkedin" />
                    </a>
                  </div> */}
                  <h4>Jannen Wollyn S. Siahaan</h4>
                  <span>191110147</span>
                  {/* <span>Chief Executive Officer</span> */}
                </div>
              </div>
            </div>
            {/* End Team Member */}
            <div
              className="col-xl-4 col-md-6 d-flex"
              data-aos="zoom-in"
              data-aos-delay={400}
            >
              <div className="team-member">
                <div className="member-img text-center">
                  <img src={team} className="img-fluid" alt="" />
                </div>
                <div className="member-info">
                  {/* <div className="social">
                    <a href>
                      <i className="bi bi-twitter" />
                    </a>
                    <a href>
                      <i className="bi bi-facebook" />
                    </a>
                    <a href>
                      <i className="bi bi-instagram" />
                    </a>
                    <a href>
                      <i className="bi bi-linkedin" />
                    </a>
                  </div> */}
                  <h4>Ruhut Martinus Situmorang</h4>
                  <span>191110961</span>
                  {/* <span>Product Manager</span> */}
                </div>
              </div>
            </div>
            {/* End Team Member */}
            <div
              className="col-xl-4 col-md-6 d-flex"
              data-aos="zoom-in"
              data-aos-delay={600}
            >
              <div className="team-member">
                <div className="member-img text-center">
                  <img src={team} className="img-fluid" alt="" />
                </div>
                <div className="member-info">
                  {/* <div className="social">
                    <a href>
                      <i className="bi bi-twitter" />
                    </a>
                    <a href>
                      <i className="bi bi-facebook" />
                    </a>
                    <a href>
                      <i className="bi bi-instagram" />
                    </a>
                    <a href>
                      <i className="bi bi-linkedin" />
                    </a>
                  </div> */}
                  <h4>Yogi Rinaldi Nainggolan</h4>
                  <span>191112334</span>
                  {/* <span>CTO</span> */}
                </div>
              </div>
            </div>
            {/* End Team Member */}
          </div>
        </div>
      </section>
      {/* End Team Section */}
    </main>
  );
};

export default Main;
