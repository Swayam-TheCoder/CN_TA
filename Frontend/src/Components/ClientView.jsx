import React, { useEffect, useState } from "react";

export default function ClientView() {
  const [alerts, setAlerts] = useState([]);
  const [timer, setTimer] = useState(5);

const fetchAlerts = async () => {
  const res = await fetch("http://127.0.0.1:5030/api/client_alerts");
  const data = await res.json();
  setAlerts(data);
};

  useEffect(() => {
    fetchAlerts();
    const intervalFetch = setInterval(fetchAlerts, 5000);
    const intervalTimer = setInterval(
      () => setTimer((t) => (t > 0 ? t - 1 : 0)),
      1000
    );

    if (timer === 0) setTimer(5);

    return () => {
      clearInterval(intervalFetch);
      clearInterval(intervalTimer);
    };
  }, [timer]);

  return (
  <div className="max-w-2xl w-full bg-gradient-to-br from-slate-900/80 via-slate-800/80 to-gray-900/80 backdrop-blur-xl rounded-2xl p-6 shadow-2xl border border-white/10 text-white">
    <h2 className="text-3xl font-extrabold bg-gradient-to-r from-rose-400 to-amber-300 bg-clip-text text-transparent mb-4 tracking-wide">
      📢 Live Alerts
    </h2>

    <div className="space-y-4">
      {alerts.length > 0 ? (
        alerts.map((a) => (
          <div
            key={a.id}
            className="p-4 bg-gradient-to-r from-rose-500/10 to-amber-400/10 border border-rose-400/20 rounded-xl shadow-lg hover:shadow-rose-500/20 transition transform hover:scale-[1.02]"
          >
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-rose-300">
                ⚠️ {a.message}
              </h3>
              <span className="text-xs text-gray-400">{a.timestamp}</span>
            </div>
          </div>
        ))
      ) : (
        <div className="p-4 text-gray-400 text-sm italic bg-slate-800/50 rounded-lg border border-white/10 text-center">
          No active alerts at the moment 🚫
        </div>
      )}
    </div>

    <div className="mt-6 text-center text-sm text-gray-400">
      Next refresh in{" "}
      <span className="text-emerald-400 font-semibold">{timer}</span>{" "}
      seconds...
    </div>
  </div>
);

}
