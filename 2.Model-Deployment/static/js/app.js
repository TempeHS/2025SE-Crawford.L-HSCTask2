if ("serviceWorker" in navigator) {
	window.addEventListener("load", function () {
		navigator.serviceWorker
			.register(`${window.location.origin}/static/js/serviceWorker.js`)
			.then((res) => console.log(`Service worker registered with scope: ${res.scope}`))
			.catch((err) => console.log("Service worker not registered. Error:", err.message, "Stack:", err.stack));
	});
}



// Function to validate the form inputs
const relHumElement = document.getElementById('rel_hum');
if (relHumElement) {
	relHumElement.addEventListener('invalid', function () {
		this.setCustomValidity('Please enter a value between 0 and 100.');
	});

	// Function to reset the custom validity message when the input is valid
	relHumElement.addEventListener('input', function () {
		this.setCustomValidity('');
	});
}

document.getElementById("predictionForm").addEventListener("submit", async function (event) {
	event.preventDefault(); // Prevent the default form submission

	// Collect form data
	const formData = {
		air_temp: document.getElementById("air_temp").value,
		dewpt: document.getElementById("dewpt").value,
		rel_hum: document.getElementById("rel_hum").value,
		press: document.getElementById("press").value,
		apparent_t: document.getElementById("apparent_t").value,
	};

	try {
		// Send data as JSON to the /predict endpoint
		const response = await fetch("/predict", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(formData),
		});

		// Handle the response
		const result = await response.json();
		console.log("Prediction result:", result);
		alert("Prediction result: " + JSON.stringify(result));
	} catch (error) {
		console.error("Error submitting form:", error);
		alert("An error occurred while submitting the form.");
	}
});

document.getElementById("predictionForm").addEventListener("submit", async function (event) {
	event.preventDefault();
	const formData = new FormData(event.target);
	const data = Object.fromEntries(formData.entries());

	const response = await fetch("/predict", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(data),
	});

	const result = await response.json();
	if (result.status === "success") {
		document.getElementById("windDir").textContent = result.prediction.wind_dir_deg;
		document.getElementById("windSpd").textContent = result.prediction.wind_spd_kmh;
		document.getElementById("gustSpd").textContent = result.prediction.gust_kmh;
		document.getElementById("predictionResults").style.display = "block";
	} else {
		alert("Error: " + result.message);
	}
});