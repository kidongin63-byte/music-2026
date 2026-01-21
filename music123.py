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
    
    st.info("💡 **Suno AI 팁**\n\nSuno는 `[Verse]`, `[Chorus]` 같은 태그를 인식하여 곡의 기승전결을 만듭니다. 생성된 가사를 그대로 복사해서 Custom Mode에 붙여넣으세요!")

# --- CSS 스타일링 (네온 & 그라데이션) ---
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #1a1c2c 0%, #4a192c 100%);
        color: #fff;
    }
    
    /* 타이틀 */
    h1 {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        text-shadow: 0 0 10px #ff00de, 0 0 20px #ff00de;
        margin-bottom: 10px;
    }
    
    /* 입력 위젯 스타일 */
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid #ff00de;
        border-radius: 8px;
    }
    .stTextInput label, .stSelectbox label {
        color: #00f2ff !important;
        font-weight: bold;
    }

    /* 버튼 스타일 */
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
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(255, 0, 222, 0.6);
    }

    /* 결과 박스 (Suno 스타일) */
    .suno-box {
        background-color: #0e1117;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        line-height: 1.6;
        color: #e0e0e0;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
    }
    .tag { color: #ffd700; font-weight: bold; } /* 태그 색상 (노랑) */
    .style-prompt { color: #00f2ff; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# --- 메인 UI ---
st.title("🎧 Suno AI Lyrics Master")
st.markdown("<div style='text-align:center; color:#ccc; margin-bottom:30px;'>Suno/Udio 전용 구조화된 가사 생성기</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. 곡 정보 입력")
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
    # API 키가 없으면 Mock 데이터 반환
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

[Interlude]
(Saxophone Solo)

[Verse 2]
차가운 바람도 우릴 못 막아
네 손을 잡고 어디든 갈게
복잡한 세상은 잠시 잊어
음악 속에 우리 둘만 남게

[Chorus]
춤을 춰, 도시의 별들 아래
We keep on dancing through the night
이 순간이 영원하길 바래
Shining so bright, holding you tight

[Bridge]
시간이 멈춘 듯해
새벽이 올 때까지
Don't stop the music
Oh yeah!

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
        1. 맨 윗줄에 Suno의 'Style of Music' 칸에 넣을 **영어 스타일 프롬프트**를 작성하세요. (악기, BPM, 보컬 성별 포함)
           형식: **[Style Prompt]** (내용)
        2. 그 아래에 가사를 작성하세요. Suno가 인식할 수 있는 태그를 반드시 포함하세요.
           필수 태그 예시: [Intro], [Verse], [Pre-Chorus], [Chorus], [Bridge], [Outro], [Instrumental Break], [Rap Verse] 등.
           형식: **[Lyrics]** (내용)
        3. 구조 타입 '{structure}'에 맞게 섹션을 배치하세요.
        4. 가사 중간에 (Ad-lib), (Backing Vocals) 같은 연출 지시어도 포함하세요.
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
            with st.spinner("🎧 비트를 분석하고 가사를 쓰는 중..."):
                result_text = generate_suno_prompt(genre, theme, mood, structure_type, lang)
                
                # 결과 텍스트를 HTML로 변환하여 스타일 적용 (태그 강조)
                formatted_text = result_text.replace("[", "<span class='tag'>[").replace("]", "]</span>")
                formatted_text = formatted_text.replace("**[Style Prompt]**", "<strong style='color:#00f2ff; font-size:1.1em;'>🎹 Style Prompt (복사해서 Style 칸에 입력)</strong>")
                formatted_text = formatted_text.replace("**[Lyrics]**", "<br><br><strong style='color:#00f2ff; font-size:1.1em;'>📜 Lyrics (복사해서 Lyrics 칸에 입력)</strong>")
                
                st.markdown(f'<div class="suno-box">{formatted_text}</div>', unsafe_allow_html=True)
                
                # API 키가 없을 때 안내
                if not api_key:
                    st.caption("ℹ️ 현재는 데모(Mock) 모드입니다. 실제 AI 생성을 하려면 왼쪽 사이드바에 Google API Key를 입력하세요.")