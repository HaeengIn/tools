/**
 * Fill HTML Elements
 */

// Usage Paragragh
const typeHint = document.getElementById("typeHint");
const typeHintDetail = document.getElementById("typeHintDetail");

typeHint.textContent = "If you want to specify type, code like this:";
typeHintDetail.innerHTML =
  "Even if you do not perform this step, the default type for <b>'templates'</b> is Jinja2Templates.";
