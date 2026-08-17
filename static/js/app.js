// Arkas 2. El Pazarlama AI - Frontend Application Logic

let currentVehicles = [];
let selectedVehicle = null;
let currentBrand = "all";
let currentBodyType = "all";
let currentSearch = "";
let currentModalTab = "safe";
let currentModalPosterType = "post";

// DOM Elements
const postersGrid = document.getElementById("posters-grid");
const searchInput = document.getElementById("search-input");
const bodyTypeFilter = document.getElementById("body-type-filter");
const brandTabsContainer = document.getElementById("brand-tabs");
const resultsCount = document.getElementById("results-count");
const btnRunPipeline = document.getElementById("btn-run-pipeline");
const btnRefresh = document.getElementById("btn-refresh");

// Stats Elements
const statVehicles = document.getElementById("stat-vehicles");
const statPosters = document.getElementById("stat-posters");
const statCopies = document.getElementById("stat-copies");
const statBrands = document.getElementById("stat-brands");

// Modal Elements
const modal = document.getElementById("creative-modal");
const modalCloseBtn = document.getElementById("modal-close-btn");
const modalPosterImg = document.getElementById("modal-poster-img");
const btnDownloadPoster = document.getElementById("btn-download-poster");
const modalBrandTag = document.getElementById("modal-brand-tag");
const modalVehicleTitle = document.getElementById("modal-vehicle-title");
const modalSpecsSub = document.getElementById("modal-specs-sub");
const modalCopyContainer = document.getElementById("modal-copy-container");
const btnViewPost = document.getElementById("btn-view-post");
const btnViewBanner = document.getElementById("btn-view-banner");
const tabSafe = document.getElementById("tab-safe");
const tabBold = document.getElementById("tab-bold");
const tabStory = document.getElementById("tab-story");
const btnCopyText = document.getElementById("btn-copy-text");
const btnRegenerateSingle = document.getElementById("btn-regenerate-single");

// Toast
const toast = document.getElementById("toast");
const toastMessage = document.getElementById("toast-message");

function showToast(msg, duration = 3000) {
  toastMessage.innerText = msg;
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, duration);
}

// Format Currency
function formatCurrency(val) {
  return new Intl.NumberFormat('tr-TR').format(val) + " TL";
}

function formatKM(val) {
  return new Intl.NumberFormat('tr-TR').format(val) + " KM";
}

// Fetch Stats
async function loadStats() {
  try {
    const res = await fetch("/api/stats");
    const data = await res.json();
    statVehicles.innerText = data.total_vehicles;
    statPosters.innerText = data.total_posters;
    statCopies.innerText = data.total_copies;
    statBrands.innerText = data.brands.length;
  } catch (err) {
    console.error("Error loading stats:", err);
  }
}

// Fetch Brands for Tabs
async function loadBrands() {
  try {
    const res = await fetch("/api/brands");
    const brands = await res.json();
    
    brandTabsContainer.innerHTML = `<button class="brand-tab ${currentBrand === 'all' ? 'active' : ''}" data-brand="all">Tümü</button>`;
    
    brands.forEach(b => {
      const btn = document.createElement("button");
      btn.className = `brand-tab ${currentBrand === b ? 'active' : ''}`;
      btn.dataset.brand = b;
      btn.innerText = b;
      btn.addEventListener("click", () => {
        document.querySelectorAll(".brand-tab").forEach(t => t.classList.remove("active"));
        btn.classList.add("active");
        currentBrand = b;
        loadVehicles();
      });
      brandTabsContainer.appendChild(btn);
    });

    // Event listener for "all" tab
    brandTabsContainer.querySelector('[data-brand="all"]').addEventListener("click", (e) => {
      document.querySelectorAll(".brand-tab").forEach(t => t.classList.remove("active"));
      e.target.classList.add("active");
      currentBrand = "all";
      loadVehicles();
    });
  } catch (err) {
    console.error("Error loading brands:", err);
  }
}

// Fetch Vehicles & Posters
async function loadVehicles() {
  resultsCount.innerText = "İlanlar ve afişler taranıyor...";
  postersGrid.innerHTML = `
    <div style="grid-column: 1 / -1; text-align: center; padding: 60px; color: var(--text-muted);">
      <div style="font-size: 2rem; margin-bottom: 12px;">⏳</div>
      <div>Veritabanından afişler yükleniyor...</div>
    </div>
  `;

  const params = new URLSearchParams();
  if (currentBrand && currentBrand !== "all") params.append("brand", currentBrand);
  if (currentBodyType && currentBodyType !== "all") params.append("body_type", currentBodyType);
  if (currentSearch) params.append("search", currentSearch);

  try {
    const res = await fetch(`/api/vehicles?${params.toString()}`);
    currentVehicles = await res.json();
    renderPostersGrid();
    loadStats();
  } catch (err) {
    postersGrid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 60px; color: #EF4444;">
        Afişler yüklenirken bir hata oluştu. Lütfen backend sunucusunu kontrol edin.
      </div>
    `;
  }
}

// Render Posters Grid
function renderPostersGrid() {
  resultsCount.innerText = `${currentVehicles.length} araç afişi listelendi`;
  postersGrid.innerHTML = "";

  if (currentVehicles.length === 0) {
    postersGrid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 80px 20px; background: var(--bg-card); border-radius: var(--radius-lg); border: 1px dashed var(--border-color);">
        <div style="font-size: 3rem; margin-bottom: 16px;">🚗</div>
        <h3 style="margin-bottom: 8px;">Henüz İlan veya Afiş Bulunamadı</h3>
        <p style="color: var(--text-muted); margin-bottom: 20px;">Yukarıdaki "⚡ Scraper & AI Motorunu Çalıştır" butonuna basarak ilk ilanları ve afişleri üretebilirsiniz.</p>
        <button onclick="runPipeline()" class="btn btn-primary">⚡ Şimdi Çalıştır</button>
      </div>
    `;
    return;
  }

  currentVehicles.forEach(vehicle => {
    const postPoster = vehicle.posters.find(p => p.poster_type === "instagram_post") || vehicle.posters[0];
    const posterImgUrl = postPoster ? postPoster.file_url : (vehicle.primary_image_url || "/static/placeholder.png");

    const card = document.createElement("div");
    card.className = "poster-card";
    card.innerHTML = `
      <div class="poster-preview-wrapper">
        <img class="poster-preview-img" src="${posterImgUrl}" alt="${vehicle.brand} ${vehicle.model}" loading="lazy">
        <div class="poster-overlay-badge">4:5 Instagram Ready</div>
      </div>
      <div class="poster-card-body">
        <div class="vehicle-meta-top">
          <span class="card-brand-tag">${vehicle.brand}</span>
          <span class="card-year-tag">${vehicle.year} Model</span>
        </div>
        <h3 class="card-title">${vehicle.model} ${vehicle.sub_model || ''}</h3>
        <div class="card-specs-row">
          <span>📍 ${formatKM(vehicle.km)}</span>
          <span>⛽ ${vehicle.fuel_type || 'Benzin'}</span>
          <span>⚙️ ${vehicle.transmission || 'Otomatik'}</span>
        </div>
        <div class="card-price-row">
          <div class="card-price">${formatCurrency(vehicle.price)}</div>
          <div class="card-actions">
            <button class="btn-icon btn-view" title="Kreatif ve Metin Detayı">🔍</button>
            <a href="${posterImgUrl}" download="${vehicle.brand}_${vehicle.model}_afis.png" class="btn-icon" title="Afişi İndir">📥</a>
          </div>
        </div>
      </div>
    `;

    // Click triggers modal
    card.querySelector(".poster-preview-wrapper").addEventListener("click", () => openModal(vehicle));
    card.querySelector(".btn-view").addEventListener("click", () => openModal(vehicle));

    postersGrid.appendChild(card);
  });
}

// Modal Logic
function openModal(vehicle) {
  selectedVehicle = vehicle;
  currentModalTab = "safe";
  currentModalPosterType = "post";

  modalBrandTag.innerText = vehicle.brand.toUpperCase();
  modalVehicleTitle.innerText = `${vehicle.brand} ${vehicle.model} ${vehicle.sub_model || ''}`;
  modalSpecsSub.innerText = `${vehicle.year} Model • ${formatKM(vehicle.km)} • ${vehicle.fuel_type} • ${vehicle.transmission} • ${formatCurrency(vehicle.price)}`;

  updateModalPoster();
  updateModalCopy();

  modal.classList.add("active");
}

function updateModalPoster() {
  if (!selectedVehicle) return;
  const poster = selectedVehicle.posters.find(p => p.poster_type === (currentModalPosterType === "post" ? "instagram_post" : "banner")) || selectedVehicle.posters[0];
  const url = poster ? poster.file_url : selectedVehicle.primary_image_url;
  
  modalPosterImg.src = url;
  btnDownloadPoster.href = url;
  btnDownloadPoster.download = `${selectedVehicle.brand}_${selectedVehicle.model}_${currentModalPosterType}.png`;

  btnViewPost.classList.toggle("active", currentModalPosterType === "post");
  btnViewBanner.classList.toggle("active", currentModalPosterType === "banner");
}

function updateModalCopy() {
  if (!selectedVehicle) return;

  tabSafe.classList.toggle("active", currentModalTab === "safe");
  tabBold.classList.toggle("active", currentModalTab === "bold");
  tabStory.classList.toggle("active", currentModalTab === "story");

  const safeCopy = selectedVehicle.copies.find(c => c.variant === "safe");
  const boldCopy = selectedVehicle.copies.find(c => c.variant === "bold");

  if (currentModalTab === "safe") {
    if (safeCopy) {
      modalCopyContainer.innerText = `${safeCopy.headline}\n\n${safeCopy.body}\n\n${safeCopy.cta}\n\n${(safeCopy.hashtags || []).join(" ")}`;
    } else {
      modalCopyContainer.innerText = "Kurumsal metin henüz oluşturulmadı.";
    }
  } else if (currentModalTab === "bold") {
    if (boldCopy) {
      modalCopyContainer.innerText = `${boldCopy.headline}\n\n${boldCopy.body}\n\n${boldCopy.cta}\n\n${(boldCopy.hashtags || []).join(" ")}`;
    } else {
      modalCopyContainer.innerText = "Dinamik/Bold metin henüz oluşturulmadı.";
    }
  } else if (currentModalTab === "story") {
    const copy = safeCopy || boldCopy;
    if (copy && copy.story_frames && copy.story_frames.length > 0) {
      const framesText = copy.story_frames.map(f => `🎬 Sahne ${f.scene}:\n${f.text}`).join("\n\n────────────────\n\n");
      modalCopyContainer.innerText = `📱 3 Slaytlık Instagram Hikaye Akışı:\n\n${framesText}`;
    } else {
      modalCopyContainer.innerText = "Hikaye akışı bulunamadı.";
    }
  }
}

// Modal Event Listeners
btnViewPost.addEventListener("click", () => {
  currentModalPosterType = "post";
  updateModalPoster();
});

btnViewBanner.addEventListener("click", () => {
  currentModalPosterType = "banner";
  updateModalPoster();
});

tabSafe.addEventListener("click", () => {
  currentModalTab = "safe";
  updateModalCopy();
});

tabBold.addEventListener("click", () => {
  currentModalTab = "bold";
  updateModalCopy();
});

tabStory.addEventListener("click", () => {
  currentModalTab = "story";
  updateModalCopy();
});

modalCloseBtn.addEventListener("click", () => {
  modal.classList.remove("active");
});

modal.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.classList.remove("active");
  }
});

btnCopyText.addEventListener("click", () => {
  const text = modalCopyContainer.innerText;
  navigator.clipboard.writeText(text).then(() => {
    showToast("📋 Reklam metni panoya kopyalandı!");
  });
});

btnRegenerateSingle.addEventListener("click", async () => {
  if (!selectedVehicle) return;
  btnRegenerateSingle.disabled = true;
  btnRegenerateSingle.innerText = "⏳ Üretiliyor...";

  try {
    const res = await fetch(`/api/pipeline/generate-single/${selectedVehicle.id}`, { method: "POST" });
    const data = await res.json();
    if (data.status === "success") {
      showToast("✨ Kreatif ve afişler yeniden üretildi!");
      const detailRes = await fetch(`/api/vehicles/${selectedVehicle.id}`);
      selectedVehicle = await detailRes.json();
      updateModalPoster();
      updateModalCopy();
      loadVehicles();
    }
  } catch (err) {
    showToast("❌ Yeniden üretim sırasında bir hata oluştu.");
  } finally {
    btnRegenerateSingle.disabled = false;
    btnRegenerateSingle.innerText = "⚡ Yeniden Üret";
  }
});

// Run Pipeline (Scraper + Agent + Poster Engine)
async function runPipeline() {
  btnRunPipeline.disabled = true;
  btnRunPipeline.innerHTML = `<span>⏳ Taranıyor & Afişler Üretiliyor...</span>`;
  showToast("🚀 Scraper ve AI Afiş motoru başlatıldı. Lütfen bekleyin...");

  try {
    const res = await fetch("/api/pipeline/run", { method: "POST" });
    const data = await res.json();
    if (data.status === "success") {
      showToast(`🎉 Tamamlandı! ${data.scrape_stats.total} ilan işlendi, ${data.posters_rendered} afiş üretildi.`);
      await loadBrands();
      await loadVehicles();
    }
  } catch (err) {
    showToast("❌ Pipeline çalışırken bir hata oluştu.");
  } finally {
    btnRunPipeline.disabled = false;
    btnRunPipeline.innerHTML = `<span>⚡ Scraper & AI Motorunu Çalıştır</span>`;
  }
}

// Event Listeners
btnRunPipeline.addEventListener("click", runPipeline);
btnRefresh.addEventListener("click", () => {
  loadStats();
  loadBrands();
  loadVehicles();
  showToast("🔄 Veriler yenilendi.");
});

bodyTypeFilter.addEventListener("change", (e) => {
  currentBodyType = e.target.value;
  loadVehicles();
});

let searchDebounceTimer;
searchInput.addEventListener("input", (e) => {
  clearTimeout(searchDebounceTimer);
  searchDebounceTimer = setTimeout(() => {
    currentSearch = e.target.value.trim();
    loadVehicles();
  }, 300);
});

// Init on Page Load
document.addEventListener("DOMContentLoaded", () => {
  loadStats();
  loadBrands();
  loadVehicles();
});
