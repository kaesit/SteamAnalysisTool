import { useState } from 'react';
import { Terminal, Cpu, Database, Binary, AlertTriangle, CheckSquare } from 'lucide-react';

export function AnalysisForm() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showResult, setShowResult] = useState(false);

  const handleAnalyze = (e: React.FormEvent) => {
    e.preventDefault();
    setIsAnalyzing(true);
    setTimeout(() => {
      setIsAnalyzing(false);
      setShowResult(true);
    }, 3000);
  };

  return (
    <div className="animate-in fade-in duration-300 max-w-[1400px] mx-auto">
      <div className="mb-10 flex justify-between items-end border-b-2 border-sys-blue pb-6">
        <div>
          <div className="flex items-center mb-2">
            <div className="w-6 h-6 bg-sys-text mr-3 flex items-center justify-center rounded-sm">
              <div className="w-2 h-2 bg-sys-black" />
            </div>
            <div className="text-sys-muted text-[10px] tracking-widest font-bold uppercase">MODULE: UPLINK_INIT_V2.1</div>
          </div>
          <h1 className="text-4xl font-bold text-sys-text tracking-widest uppercase">NEW ANALYSIS UPLINK</h1>
        </div>
        <div className="text-right bg-sys-navy p-4 border border-sys-blue relative">
          <div className="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-sys-text" />
          <div className="absolute bottom-0 right-0 w-2 h-2 border-b-2 border-r-2 border-sys-text" />
          <div className="text-[10px] text-sys-muted font-bold tracking-widest uppercase">AWAITING INPUT...</div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Form Section */}
        <div className="xl:col-span-2">
          <div className="cyno-panel p-8 md:p-10">
            <div className="flex items-center mb-8 border-b border-sys-blue pb-4">
               <Terminal className="w-5 h-5 text-sys-accent mr-3" />
               <h2 className="text-sm font-bold text-sys-text tracking-widest uppercase">CONFIGURE ENTITY PARAMETERS</h2>
            </div>
            <form onSubmit={handleAnalyze} className="space-y-6">
              <div className="space-y-6">
                <div>
                  <label className="block text-[11px] font-bold text-sys-muted mb-2 uppercase tracking-widest">
                    [01] ENTITY IDENTIFIER
                  </label>
                  <input 
                    type="text" 
                    required
                    placeholder="e.g. PROJECT_NOVA" 
                    className="w-full bg-sys-black border border-sys-blue p-4 text-sys-text placeholder-sys-navy focus:outline-none focus:border-sys-accent transition-colors uppercase font-mono text-sm rounded-sm"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-[11px] font-bold text-sys-muted mb-2 uppercase tracking-widest">
                      [02] PRIMARY CLASSIFICATION
                    </label>
                    <div className="relative">
                      <select className="w-full bg-sys-black border border-sys-blue p-4 text-sys-text focus:outline-none focus:border-sys-accent transition-colors uppercase font-mono text-sm appearance-none rounded-sm">
                        <option value="action">ACTION</option>
                        <option value="rpg">RPG</option>
                        <option value="strategy">STRATEGY</option>
                        <option value="simulation">SIMULATION</option>
                        <option value="adventure">ADVENTURE</option>
                      </select>
                      <div className="absolute right-4 top-4 text-sys-accent pointer-events-none">▼</div>
                    </div>
                  </div>

                  <div>
                    <label className="block text-[11px] font-bold text-sys-muted mb-2 uppercase tracking-widest">
                      [03] FINANCIAL TARGET (USD)
                    </label>
                    <input 
                      type="number" 
                      min="0"
                      step="0.01"
                      required
                      placeholder="19.99" 
                      className="w-full bg-sys-black border border-sys-blue p-4 text-sys-accent placeholder-sys-navy focus:outline-none focus:border-sys-accent transition-colors font-mono text-sm rounded-sm"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-[11px] font-bold text-sys-muted mb-2 uppercase tracking-widest">
                    [04] META TAGS (CSV)
                  </label>
                  <input 
                    type="text" 
                    placeholder="SINGLEPLAYER, STORY_RICH, ATMOSPHERIC" 
                    className="w-full bg-sys-black border border-sys-blue p-4 text-sys-text placeholder-sys-navy focus:outline-none focus:border-sys-accent transition-colors uppercase font-mono text-sm rounded-sm"
                  />
                </div>

                <div>
                  <label className="block text-[11px] font-bold text-sys-muted mb-2 uppercase tracking-widest">
                    [05] ESTIMATED DEPLOYMENT
                  </label>
                  <input 
                    type="date" 
                    className="w-full bg-sys-black border border-sys-blue p-4 text-sys-text focus:outline-none focus:border-sys-accent transition-colors uppercase font-mono text-sm rounded-sm [color-scheme:dark]"
                  />
                </div>
              </div>

              <div className="pt-8 border-t border-sys-blue">
                <button 
                  type="submit"
                  disabled={isAnalyzing}
                  className={`w-full py-5 flex items-center justify-center transition-all ${
                    isAnalyzing 
                      ? 'bg-sys-black text-sys-muted border-2 border-sys-navy cursor-not-allowed' 
                      : 'cyno-button'
                  }`}
                >
                  {isAnalyzing ? (
                    <>
                      <div className="w-5 h-5 border-2 border-sys-muted border-t-sys-text animate-spin mr-4" />
                      <span className="tracking-widest font-bold text-sm">EXECUTING NLP PROTOCOLS...</span>
                    </>
                  ) : (
                    <>
                      <Cpu className="w-5 h-5 mr-3" />
                      <span className="tracking-widest font-bold text-sm">INITIALIZE UPLINK & ANALYZE</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Results Panel */}
        <div className="xl:col-span-1">
          {showResult ? (
            <div className="cyno-panel p-8 h-full flex flex-col animate-in fade-in slide-in-from-right-4 relative min-h-[500px]">
              <div className="absolute top-0 left-0 w-full h-1 bg-sys-accent" />
              <div className="flex items-start justify-between mb-8 border-b border-sys-blue pb-6">
                <div className="flex items-center">
                  <CheckSquare className="w-6 h-6 text-sys-accent mr-3" />
                  <div>
                    <h3 className="font-bold text-sys-text uppercase tracking-widest text-sm">ANALYSIS COMPLETE</h3>
                    <p className="text-[10px] text-sys-muted font-bold tracking-widest mt-1">CONFIDENCE: 89.4%</p>
                  </div>
                </div>
              </div>

              <div className="space-y-8 flex-1">
                <div>
                  <p className="text-[10px] text-sys-muted font-bold mb-2 uppercase tracking-widest">PREDICTED SUCCESS METRIC</p>
                  <div className="text-6xl font-bold text-sys-accent font-mono tracking-tighter">
                    76.4<span className="text-3xl">%</span>
                  </div>
                </div>

                <div className="space-y-4 pt-6 border-t border-sys-blue">
                  <div className="bg-sys-black border border-sys-blue p-4 rounded-sm">
                    <div className="flex justify-between items-center mb-3">
                      <span className="text-xs font-bold text-sys-text uppercase tracking-widest flex items-center">
                        <Binary className="w-4 h-4 mr-2 text-sys-muted" /> PRICE OPTIMIZATION
                      </span>
                      <span className="text-[10px] font-bold text-sys-accent border border-sys-accent px-2 py-0.5">NOMINAL</span>
                    </div>
                    <p className="text-xs text-sys-muted font-bold tracking-widest leading-relaxed uppercase font-mono">
                      TARGET PRICE IS 15% LOWER THAN SUCCESSFUL COMPARABLES IN ACTIVE DB.
                    </p>
                  </div>
                  
                  <div className="bg-sys-black border border-[#ef4444] p-4 rounded-sm">
                    <div className="flex justify-between items-center mb-3">
                      <span className="text-xs font-bold text-[#ef4444] uppercase tracking-widest flex items-center">
                        <AlertTriangle className="w-4 h-4 mr-2" /> GENRE SATURATION
                      </span>
                      <span className="text-[10px] font-bold text-sys-black bg-[#ef4444] px-2 py-0.5 animate-pulse">CRITICAL</span>
                    </div>
                    <p className="text-xs text-sys-muted font-bold tracking-widest leading-relaxed uppercase font-mono">
                      ACTION RPG SECTOR HIGHLY SATURATED. UNIQUE SELLING PROPOSITION REQUIRED.
                    </p>
                  </div>
                </div>
              </div>

              <button className="cyno-button w-full mt-8">
                DOWNLOAD FULL TELEMETRY
              </button>
            </div>
          ) : (
             <div className="cyno-panel p-8 h-full flex flex-col items-center justify-center text-center opacity-60 min-h-[500px]">
              <Database className="w-16 h-16 text-sys-blue mb-6" />
              <p className="text-xs text-sys-muted font-bold uppercase tracking-widest leading-loose">
                STANDBY MODE.<br/>AWAITING ENTITY PARAMETERS<br/>FOR NLP PROCESSING.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
