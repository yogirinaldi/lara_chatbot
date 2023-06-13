import React, { useState, useRef, useEffect } from "react";
import "./chatbot.css";
import laraImage from "./../../assets/images/lara-mascot.webp";
//import "../../assets/vendor/bootstrap/css/bootstrap.min.css";
//import "../../assets/vendor/bootstrap-icons/bootstrap-icons.css";
//import "../../assets/css/main.css";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Popover from "react-bootstrap/Popover";
import TextField from "@mui/material/TextField";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControl from "@mui/material/FormControl";
import FormControlLabel from "@mui/material/FormControlLabel";
import Cookies from "js-cookie";
import CryptoJS from "crypto-js";
import Grid from "@mui/material/Grid";

import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";

const theme = createTheme({
  palette: {
    primary: {
      main: "#0ea2bd",
    },
  },
});

const larakey = process.env.REACT_APP_LARA;
const larahost = process.env.REACT_APP_HOST;

const blockInvalidChar = (e) =>
  ["e", "E", "+", "-", "."].includes(e.key) && e.preventDefault();

function Chatbot() {
  const [inputValue, setInputValue] = useState("");
  const chatHistoryRef = useRef(null);
  const [inputReadOnly, setInputReadOnly] = useState(false);
  const [messages, setMessages] = useState([]);
  const [errorMessage, setErrorMessage] = useState(false);
  const [userData, setUserData] = useState({});
  const [feedbackUpdated, setFeedbackUpdated] = useState(false);
  const [userButton, setUserButton] = useState(false);
  // const [location, setLocation] = useState({});

  //console.log("RENDER");

  useEffect(() => {
    // Scroll to the bottom of the chat history after each update
    // chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    if (chatHistoryRef.current !== null && !feedbackUpdated) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
    setFeedbackUpdated(false);
  }, [messages]);

  //Load chat history from local storage on component mount
  const savedChatHistory = localStorage.getItem("chatHistory");
  // useEffect(() => {

  //   if (savedChatHistory) {
  //     setMessages(JSON.parse(savedChatHistory));
  //   }
  // }, []);

  //get location and insert to database
  // useEffect(() => {
  //   fetch("http://ip-api.com/json")
  //     .then((res) => res.json())
  //     .then((data) => {
  //       fetch("http://127.0.0.1:5000/location", {
  //         method: "POST",
  //         body: JSON.stringify({
  //           ip_address: data.query,
  //           city: data.city,
  //           region: data.regionName,
  //           isp: data.org,
  //         }),
  //         headers: {
  //           "Content-Type": "application/json",
  //         },
  //       });
  //       setLocation({
  //         ip_address: data.query,
  //         city: data.city,
  //         region: data.regionName,
  //         isp: data.org,
  //       });
  //     })
  //     .catch(() => {
  //       fetch("https://ipapi.co/json")
  //         .then((res) => res.json())
  //         .then((data) => {
  //           fetch("http://127.0.0.1:5000/location", {
  //             method: "POST",
  //             body: JSON.stringify({
  //               ip_address: data.ip,
  //               city: data.city,
  //               region: data.region,
  //               isp: data.org,
  //             }),
  //             headers: {
  //               "Content-Type": "application/json",
  //             },
  //           });
  //           setLocation({
  //             ip_address: data.ip,
  //             city: data.city,
  //             region: data.region,
  //             isp: data.org,
  //           });
  //         });
  //     });
  // }, []);

  function addMessage(text, isUser, id = null, feedback = null) {
    if (isUser) {
      setInputReadOnly(true);
    } else {
      setInputReadOnly(false);
    }
    setMessages((messages) => [...messages, { text, isUser, id, feedback }]);
    setInputValue("");

    // Load the existing chat history from local storage, or create an empty array if none exists
    let existingChatHistory = localStorage.getItem("chatHistory");
    if (existingChatHistory) {
      const decryptedChatHistory = CryptoJS.AES.decrypt(
        existingChatHistory,
        larakey
      ).toString(CryptoJS.enc.Utf8);
      if (decryptedChatHistory) {
        existingChatHistory = JSON.parse(decryptedChatHistory);
      } else {
        existingChatHistory = [];
      }
    } else {
      existingChatHistory = [];
    }

    // Create a new array that includes the existing chat history and the new message
    const updatedChatHistory = [
      ...existingChatHistory,
      { text, isUser, id, feedback },
    ];

    // Save the updated chat history to local storage
    try {
      localStorage.setItem(
        "chatHistory",
        CryptoJS.AES.encrypt(
          JSON.stringify(updatedChatHistory),
          larakey
        ).toString()
      );
    } catch {
      updatedChatHistory.shift();
      localStorage.setItem(
        "chatHistory",
        CryptoJS.AES.encrypt(
          JSON.stringify(updatedChatHistory),
          larakey
        ).toString()
      );
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    console.log(inputValue);
    addMessage(inputValue, true);
    console.log(messages);

    try {
      const res = await fetch(larahost + "/question", {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({
          pertanyaan: inputValue,
          id_user: userData.id_user,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await res.json();
      addMessage(data.data.jawaban, false, data.data.id_question);
      console.log(data.message);
      console.log(data.data.id_question);
    } catch (err) {
      console.error(err);
      setErrorMessage(true);
      setInputValue(inputValue);
    }
  };

  const handleDeleteMessages = () => {
    setMessages([]);
    localStorage.removeItem("chatHistory");
    setOpen(false);
  };

  const userSubmit = async (e) => {
    e.preventDefault();
    setUserButton(true);

    try {
      const res = await fetch(larahost + "/user", {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(userData),
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await res.json();
      setUserData({ ...userData, id_user: data.data.id_user });
      const encryptedIdUser = CryptoJS.AES.encrypt(
        data.data.id_user.toString(),
        larakey
      ).toString();
      Cookies.set("id_user", encryptedIdUser, { expires: 365 });
      localStorage.removeItem("chatHistory");
      addMessage(
        "Halo, saya LARA, chatbot konsultan hukum. Apa yang bisa saya bantu?",
        false
      );
    } catch (err) {
      console.error(err);
      setUserButton(false);
    }
  };

  const handleOnChangeUser = (e) => {
    setUserData({
      ...userData,
      [e.target.name]: e.target.value,
    });
  };

  //get cookie
  useEffect(() => {
    const cookieIdUser = Cookies.get("id_user");
    if (cookieIdUser) {
      const decryptedIdUser = CryptoJS.AES.decrypt(
        cookieIdUser,
        larakey
      ).toString(CryptoJS.enc.Utf8);

      if (decryptedIdUser !== "") {
        setUserData({ id_user: decryptedIdUser });
        if (savedChatHistory) {
          setMessages(
            JSON.parse(
              CryptoJS.AES.decrypt(savedChatHistory, larakey).toString(
                CryptoJS.enc.Utf8
              )
            )
          );
        }
      }
      //console.log(userData);
      // console.log(messages);

      // fetch(larahost + "/user/" + decryptedIdUser, {
      //   method: "GET",
      //   mode: "cors",
      //   credentials: "include",
      // })
      //   .then((res) => res.json())
      //   .then((data) => {
      //     setUserData(data.data);
      //     if (savedChatHistory) {
      //       setMessages(
      //         JSON.parse(
      //           CryptoJS.AES.decrypt(savedChatHistory, larakey).toString(
      //             CryptoJS.enc.Utf8
      //           )
      //         )
      //       );
      //     }
      //   })
      //   .catch((error) => {
      //     //handle error
      //     console.error(error);
      //   });
    }
  }, []);

  const goodFeedback = async (e) => {
    e.preventDefault();
    const id_question = e.target.parentElement.id;
    try {
      await fetch(larahost + "/question/" + id_question, {
        method: "PUT",
        body: JSON.stringify({ feedback: true }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      console.log(messages);
      const updatedMessages = messages.map((item) => {
        if (item.id === +id_question) {
          item.feedback = true;
        }
        return item;
      });
      setMessages(updatedMessages);
      localStorage.setItem(
        "chatHistory",
        CryptoJS.AES.encrypt(
          JSON.stringify(updatedMessages),
          larakey
        ).toString()
      );
      setFeedbackUpdated(true);

      //console.log(data);
    } catch (err) {
      console.error(err);
    }
  };
  const badFeedback = async (e) => {
    e.preventDefault();
    const id_question = e.target.parentElement.id;
    try {
      await fetch(larahost + "/question/" + id_question, {
        method: "PUT",
        body: JSON.stringify({ feedback: false }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      const updatedMessages = messages.map((item) => {
        if (item.id === +id_question) {
          item.feedback = false;
        }
        return item;
      });
      setMessages(updatedMessages);
      localStorage.setItem(
        "chatHistory",
        CryptoJS.AES.encrypt(
          JSON.stringify(updatedMessages),
          larakey
        ).toString()
      );
      setFeedbackUpdated(true);
    } catch (err) {
      console.error(err);
    }
  };

  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    // <div className="container no-padding">
    //   <div className="row clearfix no-padding">
    //     <div className="col-lg-12 no-padding">

    //     </div>
    //   </div>
    // </div>
    <div className="card chat-app">
      {!userData.id_user ? (
        <ThemeProvider theme={theme}>
          <form onSubmit={userSubmit}>
            <FormControl sx={{ m: 6 }} variant="standard">
              <Typography align="center" variant="h6" component="h6">
                Silahkan isi formulir di bawah ini untuk menggunakan layanan
                konsultasi dengan chatbot.
              </Typography>
              <Grid container columnSpacing={2} alignItems="center">
                <Grid item xs={12}>
                  <TextField
                    margin="normal"
                    fullWidth
                    label="Nama"
                    name="nama"
                    required
                    onChange={handleOnChangeUser}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    margin="normal"
                    fullWidth
                    type="email"
                    label="Email"
                    name="email"
                    required
                    onChange={handleOnChangeUser}
                  />
                </Grid>
                <Grid
                  item
                  xs={3}
                  sx={{
                    minWidth: 100,
                  }}
                >
                  <TextField
                    margin="normal"
                    label="Usia"
                    name="usia"
                    type="number"
                    inputProps={{
                      min: 5,
                      max: 100,
                    }}
                    required
                    onChange={handleOnChangeUser}
                    onInput={blockInvalidChar}
                  />
                </Grid>
                <Grid item xs={9}>
                  <RadioGroup row name="jk" onChange={handleOnChangeUser}>
                    <FormControlLabel
                      value="pria"
                      control={<Radio required />}
                      label="Pria"
                    />
                    <FormControlLabel
                      value="wanita"
                      control={<Radio required />}
                      label="Wanita"
                    />
                  </RadioGroup>
                </Grid>
              </Grid>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                sx={{ mt: 2, borderRadius: 50 }}
                disabled={userButton ? true : false}
              >
                MULAI CHAT
              </Button>
            </FormControl>
          </form>
        </ThemeProvider>
      ) : (
        <div className="chat">
          <div className="chat-history" id="list-chat" ref={chatHistoryRef}>
            <ul className="m-b-0">
              {/* {messages.length !== "" && (
                <li className="clearfix">
                  <div className="message-data">
                    <img src={laraImage} alt="avatar" />
                  </div>
                  <div className="position-relative">
                    <div className="message bot-message">{halo}</div>
                  </div>
                </li>
              )} */}

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
                      {!message.isUser && <img src={laraImage} alt="avatar" />}
                    </div>
                    <div className="position-relative">
                      <div
                        className={
                          message.isUser
                            ? "message user-message float-end"
                            : "message bot-message"
                        }
                      >
                        {message.text}
                      </div>

                      {!message.isUser &&
                        message.feedback === null &&
                        message.id !== null && (
                          <OverlayTrigger
                            trigger="click"
                            placement="auto"
                            rootClose={true}
                            overlay={
                              <Popover id="popover-basic">
                                <Popover.Body>
                                  <div className="row">
                                    <a
                                      id={`${message.id}`}
                                      href="#"
                                      className="customLink"
                                      onClick={goodFeedback}
                                    >
                                      <i className="bi bi-hand-thumbs-up userFeedback"></i>
                                      <span>BAIK</span>
                                    </a>
                                  </div>
                                  <hr />
                                  <div className="row">
                                    <a
                                      id={`${message.id}`}
                                      href="#"
                                      className="customLink"
                                      onClick={badFeedback}
                                    >
                                      <i className="bi bi-hand-thumbs-down userFeedback"></i>
                                      <span>BURUK</span>
                                    </a>
                                  </div>
                                </Popover.Body>
                              </Popover>
                            }
                          >
                            <a
                              href="#"
                              className="align-middle customLink"
                              onClick={(e) => e.preventDefault()}
                            >
                              <i className="bi bi-three-dots dot"></i>
                            </a>
                          </OverlayTrigger>
                        )}
                      {message.feedback === true ? (
                        <span className="align-middle">
                          <i className="bi bi-hand-thumbs-up"></i>
                        </span>
                      ) : (
                        message.feedback === false && (
                          <span className="align-middle">
                            <i className="bi bi-hand-thumbs-down"></i>
                          </span>
                        )
                      )}
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>

          <div className="chat-message clearfix">
            {inputReadOnly ? (
              errorMessage ? (
                <div
                  className="alert alert-danger"
                  role="alert"
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <span>
                    <strong>Terjadi error</strong> Silahkan coba lagi!
                  </span>
                  <a
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      setErrorMessage(false);
                      setInputReadOnly(false);
                      handleSubmit(e);
                    }}
                    className="customLink float-right"
                  >
                    <i className="bi bi-arrow-clockwise"></i>
                  </a>
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
                  <button
                    type="button"
                    className="btn btn-outline-danger rounded-end"
                    onClick={handleClickOpen}
                    style={{ borderRadius: "2rem" }}
                  >
                    <i className="bi bi-x-lg"></i>
                  </button>
                  <Dialog
                    open={open}
                    onClose={handleClose}
                    aria-labelledby="alert-dialog-title"
                    aria-describedby="alert-dialog-description"
                  >
                    <DialogTitle id="alert-dialog-title">
                      Hapus percakapan
                    </DialogTitle>
                    <DialogContent>
                      <DialogContentText id="alert-dialog-description">
                        Apakah anda yakin ingin menghapus?
                      </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                      <Button onClick={handleClose}>Tidak</Button>
                      <Button onClick={handleDeleteMessages} autoFocus>
                        Ya
                      </Button>
                    </DialogActions>
                  </Dialog>

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
                    className="btn btn-success rounded-start"
                    style={{ borderRadius: "2rem" }}
                  >
                    <i className="bi bi-send"></i>
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Chatbot;
