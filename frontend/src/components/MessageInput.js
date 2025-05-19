import React, { useState } from "react";

function MessageInput({ onSend }) {
  const [text, setText] = useState("");
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (text.trim()) {
          onSend(text);
          setText("");
        }
      }}
    >
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type a message..."
        style={{ width: "80%" }}
      />
      <button type="submit">Send</button>
    </form>
  );
}

export default MessageInput;