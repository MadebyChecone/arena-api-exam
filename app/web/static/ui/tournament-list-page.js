import { currentToken, listTournaments } from "../utils/api.js";
import { $ } from "../utils/dom.js";
import { handleApiError, redirectToLogin, showStatus } from "../utils/page.js";
import { renderTournaments } from "./tournament-list-view.js";

function logout() {
  redirectToLogin();
}

async function loadTournaments() {
  showStatus("Loading…");

  try {
    const tournaments = await listTournaments();
    renderTournaments($("#tournaments"), tournaments);
    showStatus("");
  } catch (error) {
    handleApiError(error);
  }
}

$("#logout-button").addEventListener("click", logout);
$("#refresh-button").addEventListener("click", loadTournaments);

if (!currentToken()) {
  redirectToLogin();
} else {
  loadTournaments();
}
