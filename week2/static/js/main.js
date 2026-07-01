/**
 * main.js
 * Handles form interactions, calls the /generate endpoint, and renders the
 * returned Markdown safely into the output panel.
 */

(function () {
  const productNameEl = document.getElementById("productName");
  const descriptionEl = document.getElementById("description");
  const temperatureEl = document.getElementById("temperature");
  const topPEl = document.getElementById("topP");
  const tempValueEl = document.getElementById("tempValue");
  const topPValueEl = document.getElementById("topPValue");
  const platformSelector = document.getElementById("platformSelector");
  const generateBtn = document.getElementById("generateBtn");
  const generateBtnLabel = document.getElementById("generateBtnLabel");
  const errorMsg = document.getElementById("errorMsg");
  const outputSheet = document.getElementById("outputSheet");
  const outputEyebrow = document.getElementById("outputEyebrow");

  let selectedPlatform = null;

  // --- Dial value readouts --------------------------------------------
  temperatureEl.addEventListener("input", () => {
    tempValueEl.textContent = parseFloat(temperatureEl.value).toFixed(2);
  });
  topPEl.addEventListener("input", () => {
    topPValueEl.textContent = parseFloat(topPEl.value).toFixed(2);
  });

  // --- Channel (platform) selection ------------------------------------
  platformSelector.addEventListener("click", (e) => {
    const btn = e.target.closest(".channel-btn");
    if (!btn) return;

    document
      .querySelectorAll(".channel-btn")
      .forEach((b) => b.classList.remove("is-active"));
    btn.classList.add("is-active");
    selectedPlatform = btn.dataset.platform;
  });

  // --- Helpers -----------------------------------------------------------
  function showError(message) {
    errorMsg.textContent = message;
    errorMsg.hidden = false;
  }

  function clearError() {
    errorMsg.hidden = true;
    errorMsg.textContent = "";
  }

  function setLoading(isLoading) {
    generateBtn.disabled = isLoading;
    generateBtnLabel.textContent = isLoading ? "Generating…" : "Generate copy";
    outputSheet.classList.toggle("is-loading", isLoading);
  }

  function renderMarkdown(markdownText) {
    const rawHtml = marked.parse(markdownText, { breaks: true });
    const safeHtml = DOMPurify.sanitize(rawHtml);
    outputSheet.innerHTML = safeHtml;
  }

  // --- Main action ---------------------------------------------------
  generateBtn.addEventListener("click", async () => {
    clearError();

    const payload = {
      product_name: productNameEl.value.trim(),
      description: descriptionEl.value.trim(),
      platform: selectedPlatform,
      temperature: parseFloat(temperatureEl.value),
      top_p: parseFloat(topPEl.value),
    };

    if (!payload.product_name || !payload.description) {
      showError("Please enter a product name and description.");
      return;
    }
    if (!payload.platform) {
      showError("Please select a channel (LinkedIn / Instagram / Email).");
      return;
    }

    setLoading(true);
    outputSheet.innerHTML = '<p class="placeholder">Drafting your copy…</p>';
    outputEyebrow.textContent = `OUTPUT — ${payload.platform.toUpperCase()}`;

    try {
      const response = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong.");
      }

      renderMarkdown(data.markdown);
    } catch (err) {
      showError(err.message);
      outputSheet.innerHTML =
        '<p class="placeholder">Generation failed. Adjust your inputs and try again.</p>';
    } finally {
      setLoading(false);
    }
  });
})();