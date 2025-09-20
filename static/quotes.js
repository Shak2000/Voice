class QuotesApp {
    constructor() {
        this.subjectInput = document.getElementById('subjectInput');
        this.getQuotesBtn = document.getElementById('getQuotesBtn');
        this.quotesContainer = document.getElementById('quotesContainer');
        this.quotesTitle = document.getElementById('quotesTitle');
        this.quotesList = document.getElementById('quotesList');
        this.errorMessage = document.getElementById('errorMessage');
        
        this.initEventListeners();
    }

    initEventListeners() {
        this.getQuotesBtn.addEventListener('click', () => this.handleGetQuotes());
        this.subjectInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleGetQuotes();
            }
        });
    }

    async handleGetQuotes() {
        const subject = this.subjectInput.value.trim();
        
        if (!subject) {
            this.showError('Please enter a subject');
            return;
        }

        this.setLoading(true);
        this.hideError();
        this.hideQuotes();

        try {
            const quotes = await this.fetchQuotes(subject);
            this.displayQuotes(subject, quotes);
        } catch (error) {
            this.showError(`Failed to fetch quotes: ${error.message}`);
        } finally {
            this.setLoading(false);
        }
    }

    async fetchQuotes(subject) {
        const response = await fetch('/api/quotes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ subject })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to fetch quotes');
        }

        const data = await response.json();
        return data.quotes;
    }

    displayQuotes(subject, quotes) {
        this.quotesTitle.textContent = `Quotes about "${subject}"`;
        this.quotesList.innerHTML = '';

        quotes.forEach((quoteData, index) => {
            const quoteElement = this.createQuoteElement(quoteData, index);
            this.quotesList.appendChild(quoteElement);
        });

        this.showQuotes();
    }

    createQuoteElement(quoteData, index) {
        const quoteDiv = document.createElement('div');
        quoteDiv.className = 'quote-item';
        quoteDiv.innerHTML = `
            <div class="quote-content">
                <div class="quote-text">"${this.escapeHtml(quoteData.quote)}"</div>
                <div class="quote-context">${this.escapeHtml(quoteData.context)}</div>
            </div>
            <button class="play-btn" data-quote="${this.escapeHtml(quoteData.quote)}" data-index="${index}">
                <span class="play-icon">▶</span>
                <span class="play-text">Play</span>
            </button>
        `;

        // Add click event listener to play button
        const playBtn = quoteDiv.querySelector('.play-btn');
        playBtn.addEventListener('click', () => this.handlePlayQuote(playBtn));

        return quoteDiv;
    }

    async handlePlayQuote(playBtn) {
        const quote = playBtn.dataset.quote;
        const index = playBtn.dataset.index;
        
        this.setPlayButtonLoading(playBtn, true);

        try {
            await this.playQuoteAudio(quote);
        } catch (error) {
            console.error('Error playing quote:', error);
            // Fallback to browser TTS if Gemini TTS fails
            this.playWithBrowserTTS(quote);
        } finally {
            this.setPlayButtonLoading(playBtn, false);
        }
    }

    async playQuoteAudio(quote) {
        const response = await fetch('/api/tts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: quote })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate speech');
        }

        const data = await response.json();
        
        // Check if server wants us to use browser TTS
        if (data.audio_data === "USE_BROWSER_TTS") {
            this.playWithBrowserTTS(quote);
            return;
        }
        
        // Create audio element and play
        const audio = new Audio(data.audio_data);
        await audio.play();
    }

    playWithBrowserTTS(quote) {
        // Fallback to browser's built-in TTS
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(quote);
            utterance.rate = 0.9;
            utterance.pitch = 1;
            utterance.volume = 1;
            
            // Try to use a pleasant voice
            const voices = speechSynthesis.getVoices();
            const preferredVoice = voices.find(voice => 
                voice.lang.includes('en') && 
                (voice.name.includes('Google') || voice.name.includes('Microsoft'))
            );
            
            if (preferredVoice) {
                utterance.voice = preferredVoice;
            }
            
            speechSynthesis.speak(utterance);
        } else {
            alert('Text-to-speech is not supported in this browser');
        }
    }

    setPlayButtonLoading(playBtn, isLoading) {
        const playIcon = playBtn.querySelector('.play-icon');
        const playText = playBtn.querySelector('.play-text');
        
        if (isLoading) {
            playIcon.textContent = '⏳';
            playText.textContent = 'Loading...';
            playBtn.disabled = true;
        } else {
            playIcon.textContent = '▶';
            playText.textContent = 'Play';
            playBtn.disabled = false;
        }
    }

    setLoading(isLoading) {
        const btnText = this.getQuotesBtn.querySelector('.btn-text');
        const btnLoading = this.getQuotesBtn.querySelector('.btn-loading');
        
        if (isLoading) {
            btnText.style.display = 'none';
            btnLoading.style.display = 'inline';
            this.getQuotesBtn.disabled = true;
        } else {
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
            this.getQuotesBtn.disabled = false;
        }
    }

    showQuotes() {
        this.quotesContainer.style.display = 'block';
    }

    hideQuotes() {
        this.quotesContainer.style.display = 'none';
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorMessage.style.display = 'block';
    }

    hideError() {
        this.errorMessage.style.display = 'none';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new QuotesApp();
});