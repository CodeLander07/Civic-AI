# User Flows

## 1. New User Onboarding
1. **Landing Page**: User sees "Simplify Government" value prop.
2. **Signup**: User enters Email/Password.
3. **Auto-Login**: System auto-confirms email (Hackathon mode) and logs user in.
4. **Dashboard**: User lands on the main dashboard.

## 2. Document Simplification (The "Happy Path")
1. **Upload**: User clicks "Upload Document" and selects an image (e.g., a tax notice).
2. **Preview**: User sees the image preview.
3. **Send**: User clicks "Analyze".
4. **Processing**:
   - Client sends image to Server.
   - Server runs OCR + Gemini.
5. **Result**: User sees a simplified summary in the chat window.
   - *Example Output*: "This is a property tax bill. You need to pay ₹1200 by Dec 31st."

## 3. Scheme Query (Text Chat)
1. **Input**: User types "How do I apply for PM Kisan?" in Hindi ("PM Kisan ke liye kaise apply karun?").
2. **Processing**:
   - Server detects language.
   - Server queries Gemini (or Fallback DB if offline).
3. **Response**: User receives a step-by-step guide in Hindi.

## 4. Offline Fallback
1. **Scenario**: Gemini API is down or rate-limited.
2. **Input**: User asks about "Ayushman Bharat".
3. **Detection**: Server catches the API error.
4. **Fallback**: Server looks up "Ayushman Bharat" in `fallbacks.py`.
5. **Response**: User gets the pre-cached static information.

