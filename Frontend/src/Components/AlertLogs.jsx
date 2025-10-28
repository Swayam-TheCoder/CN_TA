import React, { useEffect, useState } from "react";

export default function AlertLogs() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetch("https://cnta-production.up.railway.app")
      .then((res) => res.json())
      .then(setAlerts);
  }, []);

  return (
    <div className="max-w-3xl w-full bg-white/5 backdrop-blur-md rounded-2xl p-6 shadow-xl border border-white/10">
      <h2 className="text-2xl font-semibold text-sky-400 mb-3">All Alerts</h2>
      <table className="w-full border-separate border-spacing-y-2">
        <thead>
          <tr className="bg-gradient-to-r from-slate-700 to-slate-800 text-gray-300 text-sm">
            <th className="py-2 px-4 text-left rounded-l-lg">Message</th>
            <th className="py-2 px-4 text-left">Timestamp</th>
            <th className="py-2 px-4 text-center rounded-r-lg">Status</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((a) => (
            <tr key={a.id} className="bg-slate-800/70 hover:bg-slate-700/70 transition rounded-lg">
              <td className="py-2 px-4">{a.id}</td>
              <td className="py-2 px-4 text-gray-400">{a.message}</td>
              <td className="py-2 px-4 text-center">{a.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
