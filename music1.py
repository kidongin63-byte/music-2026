import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Gemini 가사 생성기", page_icon="🎵", layout="wide")

# 스타일 설정
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton > button {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 30px;
    }
    h1 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    /* 텍스트 입력 필드 라벨 색상 변경 */
    .stTextInput > label, .stSelectbox > label {
        color: white !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 헤더
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("# 🎵 Gemini 가사 생성기 🎵")
    st.markdown("<p style='text-align: center; color: white;'>Google Gemini가 당신만의 특별한 가사를 만들어드립니다</p>", 
                unsafe_allow_html=True)

st.divider()

# 사이드바에서 API 키 설정 (Gemini)
api_key = st.sidebar.text_input(
    "Gemini API Key 입력",
    type="password",
    help="https://aistudio.google.com/app/apikey 에서 API 키를 받으세요"
)

# 입력 폼
col1, col2 = st.columns(2)

with col1:
    genre = st.text_input(
        "🎸 장르",
        placeholder="예: 발라드, 힙합, 록, 팝",
        help="음악의 장르를 입력하세요"
    )
    mood = st.text_input(
        "😊 분위기",
        placeholder="예: 슬픈, 신나는, 차분한, 열정적인",
        help="원하는 분위기를 입력하세요"
    )

with col2:
    theme = st.text_input(
        "💭 주제",
        placeholder="예: 사랑, 이별, 희망, 우정",
        help="가사의 주제를 입력하세요"
    )
    language = st.selectbox(
        "🌐 언어",
        ["한국어", "English"],
        help="생성할 가사의 언어를 선택하세요"
    )

# 가사 생성 버튼
if st.button("🎵 가사 생성하기", use_container_width=True, type="primary"):
    if not genre and not theme and not mood:
        st.error("⚠️ 장르, 주제, 또는 분위기 중 하나 이상을 입력해주세요.")
    elif not api_key:
        st.error("⚠️ Gemini API 키를 입력해주세요.")
    else:
        with st.spinner("🎵 Gemini가 가사를 작곡하는 중입니다..."):
            try:
                # Gemini 설정
                genai.configure(api_key=api_key)
                
                # 모델 선택 (gemini-1.5-flash가 빠르고 효율적입니다)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 프롬프트 구성
                lang_text = "한국어" if language == "한국어" else "영어"
                prompt_parts = [
                    f"당신은 전문 작사가입니다. {lang_text}로 음악 가사를 작성해주세요.",
                ]
                
                if genre:
                    prompt_parts.append(f"장르: {genre}")
                if theme:
                    prompt_parts.append(f"주제: {theme}")
                if mood:
                    prompt_parts.append(f"분위기: {mood}")
                
                prompt_parts.append("\n[Verse], [Chorus], [Bridge] 등의 구조를 명확히 표시하여 완성된 가사를 작성해주세요.")
                
                prompt = "\n".join(prompt_parts)
                
                # API 호출 (Gemini 방식)
                response = model.generate_content(prompt)
                lyrics = response.text
                
                # 결과 표시
                st.success("✅ 가사가 생성되었습니다!")
                st.markdown("---")
                st.markdown("### 📝 생성된 가사")
                st.markdown(f"""
                <div style='background-color: rgba(255, 255, 255, 0.1); 
                           border: 2px solid rgba(255, 255, 255, 0.3);
                           border-radius: 10px;
                           padding: 20px;
                           color: white;
                           font-family: monospace;
                           white-space: pre-wrap;
                           word-wrap: break-word;'>
                {lyrics}
                </div>
                """, unsafe_allow_html=True)
                
                # 다운로드 버튼
                st.download_button(
                    label="📥 가사 다운로드",
                    data=lyrics,
                    file_name=f"lyrics_{language}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}\nAPI 키가 올바른지 확인해주세요.")

st.divider()
st.markdown("""
<div style='text-align: center; color: white; font-size: 12px;'>
    <p>🎵 AI 가사 생성기 | Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)