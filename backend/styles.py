import streamlit as st

def apply_custom_styles():
    """Apply all custom CSS styles to the Streamlit app"""
    
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --tech-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --business-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --sports-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            --national-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            --others-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            --glass-bg: rgba(255, 255, 255, 0.25);
            --glass-border: rgba(255, 255, 255, 0.18);
            --dark-text: #2d3748;
            --light-text: #4a5568;
            --accent-blue: #4299e1;
        }
        
        * {
            font-family: 'Poppins', sans-serif;
            box-sizing: border-box;
        }
        
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            min-height: 100vh;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .main-header {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            padding: 3rem 2rem;
            border-radius: 25px;
            margin: 2rem 0 3rem 0;
            text-align: center;
            box-shadow: 
                0 20px 40px rgba(0,0,0,0.1),
                inset 0 1px 0 rgba(255,255,255,0.2);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .main-title {
            background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
            background-size: 200% 200%;
            animation: gradientText 4s ease infinite;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 4rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 2px 2px 20px rgba(0,0,0,0.1);
            letter-spacing: -2px;
        }
        
        @keyframes gradientText {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .main-subtitle {
            color: rgba(255,255,255,0.9);
            font-size: 1.4rem;
            margin-top: 1rem;
            font-weight: 300;
            text-shadow: 1px 1px 10px rgba(0,0,0,0.2);
            animation: fadeInUp 1s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .category-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2.5rem;
            box-shadow: 
                0 15px 35px rgba(0,0,0,0.1),
                inset 0 1px 0 rgba(255,255,255,0.2);
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
            border-left: none;
        }
        
        .category-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--category-gradient);
            border-radius: 20px 20px 0 0;
        }
        
        .category-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 
                0 25px 50px rgba(0,0,0,0.15),
                inset 0 1px 0 rgba(255,255,255,0.3);
        }
        
        .category-tech::before { background: var(--tech-gradient); }
        .category-business::before { background: var(--business-gradient); }
        .category-sports::before { background: var(--sports-gradient); }
        .category-national::before { background: var(--national-gradient); }
        .category-others::before { background: var(--others-gradient); }
        
        .category-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            color: var(--dark-text);
            display: flex;
            align-items: center;
            gap: 1rem;
            text-shadow: 1px 1px 10px rgba(0,0,0,0.1);
        }
        
        .category-icon {
            font-size: 2.5rem;
            filter: drop-shadow(2px 2px 8px rgba(0,0,0,0.2));
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
        }
        
        .article-item {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.3);
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 1.2rem;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
        }
        
        .article-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent-blue), transparent);
            transition: all 0.3s ease;
        }
        
        .article-item:hover {
            transform: translateY(-3px);
            background: rgba(255, 255, 255, 0.95);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .article-item:hover::before {
            left: 0;
        }
        
        .article-title {
            font-weight: 600;
            color: var(--dark-text);
            font-size: 1.2rem;
            margin-bottom: 0.8rem;
            line-height: 1.5;
            transition: color 0.3s ease;
        }
        
        .article-item:hover .article-title {
            color: var(--accent-blue);
        }
        
        .article-excerpt {
            color: var(--light-text);
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 1rem;
            opacity: 0.9;
        }
        
        .article-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85rem;
            color: #718096;
        }
        
        .article-url {
            color: var(--accent-blue);
            text-decoration: none;
            font-weight: 600;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            background: rgba(66, 153, 225, 0.1);
            transition: all 0.3s ease;
            border: 1px solid rgba(66, 153, 225, 0.2);
        }
        
        .article-url:hover {
            background: var(--accent-blue);
            color: white;
            transform: scale(1.05);
            text-decoration: none;
        }
        
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }
        
        .stat-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        
        .stat-card:hover::before {
            opacity: 1;
        }
        
        .stat-number {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            font-family: 'JetBrains Mono', monospace;
        }
        
        .stat-label {
            color: rgba(255,255,255,0.8);
            font-size: 1rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .control-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            padding: 2rem;
            border-radius: 20px;
            margin: 2rem 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: white !important;
            border: none !important;
            border-radius: 15px !important;
            padding: 0.8rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3) !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        }
        
        .stCheckbox > label {
            color: rgba(255,255,255,0.9) !important;
            font-weight: 500 !important;
        }
        
        .loading-container {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 4rem;
        }
        
        .spinner {
            width: 60px;
            height: 60px;
            border: 4px solid rgba(255,255,255,0.3);
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .no-articles {
            text-align: center;
            padding: 3rem 2rem;
            color: rgba(255,255,255,0.7);
            font-style: italic;
            font-size: 1.1rem;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .error-container {
            background: rgba(252, 165, 165, 0.2);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(252, 165, 165, 0.3);
            border-radius: 15px;
            padding: 1.5rem;
            color: #e53e3e;
            margin: 1rem 0;
        }
        
        .success-message {
            background: rgba(134, 239, 172, 0.2);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(134, 239, 172, 0.3);
            border-radius: 15px;
            padding: 1.5rem;
            color: #38a169;
            margin: 1rem 0;
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .stExpander {
            background: rgba(255,255,255,0.1) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            border-radius: 10px !important;
            margin: 1rem 0 !important;
        }
        
        .stProgress .stProgress-bar {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            border-radius: 10px !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2, #667eea);
        }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .main-title {
                font-size: 2.5rem;
            }
            .main-subtitle {
                font-size: 1.1rem;
            }
            .category-title {
                font-size: 1.8rem;
            }
            .stats-container {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        /* Particle effect */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
        
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(255,255,255,0.3);
            border-radius: 50%;
            animation: float-particle 15s infinite linear;
        }
        
        @keyframes float-particle {
            0% {
                transform: translateY(100vh) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh) rotate(360deg);
                opacity: 0;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Add floating particles effect
    st.markdown("""
    <div class="particles">
        <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
        <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
        <div class="particle" style="left: 40%; animation-delay: 6s;"></div>
        <div class="particle" style="left: 50%; animation-delay: 8s;"></div>
        <div class="particle" style="left: 60%; animation-delay: 10s;"></div>
        <div class="particle" style="left: 70%; animation-delay: 12s;"></div>
        <div class="particle" style="left: 80%; animation-delay: 14s;"></div>
        <div class="particle" style="left: 90%; animation-delay: 16s;"></div>
    </div>
    """, unsafe_allow_html=True)