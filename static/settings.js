// Settings page functionality
let availableVoices = [];
let currentSettings = {
    voiceId: '',
    soundEffects: true,
    autoTts: false
};

document.addEventListener('DOMContentLoaded', function() {
    // Load the navigation toolbar
    loadToolbar();
    
    // Load available voices
    loadVoices();
    
    // Load saved settings
    loadSettings();
    
    // Initialize event listeners
    initializeEventListeners();
});

function loadToolbar() {
    const toolbarContainer = document.getElementById('toolbar-container');
    if (toolbarContainer) {
        fetch('/static/index.html')
            .then(response => response.text())
            .then(html => {
                toolbarContainer.innerHTML = html;
                highlightCurrentPage();
            })
            .catch(error => {
                console.error('Error loading toolbar:', error);
            });
    }
}

function highlightCurrentPage() {
    // Highlight the current page in the toolbar
    const currentPath = window.location.pathname;
    const toolbarLinks = document.querySelectorAll('.toolbar-link');
    
    toolbarLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath) {
            link.classList.add('active');
        }
    });
}

async function loadVoices() {
    try {
        const response = await fetch('/api/voices');
        const data = await response.json();
        availableVoices = data.voices;
        
        const voiceSelect = document.getElementById('voice-select');
        voiceSelect.innerHTML = '<option value="">Select a voice...</option>';
        
        // Add voices as individual options (all are US English Gemini TTS voices)
        availableVoices.forEach(voice => {
            const option = document.createElement('option');
            option.value = voice.id;
            option.textContent = `${voice.name} (${voice.gender}) - ${voice.description}`;
            option.dataset.description = voice.description;
            option.dataset.gender = voice.gender;
            voiceSelect.appendChild(option);
        });
        
        // Enable the dropdown
        voiceSelect.disabled = false;
        
    } catch (error) {
        console.error('Error loading voices:', error);
        showStatus('Error loading voices. Please try again later.', 'error');
    }
}


function initializeEventListeners() {
    const voiceSelect = document.getElementById('voice-select');
    const testVoiceBtn = document.getElementById('test-voice-btn');
    const saveSettingsBtn = document.getElementById('save-settings-btn');
    const resetSettingsBtn = document.getElementById('reset-settings-btn');
    const soundEffectsToggle = document.getElementById('sound-effects');
    const autoTtsToggle = document.getElementById('auto-tts');
    
    // Voice selection change
    voiceSelect.addEventListener('change', function() {
        const selectedVoiceId = this.value;
        if (selectedVoiceId) {
            updateVoicePreview(selectedVoiceId);
            testVoiceBtn.disabled = false;
            saveSettingsBtn.disabled = false;
            currentSettings.voiceId = selectedVoiceId;
        } else {
            clearVoicePreview();
            testVoiceBtn.disabled = true;
            saveSettingsBtn.disabled = true;
            currentSettings.voiceId = '';
        }
    });
    
    // Test voice button
    testVoiceBtn.addEventListener('click', function() {
        testSelectedVoice();
    });
    
    // Save settings button
    saveSettingsBtn.addEventListener('click', function() {
        saveSettings();
    });
    
    // Reset settings button
    resetSettingsBtn.addEventListener('click', function() {
        resetSettings();
    });
    
    // Toggle switches
    soundEffectsToggle.addEventListener('change', function() {
        currentSettings.soundEffects = this.checked;
        saveSettings();
    });
    
    autoTtsToggle.addEventListener('change', function() {
        currentSettings.autoTts = this.checked;
        saveSettings();
    });
}

function updateVoicePreview(voiceId) {
    const voice = availableVoices.find(v => v.id === voiceId);
    if (voice) {
        const voiceInfo = document.getElementById('voice-info');
        const voiceName = voiceInfo.querySelector('.voice-name');
        const voiceLanguage = voiceInfo.querySelector('.voice-language');
        const voiceGender = voiceInfo.querySelector('.voice-gender');
        
        voiceName.textContent = voice.name;
        voiceLanguage.textContent = voice.description;
        voiceGender.textContent = voice.gender;
        
        // Add animation
        voiceInfo.style.opacity = '0';
        setTimeout(() => {
            voiceInfo.style.opacity = '1';
        }, 100);
    }
}

function clearVoicePreview() {
    const voiceInfo = document.getElementById('voice-info');
    const voiceName = voiceInfo.querySelector('.voice-name');
    const voiceLanguage = voiceInfo.querySelector('.voice-language');
    const voiceGender = voiceInfo.querySelector('.voice-gender');
    
    voiceName.textContent = 'No voice selected';
    voiceLanguage.textContent = '-';
    voiceGender.textContent = '-';
}

async function testSelectedVoice() {
    const voiceSelect = document.getElementById('voice-select');
    const testVoiceBtn = document.getElementById('test-voice-btn');
    const selectedVoiceId = voiceSelect.value;
    
    if (!selectedVoiceId) return;
    
    testVoiceBtn.disabled = true;
    testVoiceBtn.innerHTML = '🔄 Testing...';
    
    try {
        const testText = "Hello! This is a test of the selected voice. How does it sound?";
        
        const response = await fetch('/api/tts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: testText,
                voice_id: selectedVoiceId
            })
        });
        
        const data = await response.json();
        
        if (data.audio_data && data.audio_data !== "USE_BROWSER_TTS") {
            // Play the audio from Gemini TTS
            const audio = new Audio(data.audio_data);
            audio.play();
        } else {
            // Fallback to browser TTS
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(testText);
                speechSynthesis.speak(utterance);
            } else {
                showStatus('Text-to-speech is not supported in this browser.', 'warning');
            }
        }
        
        showStatus('Voice test completed successfully!', 'success');
        
    } catch (error) {
        console.error('Error testing voice:', error);
        showStatus('Error testing voice. Please try again.', 'error');
    } finally {
        testVoiceBtn.disabled = false;
        testVoiceBtn.innerHTML = '🔊 Test Voice';
    }
}

async function saveSettings() {
    const saveBtn = document.getElementById('save-settings-btn');
    const originalText = saveBtn.innerHTML;
    
    saveBtn.disabled = true;
    saveBtn.innerHTML = '💾 Saving...';
    
    try {
        // Save to server if voice is selected
        if (currentSettings.voiceId) {
            const response = await fetch('/api/settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    voice_id: currentSettings.voiceId
                })
            });
            
            const data = await response.json();
            if (!data.success) {
                throw new Error(data.message);
            }
        }
        
        // Save to localStorage
        localStorage.setItem('appSettings', JSON.stringify(currentSettings));
        
        showStatus('Settings saved successfully!', 'success');
        
    } catch (error) {
        console.error('Error saving settings:', error);
        showStatus('Error saving settings. Please try again.', 'error');
    } finally {
        saveBtn.disabled = currentSettings.voiceId === '';
        saveBtn.innerHTML = originalText;
    }
}

function loadSettings() {
    try {
        const saved = localStorage.getItem('appSettings');
        if (saved) {
            const settings = JSON.parse(saved);
            currentSettings = { ...currentSettings, ...settings };
            
            // Apply loaded settings to UI
            if (currentSettings.voiceId) {
                setTimeout(() => {
                    const voiceSelect = document.getElementById('voice-select');
                    voiceSelect.value = currentSettings.voiceId;
                    updateVoicePreview(currentSettings.voiceId);
                    document.getElementById('test-voice-btn').disabled = false;
                    document.getElementById('save-settings-btn').disabled = false;
                }, 500); // Wait for voices to load
            }
            
            document.getElementById('sound-effects').checked = currentSettings.soundEffects;
            document.getElementById('auto-tts').checked = currentSettings.autoTts;
        }
    } catch (error) {
        console.error('Error loading settings:', error);
    }
}

function resetSettings() {
    if (confirm('Are you sure you want to reset all settings to default?')) {
        currentSettings = {
            voiceId: '',
            soundEffects: true,
            autoTts: false
        };
        
        // Reset UI
        document.getElementById('voice-select').value = '';
        document.getElementById('sound-effects').checked = true;
        document.getElementById('auto-tts').checked = false;
        document.getElementById('test-voice-btn').disabled = true;
        document.getElementById('save-settings-btn').disabled = true;
        
        clearVoicePreview();
        
        // Clear localStorage
        localStorage.removeItem('appSettings');
        
        showStatus('Settings reset to default values.', 'info');
    }
}

function showStatus(message, type) {
    const statusElement = document.getElementById('settings-status');
    statusElement.textContent = message;
    statusElement.className = `status-message ${type}`;
    statusElement.style.display = 'block';
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        statusElement.style.display = 'none';
    }, 3000);
}
