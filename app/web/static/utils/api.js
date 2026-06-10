const TOKEN_KEY = "arena.token";

export function currentToken() {
  return sessionStorage.getItem(TOKEN_KEY);
}

export function saveToken(token) {
  sessionStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  sessionStorage.removeItem(TOKEN_KEY);
}

export async function login(username, password) {
  const form = new URLSearchParams();
  form.set("username", username);
  form.set("password", password);

  return api("/auth/login", {
    method: "POST",
    auth: false,
    body: form,
  });
}

export function listPlayers() {
  return api("/players");
}

export function listTournaments() {
  return api("/tournaments");
}

export function getTournament(tournamentId) {
  return api(`/tournaments/${tournamentId}`);
}

export function getTournamentSummary(tournamentId) {
  return api(`/tournaments/${tournamentId}/summary`);
}

export function startTournament(tournamentId) {
  return api(`/tournaments/${tournamentId}/start`, { method: "POST" });
}

export function cancelTournament(tournamentId) {
  return api(`/tournaments/${tournamentId}/cancel`, { method: "POST" });
}

export function recordMatchResult(matchId, winnerId) {
  return api(`/matches/${matchId}/result`, {
    method: "POST",
    json: { winner_id: winnerId },
  });
}

async function api(path, options = {}) {
  const headers = new Headers(options.headers || {});

  if (options.json !== undefined) {
    headers.set("Content-Type", "application/json");
  }

  if (options.auth !== false && currentToken()) {
    headers.set("Authorization", `Bearer ${currentToken()}`);
  }

  const response = await fetch(`/api${path}`, {
    method: options.method || "GET",
    headers,
    body:
      options.json !== undefined ? JSON.stringify(options.json) : options.body,
  });

  const text = await response.text();
  const data = parseResponseBody(text);

  if (!response.ok) {
    const error = new Error(apiErrorMessage(response, data));
    error.status = response.status;
    error.data = data;
    throw error;
  }

  return data;
}

function parseResponseBody(text) {
  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

function apiErrorMessage(response, data) {
  if (data && typeof data === "object" && "detail" in data) {
    if (Array.isArray(data.detail)) {
      return data.detail
        .map((item) => item.msg || JSON.stringify(item))
        .join(", ");
    }
    return String(data.detail);
  }

  if (typeof data === "string" && data.length > 0) {
    return data;
  }

  return `HTTP ${response.status} ${response.statusText}`;
}
