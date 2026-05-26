/* ============================================================
   @Authors: Marchetto Francesco, Visentini Nicolò, Gianesella
   Riccardo
   @Project: C -> SayHi!
   @class: 5F 2025/2026
   ============================================================ */

   

/* ============================================================
   SAYHI!
   Descrizione: Chatbot con pattern matching, knowledge base,
   punteggi di pertinenza, contatore domande e timestamp
   ============================================================ */



/* ============================================================
   SEZIONE 1: KNOWLEDGE BASE
   Ogni oggetto contiene:
   - keywords: array di parole/frasi che attivano la risposta
   - response: la risposta del bot
   - score: punteggio base di pertinenza (0-1)
   - category: categoria di appartenenza
   ============================================================ */

const knowledgeBase = [
    /* === JAVASCRIPT === */
    { keywords: ["javascript", "cos'è javascript", "che cos'è javascript"], response: "JavaScript è il linguaggio di programmazione per il web! 🚀 Lo usiamo per rendere interattive le pagine, creare giochi, app e molto altro. Insieme a HTML e CSS è uno dei pilastri del web moderno.", score: 0.95, category: "programmazione" },
    { keywords: ["differenza javascript java", "java vs javascript"], response: "Sono completamente diversi! Java è un linguaggio compilato per applicazioni enterprise e Android. JavaScript è interpretato e vive nel browser. La somiglianza nel nome è solo un caso di marketing! 😄", score: 0.98, category: "programmazione" },
    { keywords: ["variabile javascript", "dichiarare variabile"], response: "Una variabile è come una scatola con un'etichetta. In JavaScript usiamo 'let' (cambia), 'const' (fissa), o 'var' (vecchio). Esempio: let nome = 'Mario'; 📦", score: 0.94, category: "programmazione" },
    { keywords: ["spiegami variabile 5 anni", "variabile come bambino"], response: "Immagina una scatola con sopra scritto 'giocattoli'. Ci puoi mettere dentro una macchinina, poi toglierla e metterci un pupazzo. La scatola è la variabile, quello che ci metti dentro è il valore! 🧸", score: 0.96, category: "programmazione" },
    
    /* === PYTHON === */
    { keywords: ["python", "cos'è python"], response: "Python è un linguaggio super amichevole! 🐍 Si usa per Data Science, Intelligenza Artificiale, sviluppo web e automazione. È famoso perché è semplice da leggere e scrivere.", score: 0.96, category: "programmazione" },
    { keywords: ["python difficile", "imparare python"], response: "Python è il linguaggio più consigliato per chi inizia! Con 2-3 mesi di pratica puoi già creare progetti interessanti. La community è enorme e aiuta sempre! 💪", score: 0.91, category: "programmazione" },
    
    /* === INTELLIGENZA ARTIFICIALE === */
    { keywords: ["intelligenza artificiale", "cos'è ia", "ai"], response: "L'IA è come insegnare ai computer a pensare! 🧠 Non come gli umani, ma a riconoscere pattern, fare previsioni o capire il linguaggio. Esempi: assistenti vocali, raccomandazioni Netflix, auto a guida autonoma.", score: 0.97, category: "ai" },
    { keywords: ["machine learning", "ml"], response: "Il Machine Learning è un modo per far imparare ai computer dai dati, senza programmarli esplicitamente. Come insegnare a un bambino mostrandogli tanti esempi! 📚", score: 0.95, category: "ai" },
    { keywords: ["chatgpt", "gpt", "openai"], response: "ChatGPT è un assistente AI che sa conversare, scrivere codice, tradurre e molto altro! È stato addestrato su tantissimi testi presi da internet. Un compagno super utile! 🤖", score: 0.94, category: "ai" },
    
    /* === SVILUPPO WEB === */
    { keywords: ["html", "cos'è html"], response: "HTML è lo scheletro delle pagine web! 🦴 Usa tag come <h1> per i titoli, <p> per i paragrafi. Ogni sito che vedi è costruito con HTML.", score: 0.95, category: "web" },
    { keywords: ["css", "cos'è css"], response: "CSS è il vestito della pagina web! 👗 Colori, dimensioni, posizioni, animazioni... tutto ciò che rende bello un sito. Senza CSS, i siti sarebanno noiosi e bianchi!", score: 0.94, category: "web" },
    { keywords: ["frontend backend", "frontend vs backend"], response: "Frontend = ciò che vedi (colori, bottoni). Backend = ciò che non vedi (server, database). Un sito ha bisogno di entrambi per funzionare! 🏗️", score: 0.93, category: "web" },
    
    /* === CARRIERA === */
    { keywords: ["stipendio programmatore", "quanto guadagna sviluppatore"], response: "In Italia: junior 25-30k€, senior 50-70k€. All'estero (Svizzera, USA, Germania) si arriva anche a 120k€+. Ma la soddisfazione di creare non ha prezzo! 💰", score: 0.92, category: "carriera" },
    { keywords: ["linguaggio più richiesto", "miglior linguaggio"], response: "JavaScript/TypeScript è il re del web, Python domina in AI e data science, Java per grandi aziende. Scegli in base a cosa ti piace fare! 🎯", score: 0.93, category: "carriera" },
    { keywords: ["diventare programmatore", "come iniziare"], response: "1️⃣ Scegli un linguaggio (Python o JavaScript), 2️⃣ Studia le basi (corsi gratis su YouTube/freeCodeCamp), 3️⃣ Fai tanti progetti, 4️⃣ Costruisci un portfolio. Ce la puoi fare! 💪", score: 0.94, category: "carriera" },
    
    /* === UTILITA' === */
    { keywords: ["git", "github", "controllo versione"], response: "Git tiene traccia delle modifiche al tuo codice (come 'salva' per programmatori). GitHub è dove condividi i tuoi progetti con il mondo. Essenziale per lavorare in team! 🌍", score: 0.93, category: "programmazione" },
    { keywords: ["vscode", "visual studio code"], response: "VS Code è l'editor più amato dai developer! Gratuito, super personalizzabile con estensioni, ha terminale integrato e supporta tutti i linguaggi. Un gioiellino! 💎", score: 0.92, category: "programmazione" }
];

/* ============================================================
   SEZIONE 2: RISPOSTE SPECIALI
   - helpResponse: risposta al comando "aiuto"
   - greetings: risposte per saluti e ringraziamenti
   - fallbackResponses: risposte generiche per domande non riconosciute
   ============================================================ */

const helpResponse = {
    keywords: ["aiuto", "help", "comandi", "cosa sai fare", "funzionalità"],
    response: "📚 **Cosa so fare (tantissimo!):**\n\n• 💻 **JavaScript**: differenze con Java, variabili, Promise\n• 🐍 **Python**: facilità, librerie, usi principali\n• 🧠 **AI/ML**: ChatGPT, Machine Learning, futuro tecnologia\n• 🌐 **Web**: HTML, CSS, frontend vs backend\n• 📈 **Carriera**: stipendi, come iniziare, linguaggi richiesti\n• 🔧 **Tools**: Git, GitHub, VS Code\n\nScrivi 'ciao' per salutarmi o qualsiasi domanda tech!",
    score: 1.0
};

const greetings = [
    { keywords: ["ciao", "buongiorno", "salve", "hey", "buonasera"], response: "Ciao! 👋 Come posso aiutarti con la programmazione oggi?", score: 0.95 },
    { keywords: ["grazie", "thanks", "grazie mille"], response: "Prego! 😊 Sono qui per aiutarti. Hai altre domande sulla tecnologia?", score: 0.95 },
    { keywords: ["come stai", "come va"], response: "Sto benissimo! 🚀 Pronto a rispondere alle tue domande. E tu, come procede lo studio?", score: 0.90 }
];

const fallbackResponses = [
    "Interessante! 🧐 Puoi essere più specifico? Sono specializzato in programmazione, AI e web!",
    "Non ho capito bene... Prova con 'cos'è JavaScript' o 'come funziona l'AI'",
    "Hmm... la mia specialità è la tecnologia! Prova a chiedere qualcosa su Python, HTML o carriera tech",
    "Non trovo info su questo. Prova a scrivere 'aiuto' per vedere tutti i miei argomenti!"
];

/* ============================================================
   SEZIONE 3: VARIABILI GLOBALI
   Stato dell'applicazione e riferimenti DOM
   ============================================================ */

let messageCount = 0;                                           // Contatore delle domande fatte
let chatMessages = document.getElementById('chatMessages');     // Contenitore messaggi
let userInput = document.getElementById('userInput');           // Campo di testo
let sendBtn = document.getElementById('sendBtn');               // Pulsante invio
let messageCountSpan = document.getElementById('messageCount'); // Span per il contatore

/* ============================================================
   SEZIONE 4: FUNZIONI UTILITY
   ============================================================ */

/**
 * Restituisce l'orario corrente nel formato HH:MM
 * @returns {string} Orario formattato
 */
function getCurrentTime() {
    const now = new Date();
    return `${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}`;
}

/**
 * Sanitizza il testo per prevenire attacchi XSS
 * @param {string} text - Testo da sanitizzare
 * @returns {string} Testo sanitizzato
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Trova la miglior corrispondenza nella knowledge base
 * @param {string} question - Domanda dell'utente
 * @returns {object} { response, score }
 */
function findBestMatch(question) {
    const q = question.toLowerCase().trim();
    
    // Verifica se è una richiesta di aiuto
    if (helpResponse.keywords.some(k => q.includes(k))) {
        return { response: helpResponse.response, score: 1.0 };
    }
    
    // Verifica se è un saluto/ringraziamento
    for (let greeting of greetings) {
        if (greeting.keywords.some(k => q.includes(k))) {
            return { response: greeting.response, score: greeting.score };
        }
    }
    
    // Cerca nella knowledge base
    let bestMatch = null;
    let bestScore = 0;
    
    for (let item of knowledgeBase) {
        let matchScore = 0;
        for (let keyword of item.keywords) {
            if (q.includes(keyword)) {
                matchScore += item.score;
            }
        }
        if (matchScore > bestScore) {
            bestScore = matchScore;
            bestMatch = item;
        }
    }
    
    // Se trova una corrispondenza, restituisce la risposta con punteggio normalizzato
    if (bestMatch && bestScore > 0) {
        let normalizedScore = Math.min(bestScore / 2, 0.98);
        return { response: bestMatch.response, score: normalizedScore };
    }
    
    // Nessuna corrispondenza: risposta casuale di fallback
    const randomResponse = fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
    const randomScore = Math.random() * 0.35;
    return { response: randomResponse, score: randomScore };
}

/**
 * Restituisce la classe CSS in base al punteggio
 * @param {number} score - Punteggio di pertinenza
 * @returns {string} Nome della classe CSS
 */
function getScoreClass(score) {
    if (score >= 0.7) return "score-high";
    if (score >= 0.4) return "score-medium";
    return "score-low";
}

/**
 * Restituisce un'emoji in base al punteggio
 * @param {number} score - Punteggio di pertinenza
 * @returns {string} Emoji corrispondente
 */
function getScoreEmoji(score) {
    if (score >= 0.9) return "🎯";
    if (score >= 0.7) return "✅";
    if (score >= 0.4) return "📘";
    return "🤔";
}

/* ============================================================
   SEZIONE 5: FUNZIONI UI (INTERFACCIA UTENTE)
   Gestiscono la visualizzazione dei messaggi
   ============================================================ */

/**
 * Aggiunge un messaggio dell'utente alla chat
 * @param {string} message - Testo del messaggio
 */
function addUserMessage(message) {
    const time = getCurrentTime();
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-bubble">
                <div class="message-text">${escapeHtml(message)}</div>
                <div class="message-time">${time}</div>
            </div>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Aggiunge un messaggio del bot alla chat
 * @param {string} message - Testo del messaggio
 * @param {number|null} score - Punteggio di pertinenza (opzionale)
 */
function addBotMessage(message, score = null) {
    const time = getCurrentTime();
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    // Aggiunge il badge del punteggio solo se fornito
    let scoreHtml = '';
    if (score !== null && score < 1.0) {
        const percent = Math.round(score * 100);
        const emoji = getScoreEmoji(score);
        const scoreClass = getScoreClass(score);
        scoreHtml = `<div class="score-badge ${scoreClass}">${emoji} Pertinenza: ${percent}%</div>`;
    }
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="avatar-small">
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" alt="Bot">
            </div>
            <div class="message-bubble">
                <div class="message-text">${escapeHtml(message).replace(/\n/g, '<br>')}</div>
                ${scoreHtml}
                <div class="message-time">${time}</div>
            </div>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Mostra l'indicatore di caricamento (bot sta pensando)
 */
function addLoadingIndicator() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot-message';
    loadingDiv.id = 'loadingIndicator';
    loadingDiv.innerHTML = `
        <div class="message-content">
            <div class="avatar-small">
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" alt="Bot">
            </div>
            <div class="message-bubble">
                <div class="loading"></div> Sto pensando...
            </div>
        </div>
    `;
    chatMessages.appendChild(loadingDiv);
    scrollToBottom();
}

/**
 * Rimuove l'indicatore di caricamento
 */
function removeLoadingIndicator() {
    const indicator = document.getElementById('loadingIndicator');
    if (indicator) indicator.remove();
}

/**
 * Scrolla automaticamente verso il basso (ultimo messaggio)
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Aggiorna il contatore delle domande nell'interfaccia
 */
function updateMessageCount() {
    messageCountSpan.textContent = messageCount;
}

/* ============================================================
   SEZIONE 6: GESTIONE INVIO MESSAGGI
   ============================================================ */

/**
 * Gestisce l'invio di un messaggio
 * Disabilita input durante l'elaborazione, mostra loading,
 * cerca la risposta e la visualizza
 */
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // Disabilita input durante l'elaborazione
    sendBtn.disabled = true;
    userInput.disabled = true;
    
    // Mostra messaggio utente e aggiorna contatore
    addUserMessage(message);
    messageCount++;
    updateMessageCount();
    
    // Pulisce il campo input
    userInput.value = "";
    userInput.style.height = "auto";
    
    // Mostra indicatore di caricamento
    addLoadingIndicator();
    
    // Simula un piccolo ritardo per un'esperienza più naturale
    setTimeout(() => {
        const result = findBestMatch(message);
        removeLoadingIndicator();
        addBotMessage(result.response, result.score);
        
        // Riabilita input
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }, 400);
}

/**
 * Gestisce la pressione dei tasti nella textarea
 * Invio invia il messaggio, Shift+Invio va a capo
 * @param {KeyboardEvent} event - Evento della tastiera
 */
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

/**
 * Ridimensiona automaticamente la textarea in base al contenuto
 */
function autoResizeTextarea() {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 100) + 'px';
}

/* ============================================================
   SEZIONE 7: SUGGERIMENTI DINAMICI PER CATEGORIA
   ============================================================ */

/**
 * Mappa delle domande suggerite per ogni categoria
 */
const categoryQuestions = {
    programmazione: [
        "Cos'è JavaScript?",
        "Spiegami una variabile come a un bambino",
        "Differenza tra Java e JavaScript",
        "Quanto tempo per imparare Python?",
        "Cosa sono le Promise in JavaScript?"
    ],
    ai: [
        "Cos'è l'Intelligenza Artificiale?",
        "Come funziona ChatGPT?",
        "Cos'è il Machine Learning?",
        "Differenza tra AI e Machine Learning",
        "Cosa può fare l'AI nel futuro?"
    ],
    web: [
        "Cos'è HTML?",
        "Cos'è CSS?",
        "Differenza tra frontend e backend",
        "Cos'è il responsive design?",
        "A cosa serve React?"
    ],
    carriera: [
        "Quanto guadagna un programmatore?",
        "Come diventare programmatore?",
        "Quale linguaggio studiare nel 2024?",
        "Meglio università o corsi online?",
        "Quali competenze sono più richieste?"
    ],
    random: [
        "Qual è il bug più famoso della storia?",
        "Perché 10 programmatori sono meglio di 1?",
        "Spiegami un loop come a un robot",
        "Cosa significa 'debugging'?",
        "Qual è il miglior linguaggio per iniziare?"
    ]
};

/**
 * Aggiorna i bottoni dei suggerimenti in base alla categoria selezionata
 * @param {string} category - Categoria selezionata (programmazione, ai, web, carriera, random)
 */
function updateSuggestions(category) {
    const container = document.getElementById('suggestionsContainer');
    const questions = categoryQuestions[category] || categoryQuestions.programmazione;
    
    // Crea i bottoni per ogni domanda suggerita
    container.innerHTML = questions.map(q => 
        `<button class="suggestion-btn" data-question="${escapeHtml(q)}">${escapeHtml(q.length > 35 ? q.substring(0,35)+'…' : q)}</button>`
    ).join('');
    
    // Aggiunge l'evento click a ogni suggerimento
    document.querySelectorAll('.suggestion-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            userInput.value = btn.dataset.question;
            sendMessage();
        });
    });
}

/* ============================================================
   SEZIONE 8: INIZIALIZZAZIONE
   Eventi e setup all'avvio della pagina
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    // Aggiunge eventi ai bottoni delle categorie
    document.querySelectorAll('.cat-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const category = btn.dataset.category;
            updateSuggestions(category);
        });
    });
    
    // Inizializza i suggerimenti con la categoria "programmazione"
    updateSuggestions('programmazione');
    
    // Eventi principali
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', handleKeyPress);
    userInput.addEventListener('input', autoResizeTextarea);
    
    // Focus iniziale sul campo di input
    userInput.focus();
});
