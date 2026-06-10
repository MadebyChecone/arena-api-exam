import { escapeHtml } from "../utils/dom.js";

export function renderSummary(element, summary, playersById) {
  element.innerHTML = `
    <div class="summary-grid">
      ${summaryItem("Name", escapeHtml(summary.name))}
      ${summaryItem("Status", `<code>${escapeHtml(summary.status)}</code>`)}
      ${summaryItem("Round", summary.current_round)}
      ${summaryItem("Played", summary.matches_played)}
      ${summaryItem("Remaining", summary.matches_remaining)}
      ${summaryItem("Complete", summary.is_complete ? "yes" : "no")}
    </div>

    <div class="summary-section">
      <h3>Active players</h3>
      ${activePlayersList(summary.active_players, playersById)}
    </div>

    <div class="summary-section">
      <h3>Status</h3>
      ${statusActions()}
    </div>
  `;
}

function summaryItem(label, value) {
  return `
    <div class="summary-item">
      <small>${escapeHtml(label)}</small>
      <strong>${value}</strong>
    </div>
  `;
}

function activePlayersList(activePlayers, playersById) {
  if (activePlayers.length === 0) {
    return "<p>No active players.</p>";
  }

  return `
    <ul class="active-players">
      ${activePlayers
        .map((player) => activePlayerItem(player, playersById))
        .join("")}
    </ul>
  `;
}

function activePlayerItem(player, playersById) {
  const fullPlayer = playersById.get(player.id);
  const username = fullPlayer?.username || player.username;
  const elo = fullPlayer?.elo ?? "unknown";

  return `
    <li>
      <strong>${escapeHtml(username)}</strong>
      <small>#${player.id} · ELO ${escapeHtml(elo)}</small>
    </li>
  `;
}

function statusActions() {
  return `
    <div class="status-actions">
      <button type="button" data-tournament-status="start">Start</button>
      <button type="button" class="secondary" data-tournament-status="cancel">Cancel</button>
    </div>
  `;
}
