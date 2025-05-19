import React from "react";

const Notification = ({ message, onClose }) => (
  <div
    style={{
      position: "fixed",
      top: 30,
      right: 30,
      zIndex: 9999,
      minWidth: 320,
      padding: "18px 32px",
      background: "rgba(30, 255, 255, 0.13)",
      border: "2px solid #00fff7",
      borderRadius: "18px",
      boxShadow: "0 0 24px #00fff7, 0 0 8px #1a1a1a",
      color: "#00fff7",
      fontFamily: "Orbitron, 'Share Tech Mono', monospace, sans-serif",
      fontSize: 20,
      letterSpacing: 1.2,
      textShadow: "0 0 8px #00fff7, 0 0 2px #fff",
      backdropFilter: "blur(6px)",
      transition: "opacity 0.3s",
      display: "flex",
      alignItems: "center",
      gap: 16,
    }}
  >
    <span style={{ flex: 1 }}>{message}</span>
    <button
      onClick={onClose}
      style={{
        background: "none",
        border: "none",
        color: "#00fff7",
        fontSize: 22,
        cursor: "pointer",
        textShadow: "0 0 8px #00fff7",
      }}
      aria-label="Close"
    >
      ✕
    </button>
  </div>
);

export default Notification;