import React, { useState, useRef, useEffect } from "react";
import "./Chat.css";

export default function Chat({ messages, onSend, selectedAgent, onAgentChange }) {
  const [input, setInput] = useState("");
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSend(input.trim());
      setInput("");
    }
  };

  return (
    <div className="jarvis-chat">
      <div className="jarvis-chat-messages">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`jarvis-chat-message ${msg.from === "jarvis" ? "jarvis" : "user"}`}
          >
            <span>{msg.text}</span>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <form className="jarvis-chat-input" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Type your command..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
      <div className="jarvis-agent-select">
        <label htmlFor="agent-select">Agent:</label>
        <select
          id="agent-select"
          value={selectedAgent}
          onChange={e => onAgentChange(e.target.value)}
        >
          <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
          <option value="gpt-4">GPT-4</option>
          <option value="gpt-4o">GPT-4o</option>
        </select>
      </div>
    </div>
  );
}