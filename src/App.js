import "./App.css";
import React from "react";
import Header from "./components/Header";
import WelcomeSection from "./components/WelcomeSection";
import Main from "./components/Main";
import Footer from "./components/Footer";

function App() {
  // const [message, setMessage] = useState('');
  // const [response, setResponse] = useState('');

  // const handleSubmit = async (e) => {
  //   e.preventDefault();
  //   try {
  //     const res = await fetch('http://localhost:5000', {
  //       method: 'POST',
  //       mode: 'cors',
  //       body: JSON.stringify({message}),
  //       headers: {'Content-Type': 'application/json', 'access-control-allow-origin':'http://localhost:3000'},
  //     });
  //     const data = await res.json();
  //     setResponse(data.message);
  //     console.log(data.message);
  //   } catch (err) {
  //     console.error(err);
  //   }
  // };

  // const handleSubmit = (e) => {
  //   e.preventDefault();
  //   fetch('http://localhost:3001',{
  //     method: 'POST',
  //     header
  //   })
  //   console.log("ASsa");
  // };

  return (
    <div className="app">
      <Header />
      <WelcomeSection />
      <Main />
      <Footer />
    </div>
  );
}

export default App;
