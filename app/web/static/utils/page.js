import { clearToken } from "./api.js";
import { $, showMessage } from "./dom.js";

const LOGIN_MESSAGE_KEY = "arena.loginMessage";

export function showStatus(message, isError = false) {
  showMessage($("#status-message"), message, isError);
}

export function redirectToLogin(message = "") {
  clearToken();
  if (message) {
    sessionStorage.setItem(LOGIN_MESSAGE_KEY, message);
  }
  window.location.href = "/web/login";
}

export function handleApiError(error) {
  if (error.status === 401) {
    redirectToLogin("Session expired. Please log in again.");
    return;
  }

  showStatus(error.message, true);
}

export function showStoredLoginMessage(element) {
  const savedMessage = sessionStorage.getItem(LOGIN_MESSAGE_KEY);
  if (!savedMessage) {
    return;
  }

  showMessage(element, savedMessage, true);
  sessionStorage.removeItem(LOGIN_MESSAGE_KEY);
}
