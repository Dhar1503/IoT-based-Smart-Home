// ====================================================
// IoT Smart Home Dashboard — with Live Simulation + Control Buttons
// ====================================================

async function api(path, method='GET', data=null) {
  const opt = { method, headers: {} };
  if (data) {
    opt.headers['Content-Type'] = 'application/json';
    opt.body = JSON.stringify(data);
  }
  const res = await fetch('/api' + path, opt);
  return res.json();
}

// Local simulated readings (frontend-only for presentation)
let simulatedData = [];

// Generate simulated sensor readings
function generateFakeEvent() {
  const rooms = ["Living Room", "Kitchen", "Bedroom", "Garage"];
  const room = rooms[Math.floor(Math.random() * rooms.length)];
  const temp = (25 + Math.random() * 15).toFixed(1);
  const hum = (40 + Math.random() * 30).toFixed(0);
  const alertChance = Math.random() < 0.15;
  const event_type = alertChance ? "alert" : "info";
  const message = alertChance
    ? `⚠️ Alert! Temperature ${temp}°C, Humidity ${hum}% in ${room}`
    : `Temperature ${temp}°C, Humidity ${hum}% in ${room}`;
  return {
    device_name: `${room} Sensor`,
    event_type,
    message,
    temperature: parseFloat(temp),
    humidity: parseInt(hum),
    timestamp: new Date().toISOString(),
  };
}

// Keep list fresh
function updateSimulatedData() {
  const e = generateFakeEvent();
  simulatedData.unshift(e);
  if (simulatedData.length > 20) simulatedData.pop();
}

// Render the dashboard
async function refreshDashboard() {
  try {
    const devices = await api('/devices').catch(() => []);
    let events = await api('/events').catch(() => []);
    if (!Array.isArray(events) || events.length === 0) events = simulatedData;

    // === Notifications ===
    const latest = events[0];
    const notEl = document.getElementById('notifications');
    if (latest) {
      const boxClass = latest.event_type === 'alert' ? 'alert-box' : 'info-box';
      notEl.innerHTML = `<div class="${boxClass}">${latest.message}</div>`;
    } else {
      notEl.innerHTML = `<div class="info-box">Monitoring sensors...</div>`;
    }

    // === Devices Section ===
    let devHTML = "";
    devices.forEach(d => {
      let status = d.status.toLowerCase();
      let isOn = status.includes('on') || status.includes('active') || status.includes('unlocked');
      let color = isOn ? 'green' : 'red';
      let icon = d.type === 'lock' ? (isOn ? '🔓' : '🔒') : (isOn ? '🟢' : '🔴');

      devHTML += `
        <div class="device-card">
          <div class="device-name">${icon} ${d.name} (${d.type})</div>
          <div>Status: <span style="color:${color};font-weight:bold;">${d.status}</span></div>
          <div>
            ${d.type === 'lock'
              ? `<button onclick="control(${d.id}, 'unlock')">Unlock</button>
                 <button onclick="control(${d.id}, 'lock')">Lock</button>`
              : `<button onclick="control(${d.id}, 'on')">On</button>
                 <button onclick="control(${d.id}, 'off')">Off</button>`
            }
          </div>
        </div>`;
    });
    document.getElementById('devices').innerHTML = devHTML || "<p>No devices found.</p>";

    // === Recent Events ===
    const evtHTML = events.slice(0, 8).map(e => {
      const cls = e.event_type === 'alert' ? 'alert' : 'info';
      return `
        <div class="event-item ${cls}">
          <strong>${e.device_name}</strong> — ${e.message}
          <div class="event-time">${new Date(e.timestamp).toLocaleTimeString()}</div>
        </div>`;
    }).join('');
    document.getElementById('events').innerHTML = evtHTML;

    // === Readings Table ===
    const readEl = document.getElementById('readings');
    readEl.innerHTML = events.slice(0, 6).map(e => {
      const color = e.event_type === 'alert' ? 'red' : 'green';
      return `
        <tr style="color:${color}">
          <td>${e.device_name}</td>
          <td>${e.temperature}°C</td>
          <td>${e.humidity}%</td>
          <td>${e.event_type.toUpperCase()}</td>
        </tr>`;
    }).join('');

  } catch (err) {
    console.error("Error:", err);
  }
}

// Control devices manually
async function control(id, action) {
  await api(`/device/${id}/control`, 'POST', { action });
  refreshDashboard();
}

// Refresh automatically
setInterval(() => { updateSimulatedData(); refreshDashboard(); }, 4000);
updateSimulatedData();
refreshDashboard();
