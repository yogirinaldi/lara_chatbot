import React, { useState, useRef, useEffect } from "react";
import "./chatbot.css";
import laraImage from "./../../assets/images/lara-mascot.png";
import userImage from "./../../assets/images/191112334.jpg";
import "../../assets/vendor/bootstrap/css/bootstrap.min.css";
import "../../assets/vendor/bootstrap-icons/bootstrap-icons.css";
import "../../assets/css/main.css";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Popover from "react-bootstrap/Popover";

function Chatbot() {
  const [inputValue, setInputValue] = useState("");
  const chatHistoryRef = useRef(null);
  const [inputReadOnly, setInputReadOnly] = useState(false);
  const [messages, setMessages] = useState([]);
  const [errorMessage, setErrorMessage] = useState(false);
  // const [response, setResponse] = useState("");
  const [location, setLocation] = useState({});

  useEffect(() => {
    // Scroll to the bottom of the chat history after each update
    chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
  }, [messages]);

  // Load chat history from local storage on component mount
  useEffect(() => {
    const savedChatHistory = localStorage.getItem("chatHistory");
    if (savedChatHistory) {
      setMessages(JSON.parse(savedChatHistory));
    }
  }, []);

  //get location and insert to database
  useEffect(() => {
    fetch("http://ip-api.com/json")
      .then((res) => res.json())
      .then((data) => {
        fetch("http://127.0.0.1:5000/location", {
          method: "POST",
          body: JSON.stringify({
            ip_address: data.query,
            city: data.city,
            region: data.regionName,
            isp: data.org,
          }),
          headers: {
            "Content-Type": "application/json",
          },
        });
        setLocation({
          ip_address: data.query,
          city: data.city,
          region: data.regionName,
          isp: data.org,
        });
      })
      .catch(() => {
        fetch("https://ipapi.co/json")
          .then((res) => res.json())
          .then((data) => {
            fetch("http://127.0.0.1:5000/location", {
              method: "POST",
              body: JSON.stringify({
                ip_address: data.ip,
                city: data.city,
                region: data.region,
                isp: data.org,
              }),
              headers: {
                "Content-Type": "application/json",
              },
            });
            setLocation({
              ip_address: data.ip,
              city: data.city,
              region: data.region,
              isp: data.org,
            });
          });
      });
  }, []);

  function addMessage(text, isUser, id = 0) {
    if (isUser) {
      setInputReadOnly(true);
    } else {
      setInputReadOnly(false);
    }
    setMessages((messages) => [...messages, { text, isUser, id }]);
    setInputValue("");

    // Load the existing chat history from local storage, or create an empty array if none exists
    const existingChatHistory =
      JSON.parse(localStorage.getItem("chatHistory")) || [];

    // Create a new array that includes the existing chat history and the new message
    const updatedChatHistory = [...existingChatHistory, { text, isUser, id }];

    // Save the updated chat history to local storage
    localStorage.setItem("chatHistory", JSON.stringify(updatedChatHistory));

    // Schedule deletion of chat history after 24 hours
    setTimeout(() => {
      localStorage.removeItem("chatHistory");
      setMessages([]);
    }, 24 * 60 * 60 * 1000); // 24 hours in milliseconds
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    console.log(inputValue);
    addMessage(inputValue, true);
    console.log(messages);

    try {
      const res = await fetch("http://localhost:5000/question", {
        method: "POST",
        mode: "cors",
        body: JSON.stringify({
          question: inputValue,
          ip_address: location.ip_address,
        }),
        headers: {
          "Content-Type": "application/json",
          "access-control-allow-origin": "http://localhost:3000",
        },
      });
      const data = await res.json();
      addMessage(data.data.answer, false, data.data.id);
      console.log(data.message);
    } catch (err) {
      console.error(err);
      setErrorMessage(true);
    }
  };

  const handleDeleteMessages = () => {
    setMessages([]);
    localStorage.removeItem("chatHistory");
  };

  return (
    <div className="container">
      <div className="row clearfix">
        <div className="col-lg-12">
          <div className="card chat-app">
            <div className="chat">
              <div className="chat-history" id="list-chat" ref={chatHistoryRef}>
                <ul className="m-b-0">
                  {messages.map((message, index) => {
                    return (
                      <li key={index} className="clearfix">
                        <div
                          className={
                            message.isUser
                              ? "message-data text-end"
                              : "message-data"
                          }
                        >
                          <img
                            src={message.isUser ? userImage : laraImage}
                            alt="avatar"
                          />
                        </div>
                        <div
                          id={`${message.id}`}
                          className={
                            message.isUser
                              ? "message user-message float-right"
                              : "message bot-message"
                          }
                        >
                          {message.text}
                        </div>
                      </li>
                    );
                  })}
                </ul>
              </div>

              <div className="chat-message clearfix">
                {inputReadOnly ? (
                  errorMessage ? (
                    <div className="alert alert-danger" role="alert">
                      Mohon maaf. Server sedang bermasalah, coba lagi nanti!
                    </div>
                  ) : (
                    <div className="text-center">
                      <span className="typing"></span>
                      <span className="typing"></span>
                      <span className="typing"></span>
                    </div>
                  )
                ) : (
                  <form onSubmit={handleSubmit}>
                    <div className="input-group mb-0">
                      <OverlayTrigger
                        placement="top"
                        overlay={
                          <Popover id="popover-basic">
                            <Popover.Body>Hapus percakapan?</Popover.Body>
                          </Popover>
                        }
                      >
                        <button
                          type="button"
                          className="btn btn-outline-danger form-rounded"
                          onClick={handleDeleteMessages}
                        >
                          <i className="bi bi-x-lg"></i>
                        </button>
                      </OverlayTrigger>

                      <input
                        required
                        type="text"
                        className="form-control"
                        placeholder="Tanya disini ..."
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                      />

                      {/* <div className="input-group-append"></div> */}

                      <button
                        type="submit"
                        className="btn btn-success form-rounded"
                      >
                        <i className="bi bi-send"></i>
                      </button>
                    </div>
                  </form>
                )}

                {/* <form onSubmit={handleSubmit}>
                                <div className="input-group mb-0">
                                    <input 
                                        type="text" 
                                        className="form-control" 
                                        value={inputValue} 
                                        onChange={(e) => setInputValue(e.target.value)}
                                        readOnly={inputReadOnly} />
                                    
                                    <div className="input-group-prepend">
                                        <button className="input-group-text btn-get-started" disabled={inputReadOnly ? true : false} type="submit"><i className="bi bi-send" ></i></button>
                                    </div>
                                </div>
                            </form> */}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chatbot;
