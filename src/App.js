import './App.css';
import React from 'react';
import Home from './components/home/home';

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

  return (<Home />);
}

export default App;

