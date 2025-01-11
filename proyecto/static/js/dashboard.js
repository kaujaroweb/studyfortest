document.addEventListener("DOMContentLoaded", () => {
    const difficultyButtons = document.querySelectorAll(".mt-4 button");

    const defaultButton = difficultyButtons[1];
    defaultButton.classList.add("bg-red-500", "text-white");

    difficultyButtons.forEach((button) => {
        button.addEventListener("click", () => {
            difficultyButtons.forEach((btn) => {
                btn.classList.remove("bg-red-500", "text-white");
            });
            button.classList.add("bg-red-500", "text-white");
        });
    });

    const dropArea = document.querySelector(".border-2");
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "application/pdf";
    fileInput.style.display = "none";

    const successSvg = `
      <svg class="w-12 h-12 text-green-500 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.5 11.5 11 14l4-4m6 2a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
      </svg>
    `;

    const handleFile = (file) => {
        if (file && file.type === "application/pdf") {
            dropArea.innerHTML = `
          <div class="flex items-center justify-center">
            ${successSvg}
            <p class="ml-2 text-gray-600 dark:text-gray-200">Archivo cargado correctamente: ${file.name}</p>
          </div>
        `;
            console.log("Archivo cargado correctamente:", file.name);
        } else {
            alert("Por favor, selecciona un archivo PDF válido.");
            console.log("Archivo no válido:", file.type);
        }
    };

    dropArea.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        handleFile(file);
    });

    dropArea.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropArea.classList.add("border-gray-400");
    });

    dropArea.addEventListener("dragleave", () => {
        dropArea.classList.remove("border-gray-400");
    });

    dropArea.addEventListener("drop", (event) => {
        event.preventDefault();
        dropArea.classList.remove("border-gray-400");
        const file = event.dataTransfer.files[0];
        handleFile(file);
    });

    dropArea.appendChild(fileInput);

    const createExamButton = document.querySelector("#create-exam");
    console.log("Botón encontrado:", createExamButton);

    const textOutput = document.querySelector("#text-output");

    createExamButton.addEventListener("click", () => {
        console.log("Botón clickeado"); 
        const file = fileInput.files[0];


        if (!file) {
            alert("Por favor, selecciona un archivo PDF antes de continuar.");
            console.log("No se ha seleccionado un archivo PDF.");
            return;
        }

        const formData = new FormData();
        formData.append("pdf", file);

        console.log("Enviando solicitud al backend...");

        fetch("/create/generate-questions/", {
            method: "POST",
            body: formData,
        })
            .then((response) => {
                console.log("Respuesta recibida del servidor:", response);
                return response.json();
            })
            .then((data) => {
                console.log("Datos de la respuesta:", data);

                if (data.success) {
                    textOutput.innerHTML = `
                        <h3 class="mt-4 text-lg font-semibold text-blue-600">Preguntas Generadas:</h3>
                        <pre class="whitespace-pre-wrap text-gray-600 dark:text-gray-200">${data.questions_and_answers}</pre>
                    `;
                    console.log("Preguntas generadas:", data.questions_and_answers);
                } else {
                    textOutput.innerHTML = `
                        <p class="text-red-500">Error: ${data.error}</p>
                    `;
                    console.log("Error en la respuesta:", data.error);
                }
            })
            .catch((error) => {
                console.error("Error al hacer la solicitud:", error);
                textOutput.innerHTML = `
                    <p class="text-red-500">Ocurrió un error al generar las preguntas.</p>
                `;
            });
    });
});
