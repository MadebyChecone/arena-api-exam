import { escapeHtml } from "../utils/dom.js";

export function renderTournaments(element, tournaments, selectedTournamentId = null) {
  if (tournaments.length === 0) {
    element.textContent = "No tournaments found.";
    return;
  }

  const rows = tournaments
    .map((tournament) => {
      const isSelected = tournament.id === selectedTournamentId;
      return `
        <tr>
          <td>${tournament.id}</td>
          <td>${escapeHtml(tournament.name)}</td>
          <td><code>${escapeHtml(tournament.status)}</code></td>
          <td>${tournament.max_players}</td>
          <td>
            <a
              role="button"
              class="${isSelected ? "contrast" : "secondary"}"
              href="/web/tournaments/${tournament.id}"
            >${isSelected ? "Viewing" : "Open"}</a>
          </td>
        </tr>
      `;
    })
    .join("");

  element.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Status</th>
          <th>Max players</th>
          <th></th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}
