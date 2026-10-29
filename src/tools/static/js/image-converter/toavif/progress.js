function startProgressStream(jobId) {
  const currentProgress = document.getElementById("currentProgress");
  const overallProgress = document.getElementById("overallProgress");
  const currentFilename = document.getElementById("currentFilename");
  const downloadSection = document.getElementById("downloadSection");
  const downloadList = document.getElementById("downloadList");
  const downloadZip = document.getElementById("downloadZip");

  const es = new EventSource(`/toavif/progress/${jobId}`);

  es.onmessage = (e) => {
    const data = JSON.parse(e.data);

    currentProgress.value = data.current_file_progress;
    overallProgress.value = data.overall_progress;
    currentFilename.textContent = data.current_file;

    if (data.status === "error") {
      es.close();
      return;
    }

    if (data.status === "done") {
      es.close();

      for (const filename of data.files) {
        const a = document.createElement("a");
        a.href = `/toavif/download/${jobId}/${encodeURIComponent(filename)}`;
        a.download = filename;

        const btn = document.createElement("button");
        btn.textContent = filename;
        a.appendChild(btn);
        downloadList.appendChild(a);
      }

      downloadZip.href = `/toavif/download/${jobId}`;
      downloadZip.download = `toAVIF_${jobId}.zip`;
      downloadSection.style.display = "block";
    }
  };
}