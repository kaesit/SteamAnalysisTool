import { useState } from 'react';
import { Terminal, Cpu, Database, Binary, AlertTriangle, CheckSquare, Server } from 'lucide-react';

export function SteamAnalysisForm() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [title, setTitle] = useState('');
  const [maxReviews, setMaxReviews] = useState(500);
  const [resultData, setResultData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsAnalyzing(true);
    setShowResult(false);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/games/collect-steam-only', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title,
          max_reviews: maxReviews,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || data.error || 'Failed to analyze game');
      }

      setResultData(data);
      setShowResult(true);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="animate-in fade-in duration-300 max-w-[1400px] mx-auto">
      <div className="mb-10 flex justify-between items-end border-b-2 border-sys-blue pb-6">
        <div>
          <div className="flex items-center mb-2">
            <div className="w-6 h-6 bg-sys-text mr-3 flex items-center justify-center rounded-sm">
              <Server className="w-4 h-4 text-sys-black" />
            </div>
            <div className="text-sys-muted text-[10px] tracking-widest font-bold uppercase">MODULE: STEAM_DIRECT_V1.0</div>
          </div>
          <h1 className="text-4xl font-bold text-sys-text tracking-widest uppercase">STEAM API ANALYSIS</h1>
          <p className="text-sys-muted text-sm mt-2 font-mono uppercase tracking-widest">
            DIRECT CONNECTION TO STEAM WEB API. BYPASSING THIRD-PARTY TELEMETRY.
          </p>
        </div>
        <div className="text-right bg-sys-navy p-4 border border-sys-blue relative">
          <div className="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-sys-text" />
          <div className="absolute bottom-0 right-0 w-2 h-2 border-b-2 border-r-2 border-sys-text" />
          <div className="text-[10px] text-sys-muted font-bold tracking-widest uppercase">
            {isAnalyzing ? 'FETCHING DATA...' : 'AWAITING INPUT...'}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Form Section */}
        <div className="xl:col-span-2">
          <div className="cyno-panel p-8 md:p-10">
            <div className="flex items-center mb-8 border-b border-sys-blue pb-4">
               <Terminal className="w-5 h-5 text-sys-accent mr-3" />
               <h2 className="text-sm font-bold text-sys-text tracking-widest uppercase">CONFIGURE STEAM PARAMETERS</h2>
            </div>
            
            {error && (
              <div className="mb-6 bg-sys-black border border-[#ef4444] p-4 rounded-sm flex items-start">
                <AlertTriangle className="w-5 h-5 text-[#ef4444] mr-3 mt-0.5 flex-shrink-0" />
                <div>
                  <h4 className="text-xs font-bold text-[#ef4444] tracking-widest uppercase mb-1">SYSTEM ERROR</h4>
                  <p className="text-xs font-mono text-sys-muted uppercase">{error}</p>
                </div>
              </div>
            )}

            <form onSubmit={handleAnalyze} className="space-y-6">
              <div className="space-y-6">
                <div>
                  <label className="block text-[11px] font-bold text-sys-muted mb-2 uppercase tracking-widest">
                    [01] STEAM STORE TITLE
                  </label>
                  <input 
                    type="text" 
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="e.g. Portal 2" 
                    className="w-full bg-sys-black border border-sys-blue p-4 text-sys-text placeholder-sys-navy focus:outline-none focus:border-sys-accent transition-colors uppercase font-mono text-sm rounded-sm"
                  />
                  <p className="text-[10px] text-sys-muted mt-2 font-mono uppercase">
                    EXACT OR PARTIAL TITLE MATCH ON STEAM STORE.
                  </p>
                </div>

                <div>
                  <label className="block text-[11px] font-bold text-sys-muted mb-2 uppercase tracking-widest">
                    [02] MAX REVIEWS TO FETCH
                  </label>
                  <input 
                    type="number" 
                    min="10"
                    max="5000"
                    required
                    value={maxReviews}
                    onChange={(e) => setMaxReviews(parseInt(e.target.value) || 500)}
                    className="w-full bg-sys-black border border-sys-blue p-4 text-sys-accent placeholder-sys-navy focus:outline-none focus:border-sys-accent transition-colors font-mono text-sm rounded-sm"
                  />
                  <p className="text-[10px] text-sys-muted mt-2 font-mono uppercase">
                    LIMIT: 10 TO 5000 REVIEWS. HIGHER VALUES INCREASE PROCESSING TIME.
                  </p>
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
                      <span className="tracking-widest font-bold text-sm">FETCHING FROM STEAM...</span>
                    </>
                  ) : (
                    <>
                      <Server className="w-5 h-5 mr-3" />
                      <span className="tracking-widest font-bold text-sm">EXECUTE STEAM FETCH</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Results Panel */}
        <div className="xl:col-span-1">
          {showResult && resultData ? (
            <div className="cyno-panel p-8 h-full flex flex-col animate-in fade-in slide-in-from-right-4 relative min-h-[500px]">
              <div className="absolute top-0 left-0 w-full h-1 bg-sys-accent" />
              <div className="flex items-start justify-between mb-8 border-b border-sys-blue pb-6">
                <div className="flex items-center">
                  <CheckSquare className="w-6 h-6 text-sys-accent mr-3" />
                  <div>
                    <h3 className="font-bold text-sys-text uppercase tracking-widest text-sm">FETCH COMPLETE</h3>
                    <p className="text-[10px] text-sys-muted font-bold tracking-widest mt-1">STATUS: NOMINAL</p>
                  </div>
                </div>
              </div>

              <div className="space-y-8 flex-1">
                <div>
                  <p className="text-[10px] text-sys-muted font-bold mb-2 uppercase tracking-widest">POSITIVE RATIO</p>
                  <div className="text-6xl font-bold text-sys-accent font-mono tracking-tighter">
                    {(resultData.positive_ratio * 100).toFixed(1)}<span className="text-3xl">%</span>
                  </div>
                </div>

                <div className="space-y-4 pt-6 border-t border-sys-blue">
                  <div className="bg-sys-black border border-sys-blue p-4 rounded-sm">
                    <div className="flex justify-between items-center mb-3">
                      <span className="text-xs font-bold text-sys-text uppercase tracking-widest flex items-center">
                        <Binary className="w-4 h-4 mr-2 text-sys-muted" /> REVIEWS COLLECTED
                      </span>
                      <span className="text-[10px] font-bold text-sys-accent border border-sys-accent px-2 py-0.5">
                        {resultData.total_reviews_collected}
                      </span>
                    </div>
                    <p className="text-[10px] text-sys-muted font-bold tracking-widest leading-relaxed uppercase font-mono mt-2">
                      NLP TRAINING DATA EXTRACTED: {resultData.reviews_info.row_count} ROWS.
                    </p>
                  </div>
                  
                  <div className="bg-sys-black border border-sys-blue p-4 rounded-sm">
                    <div className="flex justify-between items-center mb-3">
                      <span className="text-xs font-bold text-sys-text uppercase tracking-widest flex items-center">
                        <Database className="w-4 h-4 mr-2 text-sys-muted" /> MARKET SUMMARY
                      </span>
                    </div>
                    <p className="text-[10px] text-sys-muted font-bold tracking-widest leading-relaxed uppercase font-mono">
                      SUMMARY METRICS GENERATED: {resultData.summary_info.column_count} DATA POINTS.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ) : (
             <div className="cyno-panel p-8 h-full flex flex-col items-center justify-center text-center opacity-60 min-h-[500px]">
              <Server className="w-16 h-16 text-sys-blue mb-6" />
              <p className="text-xs text-sys-muted font-bold uppercase tracking-widest leading-loose">
                STANDBY MODE.<br/>AWAITING STEAM PARAMETERS<br/>FOR DIRECT FETCH.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
