const assets = [
	"/",
	"/index.html",
	"/static/css/style.css",
	"/static/css/bootstrap.min.css",
	"/static/js/app.js",
	"/static/js/bootstrap.bundle.min.js",
	"/static/js/serviceWorker.js",
	"/static/manifest.json",
	"/templates/index.html",
	"/templates/layout.html",
	"/templates/partials/navbar.html",
	"/templates/partials/register.html",
	"/templates/partials/login.html",
	"/templates/login_success.html",
    /* add other files that are loaded here (both code files and images) */,
],
	CATALOGUE_ASSETS = "catalogue-assets";
self.addEventListener("install", (e) => {
	e.waitUntil(
		caches
			.open(CATALOGUE_ASSETS)
			.then((e) => {
				console.log(e), e.addAll(assets);
			})
			.then(self.skipWaiting())
			.catch((e) => {
				console.log(e);
			})
	);
}),
	self.addEventListener("activate", function (e) {
		e.waitUntil(
			caches
				.keys()
				.then((e) =>
					Promise.all(
						e.map((e) => {
							if (e === CATALOGUE_ASSETS)
								return (
									console.log("Removed old cache from", e),
									caches.delete(e)
								);
						})
					)
				)
				.then(() => self.clients.claim())
		);
	}),
	self.addEventListener("fetch", function (e) {
		e.respondWith(
			fetch(e.request).catch(async () => {
				const s = await caches.open(CATALOGUE_ASSETS);
				return await s.match(e.request);
			})
		);
	});