import React, { useState } from "react";
import Sphere from "./components/Sphere";
import Chat from "./components/Chat";
import Sidebar from "./components/Sidebar";
import StatusBar from "./components/StatusBar";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    { from: "jarvis", text: "JARVIS is online. How can I assist you?" }
  ]);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState("gpt-3.5-turbo");
  const [isGeneratingAudio, setIsGeneratingAudio] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [listeningAbortController, setListeningAbortController] = useState(null);

  const handleSend = async (text) => {
    setMessages((msgs) => [...msgs, { from: "user", text }]);
    setIsSpeaking(true);
    setIsGeneratingAudio(true);
    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, agent: selectedAgent }),
      });
      const data = await res.json();
      setMessages((msgs) => [
        ...msgs,
        { from: "jarvis", text: data.response }
      ]);
    } catch (e) {
      setMessages((msgs) => [
        ...msgs,
        { from: "jarvis", text: "Sorry Sir, I am having trouble connecting to my brain." }
      ]);
    }
    setIsSpeaking(false);
    setIsGeneratingAudio(false);
  };

  // Voice input handler with abort support
  const handleVoiceInput = async () => {
    if (isListening && listeningAbortController) {
      listeningAbortController.abort();
      setIsListening(false);
      setListeningAbortController(null);
      return;
    }
    const abortController = new AbortController();
    setListeningAbortController(abortController);
    setIsListening(true);
    try {
      const res = await fetch("http://localhost:8000/api/listen", {
        method: "POST",
        signal: abortController.signal
      });
      const data = await res.json();
      if (data.recognized && data.recognized.trim() !== "") {
        setMessages((msgs) => [
          ...msgs,
          { from: "user", text: data.recognized }
        ]);
        handleSend(data.recognized);
      }
    } catch (e) {
      if (e.name === "AbortError") {
        setMessages((msgs) => [
          ...msgs,
          { from: "jarvis", text: "Listening stopped." }
        ]);
      } else {
        setMessages((msgs) => [
          ...msgs,
          { from: "jarvis", text: "Sorry Sir, I could not hear you." }
        ]);
      }
    }
    setIsListening(false);
    setListeningAbortController(null);
  };

  return (
    <div className="jarvis-root">
      <Sidebar />
      <main className="jarvis-main">
        <div className="jarvis-bg-glow" />
        <StatusBar />
        <Sphere isSpeaking={isSpeaking} />
        <div className="jarvis-label">JARVIS</div>
        {isGeneratingAudio && (
          <div className="jarvis-audio-indicator">
            <span>Generating audio...</span>
          </div>
        )}
        <div className="voice-controls">
          <button
            className={`mic-btn${isListening ? " listening" : ""}`}
            onClick={handleVoiceInput}
            title={isListening ? "Stop listening" : "Speak to JARVIS"}
          >
            <span className="mic-icon" />
          </button>
          {isListening && <span className="listening-indicator">Listening...</span>}
        </div>
        <Chat
          messages={messages}
          onSend={handleSend}
          selectedAgent={selectedAgent}
          onAgentChange={setSelectedAgent}
        />
      </main>
    </div>
  );
}

export default App;