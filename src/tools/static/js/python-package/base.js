/**
 * Fill HTML Elements
 */

// Usage Paragraph
const basicUsage = document.getElementById("basicUsage");

basicUsage.textContent = "Here is a simple example of basic usage:";

// Installation Paragraph
const pip = document.getElementById("pip");
const packageName = pip.dataset.package;
const uv = document.getElementById("uv");

pip.innerHTML = `Install <b>${packageName}</b> via pip:`;
uv.textContent = "..or install via uv.";

// GitHub Link Button
const github = document.getElementById("github");

github.textContent = "GitHub";
