# 🚀 Truescope

[![React Native](https://img.shields.io/badge/React_Native-0.72-blue)](https://reactnative.dev/) 
[![Django](https://img.shields.io/badge/Django-4.2-green)](https://www.djangoproject.com/) 
[![Python](https://img.shields.io/badge/Python-3.11-yellow)](https://www.python.org/) 
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

**Truescope** is an **AI-powered news verification app** using a **hybrid approach** combining machine learning, NLP, and geospatial visualization to detect fake news and provide educational insights.  

---

## 📌 Table of Contents

- [Project Overview](#project-overview)  
- [Features](#features)  
- [Technology Stack](#technology-stack)    
- [Installation & Setup](#installation--setup)  
- [Usage](#usage)  
- [Screenshots / Demo](#screenshots--demo)  
- [API Endpoints](#api-endpoints)  
- [Future Enhancements](#future-enhancements)  
- [Contributing](#contributing)  
- [License](#license)  

---

## 🌟 Project Overview

Truescope helps users **detect fake news** and **understand the credibility** of information. It allows users to paste news text and get:

- ✅ Real vs Fake prediction  
- 📊 Confidence scores  
- 🗺️ State-wise news credibility map  
- 📰 Sources & snippets  
- 🎓 Educational tips for verifying news  

**Hybrid AI Approach:**  

1. **Machine Learning Model:** NLP-based news classification.  
2. **Geospatial Visualization:** State-wise map using React Native Maps and GeoJSON.  
3. **Educational Insights:** Tips for verifying news.  

---

## ✨ Features

- Submit news text for verification  
- Get **prediction label** (Real / Fake) and **confidence score**  
- **State-wise map visualization** of news credibility  
- Click on any state to view **state-specific news analysis**  
- Display **news sources** and snippets  
- Show **educational tips** for news verification  
- Fully functional **React Native mobile app** for Android/iOS  

---

## 🛠 Technology Stack

| Layer | Technology / Library |
|-------|--------------------|
| Frontend | React Native, Expo, TypeScript |
| Backend | Django REST Framework, Python |
| Machine Learning | HuggingFace Transformers / Custom NLP Models |
| Maps | react-native-maps, GeoJSON polygons |
| HTTP Requests | Axios |
| Navigation | React Navigation |

## ⚙️ Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/truescope.git
cd truescope

2. Install dependencies:
npm install
# or
yarn install

3. Start Expo development server:
expo start

4. Ensure backend Django server is running and update BASE_URL in:
NewsScreen.tsx
NewsResultScreen.tsx

5. Run app on Android/iOS device using Expo Go.

##📝 Usage

1. Launch app on device.
2. Sign up / Login.
3. Go to News Verification.
4. Paste news text → Click Submit.
5. View prediction, confidence, sources, and state-wise map.
6. Tap on any state polygon for state-specific news insights.

## 📷 Screenshots / Demo

You can upload a demo video or GIF in the repository:
> Replace the GIF with your actual demo video.

## 🔗 API Endpoints

POST /api/check-news/ → Predict news credibility
GET /api/map-data/ → Fetch state-wise news status

Request Example:

{
  "text": "Sample news text here",
  "lang": "en"
}

Response Example:

{
  "prediction": { "label": "Real", "confidence": 0.92 },
  "input": { "original": "Sample news text here" },
  "state": "Tamil Nadu",
  "explanation": "Model explanation here...",
  "sources": [
    { "publisher": "News Source", "snippet": "Snippet text", "url": "https://..." }
  ],
  "education": ["Check source credibility", "Cross verify with other platforms"]
}

## 🔮 Future Enhancements

Deploy backend and app for public access
Multi-language support
Advanced AI models for contextual fake news detection
Push notifications for trending fake news
User feedback system to improve AI accuracy

## 🤝 Contributing

1. Fork the repository
2. Create a branch: git checkout -b feature-name
3. Make changes & commit: git commit -m "Add feature"
4. Push: git push origin feature-name
5. Open a Pull Request


