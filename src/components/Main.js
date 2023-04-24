import React, { useEffect } from "react";
import "../assets/vendor/bootstrap/css/bootstrap.min.css";
import "../assets/css/main.css";
import "../assets/css/variables.css";
import "../assets/js/main.js";
import team1 from "../assets/img/team/team-1.jpg";
import team2 from "../assets/img/team/team-2.jpg";
import team3 from "../assets/img/team/team-3.jpg";
import maskot from "../assets/images/lara-mascot.png";
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
      <section id="about" className="about">
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
          >
            <div className="col-lg-4">
              <div className="about-img">
                <img src={maskot} className="img-fluid" alt="" />
              </div>
            </div>
            <div className="col-lg-8">
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
              Architecto nobis eos vel nam quidem vitae temporibus voluptates
              qui hic deserunt iusto omnis nam voluptas asperiores sequi tenetur
              dolores incidunt enim voluptatem magnam cumque fuga.
            </p>
          </div>
          <div className="row gy-5">
            <div
              className="col-xl-4 col-md-6 d-flex"
              data-aos="zoom-in"
              data-aos-delay={200}
            >
              <div className="team-member">
                <div className="member-img">
                  <img src={team1} className="img-fluid" alt="" />
                </div>
                <div className="member-info">
                  <div className="social">
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
                  </div>
                  <h4>Walter White</h4>
                  <span>Chief Executive Officer</span>
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
                <div className="member-img">
                  <img src={team2} className="img-fluid" alt="" />
                </div>
                <div className="member-info">
                  <div className="social">
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
                  </div>
                  <h4>Sarah Jhonson</h4>
                  <span>Product Manager</span>
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
                <div className="member-img">
                  <img src={team3} className="img-fluid" alt="" />
                </div>
                <div className="member-info">
                  <div className="social">
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
                  </div>
                  <h4>William Anderson</h4>
                  <span>CTO</span>
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
