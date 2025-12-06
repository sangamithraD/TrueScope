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

1️⃣ **Clone the Repository**

git clone https://github.com/yourusername/truescope.git
cd truescope

2️⃣ **Install Dependencies**

npm install
# or
yarn install

3️⃣ **Start Expo Development Server**

expo start

4️⃣ **Backend Configuration**

Ensure your Django backend is running, and update "BASE_URL" in:

- "NewsScreen.tsx"
- "NewsResultScreen.tsx"

**Example:**
const BASE_URL = "http://YOUR_LOCAL_IP:8000";

5️⃣ **Run on Mobile**

- Install Expo Go on your mobile
- Scan the QR code from terminal
- App will load instantly
  
## 📝 Usage Guide

-1. Launch the app on your device
-2. Login or Signup
-3. Open News Verification screen
-4. Paste any news content
-5. Tap Submit
-6. View:
   - Prediction Result
   - Confidence Score
   - Explanation
   - Verified Sources
   - State-wise risk on map
-7. Tap any state polygon to view state-specific insights

## 🔗 API Endpoints

✅ **Check News Credibility**

**POST "/api/check-news/"**

**Request:**

{
  "text": "Sample news text here",
  "lang": "en"
}

**Response:**

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

✅ **Fetch State-Wise Map Data**

**GET "/api/map-data/"**

Returns dynamic state-wise verification severity used for color mapping.

**🗺️ Map Color Legend**

Color| Meaning
🔴 Red| High Fake News Risk
🟡 Yellow| Moderate Risk
🟢 Green| Low Risk

✅ **Fetch State Based News**

**GET "/api/state-news/<str:state-name>/"**

Returns the fake news in the particular state you tap.

**request:**

GET "api/state-news/Kerala/"

**response:**

{
 "News":"Kerala is the largest state in India",
 "Prediction":"Fake",
 "Confidence" :"0.26"
 }

 ## 📷 Demo & Screenshots

🎥 A full demo video will be uploaded directly inside the repository.

«No public deployment URLs are available as this project currently runs on a local development environment.»

## 🚫 Deployment Status

- ❌ Not deployed to production yet
- ✅ Fully working on:
   - Localhost
   - Local network
   - Expo Go testing

## 🔮 Future Enhancements

- Public cloud deployment
- Multi-language verification
- Advanced deep learning models (BERT / Transformers)
- Push notifications for trending fake news
- Admin analytics dashboard
- Social media fake news monitoring
- Browser extension version

## 🤝 Contributing

1. **Fork the repository**
2. **Create a new branch**

git checkout -b feature-name

3. **Commit your changes**

git commit -m "Added new feature"

4. **Push to your branch**

git push origin feature-name

5. **Create a Pull Request**

---

## 🔒 Access & Usage Restriction  

This repository is intended **only for academic evaluation, hackathon review, and placement demonstration purposes**.  

❌ Unauthorized copying, redistribution, modification, or commercial use of this project is **strictly prohibited** without prior written permission from the TrueScope Development Team.

✅ Limited access may be granted only to:
- Project evaluators  
- Hackathon jury members  
- Recruiters & placement reviewers  

All rights are reserved by the TrueScope Development Team.


## 📜 License  

This project is released under a **Restricted Proprietary License**.  
© 2025 **TrueScope**

✅ You may:
- View the project for learning and evaluation purposes  
- Run the application locally for demo and academic use  

❌ You may NOT:
- Copy or reuse the source code  
- Redistribute the application  
- Use it for commercial products  
- Publish modified versions  

Violation of these terms may result in legal action.

## 👨‍💻 Developed By  

**TrueScope Development Team**  
*AI | Full Stack | Mobile App Development*

### Team Members

- **Sangamithra D** – Backend & AI/ML Developer  
- **Yuvarani R** – Frontend Developer
  https//github.com/yu  
- **Swetha M** – Data Analytics & Data Processing
  https//github.com/

## ✅ Project Vision  

**TrueScope – Fighting Fake News with Artificial Intelligence**  

TrueScope is designed to:
- Detect fake news using a **Hybrid AI approach**
- Analyze state-wise credibility patterns  
- Provide verified news sources  
- Improve digital media awareness  
- Help users make informed decisions  

