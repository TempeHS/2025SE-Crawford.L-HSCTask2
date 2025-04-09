if ("serviceWorker" in navigator) {
	window.addEventListener("load", function () {
		navigator.serviceWorker
			.register("/static/js/serviceWorker.js")
			.then((res) => console.log("service worker registered"))
			.catch((err) => console.log("service worker not registered", err));
	});
}

// Function to enable dark mode
function enableDarkMode() {
	document.body.classList.add("dark-mode");
	localStorage.setItem("darkMode", "enabled");
	console.log("Dark mode enabled");
}

// Function to disable dark mode
function disableDarkMode() {
	document.body.classList.remove("dark-mode");
	localStorage.setItem("darkMode", "disabled");
	console.log("Dark mode disabled");
}

document.addEventListener("DOMContentLoaded", function () {
	const darkModeSwitch = document.getElementById("darkModeSwitch");
	if (darkModeSwitch) {
		// Check if dark mode is enabled in local storage
		if (localStorage.getItem("darkMode") === "enabled") {
			document.body.classList.add("dark-mode");
			darkModeSwitch.checked = true;
		}

		darkModeSwitch.addEventListener("change", function (event) {
			if (event.target.checked) {
				enableDarkMode();
			} else {
				disableDarkMode();
			}
		});
	}
});

document.addEventListener('DOMContentLoaded', function () {
	const form = document.querySelector('#registerForm');
	form.addEventListener('submit', function (event) {
		event.preventDefault();
		const csrfToken = document.querySelector('input[name="csrf_token"]').value;
		const formData = new FormData(form);
		formData.append('csrf_token', csrfToken);

		fetch('/register', {
			method: 'POST',
			body: formData,
			headers: {
				'X-CSRFToken': csrfToken
			}
		})
			.then(response => response.json())
			.then(data => {
				console.log(data);
			})
			.catch(error => {
				console.error('Error:', error);
			});
	});
});

document.addEventListener('DOMContentLoaded', (event) => {
	const diaryTimeInput = document.querySelector('input[name="diary_time"]');
	if (diaryTimeInput) {
		const now = new Date();
		const year = now.getFullYear();
		const month = String(now.getMonth() + 1).padStart(2, '0');
		const day = String(now.getDate()).padStart(2, '0');
		const hours = String(now.getHours()).padStart(2, '0');
		const minutes = String(now.getMinutes()).padStart(2, '0');
		const localDatetime = `${year}-${month}-${day}T${hours}:${minutes}`;
		diaryTimeInput.value = localDatetime;
	}
});