document.addEventListener("DOMContentLoaded", () => {
    let timerInterval = null;
    let secondsElapsed = 0;
    let isRunning = false;
    let lapCount = 0;

    const display = document.getElementById("display");
    const splitInput = document.getElementById("split-name");
    const statusLog = document.getElementById("status-log");
    const lapList = document.getElementById("lap-list");
    const startBtn = document.getElementById("start-btn");

    const formatTime = (totalSeconds) => {
        const h = String(Math.floor(totalSeconds / 3600)).padStart(2, '0');
        const m = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, '0');
        const s = String(totalSeconds % 60).padStart(2, '0');
        return `${h}:${m}:${s}`;
    };

    const showLog = (msg, isError = false) => {
        statusLog.style.display = "block";
        statusLog.style.color = isError ? "var(--danger)" : "var(--success)";
        statusLog.style.borderColor = isError ? "rgba(239, 68, 68, 0.3)" : "rgba(16, 185, 129, 0.3)";
        statusLog.style.background = isError ? "rgba(239, 68, 68, 0.1)" : "rgba(16, 185, 129, 0.1)";
        statusLog.innerText = `> ${msg}`;
        setTimeout(() => { statusLog.style.display = "none"; }, 4000);
    };

    const addLapToUI = (timeString, splitName) => {
        lapCount++;
        const li = document.createElement("li");
        li.className = "lap-item";
        li.innerHTML = `<span class="lap-number">Lap ${String(lapCount).padStart(2, '0')}</span> <span>${splitName}</span> <span>${timeString}</span>`;
        lapList.prepend(li);
    };

    document.getElementById("start-btn").addEventListener("click", () => {
        if (isRunning) return;
        isRunning = true;
        startBtn.innerText = "Running...";
        startBtn.style.background = "#059669";
        
        timerInterval = setInterval(() => {
            secondsElapsed++;
            display.innerText = formatTime(secondsElapsed);
        }, 1000);
    });

    document.getElementById("lap-btn").addEventListener("click", () => {
        if (!isRunning && secondsElapsed === 0) return;
        const currentSplit = splitInput.value.trim() || "Uncategorized";
        addLapToUI(formatTime(secondsElapsed), currentSplit);
    });

    document.getElementById("stop-btn").addEventListener("click", async () => {
        if (!isRunning && secondsElapsed === 0) return;
        
        clearInterval(timerInterval);
        isRunning = false;
        startBtn.innerText = "Start";
        startBtn.style.background = "var(--success)";
        
        const finalSplitName = splitInput.value.trim() || "Master Session";
        const recordedDuration = secondsElapsed;
        
        // Auto-lap the final time
        addLapToUI(formatTime(recordedDuration), finalSplitName + " (Final)");
        
        try {
            const response = await fetch("/api/track", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ split_name: finalSplitName, duration_seconds: recordedDuration })
            });

            const result = await response.json();
            if (result.status === "success") {
                showLog(`Session [${result.recorded_split}] saved to database.`);
            } else {
                showLog("Server rejected the payload.", true);
            }
        } catch (error) {
            showLog(`Database disconnected. ${error.message}`, true);
        }

        // Reset timer but keep laps visible until next start
        secondsElapsed = 0;
        display.innerText = "00:00:00";
    });
});