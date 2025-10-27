import React, { useState } from "react";

export default function AdminPanel() {
  const [message, setMessage] = useState("");

  const sendAlert = async () => {
    if (!message) return alert("Please enter a message!");
    const res = await fetch("http://127.0.0.1:5030/api/send_alert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    if (data.success) {
      alert("Alert sent successfully!");
      setMessage("");
    }
  };

  return (
    <div className="max-w-lg w-full bg-white/5 backdrop-blur-md rounded-2xl p-6 shadow-2xl border border-white/10 hover:shadow-emerald-500/20 transition">
      <h2 className="text-2xl font-semibold text-emerald-400 mb-3"> Admin Panel</h2>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Enter alert message..."
        className="w-full p-3 rounded-xl bg-slate-800/70 border border-white/10 focus:outline-none focus:ring-2 focus:ring-emerald-400 text-gray-100 placeholder-gray-500" 
        rows="4"
      />
      <button
        onClick={sendAlert}
        className="mt-4 w-full py-2.5 bg-gradient-to-r from-emerald-500 to-sky-500 hover:from-emerald-400 hover:to-sky-400 font-semibold rounded-xl shadow-lg shadow-emerald-500/25 transition-all"
  >
        Send Alert
      </button>
    </div>
  );
}
