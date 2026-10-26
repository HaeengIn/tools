/**
 * Fill HTML Elements
 */
// Descriptions
const getkstDescription = document.getElementById("getkstDescription");
const autoTemplateDescription = document.getElementById(
  "autoTemplateDescription",
);
const toAvifDescription = document.getElementById("toAvifDescription");
const toJpgDescription = document.getElementById("toJpgDescription");

getkstDescription.innerHTML =
  "<b>getKST</b> is a most convenient Python Package for getting timezone data of <b>'Asia/Seoul'</b>.";
autoTemplateDescription.innerHTML =
  "<b>auto-template</b> is a convenient module that allows you to quickly set up Jinja2 templates in FastAPI.";
toAvifDescription.innerHTML = "<b>toAVIF</b> is a best solution if you want to convert images to AVIF format.";
toJpgDescription.innerHTML = "<b>toJPG</b> is a best solution if you want to convert images to JPG format.";


// Buttons
const getkstButton = document.getElementById("getkstButton");
const autoTemplateButton = document.getElementById("autoTemplateButton");
const toAvifTry = document.getElementById("toAvifTry");
const toAvifDetail = document.getElementById("toAvifDetail");
const toJpgTry = document.getElementById("toJpgTry");
const toJpgDetail = document.getElementById("toJpgDetail");

getkstButton.textContent = "View getKST";
autoTemplateButton.textContent = "View auto-template";
toAvifTry.textContent = "Try Now!";
toAvifDetail.textContent = "View Details";
toJpgTry.textContent = "Try Now!";
toJpgDetail.textContent = "View Details";