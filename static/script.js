document.getElementById("predictForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const resultBox = document.getElementById("result");

    // Reset result box state
    resultBox.classList.remove("hidden");
    resultBox.style.background = "#fff3cd";
    resultBox.style.color = "#856404";
    resultBox.innerText = "Predicting land price...";

    // Collect input values
    const location = document.getElementById("location").value.trim();
    const totalSqft = Number(document.getElementById("sqft").value);
    const bath = Number(document.getElementById("bath").value);
    const bhk = Number(document.getElementById("bhk").value);

    // Basic validation (frontend-level)
    if (!location || totalSqft <= 0 || bath <= 0 || bhk <= 0) {
        resultBox.style.background = "#f8d7da";
        resultBox.style.color = "#721c24";
        resultBox.innerText = "Please enter valid values in all fields.";
        return;
    }

    const payload = {
        location: location,
        total_sqft: totalSqft,
        bath: bath,
        bhk: bhk
    };

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        // Handle non-200 responses explicitly
        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        // Display result cleanly
        resultBox.style.background = "linear-gradient(135deg, #e8f5e9, #d0f0d6)";
        resultBox.style.color = "#1b5e20";
        resultBox.innerHTML = `
            Estimated Land Price<br>
            <span style="font-size: 28px; font-weight: 800;">
                ₹ ${data.predicted_price_per_sqft} / sq.ft
            </span>
        `;

    } catch (error) {
        // Graceful error handling
        resultBox.style.background = "#f8d7da";
        resultBox.style.color = "#721c24";
        resultBox.innerText =
            "Prediction failed. Please check your input or try again later.";
    }
});
