import React, { useState } from "react";
import "./Sidebar.css";

export default function Sidebar() {
  const [open, setOpen] = useState(false);

  return (
    <aside
      className={`jarvis-sidebar${open ? " open" : ""}`}
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
    >
      <div
        className={`sidebar-toggle${open ? " open" : ""}`}
        onClick={() => setOpen((v) => !v)}
        tabIndex={0}
        title={open ? "Hide sidebar" : "Show sidebar"}
      >
        <span className="arrow">{open ? "⮜" : "⮞"}</span>
      </div>
      <div className="sidebar-content">
        <h2>JARVIS</h2>
        <nav>
          <ul>
            <li>Memory Logs</li>
            <li>Projects</li>
            <li>Settings</li>
          </ul>
        </nav>
        <footer>
          <small>v1.0</small>
        </footer>
      </div>
    </aside>
  );
}