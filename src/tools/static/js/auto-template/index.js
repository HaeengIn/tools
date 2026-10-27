/**
 * Fill HTML Elements
 */

// Usage Paragragh
const basicUsage = document.getElementById("basicUsage");
const typeHint = document.getElementById("typeHint");
const typeHintDetail = document.getElementById("typeHintDetail");

basicUsage.textContent = "Here is a simple example of basic usage:";
typeHint.textContent = "If you want to specify type, code like this:"
typeHintDetail.innerHTML = "Even if you do not perform this step, the default type for <b>'templates'</b> is Jinja2Templates."

// Installation Paragraph
const pip = document.getElementById("pip");
const uv = document.getElementById("uv");

pip.innerHTML = "Install <b>auto-template</b> via pip:";
uv.textContent = "..or install via uv.";

// GitHub Link Button
const github = document.getElementById("github");

github.textContent = "GitHub";
