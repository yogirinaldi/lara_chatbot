import React, { useState, useRef,useEffect  }from 'react';
import './home.css';
import mikaLogo from './../../assets/images/mika-mascot.png';
import userImage from './../../assets/images/191112334.jpg';

function Home() {
    
    const [inputValue, setInputValue] = useState('');
    const chatHistoryRef = useRef(null);
    const [inputReadOnly, setInputReadOnly] = useState(false);
    const [messages, setMessages] = useState([]);
    const [response, setResponse] = useState('');

    useEffect(() => {
        // Scroll to the bottom of the chat history after each update
        chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }, [messages]);

    function addMessage(text, isUser) {
        if (isUser) {
            setInputReadOnly(true);
        }else{
            setInputReadOnly(false);
        }
        setMessages((messages)=> [...messages, { text, isUser }]);
        setInputValue('');
        
    }
    
    const handleSubmit = async (e) => {
        e.preventDefault();

        console.log(inputValue)
        addMessage(inputValue,true);
        console.log(messages);

        try {
        const res = await fetch('http://localhost:5000', {
            method: 'POST',
            mode: 'cors',
            body: JSON.stringify({inputValue}),
            headers: {'Content-Type': 'application/json', 'access-control-allow-origin':'http://localhost:3000'},
        });
        const data = await res.json()
        addMessage(data.message,false);
        console.log(data.message);
        } catch (err) {
        console.error(err);
        }       
        


    };

  return (
    <div className="container">
        <div className="row clearfix">
            <div className="col-lg-12">
                <div className="card chat-app">
                    <div className="chat">
                        <div className="chat-header clearfix">
                            <div className="row">
                                <div className="col-lg-1 d-flex justify-content-center align-items-center">
                                    <img src={mikaLogo}  alt="..." />
                                </div>
                                <div className="col offset-lg-1">
                                    <figure className="text-center">
                                        <blockquote className="blockquote">
                                            <p>MIKA</p>
                                        </blockquote>
                                        <p className="blockquote-footer">
                                            Halo, Saya MIKA, asisten pribadimu. saya siap membantu memberikan informasi mengenai akses jadwal kuliah dan ujian.
                                            absensi, kalender dan peraturan akademik. informasi wisuda dan lainnya.
                                        </p>
                                    </figure>                                    
                                </div>
                                <div className="col-lg-1 offset-lg-1 d-flex justify-content-center align-items-center">
                                    
                                         {/* <i className="bi bi-x-lg"></i>  */}                                   

                                </div>
                            </div>
                        </div>
                        <div className="chat-history" id="list-chat" ref={chatHistoryRef}>
                            <ul className="m-b-0">
                                {messages.map((message, index) => {
                                    return(
                                        <li key={index} className="clearfix">
                                    <div className={message.isUser ? 'message-data text-end' : 'message-data'}>
                                        <img src={message.isUser ? userImage : mikaLogo} alt="avatar" />
                                    </div>
                                    <div className={message.isUser ? 'message user-message float-right' : 'message bot-message'}>{message.text}</div>
                                    </li>
                                    )
                                })}
                            </ul>
                        </div>
                        <div className="chat-message clearfix">
                            <form onSubmit={handleSubmit}>
                                <div className="input-group mb-0">
                                    <input 
                                        type="text" 
                                        className="form-control" 
                                        value={inputValue} 
                                        onChange={(e) => setInputValue(e.target.value)}
                                        readOnly={inputReadOnly} />
                                    <div className="input-group-prepend">
                                        <button className="input-group-text" disabled={inputReadOnly ? true : false} type="submit"><i className="bi bi-send" ></i></button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
  );
}

export default Home;
