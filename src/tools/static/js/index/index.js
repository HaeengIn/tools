/**
 * Fill HTML Elements
 */

// Usage Paragragh
const basicUsage = document.getElementById("basicUsage");
const datetimeUsage = document.getElementById("datetimeUsage");
const formatUsage = document.getElementById("formatUsage");

basicUsage.textContent = "Here is a simple example of basic usage:";
datetimeUsage.innerHTML =
  "..Also you can convert string type data to <b>datetime</b> type data if you use <b>toDatetime()</b>";
formatUsage.textContent = "..or use any date format you want!";

// Installation Paragraph
const pip = document.getElementById("pip");
const uv = document.getElementById("uv");

pip.innerHTML = "Install <b>getKST</b> via pip:";
uv.textContent = "..or install via uv.";

// GitHub Link Button
const github = document.getElementById("github");

github.textContent = "GitHub";
