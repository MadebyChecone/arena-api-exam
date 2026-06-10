export function $(selector) {
  return document.querySelector(selector);
}

export function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => {
    const replacements = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    };
    return replacements[char];
  });
}

export function showMessage(element, message, isError = false) {
  if (!message) {
    element.textContent = "";
    return;
  }

  const safeMessage = escapeHtml(message);
  element.innerHTML = isError ? `<mark>${safeMessage}</mark>` : safeMessage;
}

export function showPanelError(element, error) {
  element.innerHTML = `<mark>${escapeHtml(error.message)}</mark>`;
}
