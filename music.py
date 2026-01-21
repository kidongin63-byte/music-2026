import React, { useState } from 'react';
import { Music, Sparkles, Loader2 } from 'lucide-react';

export default function LyricsGenerator() {
  const [genre, setGenre] = useState('');
  const [theme, setTheme] = useState('');
  const [mood, setMood] = useState('');
  const [language, setLanguage] = useState('korean');
  const [lyrics, setLyrics] = useState('');
  const [loading, setLoading] = useState(false);

  const generateLyrics = async () => {
    if (!genre && !theme && !mood) {
      alert('장르, 주제, 또는 분위기 중 하나 이상을 입력해주세요.');
      return;
    }

    setLoading(true);
    setLyrics('');

    try {
      const prompt = `${language === 'korean' ? '한국어' : '영어'}로 음악 가사를 작성해주세요.
${genre ? `장르: ${genre}` : ''}
${theme ? `주제: ${theme}` : ''}
${mood ? `분위기: ${mood}` : ''}

verse, chorus, bridge 구조를 포함한 완성된 가사를 작성해주세요.`;

      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-20250514',
          max_tokens: 1000,
          messages: [
            {
              role: 'user',
              content: prompt
            }
          ]
        })
      });

      const data = await response.json();
      const generatedLyrics = data.content
        .filter(item => item.type === 'text')
        .map(item => item.text)
        .join('\n');
      
      setLyrics(generatedLyrics);
    } catch (error) {
      console.error('가사 생성 오류:', error);
      alert('가사 생성 중 오류가 발생했습니다. 다시 시도해주세요.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-pink-800 p-6">
      <div className="max-w-4xl mx-auto">
        {/* 헤더 */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Music className="w-12 h-12 text-pink-300" />
            <h1 className="text-5xl font-bold text-white">가사 생성기</h1>
            <Sparkles className="w-12 h-12 text-yellow-300" />
          </div>
          <p className="text-purple-200 text-lg">AI가 당신만의 특별한 가사를 만들어드립니다</p>
        </div>

        {/* 입력 폼 */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 mb-6 shadow-2xl">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-white font-semibold mb-2">장르</label>
              <input
                type="text"
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
                placeholder="예: 발라드, 힙합, 록, 팝"
                className="w-full px-4 py-3 rounded-lg bg-white/20 text-white placeholder-purple-200 border border-white/30 focus:outline-none focus:ring-2 focus:ring-pink-400"
              />
            </div>
            <div>
              <label className="block text-white font-semibold mb-2">주제</label>
              <input
                type="text"
                value={theme}
                onChange={(e) => setTheme(e.target.value)}
                placeholder="예: 사랑, 이별, 희망, 우정"
                className="w-full px-4 py-3 rounded-lg bg-white/20 text-white placeholder-purple-200 border border-white/30 focus:outline-none focus:ring-2 focus:ring-pink-400"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-white font-semibold mb-2">분위기</label>
              <input
                type="text"
                value={mood}
                onChange={(e) => setMood(e.target.value)}
                placeholder="예: 슬픈, 신나는, 차분한, 열정적인"
                className="w-full px-4 py-3 rounded-lg bg-white/20 text-white placeholder-purple-200 border border-white/30 focus:outline-none focus:ring-2 focus:ring-pink-400"
              />
            </div>
            <div>
              <label className="block text-white font-semibold mb-2">언어</label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full px-4 py-3 rounded-lg bg-white/20 text-white border border-white/30 focus:outline-none focus:ring-2 focus:ring-pink-400"
              >
                <option value="korean" className="bg-purple-900">한국어</option>
                <option value="english" className="bg-purple-900">English</option>
              </select>
            </div>
          </div>

          <button
            onClick={generateLyrics}
            disabled={loading}
            className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white font-bold py-4 px-6 rounded-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                가사 생성 중...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                가사 생성하기
              </>
            )}
          </button>
        </div>

        {/* 결과 표시 */}
        {lyrics && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
              <Music className="w-6 h-6" />
              생성된 가사
            </h2>
            <div className="bg-white/5 rounded-lg p-6 border border-white/20">
              <pre className="text-white whitespace-pre-wrap font-sans leading-relaxed">
                {lyrics}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}