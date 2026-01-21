import streamlit as st
import google.generativeai as genai
import time

# --- 페이지 설정 ---
st.set_page_config(page_title="Suno Lyrics Master", page_icon="🎧", layout="wide")

# --- 사이드바: API 키 설정 ---
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input("Google API Key 입력", type="password", help="Gemini API 키를 입력하세요.")
    if api_key:
        genai.configure(api_key=api_key)
    
    st.info("💡 **Suno AI 팁**\n\nSuno는 `[Verse]`, `[Chorus]` 같은 태그를 인식하여 곡의 기승전결을 만듭니다.")

# --- CSS 스타일링 (수정된 부분) ---
st.markdown("""
<style>
    /* 1. 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #1a1c2c 0%, #4a192c 100%);
        color: #fff;
    }
    
    /* 2. 타이틀 스타일 */
    h1 {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        text-shadow: 0 0 10px #ff00de, 0 0 20px #ff00de;
        margin-bottom: 20px;
    }
    
    /* 3. [중요] 입력창 스타일 개선 */
    /* 입력창 배경을 어둡게(#333) 만들고, 글자는 흰색(#fff)으로 설정 */
    .stTextInput > div > div > input {
        background-color: #2b2d42 !important; /* 어두운 남색 배경 */
        color: #ffffff !important;           /* 흰색 글씨 */
        border: 1px solid #ff00de;           /* 테두리 포인트 */
        border-radius: 8px;
    }
    
    /* 셀렉트박스(드롭다운)도 동일하게 어둡게 변경 */
    .stSelectbox > div > div > div {
        background-color: #2b2d42 !important;
        color: #ffffff !important;
        border: 1px solid #ff00de;
        border-radius: 8px;
    }
    
    /* 입력창 위의 라벨(제목) 색상 */
    .stTextInput label, .stSelectbox label, .stRadio label {
        color: #00f2ff !important; /* 형광 하늘색 */
        font-weight: bold;
        font-size: 1rem;
    }
    
    /* 라디오 버튼 선택 항목 색상 */
    .stRadio div[role='radiogroup'] > label {
        color: white !important;
    }

    /* 4. 버튼 스타일 */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #ff00de, #00f2ff);
        border: none;
        color: white;
        font-weight: bold;
        padding: 15px;
        font-size: 1.2rem;
        border-radius: 30px;
        transition: 0.3s;
        margin-top: 10px;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(255, 0, 222, 0.6);
        color: white !important;
    }

    /* 5. 결과 박스 스타일 */
    .suno-box {
        background-color: #0e1117;
        border: 1px solid #555;
        border-radius: 10px;
        padding: 25px;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        line-height: 1.6;
        color: #e0e0e0;
        box-shadow: inset 0 0 30px rgba(0,0,0,0.8);
    }
    .tag { color: #ffd700; font-weight: bold; } 
</style>
""", unsafe_allow_html=True)

# --- 메인 UI ---
st.title("🎧 Suno AI Lyrics Master")
st.markdown("<div style='text-align:center; color:#ccc; margin-bottom:30px;'>Suno/Udio 전용 구조화된 가사 생성기</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. 곡 정보 입력")
    # 입력창
    genre = st.text_input("🎸 장르 (Genre)", placeholder="예: K-Pop, City Pop, Jazz")
    theme = st.text_input("💭 주제 (Theme)", placeholder="예: 네온 사인 아래 춤추는 밤")
    mood = st.text_input("🎭 분위기 (Mood)", placeholder="예: 몽환적인, 신나는, 그루비한")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("2. 구조 선택")
    structure_type = st.selectbox(
        "📑 곡 구성 방식", 
        ["Standard (Verse-Chorus)", "Hip-Hop (Intro-Verse-Hook)", "Ballad (Slow Build-up)", "Experimental (복잡한 구성)"]
    )
    lang = st.radio("🌏 언어", ["Korean", "English"], horizontal=True)

# --- 생성 로직 ---
def generate_suno_prompt(genre, theme, mood, structure, lang):
    # API 키가 없으면 데모 결과 반환
    if not api_key:
        time.sleep(2)
        return """**[Style Prompt]**
Upbeat City Pop, Female Vocals, Groovy Bassline, 80s Retro Vibe, 120 BPM

**[Lyrics]**
[Intro]
(Synthesizer Solo)
Yeah...
Neon lights calling...

[Verse 1]
어두운 골목길을 지나
화려한 불빛 속으로 dive
오늘 밤은 아무 생각 마
Just feel the rhythm, feel the vibe

[Pre-Chorus]
심장이 뛰는 소리가 들려? (Can you hear it?)
멈출 수 없는 이 기분 (So high)

[Chorus]
춤을 춰, 도시의 별들 아래
We keep on dancing through the night
이 순간이 영원하길 바래
Shining so bright, holding you tight

[Outro]
Fade out...
Just you and me...
(End)"""

    # 실제 AI 호출
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        system_prompt = f"""
        당신은 AI 음악 생성 서비스(Suno v3, Udio)를 위한 전문 작사가입니다.
        다음 정보에 맞춰 가사를 작성해 주세요.
        
        입력 정보:
        - 장르: {genre}
        - 주제: {theme}
        - 분위기: {mood}
        - 구조 타입: {structure}
        - 언어: {lang}
        
        [요구사항]
        1. 맨 윗줄에 Suno의 'Style of Music' 칸에 넣을 **영어 스타일 프롬프트**를 작성하세요.
           형식: **[Style Prompt]** (내용)
        2. 그 아래에 가사를 작성하세요. Suno가 인식할 수 있는 태그를 반드시 포함하세요.
           필수 태그: [Intro], [Verse], [Chorus], [Bridge], [Outro] 등.
           형식: **[Lyrics]** (내용)
        """
        
        response = model.generate_content(system_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- 생성 버튼 및 결과 표시 ---
with col1:
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("🎵 Suno용 가사 생성하기")

with col2:
    st.subheader("3. 결과 (Copy & Paste)")
    if generate_btn:
        if not genre or not theme:
            st.warning("⚠️ 장르와 주제를 입력해주세요!")
        else:
            with st.spinner("🎧 가사를 작성 중입니다..."):
                result_text = generate_suno_prompt(genre, theme, mood, structure_type, lang)
                
                # HTML 스타일링
                formatted_text = result_text.replace("[", "<span class='tag'>[").replace("]", "]</span>")
                formatted_text = formatted_text.replace("**[Style Prompt]**", "<strong style='color:#00f2ff; font-size:1.1em;'>🎹 Style Prompt (복사용)</strong>")
                formatted_text = formatted_text.replace("**[Lyrics]**", "<br><br><strong style='color:#00f2ff; font-size:1.1em;'>📜 Lyrics (복사용)</strong>")
                
                st.markdown(f'<div class="suno-box">{formatted_text}</div>', unsafe_allow_html=True)
                
                if not api_key:
                    st.caption("ℹ️ 현재는 데모 모드입니다. 실제 AI 생성을 위해 API 키를 입력하세요.")