// Wait until the entire DOM is loaded before executing scripts
document.addEventListener("DOMContentLoaded", () => {
  // Modal elements for displaying product details
  const modal = document.getElementById("modal");
  const modalTitle = document.getElementById("modalTitle");
  const modalImage = document.getElementById("modalImage");
  const modalDescription = document.getElementById("modalDescription");

  // Filter UI container and product listing container
  const filterSection = document.getElementById("filterSection");
  const productList = document.getElementById("productList");

  // Define available filter categories and their values
  const collections = {
    type: ["hydraulic", "conveyor", "laser", "robotic", "mixer", "lift", "crane", "drill"],
    industry: ["automotive", "construction", "electronics", "warehouse", "mining"],
    function: ["cutting", "lifting", "transporting", "mixing", "drilling"]
  };

  // Dynamically creates a dropdown for each filter type (type, industry, function)
  function createFilterDropdown(filterType, options) {
    const select = document.createElement("select");
    select.id = `${filterType}Filter`;

    // Default option (All types, All industries, etc.)
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = `All ${filterType.charAt(0).toUpperCase() + filterType.slice(1)}s`;
    select.appendChild(defaultOption);

    // Add each option to the dropdown
    options.forEach((opt) => {
      const option = document.createElement("option");
      option.value = opt;
      option.textContent = opt.charAt(0).toUpperCase() + opt.slice(1);
      select.appendChild(option);
    });

    // Append the dropdown to the filter section
    filterSection.appendChild(select);

    // Attach change event to trigger filtering when user selects a value
    select.addEventListener("change", applyFilters);
  }

  // Create dropdowns for each collection category
  Object.entries(collections).forEach(([key, values]) => {
    createFilterDropdown(key, values);
  });

  // Filtering logic: shows only cards matching the selected filters
  function applyFilters() {
    const selectedType = document.getElementById("typeFilter").value;
    const selectedIndustry = document.getElementById("industryFilter").value;
    const selectedFunction = document.getElementById("functionFilter").value;

    const cards = productList.querySelectorAll(".product-card");
    cards.forEach((card) => {
      const matchesType = !selectedType || card.dataset.type === selectedType;
      const matchesIndustry = !selectedIndustry || card.dataset.industry === selectedIndustry;
      const matchesFunction = !selectedFunction || card.dataset.function === selectedFunction;

      // Only display cards that match all selected filters
      card.style.display = matchesType && matchesIndustry && matchesFunction ? "flex" : "none";
    });
  }

  // Handle clicks on product cards or "Request Quote" buttons
  document.addEventListener("click", (e) => {
    const isQuoteBtn = e.target.closest(".btn.quote"); // Detect click on quote button
    const isProductCardClick = e.target.closest(".product-card") && !e.target.closest(".btn"); // Avoid button inside card

    // When "Request Quote" is clicked
    if (isQuoteBtn) {
      const card = isQuoteBtn.closest(".product-card");
      const productName = card.querySelector(".product-name").textContent;

      // Fill the quote modal with the product name and open it
      document.getElementById("quoteProductName").value = productName;
      document.getElementById("quoteModal").style.display = "flex";
      return;
    }

    // When product card is clicked (excluding buttons), show modal with details
    if (isProductCardClick) {
      const card = e.target.closest(".product-card");
      modalTitle.textContent = card.querySelector(".product-name").textContent;
      modalImage.src = card.querySelector("img").src;
      modalDescription.textContent = card.querySelector(".product-description").textContent;
      modal.style.display = "flex";
    }
  });
});

// Closes the modal window when triggered
function closeModal() {
  document.getElementById("modal").style.display = "none";
}
