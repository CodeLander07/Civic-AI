# The Solution: Civic-AI

## 💡 The Core Concept
Civic-AI is a "Translator for Bureaucracy." It sits between the citizen and the state, decoding the complex signals from the government into clear, actionable messages for the user.

## 🛠 Key Components

### 1. The "Simplifier" Engine (GenAI)
At the heart of the system is a fine-tuned prompt chain running on **Google Gemini 1.5 Flash**.
- **Input:** Complex text (from OCR or user query).
- **Processing:** The AI identifies legal terms, dates, and obligations. It then rewrites the content using simple analogies and local idioms.
- **Output:** A summary that a 10-year-old could understand.

### 2. Visual Intelligence (OCR)
We don't expect users to type out long notices.
- **Action:** Users snap a photo of a letter or form.
- **Tech:** The system uses OCR to extract text, even from grainy or low-light images, before passing it to the Simplifier.

### 3. The "Offline First" Fallback
We recognize that AI services can go down or be slow.
- **Mechanism:** A robust fallback system (implemented in `server/fallbacks.py`) contains pre-indexed data on major schemes (PM Kisan, Ayushman Bharat, etc.).
- **Benefit:** If the AI is unreachable, the user still gets accurate, structured information from our local database.

### 4. Multilingual Interface
The entire application is designed to be language-agnostic.
- **UI:** Labels and buttons can be localized.
- **Content:** All AI responses are generated in the user's selected language (Hindi, Marathi, Tamil, etc.).

## 🌈 User Journey
1. **Snap:** User takes a photo of a confusing notice.
2. **Select:** User chooses their language (e.g., "Hindi").
3. **Understand:** App says: "This is a tax notice. You need to pay ₹500 by next Monday. Here is the link."
4. **Act:** User clicks the link and completes the task.
