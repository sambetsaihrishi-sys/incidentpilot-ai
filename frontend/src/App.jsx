import { useState } from "react";
import "./App.css";

const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8001";

function App() {
  const [form, setForm] = useState({
    service: "payment-api",
    status_code: 500,
    error_message: "",
    endpoint: "/api/payment",
    response_time_ms: 12000,
    severity: "HIGH",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const [resolution, setResolution] = useState({
    root_cause: "",
    resolution: "",
    resolution_time_minutes: 10,
  });

  const [resolveMessage, setResolveMessage] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]:
        e.target.name === "status_code" ||
        e.target.name === "response_time_ms"
          ? Number(e.target.value)
          : e.target.value,
    });
  };

  const analyzeIncident = async (e) => {
    e.preventDefault();

    setLoading(true);
    setResult(null);
    setResolveMessage("");

    try {
      const response = await fetch(`${API_URL}/incidents/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to create incident");
      }

      setResult(data);
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  const resolveIncident = async () => {
    if (!result?.incident_id) return;

    try {
      const response = await fetch(
        `${API_URL}/incidents/${result.incident_id}/resolve`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            ...resolution,
            resolution_time_minutes: Number(
              resolution.resolution_time_minutes
            ),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to resolve incident");
      }

      setResolveMessage(
        data.memory_saved
          ? "Incident resolved and learned by Hindsight ✓"
          : "Incident resolved, but memory could not be stored."
      );
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div className="app">
      <header>
        <div>
          <h1>⚡ IncidentPilot AI</h1>
          <p>Memory-powered incident response using Hindsight</p>
        </div>

        <span className="status">● Hindsight Connected</span>
      </header>

      <main>
        <section className="card incident-card">
          <div className="section-title">
            <div>
              <span className="step">01</span>
              <h2>New Production Incident</h2>
            </div>
          </div>

          <form onSubmit={analyzeIncident}>
            <div className="grid">
              <label>
                Service
                <input
                  name="service"
                  value={form.service}
                  onChange={handleChange}
                />
              </label>

              <label>
                Status Code
                <input
                  type="number"
                  name="status_code"
                  value={form.status_code}
                  onChange={handleChange}
                />
              </label>

              <label>
                Endpoint
                <input
                  name="endpoint"
                  value={form.endpoint}
                  onChange={handleChange}
                />
              </label>

              <label>
                Severity
                <select
                  name="severity"
                  value={form.severity}
                  onChange={handleChange}
                >
                  <option>LOW</option>
                  <option>MEDIUM</option>
                  <option>HIGH</option>
                  <option>CRITICAL</option>
                </select>
              </label>
            </div>

            <label>
              Error Message
              <textarea
                name="error_message"
                value={form.error_message}
                onChange={handleChange}
                placeholder="Example: PostgreSQL connections are timing out..."
                required
              />
            </label>

            <label>
              Response Time (ms)
              <input
                type="number"
                name="response_time_ms"
                value={form.response_time_ms}
                onChange={handleChange}
              />
            </label>

            <button className="primary" type="submit" disabled={loading}>
              {loading
                ? "Searching Hindsight Memory..."
                : "Analyze Incident"}
            </button>
          </form>
        </section>

        {result && (
          <>
         
          <section className="memory-proof">
  <div>
    <span className="proof-label">HINDSIGHT MEMORY STATUS</span>

    <h3>
      {result.similar_incidents?.length > 0
        ? "Previous experience found"
        : "Cold start — no previous experience"}
    </h3>

    <p>
      {result.similar_incidents?.length > 0
        ? `IncidentPilot recalled ${result.similar_incidents.length} relevant memories and used them to improve this diagnosis.`
        : "IncidentPilot has not seen a similar incident yet. Resolve it to teach the agent for the future."}
    </p>
  </div>

  <div className="proof-count">
    {result.similar_incidents?.length || 0}
    <span>memories recalled</span>
  </div>
</section>
            <div className="two-column">
              <section className="card">
                <div className="section-title">
                  <div>
                    <span className="step">02</span>
                    <h2>Hindsight Memory</h2>
                  </div>
                </div>

                <p className="subtext">
                  Similar incidents recalled from persistent memory
                </p>

                {result.similar_incidents?.length > 0 ? (
                  result.similar_incidents.map((memory, index) => (
                    <div className="memory" key={index}>
                      <span className="memory-number">
                        {index + 1}
                      </span>
                      <p>{memory}</p>
                    </div>
                  ))
                ) : (
                  <div className="empty">
                    No previous matching incidents found.
                  </div>
                )}
              </section>

              <section className="card recommendation">
                <div className="section-title">
                  <div>
                    <span className="step">03</span>
                    <h2>AI Recommendation</h2>
                  </div>
                </div>

                <p className="subtext">
                  Generated using the current incident + recalled memories
                </p>

                <div className="recommendation-text">
                  {result.ai_recommendation}
                </div>
              </section>
            </div>

            <section className="card">
              <div className="section-title">
                <div>
                  <span className="step">04</span>
                  <h2>Resolve & Teach IncidentPilot</h2>
                </div>

                <span className="incident-id">
                  Incident #{result.incident_id}
                </span>
              </div>

              <p className="subtext">
                Confirm the solution so Hindsight can use this experience
                for future incidents.
              </p>

              <div className="grid">
                <label>
                  Root Cause
                  <textarea
                    value={resolution.root_cause}
                    onChange={(e) =>
                      setResolution({
                        ...resolution,
                        root_cause: e.target.value,
                      })
                    }
                    placeholder="What actually caused the incident?"
                  />
                </label>

                <label>
                  Successful Resolution
                  <textarea
                    value={resolution.resolution}
                    onChange={(e) =>
                      setResolution({
                        ...resolution,
                        resolution: e.target.value,
                      })
                    }
                    placeholder="What fixed the incident?"
                  />
                </label>
              </div>

              <label>
                Resolution Time (minutes)
                <input
                  type="number"
                  value={resolution.resolution_time_minutes}
                  onChange={(e) =>
                    setResolution({
                      ...resolution,
                      resolution_time_minutes: e.target.value,
                    })
                  }
                />
              </label>

              <button
                className="resolve"
                onClick={resolveIncident}
                disabled={
                  !resolution.root_cause || !resolution.resolution
                }
              >
                Resolve & Save to Hindsight
              </button>

              {resolveMessage && (
                <div className="success">{resolveMessage}</div>
              )}
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default App;