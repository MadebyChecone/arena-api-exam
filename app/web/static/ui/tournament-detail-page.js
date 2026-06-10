import {
  cancelTournament,
  currentToken,
  getTournament,
  getTournamentSummary,
  listPlayers,
  recordMatchResult,
  startTournament,
} from "../utils/api.js";
import { $, showPanelError } from "../utils/dom.js";
import { handleApiError, redirectToLogin, showStatus } from "../utils/page.js";
import { renderBracket } from "./bracket-view.js";
import { renderSummary } from "./tournament-summary-view.js";

const tournamentId = Number(document.body.dataset.tournamentId);

let playersById = new Map();

function logout() {
  redirectToLogin();
}

async function loadTournamentPage() {
  showStatus("Loading…");
  $("#summary").textContent = "Loading summary…";
  $("#bracket").textContent = "Loading tournament tree…";

  let playerWarning = "";
  try {
    const players = await listPlayers();
    playersById = new Map(players.map((player) => [player.id, player]));
  } catch (error) {
    if (error.status === 401) {
      handleApiError(error);
      return;
    }
    playersById = new Map();
    playerWarning = `Could not load player names/ELO: ${error.message}`;
  }

  const [detailResult, summaryResult] = await Promise.allSettled([
    getTournament(tournamentId),
    getTournamentSummary(tournamentId),
  ]);

  const unauthorized = [detailResult, summaryResult].find(
    (result) => result.status === "rejected" && result.reason.status === 401,
  );
  if (unauthorized) {
    handleApiError(unauthorized.reason);
    return;
  }

  if (detailResult.status === "fulfilled") {
    const tournament = detailResult.value.tournament;
    $("#tournament-title").textContent = `${tournament.name} #${tournament.id}`;
    renderBracket(
      $("#bracket"),
      detailResult.value.matches || [],
      playersById,
    );
  } else {
    showPanelError($("#bracket"), detailResult.reason);
  }

  if (summaryResult.status === "fulfilled") {
    renderSummary($("#summary"), summaryResult.value, playersById);
  } else {
    showPanelError($("#summary"), summaryResult.reason);
  }

  showStatus(playerWarning, Boolean(playerWarning));
}

async function recordResult(matchId, winnerId) {
  showStatus(`Recording result for match #${matchId}…`);

  try {
    await recordMatchResult(matchId, winnerId);
    await loadTournamentPage();
    showStatus("Result recorded.");
  } catch (error) {
    handleApiError(error);
  }
}

async function changeTournamentStatus(action) {
  showStatus(`${action === "start" ? "Starting" : "Cancelling"} tournament…`);

  try {
    if (action === "start") {
      await startTournament(tournamentId);
    } else if (action === "cancel") {
      await cancelTournament(tournamentId);
    }

    await loadTournamentPage();
    showStatus("Tournament status updated.");
  } catch (error) {
    handleApiError(error);
  }
}

$("#logout-button").addEventListener("click", logout);
$("#refresh-button").addEventListener("click", loadTournamentPage);

$("#summary").addEventListener("click", (event) => {
  const button = event.target.closest?.("[data-tournament-status]");
  if (!button) {
    return;
  }

  changeTournamentStatus(button.dataset.tournamentStatus);
});

$("#bracket").addEventListener("click", (event) => {
  const button = event.target.closest?.("[data-record-result]");
  if (!button) {
    return;
  }

  recordResult(Number(button.dataset.matchId), Number(button.dataset.winnerId));
});

if (!currentToken()) {
  redirectToLogin();
} else {
  loadTournamentPage();
}
