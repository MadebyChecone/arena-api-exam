import { currentToken, login, saveToken } from "../utils/api.js";
import { $, showMessage } from "../utils/dom.js";
import { showStoredLoginMessage } from "../utils/page.js";

if (currentToken()) {
  window.location.href = "/web/";
}

showStoredLoginMessage($("#login-message"));

$("#login-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  const form = new FormData(event.currentTarget);
  const username = String(form.get("username") || "").trim();
  const password = String(form.get("password") || "");

  showMessage($("#login-message"), "Logging in…");

  try {
    const result = await login(username, password);
    saveToken(result.access_token);
    window.location.href = "/web/";
  } catch (error) {
    showMessage($("#login-message"), error.message, true);
  }
});
