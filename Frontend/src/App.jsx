import React from "react";
import AdminPanel from "./Components/AdminPanel";
import AlertLogs from "./Components/AlertLogs";
import ClientView from "./Components/ClientView";

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-gray-900 text-white font-inter">
      <header class="p-6 text-center border-b border-white/10 backdrop-blur-md">
        <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-sky-400 tracking-wide">
          🌐 Disaster Alert Notification System
        </h1>
        <p class="text-gray-400 mt-2">Fast, reliable, and life-saving alerts</p>
      </header>

      <main class="flex flex-col items-center justify-center py-10 space-y-10">
        <AdminPanel />
        <AlertLogs />
        <ClientView />
      </main>
    </div>  
  );
}


// http://127.0.0.1:5030/api/send_alert