const uploadSection = document.getElementById("uploadSection");
const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadButton");
const uploadProgress = document.getElementById("uploadProgress");

uploadBtn.addEventListener("click", async () => {
  if (!selectedFiles.length) return;

  const sessionToken = sessionStorage.getItem("session_token");
  const formData = new FormData();

  formData.append("session_token", sessionToken);

  for (const file of selectedFiles) {
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

let selectedFiles = [];

fileInput.addEventListener("change", () => {
  for (const file of fileInput.files) {
    if (
      !selectedFiles.some((f) => f.name === file.name && f.size === file.size)
    ) {
      selectedFiles.push(file);
    }
  }

  renderFileList();
});

function renderFileList() {
  const filePreviewList = document.getElementById("filePreviewList");

  filePreviewList.innerHTML = "";

  for (let i = 0; i < selectedFiles.length; i++) {
    const file = selectedFiles[i];
    const img = document.createElement("img");
    const name = document.createElement("span");
    const removeButton = document.createElement("button");
    const item = document.createElement("div");

    img.src = URL.createObjectURL(file);
    img.onload = () => URL.revokeObjectURL(img.src);

    name.textContent = file.name;

    removeButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 10 10">
  <line x1="1" y1="1" x2="9" y2="9" stroke="white" stroke-width="2" stroke-linecap="round"/>
  <line x1="9" y1="1" x2="1" y2="9" stroke="white" stroke-width="2" stroke-linecap="round"/>
</svg>`;
    removeButton.className = "remove-button";
    removeButton.addEventListener("click", () => {
      selectedFiles.splice(i, 1);
      renderFileList();
    });

    item.appendChild(img);
    item.appendChild(name);
    item.appendChild(removeButton);
    item.className = "file-preview-item";
    filePreviewList.appendChild(item);
  }

  const dt = new DataTransfer();
  for (const file of selectedFiles) {
    dt.items.add(file);
  }
  fileInput.files = dt.files;
}
