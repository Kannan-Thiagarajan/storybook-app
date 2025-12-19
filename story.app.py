
import React, { useState } from 'react';
import { SCHOOL_NAME, SCHOOL_LOGO_URL, TEACHER_AVATAR_URL, INTRO_TEXT, CREATOR_NAME, GENRES, ACTIVITY_TITLE } from './constants';
import { ReflectionData, TeacherFeedback } from './types';
import { generateTeacherFeedback } from './services/geminiService';
import Certificate from './components/Certificate';

const App: React.FC = () => {
  const [step, setStep] = useState<'form' | 'loading' | 'certificate'>('form');
  const [formData, setFormData] = useState<ReflectionData>({
    studentName: '',
    bookTitle: '',
    author: '',
    genre: GENRES[0],
    keyCharacters: '',
    favoritePart: '',
    moral: '',
    rating: 5
  });
  const [feedback, setFeedback] = useState<TeacherFeedback | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStep('loading');
    
    try {
      const aiFeedback = await generateTeacherFeedback(formData);
      setFeedback(aiFeedback);
      setStep('certificate');
      // Trigger Confetti
      // @ts-ignore
      if (typeof confetti === 'function') {
        // @ts-ignore
        confetti({
          particleCount: 150,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#f59e0b', '#6366f1', '#ec4899']
        });
      }
    } catch (error) {
      console.error("AI Error:", error);
      setFeedback({
        comment: "Outstanding exploration of this story! Your mind is a vast universe.",
        ratingWord: "Legendary!"
      });
      setStep('certificate');
    }
  };

  const handlePrint = () => {
    // Small delay to ensure any layout shifts are finished
    setTimeout(() => {
      window.print();
    }, 100);
  };

  const reset = () => {
    setStep('form');
    setFormData({
      studentName: '',
      bookTitle: '',
      author: '',
      genre: GENRES[0],
      keyCharacters: '',
      favoritePart: '',
      moral: '',
      rating: 5
    });
    setFeedback(null);
  };

  return (
    <div className="min-h-screen flex flex-col pb-12 transition-colors duration-500 overflow-x-hidden">
      {/* Header */}
      <header className="no-print bg-slate-900/80 border-b border-slate-800 shadow-xl backdrop-blur-md p-4 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <img src={SCHOOL_LOGO_URL} alt="Logo" className="h-10 w-10 object-contain" />
            <div>
              <h1 className="text-lg font-kids text-amber-500 leading-none">{SCHOOL_NAME}</h1>
              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest mt-1">Reading Galaxy Portal</p>
            </div>
          </div>
          <div className="hidden md:flex items-center gap-2 text-xs font-bold bg-slate-800 px-3 py-1.5 rounded-full border border-slate-700">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            AI LIBRARIAN ONLINE
          </div>
        </div>
      </header>

      <main className="flex-grow max-w-5xl mx-auto w-full px-4 pt-8">
        
        {/* Activity Highlight Title */}
        <div className="no-print mb-8 text-center animate-in fade-in zoom-in duration-1000">
            <h2 className="text-2xl md:text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-amber-200 to-amber-500 tracking-tighter uppercase drop-shadow-[0_0_15px_rgba(251,191,36,0.3)]">
                f"🚀 {ACTIVITY_TITLE} 🚀"
            </h2>
            <div className="h-1 w-32 bg-amber-500 mx-auto mt-2 rounded-full shadow-[0_0_10px_rgba(245,158,11,1)]"></div>
        </div>

        {step === 'form' && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-6 duration-700">
            
            {/* Instructions Panel */}
            <div className="bg-indigo-600/20 border border-indigo-500/30 rounded-3xl p-6 flex flex-col md:flex-row items-center gap-6 shadow-2xl overflow-hidden relative">
              <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full -mr-16 -mt-16 blur-3xl"></div>
              <div className="flex-shrink-0 bg-indigo-500/20 p-4 rounded-full border border-indigo-500/50">
                <span className="text-4xl">📚</span>
              </div>
              <div>
                <h2 className="text-xl font-kids text-indigo-300">Holiday Mission Instructions</h2>
                <ul className="text-sm text-indigo-100/80 mt-2 space-y-1">
                  <li>✨ Read <strong>ANY</strong> book you like - your gifts or library treasures!</li>
                  <li>✨ Fill in the reflection form below to unlock your reward.</li>
                  <li>✨ <strong>IMPORTANT:</strong> Use the button below to <strong>PRINT</strong> your certificate. Collect them for the end-of-semester showcase!</li>
                </ul>
              </div>
            </div>

            {/* Teacher Intro */}
            <div className="glass-card rounded-3xl shadow-2xl overflow-hidden border border-slate-700">
              <div className="bg-gradient-to-r from-amber-600/90 to-amber-500/90 p-6 flex items-center gap-6">
                <div className="relative">
                  <img 
                    src={TEACHER_AVATAR_URL} 
                    alt="AI Teacher" 
                    className="w-20 h-20 rounded-full border-4 border-white/20 shadow-xl object-cover bg-slate-800" 
                  />
                  <div className="absolute -bottom-1 -right-1 bg-green-500 w-5 h-5 rounded-full border-2 border-slate-900 shadow-lg"></div>
                </div>
                <div className="text-white">
                  <h2 className="text-2xl font-kids tracking-tight">System Initialization...</h2>
                  <p className="text-amber-50 text-sm leading-relaxed mt-1 opacity-90">{INTRO_TEXT}</p>
                </div>
              </div>

              {/* Input Form */}
              <form onSubmit={handleSubmit} className="p-8 space-y-8">
                <div className="grid md:grid-cols-2 gap-8">
                  <div className="space-y-3">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                      <span className="text-amber-500">01.</span> Explorer Name
                    </label>
                    <input
                      required
                      type="text"
                      className="w-full p-4 rounded-2xl bg-slate-800/50 border border-slate-700 focus:border-amber-500 focus:ring-4 focus:ring-amber-500/10 outline-none transition-all text-white placeholder-slate-500"
                      placeholder="Enter your full name"
                      value={formData.studentName}
                      onChange={(e) => setFormData({...formData, studentName: e.target.value})}
                    />
                  </div>
                  <div className="space-y-3">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                      <span className="text-amber-500">02.</span> Book Title
                    </label>
                    <input
                      required
                      type="text"
                      className="w-full p-4 rounded-2xl bg-slate-800/50 border border-slate-700 focus:border-amber-500 focus:ring-4 focus:ring-amber-500/10 outline-none transition-all text-white placeholder-slate-500"
                      placeholder="Which world did you visit?"
                      value={formData.bookTitle}
                      onChange={(e) => setFormData({...formData, bookTitle: e.target.value})}
                    />
                  </div>
                </div>

                <div className="grid md:grid-cols-3 gap-6">
                  <div className="space-y-3">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                      <span className="text-amber-500">03.</span> Author
                    </label>
                    <input
                      required
                      type="text"
                      className="w-full p-4 rounded-xl bg-slate-800/50 border border-slate-700 focus:border-amber-500 transition-all text-white"
                      placeholder="The Author"
                      value={formData.author}
                      onChange={(e) => setFormData({...formData, author: e.target.value})}
                    />
                  </div>
                  <div className="space-y-3">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                      <span className="text-amber-500">04.</span> Genre
                    </label>
                    <select
                      className="w-full p-4 rounded-xl bg-slate-800/50 border border-slate-700 focus:border-amber-500 transition-all text-white appearance-none cursor-pointer"
                      value={formData.genre}
                      onChange={(e) => setFormData({...formData, genre: e.target.value})}
                    >
                      {GENRES.map(g => <option key={g} value={g} className="bg-slate-900">{g}</option>)}
                    </select>
                  </div>
                  <div className="space-y-3">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                      <span className="text-amber-500">05.</span> Rating
                    </label>
                    <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-800/50 border border-slate-700 star-rating">
                      {[1, 2, 3, 4, 5].map((s) => (
                        <button
                          key={s}
                          type="button"
                          onClick={() => setFormData({...formData, rating: s})}
                          className={`text-2xl transition-all ${s <= formData.rating ? 'text-amber-400 scale-110 drop-shadow-[0_0_8px_rgba(251,191,36,0.5)]' : 'text-slate-600 grayscale opacity-50'}`}
                        >
                          ★
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <label className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                    <span className="text-amber-500">06.</span> Key Characters
                  </label>
                  <input
                    required
                    type="text"
                    className="w-full p-4 rounded-2xl bg-slate-800/50 border border-slate-700 focus:border-amber-500 transition-all text-white placeholder-slate-600"
                    placeholder="e.g. Harry, Hermione, and Ron"
                    value={formData.keyCharacters}
                    onChange={(e) => setFormData({...formData, keyCharacters: e.target.value})}
                  />
                </div>

                <div className="grid md:grid-cols-2 gap-8">
                  <div className="space-y-3">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                      <span className="text-amber-500">07.</span> Favorite Moment
                    </label>
                    <textarea
                      required
                      rows={3}
                      className="w-full p-4 rounded-2xl bg-slate-800/50 border border-slate-700 focus:border-amber-500 transition-all text-white resize-none"
                      placeholder="What was the most exciting part for you?"
                      value={formData.favoritePart}
                      onChange={(e) => setFormData({...formData, favoritePart: e.target.value})}
                    />
                  </div>
                  <div className="space-y-3">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                      <span className="text-amber-500">08.</span> The Big Lesson
                    </label>
                    <textarea
                      required
                      rows={3}
                      className="w-full p-4 rounded-2xl bg-slate-800/50 border border-slate-700 focus:border-amber-500 transition-all text-white resize-none"
                      placeholder="What did this book teach you?"
                      value={formData.moral}
                      onChange={(e) => setFormData({...formData, moral: e.target.value})}
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-500 hover:to-amber-400 text-white font-kids text-xl py-6 rounded-2xl shadow-[0_8px_32px_rgba(245,158,11,0.3)] transform hover:-translate-y-1 active:scale-[0.98] transition-all flex items-center justify-center gap-4 group"
                >
                  <span className="text-2xl group-hover:rotate-12 transition-transform">🎓</span>
                  Process Reflection & Get Reward
                </button>
              </form>
            </div>
          </div>
        )}

        {step === 'loading' && (
          <div className="flex flex-col items-center justify-center py-32 space-y-8 animate-in fade-in duration-500">
            <div className="relative">
                <div className="w-40 h-40 rounded-full border-[10px] border-slate-800/50 border-t-amber-500 animate-spin"></div>
                <img 
                  src={TEACHER_AVATAR_URL} 
                  className="w-28 h-28 rounded-full absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 shadow-2xl bg-slate-900 border-4 border-slate-700" 
                />
            </div>
            <div className="text-center space-y-2">
              <h2 className="text-3xl font-kids text-amber-500 tracking-wide animate-pulse">Analyzing Reflection...</h2>
              <p className="text-slate-400 text-lg italic">The AI Librarian is impressed by your progress!</p>
            </div>
          </div>
        )}

        {step === 'certificate' && feedback && (
          <div className="space-y-10 animate-in fade-in zoom-in duration-1000">
            <div className="no-print bg-amber-500/10 border border-amber-500/30 rounded-3xl p-8 flex flex-col md:flex-row items-center gap-8 shadow-2xl relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-amber-500 to-transparent"></div>
              <div className="bg-amber-500/20 p-6 rounded-full border border-amber-500/40 shadow-inner">
                <span className="text-5xl">🎖️</span>
              </div>
              <div>
                <h3 className="text-2xl font-kids text-amber-400">Mission Accomplished, {formData.studentName}!</h3>
                <p className="text-slate-300 text-lg leading-relaxed mt-2 italic">"{feedback.comment}"</p>
                <div className="mt-4 flex items-center gap-4">
                  <span className="px-4 py-1.5 bg-amber-500 text-white text-xs font-bold rounded-full uppercase tracking-widest">{feedback.ratingWord}</span>
                  <span className="text-xs text-slate-500 font-medium italic">Verified for Holiday Challenge</span>
                </div>
              </div>
            </div>

            <div className="flex justify-center transition-all duration-1000 hover:scale-[1.01] overflow-hidden rounded-lg shadow-2xl">
                <Certificate data={formData} feedback={feedback} />
            </div>

            <div className="no-print flex flex-col sm:flex-row items-center justify-center gap-6 py-8">
              <button
                type="button"
                onClick={handlePrint}
                className="w-full sm:w-auto px-12 py-5 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:shadow-[0_0_40px_rgba(79,70,229,0.4)] text-white font-bold rounded-2xl shadow-xl transition-all flex items-center justify-center gap-3 transform hover:-translate-y-1 active:scale-95 group cursor-pointer"
              >
                <span className="text-2xl group-hover:scale-125 transition-transform">🖨️</span>
                Print & Collect Certificate
              </button>
              <button
                type="button"
                onClick={reset}
                className="w-full sm:w-auto px-10 py-5 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold rounded-2xl border border-slate-700 transition-all flex items-center justify-center gap-2 active:scale-95 cursor-pointer"
              >
                <span>🚀</span> Start Next Mission
              </button>
            </div>
            
            <div className="no-print text-center bg-slate-900/50 p-6 rounded-2xl border border-dashed border-slate-700">
              <p className="text-sm text-slate-500">
                <strong>Reading Tip:</strong> Collect all your holiday reflections to win a special badge next semester!
              </p>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="no-print mt-auto py-12 text-center text-slate-600 text-sm">
        <div className="max-w-xs mx-auto border-t border-slate-800/50 pt-6">
          <p>© {new Date().getFullYear()} {SCHOOL_NAME}</p>
          <p className="mt-2 text-slate-500">
            Handcrafted for SJKT Scholars by <br/>
            <span className="font-bold text-amber-600/70 hover:text-amber-500 transition-colors cursor-default">{CREATOR_NAME}</span>
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;

