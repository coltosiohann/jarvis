import React, { useEffect, useState } from "react";
import "./StatusBar.css";

export default function StatusBar() {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const dateStr = now.toLocaleDateString();
  const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

  return (
    <div className="jarvis-status-bar">
      <div className="status-datetime">{dateStr} {timeStr}</div>
      <div className="status-message">System is fully operational!</div>
    </div>
  );
}