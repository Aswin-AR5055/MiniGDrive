let recognition;

const voiceBtn = document.getElementById('voice-command-btn');
const voiceCancelBtn = document.getElementById('voice-cancel-btn');
const voiceStatus = document.getElementById('voice-status');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
  alert("Your browser does not support voice recognition.");
  voiceBtn.disabled = true;
} else {
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'en-US';

  voiceBtn.onclick = () => {
    recognition.start();
    voiceStatus.textContent = "Listening...";
    voiceBtn.disabled = true;
    voiceCancelBtn.style.display = "inline-block";
    voiceBtn.classList.add('listening');
  };

  voiceCancelBtn.onclick = () => {
    recognition.abort();
    voiceStatus.textContent = "Error: aborted.";
    voiceBtn.disabled = false;
    voiceCancelBtn.style.display = "none";
    voiceBtn.classList.remove('listening');
    setTimeout(() => {
      voiceStatus.textContent = "";
    }, 2000);
  };

  recognition.onresult = (event) => {
    let command = event.results[0][0].transcript.toLowerCase().replace(/[.,!?]$/g, '').trim();
    voiceStatus.textContent = `Heard: "${command}"`;
    voiceBtn.disabled = false;
    voiceCancelBtn.style.display = "none";
    voiceBtn.classList.remove('listening');

    let recognized = false;

    if (command.includes('upload') && command.includes('file')) {
      document.getElementById('fileInput').click();
      recognized = true;
    } else if (command.includes('delete') && command.includes('file')) {
      const filename = command.split('file').pop().trim();
      deleteFileByName(filename);
      recognized = true;
    } else if (command.includes('list files')) {
      listFiles();
      recognized = true;
    } else if (command === 'logout' || command === 'log me out' || command.includes('sign out')) {
      voiceStatus.textContent = "Logging out...";
      window.location.href = "/logout";
      recognized = true;
    } else if (
      command.includes('trash') &&
      (
        command.includes('view') ||
        command.includes('open') ||
        command.includes('go to') ||
        command.includes('show') ||
        command.includes('check') ||
        command.includes('my') ||
        command.includes('take me to') ||
        command === 'trash'
      )
    ) {
      const trashLink = document.querySelector('a[href*="trash"]');
      if (trashLink) {
        trashLink.click();
        voiceStatus.textContent = "Opening Trash...";
        recognized = true;
      } else {
        voiceStatus.textContent = "Trash link not found.";
      }
    } else if (command === 'go to dashboard' || command.includes('view dashboard') || command.includes('open dashboard') || command.includes('dashboard')) {
      const dashboardLink = document.querySelector('a[href*="dashboard"]');
      if (dashboardLink) {
        dashboardLink.click();
        voiceStatus.textContent = "Opening Dashboard...";
        recognized = true;
      } else {
        voiceStatus.textContent = "Dashboard link not found.";
      }
    } else if (command === 'go to profile' || command.includes('view profile') || command.includes('open profile') || command.includes('profile')) {
      const profileLink = document.querySelector('a[href*="profile"]');
      if (profileLink) {
        profileLink.click();
        voiceStatus.textContent = "Opening Profile...";
        recognized = true;
      } else {
        voiceStatus.textContent = "Profile link not found.";
      }
    } else if (command === 'switch language to english' || command === 'change language to english' || command === 'english language') {
      setLanguage('en');
      voiceStatus.textContent = "Switched language to English.";
      recognized = true;
    } else if (command === 'switch language to tamil' || command === 'change language to tamil' || command === 'tamil language') {
      setLanguage('ta');
      voiceStatus.textContent = "மொழி தமிழ் ஆக மாற்றப்பட்டது.";
      recognized = true;
    } else if (command === 'switch language to hindi' || command === 'change language to hindi' || command === 'hindi language') {
      setLanguage('hi');
      voiceStatus.textContent = "भाषा हिंदी में बदल गई है।";
      recognized = true;
    } else if (command === 'switch to dark mode' || command === 'enable dark mode' || command === 'dark mode') {
      setTheme('dark');
      voiceStatus.textContent = "Switched to Dark Mode.";
      recognized = true;
    } else if (command === 'switch to light mode' || command === 'enable light mode' || command === 'light mode') {
      setTheme('light');
      voiceStatus.textContent = "Switched to Light Mode.";
      recognized = true;
    } else if (command.startsWith('search for')) {
      const searchTerm = command.replace('search for', '').trim();
      if (searchTerm) {
        searchFileByName(searchTerm);
        voiceStatus.textContent = `Searching for "${searchTerm}"...`;
        recognized = true;
      } else {
        voiceStatus.textContent = "Please specify a filename to search for.";
      }
    } else if (
      command.includes('favourite') || 
      command.includes('favorite') ||
      command.includes('view favourites') ||
      command.includes('open favourites') ||
      command.includes('go to favourites') ||
      command.includes('show favourites') ||
      command.includes('my favourites')
    ) {
      const favouritesLink = document.querySelector('a[href*="favourites"], a[href*="favorites"]');
      if (favouritesLink) {
        favouritesLink.click();
        voiceStatus.textContent = "Opening Favourites...";
        recognized = true;
      } else {
        voiceStatus.textContent = "Favourites link not found.";
      }
    } else {
      voiceStatus.textContent = "Command not recognized.";
    }

    if (!command.includes('logout') && !command.includes('log me out') && !command.includes('sign out')) {
      setTimeout(() => {
        voiceStatus.textContent = "";
      }, 2000);
    }
  };

  recognition.onerror = (event) => {
    voiceStatus.textContent = `Error: ${event.error}`;
    voiceBtn.disabled = false;
    voiceCancelBtn.style.display = "none";
    voiceBtn.classList.remove('listening');
  };

  recognition.onend = () => {
    voiceBtn.disabled = false;
    voiceCancelBtn.style.display = "none";
    voiceBtn.classList.remove('listening');
  };
}

// --- Helper Functions ---

function deleteFileByName(filename) {
  const fileCards = document.querySelectorAll('.file-card');
  let found = false;
  fileCards.forEach(card => {
    const name = card.getAttribute('data-filename');
    if (name && name.toLowerCase() === filename.toLowerCase()) {
      const deleteBtn = card.querySelector('a[title*="Trash"], a[title*="Move to Trash"]');
      if (deleteBtn) {
        deleteBtn.click();
        voiceStatus.textContent = `Deleting "${filename}"...`;
        found = true;
      }
    }
  });
  if (!found) {
    voiceStatus.textContent = `File "${filename}" not found.`;
  }
}

function openFileByName(filename) {
  const fileCards = document.querySelectorAll('.file-card');
  let found = false;
  fileCards.forEach(card => {
    const name = card.getAttribute('data-filename');
    if (name && name.toLowerCase() === filename.toLowerCase()) {
      const thumb = card.querySelector('.file-card-thumbnail');
      if (thumb) {
        thumb.click();
        voiceStatus.textContent = `Opening "${filename}"...`;
        found = true;
      }
    }
  });
  if (!found) {
    voiceStatus.textContent = `File "${filename}" not found.`;
  }
}

function listFiles() {
  const fileCards = document.querySelectorAll('.file-card');
  if (fileCards.length === 0) {
    voiceStatus.textContent = "No files to list.";
    return;
  }
  fileCards.forEach(card => {
    card.style.outline = '2px solid #4285f4';
    setTimeout(() => {
      card.style.outline = '';
    }, 1200);
  });
  voiceStatus.textContent = `Listed ${fileCards.length} files.`;
}

function setLanguage(langCode) {
  recognition.lang = langCode === 'en' ? 'en-US' : langCode === 'ta' ? 'ta-IN' : langCode === 'hi' ? 'hi-IN' : 'en-US';
  const url = new URL(window.location.href);
  url.searchParams.set('lang', langCode);
  window.location.href = url.toString();
}

function setTheme(mode) {
  if (mode === 'dark') {
    document.body.classList.add('dark-mode');
    document.body.classList.remove('light-mode');
    localStorage.setItem('theme', 'dark');
  } else {
    document.body.classList.add('light-mode');
    document.body.classList.remove('dark-mode');
    localStorage.setItem('theme', 'light');
  }
}

function searchFileByName(filename) {
  const searchInput = document.querySelector('input[type="search"], input[name*="search"], input#search');
  if (searchInput) {
    searchInput.value = filename;
    searchInput.dispatchEvent(new Event('input', { bubbles: true }));
    searchInput.focus();
  }
  const fileCards = document.querySelectorAll('.file-card');
  let found = false;
  fileCards.forEach(card => {
    const name = card.getAttribute('data-filename');
    if (name && name.toLowerCase().includes(filename.toLowerCase())) {
      card.style.outline = '2px solid #34a853';
      found = true;
      setTimeout(() => {
        card.style.outline = '';
      }, 1500);
    }
  });
  if (!found) {
    voiceStatus.textContent = `No files found matching "${filename}".`;
  }
}
