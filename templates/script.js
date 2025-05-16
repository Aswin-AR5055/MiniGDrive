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
                e.stopPropagation(); // Prevent click from propagating to overlay potentially
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
         // Optional: Close sidebar when clicking a sidebar item on mobile
         if (driveSidebar) {
             driveSidebar.addEventListener('click', (e) => {
                  // Check if screen is small and a sidebar link was clicked
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
            applyTheme(savedTheme || "light");
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

                 // Simulate progress
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
                              // Optional: Reset drop zone after submission attempt
                              // setTimeout(() => {
                              //     dropZoneContent.innerHTML = originalDropZoneHTML;
                              //     uploadStatus.textContent = '';
                              // }, 1500);
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
        });
