const voiceBtn = document.getElementById('voice-command-btn');
const voiceCancelBtn = document.getElementById('voice-cancel-btn');
const voiceStatus = document.getElementById('voice-status');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
  alert("Your browser does not support voice recognition.");
  voiceBtn.disabled = true;
} else {
  const recognition = new SpeechRecognition();
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
  } else if (command.includes('open') && command.includes('file')) {
    const filename = command.split('file').pop().trim();
    openFileByName(filename);
    recognized = true;
  } else if (command.includes('list files')) {
    listFiles();
    recognized = true;
  } else if (command === 'logout' || command === 'log me out' || command.includes('sign out')) {
    voiceStatus.textContent = "Logging out...";
    window.location.href = "/logout";
    recognized = true;
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

// --- Actual implementations ---

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
