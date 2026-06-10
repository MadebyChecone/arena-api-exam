import { escapeHtml } from "../utils/dom.js";

export function renderBracket(element, matches, playersById) {
  if (matches.length === 0) {
    element.textContent = "No matches yet. Start the tournament first.";
    return;
  }

  const rounds = groupMatchesByRound(matches);
  const lastRound = rounds[rounds.length - 1][0];

  element.innerHTML = `
    <div class="bracket" aria-label="Tournament bracket">
      ${rounds
        .map(
          ([round, roundMatches]) => `
            <section class="bracket-round">
              <h3>${roundTitle(round, lastRound)}</h3>
              <div class="round-matches">
                ${roundMatches
                  .map((match) => matchCard(match, playersById))
                  .join("")}
              </div>
            </section>
          `,
        )
        .join("")}
    </div>
  `;
}

function groupMatchesByRound(matches) {
  const byRound = new Map();

  for (const match of matches) {
    if (!byRound.has(match.round)) {
      byRound.set(match.round, []);
    }
    byRound.get(match.round).push(match);
  }

  return [...byRound.entries()]
    .sort(([leftRound], [rightRound]) => leftRound - rightRound)
    .map(([round, roundMatches]) => [
      round,
      roundMatches.sort(
        (left, right) => left.slot_in_round - right.slot_in_round,
      ),
    ]);
}

function roundTitle(round, lastRound) {
  if (round === lastRound) {
    return "Final";
  }
  return `Round ${round}`;
}

function matchCard(match, playersById) {
  return `
    <article class="match-card">
      <header class="match-header">
        <strong>Match #${match.id}</strong>
        <small>slot ${match.slot_in_round}</small>
      </header>

      ${playerLine("A", match.player_a_id, match.winner_id, playersById)}
      ${playerLine("B", match.player_b_id, match.winner_id, playersById)}

      <footer class="match-footer">
        ${matchAction(match, playersById)}
      </footer>
    </article>
  `;
}

function playerLine(slot, playerId, winnerId, playersById) {
  const isWinner = playerId !== null && playerId === winnerId;
  const className = isWinner ? "match-player winner" : "match-player";
  const player = playerId === null ? null : playersById.get(playerId);
  const elo = player?.elo;

  return `
    <div class="${className}">
      <span>${slot}</span>
      <div class="match-player-name">
        <strong>${escapeHtml(playerLabel(playerId, playersById))}</strong>
        ${elo === undefined ? "" : `<small>ELO ${escapeHtml(elo)}</small>`}
      </div>
    </div>
  `;
}

function matchAction(match, playersById) {
  const winner =
    match.winner_id === null
      ? ""
      : `<p>Winner: <strong>${escapeHtml(playerLabel(match.winner_id, playersById))}</strong></p>`;

  const candidateIds = [match.player_a_id, match.player_b_id].filter(
    (playerId) => playerId !== null && playerId !== undefined,
  );

  if (candidateIds.length === 0) {
    return `${winner}<small>No player to submit yet.</small>`;
  }

  const readinessNote =
    candidateIds.length < 2
      ? "<small>Backend should reject this until both players are known.</small>"
      : "";

  return `
    ${winner}
    ${readinessNote}
    <div class="match-actions">
      ${candidateIds
        .map(
          (playerId) => `
            <button
              type="button"
              class="secondary"
              data-record-result
              data-match-id="${match.id}"
              data-winner-id="${playerId}"
            >Submit ${escapeHtml(playerLabel(playerId, playersById))} as winner</button>
          `,
        )
        .join("")}
    </div>
  `;
}

function playerLabel(playerId, playersById) {
  if (playerId === null || playerId === undefined) {
    return "TBD";
  }

  const player = playersById.get(playerId);
  return player ? `${player.username} (#${playerId})` : `Player #${playerId}`;
}
