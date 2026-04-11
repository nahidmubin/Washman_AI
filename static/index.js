function autoResize(textarea) {
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}

function startListening() {
    const textarea = document.getElementById("userInput");

    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        alert("Sorry, your browser does not support speech recognition.");
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US"; //"bn-BD"
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = function (event) {
        const speechResult = event.results[0][0].transcript;
        textarea.value = speechResult;
        autoResize(textarea);
    };

    recognition.onerror = function (event) {
        alert("Speech recognition error: " + event.error);
    };
}

// Smooth scroll to HTMX response
document.body.addEventListener("htmx:sseMessage", function (event) {
    const el = document.getElementById("reply"); // your SSE element

    if (el) {
        el.scrollIntoView({ behavior: "auto", block: "end" });
    }
});
