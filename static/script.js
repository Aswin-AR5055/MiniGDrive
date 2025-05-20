const body = document.getElementById("body");
const themeIcon = document.getElementById("theme-icon");
const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const dropZone = document.getElementById('dropZone');
const dropZoneContent = document.getElementById('dropZoneContent');
const uploadProgress = document.getElementById('uploadProgress');
const uploadStatus = document.getElementById('uploadStatus');
const originalDropZoneHTML = dropZoneContent.innerHTML;

// --- Mobile Sidebar Toggle ---
const menuToggleBtn = document.getElementById('menuToggleBtn');
const sidebarOverlay = document.getElementById('sidebarOverlay');
const driveSidebar = document.getElementById('driveSidebar');

function openSidebar() {
    body.classList.add('sidebar-open');
}
function closeSidebar() {
    body.classList.remove('sidebar-open');
}

if (menuToggleBtn) {
    menuToggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (body.classList.contains('sidebar-open')) {
            closeSidebar();
        } else {
            openSidebar();
        }
    });
}
if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeSidebar);
}
if (driveSidebar) {
    driveSidebar.addEventListener('click', (e) => {
        if (window.innerWidth <= 992 && e.target.closest('.sidebar-item')) {
            closeSidebar();
        }
    });
}

// --- Theme Handling ---
function applyTheme(theme) {
    if (theme === "dark") {
        body.classList.add("dark-mode");
        themeIcon.textContent = "light_mode";
    } else {
        body.classList.remove("dark-mode");
        themeIcon.textContent = "dark_mode";
    }
}
function checkTheme() {
    const savedTheme = localStorage.getItem("theme");
    applyTheme(savedTheme || "dark");
}
function toggleDarkMode() {
    const isDark = body.classList.contains("dark-mode");
    const newTheme = isDark ? "light" : "dark";
    localStorage.setItem("theme", newTheme);
    applyTheme(newTheme);
}

// --- File Upload Handling ---
function handleFileUpload(files) {
    if (files.length > 0) {
        const file = files[0];
        uploadStatus.textContent = `Uploading ${file.name}...`;
        dropZoneContent.innerHTML = `
            <div class="d-flex flex-column align-items-center">
                <div class="gdrive-spinner">
                    <div class="triangle yellow"></div>
                    <div class="triangle green"></div>
                    <div class="triangle blue"></div>
                </div>
                <strong class="mt-2">Uploading ${file.name}</strong>
                <div class="upload-progress mt-2" id="uploadProgressInner" style="width: 0%; height: 4px;"></div>
            </div>`;
        const progressInner = document.getElementById('uploadProgressInner');
        let progress = 0;
        uploadProgress.style.width = '0%';
        progressInner.style.width = '0%';

        const interval = setInterval(() => {
            progress += 10;
            progressInner.style.width = `${progress}%`;
            if (progress >= 100) {
                clearInterval(interval);
                setTimeout(() => {
                    uploadForm.submit();
                }, 300);
            }
        }, 100);
    }
}

// --- Drag and Drop & Click ---
if (dropZone) {
    dropZone.addEventListener('click', (e) => {
        if (e.target === dropZone || dropZoneContent.contains(e.target)) {
            const spinner = dropZoneContent.querySelector('.spinner');
            if (!spinner) {
                fileInput.click();
            }
        }
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const spinner = dropZoneContent.querySelector('.spinner');
        if (!spinner) {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                handleFileUpload(files);
            }
        }
    });
} else {
    console.warn("Drop zone element not found.");
}

// --- Initial Setup ---
document.addEventListener('DOMContentLoaded', () => {
    checkTheme();

    // Set initial active sidebar item
    const myFilesLink = document.querySelector('.sidebar-item[href="#"]');
    if (myFilesLink) {
        myFilesLink.classList.add('active');
    }

    // --- File Preview Modal Logic ---
    const modalElem = document.getElementById('filePreviewModal');
    const modalTitle = document.getElementById('filePreviewTitle');
    const modalBody = document.getElementById('filePreviewBody');
    // Bootstrap modal instance (BS5)
    let filePreviewModal = null;
    if (modalElem && window.bootstrap) {
        filePreviewModal = new bootstrap.Modal(modalElem);
    }

    document.querySelectorAll('.file-card-thumbnail').forEach(cardThumb => {
        cardThumb.addEventListener('click', function(e) {
            e.stopPropagation();
            const card = cardThumb.closest('.file-card');
            const filename = card.getAttribute('data-filename');
            const ext = filename.split('.').pop().toLowerCase();
            let content = '';
            if (['jpg','jpeg','png','gif','webp','svg'].includes(ext)) {
                content = `<img src="/download/${filename}" class="img-fluid" alt="${filename}">`;
                showPreview(content, filename);
            } else if (ext === 'pdf') {
                content = `<embed src="/download/${filename}" type="application/pdf" width="100%" height="500px"/>`;
                showPreview(content, filename);
            } else if (['txt','md','py','js','css','html'].includes(ext)) {
                modalBody.innerHTML = `<div>Loading...</div>`;
                modalTitle.textContent = filename;
                fetch(`/download/${filename}`)
                    .then(res => res.text())
                    .then(text => {
                        showPreview(`<pre style="white-space: pre-wrap; max-height:400px;">${escapeHtml(text)}</pre>`, filename);
                    });
            } else {
                content = `<div>No preview available for this file type.</div>`;
                showPreview(content, filename);
            }
        });
    });

    function showPreview(content, title) {
        modalBody.innerHTML = content;
        modalTitle.textContent = title;
        if (filePreviewModal) filePreviewModal.show();
    }

    // --- Sorting & Filtering ---
    const fileGrid = document.querySelector('.file-grid');
    const allCards = Array.from(document.querySelectorAll('.file-card'));
    const sortFiles = document.getElementById('sortFiles');
    const fileSearch = document.getElementById('fileSearch');

    function renderCards(cards) {
        fileGrid.innerHTML = '';
        cards.forEach(card => fileGrid.appendChild(card));
    }

    if (sortFiles) {
        sortFiles.addEventListener('change', function() {
            let sorted = [...allCards];
            const val = this.value;
            sorted.sort((a, b) => {
                if(val === 'name') {
                    return a.dataset.filename.localeCompare(b.dataset.filename);
                } else if(val === 'date') {
                    // Most recent first
                    return (b.dataset.date || '').localeCompare(a.dataset.date || '');
                } else if(val === 'size') {
                    return (parseInt(b.dataset.size)||0) - (parseInt(a.dataset.size)||0);
                } else if(val === 'type') {
                    return a.dataset.type.localeCompare(b.dataset.type);
                }
            });
            renderCards(sorted);
        });
    }

    if (fileSearch) {
        fileSearch.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            allCards.forEach(card => {
                card.style.display = card.dataset.filename.toLowerCase().includes(query) ? '' : 'none';
            });
        });
    }
});

// --- Utility: Escape HTML for safe text preview ---
function escapeHtml(text) {
    return text.replace(/[&<>"'`=\/]/g, function (s) {
        return ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;',
            '`': '&#96;',
            '=': '&#61;',
            '/': '&#47;'
        })[s];
    });
}

// --- Animations (for use when adding/removing cards dynamically) ---
function animateAdd(card) {
    card.classList.add('fade-in');
    setTimeout(() => card.classList.remove('fade-in'), 300);
}
function animateDelete(card) {
    card.classList.add('fade-out');
    setTimeout(() => card.remove(), 300);
}
document.addEventListener("DOMContentLoaded", function() {
    const selectAll = document.getElementById("selectAll");
    const deleteBtn = document.getElementById("deleteSelectedBtn");

    function getFileCheckboxes() {
        return document.querySelectorAll('input[name="selected_files"]');
    }

    if (selectAll) {
        selectAll.addEventListener("change", function() {
            getFileCheckboxes().forEach(cb => cb.checked = selectAll.checked);
        });
    }

    // Uncheck "Select All" if any file is unchecked
    document.addEventListener("change", function(e) {
        if (e.target.name === "selected_files" && !e.target.checked && selectAll) {
            selectAll.checked = false;
        }
        // If all are checked, check "Select All"
        if (e.target.name === "selected_files" && selectAll) {
            const boxes = getFileCheckboxes();
            selectAll.checked = Array.from(boxes).every(cb => cb.checked);
        }
    });
    // --- Trash Section Select All & Delete Selected ---
    const selectAllTrash = document.getElementById("selectAllTrash");
    const deleteSelectedTrashBtn = document.getElementById("deleteSelectedTrashBtn");

    function getTrashCheckboxes() {
        return document.querySelectorAll('input[name="selected_trash_files"]');
    }

    if (selectAllTrash) {
        selectAllTrash.addEventListener("change", function() {
            getTrashCheckboxes().forEach(cb => cb.checked = selectAllTrash.checked);
        });
    }

    document.addEventListener("change", function(e) {
        if (e.target.name === "selected_trash_files" && !e.target.checked && selectAllTrash) {
            selectAllTrash.checked = false;
        }
        if (e.target.name === "selected_trash_files" && selectAllTrash) {
            const boxes = getTrashCheckboxes();
            selectAllTrash.checked = Array.from(boxes).every(cb => cb.checked);
        }
    });

    if (deleteSelectedTrashBtn) {
        deleteSelectedTrashBtn.addEventListener("click", function() {
            const selected = Array.from(getTrashCheckboxes()).filter(cb => cb.checked).map(cb => cb.value);
            if (selected.length === 0) {
                alert("No files selected.");
                return;
            }
            if (!confirm("Are you sure you want to permanently delete the selected files?")) return;

            fetch("/permadelete_selected", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({files: selected})
            })
            .then(res => {
                if (res.ok) location.reload();
                else alert("Failed to delete files.");
            });
        });
    }
    const restoreSelectedTrashBtn = document.getElementById("restoreSelectedTrashBtn");

if (restoreSelectedTrashBtn) {
    restoreSelectedTrashBtn.addEventListener("click", function() {
        const selected = Array.from(getTrashCheckboxes()).filter(cb => cb.checked).map(cb => cb.value);
        if (selected.length === 0) {
            alert("No files selected.");
            return;
        }
        fetch("/restore_selected", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({files: selected})
        })
        .then(res => {
            if (res.ok) location.reload();
            else alert("Failed to restore files.");
        });
    });
}

    if (deleteBtn) {
        deleteBtn.addEventListener("click", function() {
            const selected = Array.from(getFileCheckboxes()).filter(cb => cb.checked).map(cb => cb.value);
            if (selected.length === 0) {
                alert("No files selected.");
                return;
            }
            if (!confirm("Are you sure you want to delete the selected files?")) return;

            fetch("/delete_selected", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({files: selected})
            })
            .then(res => {
                if (res.ok) location.reload();
                else alert("Failed to delete files.");
            });
        });
    }
});