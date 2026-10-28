const uploadSection = document.getElementById("uploadSection");
const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadButton");
const uploadProgress = document.getElementById("uploadProgress");

uploadBtn.addEventListener("click", async () => {
  const files = fileInput.files;

  if (!files.length) return;

  const sessionToken = sessionStorage.getItem("session_token");
  const formData = new FormData();

  formData.append("session_token", sessionToken);

  for (const file of files) {
    formData.append("files", file);
  }

  const xhr = new XMLHttpRequest();

  xhr.upload.onprogress = (e) => {
    if (!e.lengthComputable) return;
    const percent = (e.loaded / e.total) * 100;
    uploadProgress.value = percent;
  };

  xhr.onload = () => {
    if (xhr.status !== 200) return;
    const { job_id } = JSON.parse(xhr.responseText);
    sessionStorage.setItem("job_id", job_id);
    startProgressStream(job_id);
  };

  xhr.open("POST", "/toavif/upload");
  xhr.send(formData);
});

fileInput.addEventListener("change", () => {
  const filePreviewList = document.getElementById("filePreviewList");
  filePreviewList.innerHTML = "";

  for (const file of fileInput.files) {
    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    img.onload = () => URL.revokeObjectURL(img.src);

    const name = document.createElement("span");
    name.textContent = file.name;

    const item = document.createElement("div");
    item.className = "preview";
    item.appendChild(img);
    item.appendChild(name);
    filePreviewList.appendChild(item);
  }
});
