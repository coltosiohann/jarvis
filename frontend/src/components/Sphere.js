import React, { useEffect, useRef } from "react";
import "./Sphere.css";

export default function Sphere({ isSpeaking }) {
  const sphereRef = useRef();

  useEffect(() => {
    if (isSpeaking) {
      sphereRef.current.classList.add("pulse");
    } else {
      sphereRef.current.classList.remove("pulse");
    }
  }, [isSpeaking]);

  return (
    <div ref={sphereRef} className="jarvis-sphere-bg">
      <svg width="320" height="320" viewBox="0 0 320 320">
        <defs>
          <radialGradient id="glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#00f2fe" stopOpacity="1" />
            <stop offset="100%" stopColor="#001a33" stopOpacity="0.1" />
          </radialGradient>
        </defs>
        <circle
          cx="160"
          cy="160"
          r="140"
          fill="url(#glow)"
          stroke="#00f2fe"
          strokeWidth="2"
          opacity="0.7"
        />
        <g className="animated-waves">
          <ellipse
            cx="160"
            cy="160"
            rx="120"
            ry="60"
            fill="none"
            stroke="#00f2fe"
            strokeWidth="2"
            opacity="0.5"
          />
          <ellipse
            cx="160"
            cy="160"
            rx="90"
            ry="140"
            fill="none"
            stroke="#00f2fe"
            strokeWidth="1"
            opacity="0.3"
          />
          <ellipse
            cx="160"
            cy="160"
            rx="60"
            ry="100"
            fill="none"
            stroke="#00f2fe"
            strokeWidth="1"
            opacity="0.2"
          />
        </g>
      </svg>
    </div>
  );
}