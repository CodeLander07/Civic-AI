
"""
Fallback content for Civic-AI when AI services are unavailable.
Contains information about popular Indian government schemes.
"""

FALLBACK_SCHEMES = {
    "kisan": {
        "title": "PM Kisan Samman Nidhi Yojana",
        "description": "A central sector scheme with 100% funding from Government of India to provide income support to all landholding farmer families.",
        "benefits": [
            "Financial benefit of Rs. 6000/- per year",
            "Payable in three equal installments of Rs. 2000/- each",
            "Direct transfer to bank accounts"
        ],
        "eligibility": [
            "All landholding farmer families",
            "Subject to certain exclusion criteria (e.g., institutional landholders, income tax payers)"
        ],
        "application": "Apply online at pmkisan.gov.in or through PM-KISAN Mobile App."
    },
    "health": {
        "title": "Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
        "description": "The world's largest health insurance/assurance scheme fully financed by the government.",
        "benefits": [
            "Cover of Rs. 5 lakhs per family per year",
            "For secondary and tertiary care hospitalization",
            "Cashless access to health care services"
        ],
        "eligibility": [
            "Families identified based on SECC 2011 data",
            "No cap on family size or age"
        ],
        "application": "Check eligibility at mera.pmjay.gov.in or visit an Empanelled Health Care Provider (EHCP)."
    },
    "housing": {
        "title": "Pradhan Mantri Awas Yojana (PMAY)",
        "description": "A mission to provide housing for all in urban and rural areas.",
        "benefits": [
            "Financial assistance for house construction",
            "Interest subsidy on home loans",
            "Toilet and electricity connection included"
        ],
        "eligibility": [
            "Economically Weaker Section (EWS)",
            "Low Income Group (LIG)",
            "Middle Income Group (MIG)"
        ],
        "application": "Apply through PMAY-Urban or PMAY-Gramin official portals or Common Service Centres (CSC)."
    },
    "business": {
        "title": "Pradhan Mantri MUDRA Yojana (PMMY)",
        "description": "A scheme to provide loans up to 10 lakh to the non-corporate, non-farm small/micro enterprises.",
        "benefits": [
            "Shishu: Loans up to Rs. 50,000",
            "Kishore: Loans from Rs. 50,000 to Rs. 5,00,000",
            "Tarun: Loans from Rs. 5,00,000 to Rs. 10,00,000"
        ],
        "eligibility": [
            "Non-Corporate Small Business Segment (NCSB)",
            "Proprietorship / Partnership firms running small manufacturing units"
        ],
        "application": "Apply at any commercial bank, RRB, Small Finance Bank, MFI or NBFC."
    },
    "gas": {
        "title": "Pradhan Mantri Ujjwala Yojana (PMUY)",
        "description": "A scheme to provide LPG connections to women from Below Poverty Line (BPL) households.",
        "benefits": [
            "Cash assistance for new LPG connection",
            "Smoke-free cooking environment",
            "Improved health for women and children"
        ],
        "eligibility": [
            "Adult woman belonging to a poor household",
            "No other LPG connection in the same household"
        ],
        "application": "Apply at the nearest LPG distributor or online through the official portal."
    }
}

GENERAL_FALLBACK = {
    "title": "Civic-AI Service Notice",
    "description": "We are currently experiencing high traffic. Here is some general information about popular services.",
    "schemes": [
        "PM Kisan Samman Nidhi (Farmer Support)",
        "Ayushman Bharat (Health Insurance)",
        "PM Awas Yojana (Housing)",
        "PM Mudra Yojana (Small Business Loans)"
    ],
    "note": "Please try your specific query again in a few moments."
}

def get_fallback_response(query: str, language: str = "en") -> str:
    """
    Selects a smart fallback response based on keywords in the query.
    """
    query_lower = query.lower()
    
    # Keyword matching
    selected_scheme = None
    
    if "kisan" in query_lower or "farm" in query_lower or "agri" in query_lower:
        selected_scheme = FALLBACK_SCHEMES["kisan"]
    elif "health" in query_lower or "medic" in query_lower or "doctor" in query_lower or "hospital" in query_lower or "ayushman" in query_lower:
        selected_scheme = FALLBACK_SCHEMES["health"]
    elif "house" in query_lower or "home" in query_lower or "awas" in query_lower or "flat" in query_lower:
        selected_scheme = FALLBACK_SCHEMES["housing"]
    elif "loan" in query_lower or "money" in query_lower or "business" in query_lower or "mudra" in query_lower:
        selected_scheme = FALLBACK_SCHEMES["business"]
    elif "gas" in query_lower or "lpg" in query_lower or "cooking" in query_lower or "ujjwala" in query_lower:
        selected_scheme = FALLBACK_SCHEMES["gas"]
    
    # Construct the response
    if selected_scheme:
        response = f"# {selected_scheme['title']}\n\n"
        
        if language.lower() not in ["en", "english"]:
            response += f"*(Note: Content is displayed in English as translation services are currently offline. Requested Language: {language})*\n\n"
            
        response += f"**Note:** *Showing offline information as AI services are momentarily unavailable.*\n\n"
        response += f"{selected_scheme['description']}\n\n"
        
        response += "### Key Benefits\n"
        for benefit in selected_scheme['benefits']:
            response += f"- {benefit}\n"
        
        response += "\n### Eligibility\n"
        for criteria in selected_scheme['eligibility']:
            response += f"- {criteria}\n"
            
        response += f"\n### How to Apply\n{selected_scheme['application']}"
        
        return response
    
    # General fallback if no keywords match
    response = f"# {GENERAL_FALLBACK['title']}\n\n"
    
    if language.lower() not in ["en", "english"]:
        response += f"*(Note: Content is displayed in English as translation services are currently offline. Requested Language: {language})*\n\n"
        
    response += f"{GENERAL_FALLBACK['description']}\n\n"
    response += "### Popular Schemes:\n"
    for scheme in GENERAL_FALLBACK['schemes']:
        response += f"- {scheme}\n"
    
    response += f"\n*{GENERAL_FALLBACK['note']}*"
    return response

def get_image_fallback_response(language: str = "en") -> dict:
    """
    Returns a simulated image analysis response.
    """
    return {
        "extracted_text": "GOVERNMENT OF INDIA\nMINISTRY OF RURAL DEVELOPMENT\n\nNOTICE\n\nSubject: Implementation of Pradhan Mantri Awas Yojana - Gramin (PMAY-G)\n\nThis is to inform all beneficiaries that the deadline for document submission has been extended to 31st March 2024. Eligible applicants must submit their Aadhaar card, MGNREGA job card, and bank account details to the Gram Panchayat office.\n\nBy Order,\nBlock Development Officer",
        "explanation": f"# Document Analysis (Offline Mode)\n\n**Document Type:** Government Notice (PMAY-G)\n\n**Summary:**\nThis is an official notice regarding the **Pradhan Mantri Awas Yojana (Gramin)** housing scheme.\n\n**Key Updates:**\n- **Deadline Extended:** You now have until **31st March 2024** to submit your documents.\n- **Required Documents:**\n  - Aadhaar Card\n  - MGNREGA Job Card\n  - Bank Account Details\n\n**Action Required:**\nSubmit these documents to your local **Gram Panchayat office** immediately to ensure you receive your housing benefits.\n\n*Note: This is a simulated response for demonstration purposes.*"
    }
