import { useState, useRef, useEffect } from 'react'

const ChatBox = () => {
    const chatEndRef = useRef(null)

    const [message, setMessage] = useState("");
    const [chatAll, setChatAll] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    

    const apiCall = async () => {
        setIsLoading(true);
        setChatAll((currentChat) => [...currentChat, { role: "user", content: message }]);
        try {
            const response = await fetch('http://127.0.0.1:8000/chat', {
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": JSON.stringify({ message })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setChatAll((currentChat) => [...currentChat, { role: "assistant", content: data.response }]);
            console.log('Response:', data);
        }
        catch (error) {
            console.error('Error:', error);
            setChatAll((currentChat) => [...currentChat, { role: "assistant", content: "Sorry, I encountered an error. Please try again." }]);
        }
        finally {
            setMessage("");
            setIsLoading(false);
        }
    }

    

  useEffect(() => {
        if (chatEndRef.current) {
            chatEndRef.current.scrollTop = chatEndRef.current.scrollHeight;
        }
    }, [chatAll]);

  return (
    <div className="chat-box">
        <div className="chat-title">RAG Chat</div>
        <div className="chat-live" ref={chatEndRef}>
        {chatAll.map((chat, index) => (
            <div key={index} className={`chat-message ${chat.role}`}>{chat.content}</div>
        ))}
        {isLoading && <div className="chat-message assistant loading">thinking...</div>}

        </div>

        <div className="input-box">
        <label htmlFor="message"></label>
        <input
            type="text"
            onChange={(e) => setMessage(e.target.value)}
            placeholder="say hi to your ai assistant"
            value={message}
            disabled={isLoading}
        />
        <button onClick={apiCall} disabled={isLoading}>
          Send
        </button>
        </div>

    </div>
  )
}

export default ChatBox