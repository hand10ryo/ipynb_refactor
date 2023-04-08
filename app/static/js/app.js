window.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("file-input");
  
  if (fileInput) {
    fileInput.addEventListener("change", async (e) => {
      const file = e.target.files[0];
      if (!file) {
        return;
      }

      document.getElementById("status").innerText = "Processing...";

      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("/refactor", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const jsonResponse = await response.json();
        const downloadLink = document.createElement("a");
        downloadLink.href = `/download/${jsonResponse.refactored_ipynb}`;
        downloadLink.innerText = "Download refactored notebook";
        document.getElementById("status").innerText = "";
        document.getElementById("result").innerHTML = "";
        document.getElementById("result").appendChild(downloadLink);
      } catch (error) {
        document.getElementById("status").innerText = "An error occurred:";
        document.getElementById("result").innerText = error;
      }
    });
  }
});
