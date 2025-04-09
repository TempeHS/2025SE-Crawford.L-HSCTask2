if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("static/js/serviceWorker.js")
      .then((res) => console.log("service worker registered"))
      .catch((err) => console.log("service worker not registered", err));
  });
}

document.addEventListener("DOMContentLoaded", function () {
  const navLinks = document.querySelectorAll(".nav-link");
  const currentUrl = window.location.pathname;

  navLinks.forEach((link) => {
    const linkUrl = link.getAttribute("href");
    if (linkUrl === currentUrl) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    } else {
      link.classList.remove("active");
      link.removeAttribute("aria-current");
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("search-form");
  const input = document.getElementById("search-input");

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const searchTerm = input.value.trim().toLowerCase();
    if (searchTerm) {
      highlightText(searchTerm);
    }
  });

  function highlightText(searchTerm) {
    const mainContent = document.querySelector("main");
    removeHighlights(mainContent);
    highlightTextNodes(mainContent, searchTerm);
  }

  function removeHighlights(element) {
    const highlightedElements = element.querySelectorAll("span.highlight");
    highlightedElements.forEach((el) => {
      el.replaceWith(el.textContent);
    });
  }

  function highlightTextNodes(element, searchTerm) {
    const regex = new RegExp(`(${searchTerm})`, "gi");
    const walker = document.createTreeWalker(
      element,
      NodeFilter.SHOW_TEXT,
      null,
      false
    );
    let node;
    while ((node = walker.nextNode())) {
      const parent = node.parentNode;
      if (
        parent &&
        parent.nodeName !== "SCRIPT" &&
        parent.nodeName !== "STYLE"
      ) {
        const text = node.nodeValue;
        const highlightedText = text.replace(
          regex,
          '<span class="highlight">$1</span>'
        );
        if (highlightedText !== text) {
          const tempDiv = document.createElement("div");
          tempDiv.innerHTML = highlightedText;
          while (tempDiv.firstChild) {
            parent.insertBefore(tempDiv.firstChild, node);
          }
          parent.removeChild(node);
        }
      }
    }
  }
});

// document.addEventListener("DOMContentLoaded", function () {
//   if (window.location.pathname === "/") {
//     const buttons = [
//       { id: "all", url: "/" },
//       { id: "python", url: "?lang=python" },
//       { id: "cpp", url: "?lang=cpp" },
//       { id: "bash", url: "?lang=bash" },
//       { id: "sql", url: "?lang=sql" },
//       { id: "html", url: "?lang=html" },
//       { id: "css", url: "?lang=css" },
//       { id: "js", url: "?lang=javascript" },
//       { id: "other", url: "?lang=other" },
//       { id: "unknown", url: "?lang=unknown" }
//     ];

//     buttons.forEach((button) => {
//       const element = document.getElementById(button.id);
//       if (element) {
//         element.addEventListener("click", function () {
//           window.location.href = button.url;
//         });
//       }
//     });
//   }
// });