# ⚡ GitHub Repository Analyzer

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**AI-Powered Repository Intelligence Platform**

Analyze any GitHub repository instantly with comprehensive insights, tech stack detection, and AI-powered improvement suggestions.

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Tech Stack](#tech-stack) • [Screenshots](#screenshots)

</div>

---

## ✨ Features

### 🎯 Core Functionality

- **📊 Comprehensive Repository Analysis**
  - Detailed repository metrics (stars, forks, watchers, issues)
  - Repository health indicators
  - Creation and update timestamps
  - License and topic information
  - Repository size and language statistics

- **🛠️ Advanced Tech Stack Detection**
  - Detects 50+ technologies, frameworks, and tools
  - Identifies programming languages
  - Recognizes popular frameworks (React, Vue, Django, Flask, etc.)
  - Detects DevOps tools (Docker, Kubernetes, CI/CD)
  - Identifies testing frameworks and build tools
  - Database and package manager detection

- **🤖 AI-Powered Suggestions**
  - Smart improvement recommendations
  - Code quality insights
  - Security best practices
  - Documentation suggestions
  - Testing and structure improvements

### 🎨 Design & UX

- **🌙 Premium Dark Tech Theme**
  - Modern glassmorphism effects
  - Vibrant gradient accents
  - Smooth color transitions
  - Professional typography (Inter font)

- **✨ Smooth Animations**
  - Entrance animations for all elements
  - Hover effects and micro-interactions
  - Scroll-based reveal animations
  - Loading states and transitions
  - Particle effects on mouse movement

- **📱 Responsive Design**
  - Mobile-first approach
  - Adaptive layouts for all screen sizes
  - Touch-friendly interactions
  - Optimized for tablets and desktops

### 🚀 Interactive Features

- **Click-to-copy** repository names
- **Real-time form validation**
- **Loading overlays** with progress indicators
- **Notification system** for user feedback
- **Smooth scrolling** and navigation
- **Performance optimizations** for low-end devices

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/github_repo_analyzer.git
cd github_repo_analyzer
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables (Optional)

For AI-powered suggestions, create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

> **Note:** AI suggestions will show a fallback message if the API key is not configured.

### Step 5: Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## 📖 Usage

### Analyzing a Repository

1. **Enter Repository URL**
   - Paste any public GitHub repository URL
   - Format: `https://github.com/username/repository`

2. **Click "Analyze Repository"**
   - The app will fetch repository data
   - Tech stack will be automatically detected
   - AI suggestions will be generated (if configured)

3. **View Results**
   - **Repository Overview**: Stars, forks, watchers, and more
   - **Tech Stack**: All detected technologies
   - **AI Suggestions**: Improvement recommendations
   - **Health Metrics**: Repository activity and popularity scores

### Example URLs to Try

```
https://github.com/facebook/react
https://github.com/pallets/flask
https://github.com/django/django
https://github.com/microsoft/vscode
```

---

## 🛠️ Tech Stack

### Backend

- **Flask** - Web framework
- **PyGithub** - GitHub API integration
- **OpenAI API** - AI-powered suggestions

### Frontend

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with variables
- **JavaScript (ES6+)** - Interactive features
- **Google Fonts (Inter)** - Typography

### Design System

- **CSS Custom Properties** - Design tokens
- **Glassmorphism** - Modern UI effects
- **Gradient Accents** - Visual hierarchy
- **Smooth Animations** - Enhanced UX

---

## 📁 Project Structure

```
github_repo_analyzer/
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── static/
│   ├── style.css              # Main stylesheet (enhanced)
│   └── script.js              # Interactive features
├── templates/
│   └── index.html             # Main template (redesigned)
└── utils/
    ├── __init__.py
    ├── github_analyzer.py     # Repository analysis (enhanced)
    ├── tech_stack_detector.py # Tech detection (50+ technologies)
    └── ai_suggester.py        # AI suggestions
```

---

## 🎨 Design Features

### Color Palette

- **Primary**: `#3b82f6` (Blue)
- **Accent**: `#8b5cf6` (Purple)
- **Success**: `#10b981` (Green)
- **Warning**: `#f59e0b` (Orange)
- **Background**: `#0a0e1a` (Dark)

### Typography

- **Font Family**: Inter (Google Fonts)
- **Weights**: 400 (Regular), 600 (Semi-bold), 700 (Bold), 800 (Extra-bold)

### Animations

- **Fade In/Out**: Smooth opacity transitions
- **Slide In**: Directional entrance animations
- **Scale**: Hover effects and micro-interactions
- **Float**: Subtle vertical movements
- **Pulse**: Breathing animations

---

## 🔧 Configuration

### Customizing the Theme

Edit `static/style.css` to modify CSS variables:

```css
:root {
    --color-primary: #3b82f6;
    --color-accent: #8b5cf6;
    /* Add your custom colors */
}
```

### Adding More Tech Detection

Edit `utils/tech_stack_detector.py`:

```python
if "your-file.ext" in file:
    tech.add("Your Technology")
```

### Customizing AI Prompts

Edit `utils/ai_suggester.py` to modify the AI prompt template.

---

## 📊 Features Comparison

| Feature | Basic Version | Enhanced Version ✨ |
|---------|--------------|---------------------|
| Repository Stats | ⭐ Stars, Language | ⭐ Stars, Forks, Watchers, Issues, Dates, Size, License, Topics |
| Tech Detection | 8 technologies | 50+ technologies |
| UI Design | Basic styling | Premium dark tech theme with glassmorphism |
| Animations | None | Smooth entrance, hover, and scroll animations |
| Interactivity | Static | Click-to-copy, notifications, particle effects |
| Responsive | Basic | Mobile-first, fully responsive |
| Loading States | None | Loading overlays and progress indicators |
| Health Metrics | None | Activity level, popularity score, community strength |

---

## 🚀 Performance

- **Optimized animations** for smooth 60fps performance
- **Lazy loading** for scroll-based animations
- **Reduced motion** support for low-end devices
- **Efficient DOM manipulation**
- **Minimal JavaScript footprint**

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Flask** - Lightweight web framework
- **PyGithub** - GitHub API wrapper
- **OpenAI** - AI-powered suggestions
- **Google Fonts** - Inter typeface
- **GitHub** - Repository hosting and API

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

<div align="center">

**Built with ❤️ using Flask & AI**

⭐ Star this repo if you find it helpful!

</div>
