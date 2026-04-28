import { useState } from 'react';
import { Sparkles, Gamepad2, Tags, Calendar, DollarSign, Target, CheckCircle2 } from 'lucide-react';

export function AnalysisForm() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showResult, setShowResult] = useState(false);

  const handleAnalyze = (e: React.FormEvent) => {
    e.preventDefault();
    setIsAnalyzing(true);
    // Simulate NLP processing time
    setTimeout(() => {
      setIsAnalyzing(false);
      setShowResult(true);
    }, 2500);
  };

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-100 tracking-tight">New Game Analysis</h1>
        <p className="text-gray-400 mt-1">Input your game details for NLP-powered market prediction</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Form Section */}
        <div className="lg:col-span-2">
          <div className="glass-panel p-8">
            <form onSubmit={handleAnalyze} className="space-y-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2 flex items-center">
                    <Gamepad2 className="w-4 h-4 mr-2 text-violet-400" />
                    Game Title
                  </label>
                  <input 
                    type="text" 
                    required
                    placeholder="e.g. Project Nova" 
                    className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-gray-200 placeholder-gray-600 focus:outline-none focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/50 transition-all"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2 flex items-center">
                      <Target className="w-4 h-4 mr-2 text-cyan-400" />
                      Primary Genre
                    </label>
                    <select className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-gray-200 focus:outline-none focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/50 transition-all appearance-none">
                      <option value="action">Action</option>
                      <option value="rpg">RPG</option>
                      <option value="strategy">Strategy</option>
                      <option value="simulation">Simulation</option>
                      <option value="adventure">Adventure</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2 flex items-center">
                      <DollarSign className="w-4 h-4 mr-2 text-emerald-400" />
                      Target Price (USD)
                    </label>
                    <input 
                      type="number" 
                      min="0"
                      step="0.01"
                      required
                      placeholder="19.99" 
                      className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-gray-200 placeholder-gray-600 focus:outline-none focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/50 transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2 flex items-center">
                    <Tags className="w-4 h-4 mr-2 text-fuchsia-400" />
                    Steam Tags (comma separated)
                  </label>
                  <input 
                    type="text" 
                    placeholder="e.g. Singleplayer, Story Rich, Atmospheric" 
                    className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-gray-200 placeholder-gray-600 focus:outline-none focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/50 transition-all"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2 flex items-center">
                    <Calendar className="w-4 h-4 mr-2 text-orange-400" />
                    Target Release Date
                  </label>
                  <input 
                    type="date" 
                    className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-gray-200 placeholder-gray-600 focus:outline-none focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/50 transition-all [color-scheme:dark]"
                  />
                </div>
              </div>

              <div className="pt-4">
                <button 
                  type="submit"
                  disabled={isAnalyzing}
                  className={`w-full py-4 rounded-xl font-bold text-white flex items-center justify-center transition-all ${
                    isAnalyzing 
                      ? 'bg-violet-600/50 cursor-not-allowed' 
                      : 'bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-500 hover:to-fuchsia-500 shadow-[0_0_20px_rgba(139,92,246,0.3)] hover:shadow-[0_0_25px_rgba(139,92,246,0.5)]'
                  }`}
                >
                  {isAnalyzing ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-3" />
                      Analyzing via BERT Model...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5 mr-2" />
                      Generate Oracle Report
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-1">
          {showResult ? (
            <div className="glass-panel p-6 animate-in fade-in slide-in-from-right-8 duration-500 relative overflow-hidden h-full flex flex-col">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-400 to-cyan-400" />
              
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center">
                  <CheckCircle2 className="w-6 h-6 text-emerald-400" />
                </div>
                <div>
                  <h3 className="font-bold text-gray-100">Analysis Complete</h3>
                  <p className="text-xs text-gray-400">Confidence Score: 89%</p>
                </div>
              </div>

              <div className="space-y-6 flex-1">
                <div>
                  <p className="text-sm text-gray-400 mb-1">Predicted Success Rate</p>
                  <div className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
                    76.4%
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="p-3 rounded-xl bg-white/5 border border-white/5">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium text-gray-300">Price Optimization</span>
                      <span className="text-xs text-emerald-400">Good</span>
                    </div>
                    <p className="text-xs text-gray-500">Your price is 15% lower than similar successful titles.</p>
                  </div>
                  
                  <div className="p-3 rounded-xl bg-white/5 border border-white/5">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium text-gray-300">Genre Saturation</span>
                      <span className="text-xs text-rose-400">High Risk</span>
                    </div>
                    <p className="text-xs text-gray-500">Action RPG market is highly saturated. Ensure unique selling points.</p>
                  </div>
                </div>
              </div>

              <button className="w-full mt-6 py-3 rounded-xl bg-white/5 hover:bg-white/10 text-gray-200 font-medium border border-white/10 transition-colors text-sm flex items-center justify-center">
                Export Detailed Report
              </button>
            </div>
          ) : (
            <div className="glass-panel p-6 h-full flex flex-col items-center justify-center text-center opacity-50">
              <Sparkles className="w-12 h-12 text-gray-600 mb-4" />
              <p className="text-gray-400 text-sm">
                Fill out the game details and click generate to see the AI market analysis report.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
