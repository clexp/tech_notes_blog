(function () {
  "use strict";

  let searchIndex = null;
  let searchInitialized = false;

  // Wait for everything to be ready
  function initializeSearch() {
    console.log("Initializing search...");

    const searchInput = document.getElementById("search");
    const searchResults = document.getElementById("search-results");
    const searchResultsList = document.getElementById("search-results-list");

    // Check if elements exist
    if (!searchInput || !searchResults || !searchResultsList) {
      console.error("Search elements not found:", {
        searchInput: !!searchInput,
        searchResults: !!searchResults,
        searchResultsList: !!searchResultsList,
      });
      return false;
    }

    // Check if search index is available
    if (typeof window.searchIndex === "undefined") {
      console.error("window.searchIndex not available");
      return false;
    }

    // Load search index
    try {
      searchIndex = elasticlunr.Index.load(window.searchIndex);
      console.log("Search index loaded successfully");
    } catch (e) {
      console.error("Failed to load search index:", e);
      return false;
    }

    // Clear any existing event listeners by cloning the input
    const newSearchInput = searchInput.cloneNode(true);
    searchInput.parentNode.replaceChild(newSearchInput, searchInput);

    // Set up event listeners on the new input
    setupEventListeners(newSearchInput, searchResults, searchResultsList);

    searchInitialized = true;
    console.log("Search initialized successfully");
    return true;
  }

  function setupEventListeners(searchInput, searchResults, searchResultsList) {
    // Search function
    function performSearch(query) {
      if (!query || query.length < 2 || !searchIndex) {
        return [];
      }

      try {
        return searchIndex
          .search(query, {
            fields: {
              title: { boost: 2 },
              body: { boost: 1 },
            },
            bool: "OR",
          })
          .slice(0, 8);
      } catch (e) {
        console.error("Search error:", e);
        return [];
      }
    }

    // Create clean title from URL
    function getTitle(url) {
      const parts = url.split("/").filter(Boolean);
      const slug = parts[parts.length - 1] || "Home";
      return slug.replace(/-/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
    }

    // Convert absolute URL to relative for local development
    function convertToRelativeUrl(url) {
      // Handle both production URLs and ensure relative paths
      if (url.startsWith("https://blog.clexp.net")) {
        url = url.replace("https://blog.clexp.net", "");
      } else if (url.startsWith("http://127.0.0.1:")) {
        // Remove any localhost URL prefix
        url = url.replace(/^https?:\/\/127\.0\.0\.1:\d+/, "");
      } else if (url.startsWith("http://localhost")) {
        url = url.replace(/http:\/\/localhost:\d+/, "");
      }

      // Ensure URL starts with / for relative paths
      if (!url.startsWith("/")) {
        url = "/" + url;
      }

      // Remove any trailing /index.html if present
      url = url.replace(/\/index\.html$/, "/");

      return url;
    }

    // Display results
    function displayResults(results) {
      searchResultsList.innerHTML = "";

      if (results.length === 0) {
        searchResultsList.innerHTML =
          '<div class="no-results">No results found</div>';
        return;
      }

      results.forEach((result) => {
        const item = document.createElement("div");
        item.className = "search-result-item";
        const title = getTitle(result.ref);

        // Convert absolute URL to relative for local development
        let url = convertToRelativeUrl(result.ref);

        item.innerHTML = `<a href="${url}">${title}</a>`;
        searchResultsList.appendChild(item);
      });
    }

    // Input event
    searchInput.addEventListener("input", function (e) {
      const query = e.target.value.trim();

      if (query.length >= 2) {
        const results = performSearch(query);
        displayResults(results);
        searchResults.classList.remove("hidden");
      } else {
        searchResults.classList.add("hidden");
      }
    });

    // Keydown event
    searchInput.addEventListener("keydown", function (e) {
      const query = e.target.value.trim();

      if (e.key === "Enter" && query.length >= 2) {
        e.preventDefault();

        const results = performSearch(query);
        if (results.length > 0) {
          const url = convertToRelativeUrl(results[0].ref);
          searchResults.classList.add("hidden");
          window.location.href = url;
        }
      }

      if (e.key === "Escape") {
        searchResults.classList.add("hidden");
        searchInput.blur();
      }
    });

    // Focus event
    searchInput.addEventListener("focus", function () {
      const query = searchInput.value.trim();
      if (query.length >= 2) {
        const results = performSearch(query);
        displayResults(results);
        searchResults.classList.remove("hidden");
      }
    });

    // Click outside
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".search-container")) {
        searchResults.classList.add("hidden");
      }
    });

    console.log("Event listeners attached");
  }

  // Try to initialize when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      // Small delay to ensure all scripts have loaded
      setTimeout(initializeSearch, 100);
    });
  } else {
    // DOM already ready
    setTimeout(initializeSearch, 100);
  }

  // Fallback: try again after a longer delay
  setTimeout(function () {
    if (!searchInitialized) {
      console.log("Retrying search initialization...");
      initializeSearch();
    }
  }, 1000);

  // Export for debugging
  window.searchDebug = {
    reinitialize: initializeSearch,
    isInitialized: function () {
      return searchInitialized;
    },
    hasIndex: function () {
      return !!searchIndex;
    },
  };
})();
