import { useState, useRef } from 'react';
import { Terminal, Cpu, Database, Binary, AlertTriangle, CheckSquare, Server, Calendar, Hash } from 'lucide-react';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export function AnalysisForm() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);

  // Form State
  const [title, setTitle] = useState('');
  const [classification, setClassification] = useState('action');
  const [price, setPrice] = useState<number>(19.99);
  const [tags, setTags] = useState('');
  const [deploymentDate, setDeploymentDate] = useState('');

  // Result State
  const [predictionData, setPredictionData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const resultsRef = useRef<HTMLDivElement>(null);
  const printRef = useRef<HTMLDivElement>(null);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsAnalyzing(true);
    setShowResult(false);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/analysis/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: title,
          classification: classification,
          price_usd: price,
          meta_tags: tags,
          deployment_date: deploymentDate || undefined
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || data.error || 'Failed to analyze game');
      }

      setPredictionData(data);
      setShowResult(true);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleDownloadPdf = async () => {
    if (!printRef.current || !predictionData) return;

    setIsGeneratingPdf(true);

    try {
      // Temporarily make the print container visible for html2canvas
      const printElement = printRef.current;
      printElement.style.position = 'absolute';
      printElement.style.left = '0';
      printElement.style.top = '0';
      printElement.style.zIndex = '-1';
      printElement.style.display = 'block';

      const canvas = await html2canvas(printElement, {
        scale: 2,
        backgroundColor: '#0a0a0a', // sys-black equivalent
        windowWidth: 800,
      });

      // Hide it again
      printElement.style.display = 'none';

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');

      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`${title || 'project'}_telemetry.pdf`);
    } catch (err) {
      console.error('Failed to generate PDF', err);
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  return (
    <div className="animate-in fade-in duration-300 max-w-[1400px] mx-auto relative">

      {/* HIDDEN PRINT LAYOUT - Futuristic Bill format */}
      {showResult && predictionData && (
        <div
          ref={printRef}
          style={{ display: 'none' }}
          className="w-[800px] bg-sys-black text-sys-text p-12 font-mono border-2 border-sys-blue"
        >
          {/* Header */}
          <div className="border-b-2 border-sys-blue pb-6 mb-8">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h1 className="text-3xl font-bold tracking-widest text-sys-text mb-1 uppercase">UPLINK TELEMETRY</h1>
                <h2 className="text-sm font-bold tracking-widest text-sys-accent uppercase">OFFICIAL ANALYSIS RECEIPT</h2>
              </div>
              <div className="text-right">
                <div className="text-[10px] text-sys-muted font-bold tracking-widest uppercase mb-1">TX_ID: {Math.random().toString(36).substring(2, 10).toUpperCase()}</div>
                <div className="text-[10px] text-sys-muted font-bold tracking-widest uppercase">DATE: {new Date().toISOString().split('T')[0]}</div>
              </div>
            </div>

            {/* Fake Barcode */}
            <div className="text-4xl text-sys-muted font-black tracking-tighter opacity-50 select-none">
              ||||| ||| || |||||| | ||| || ||||
            </div>
          </div>

          {/* Metadata */}
          <div className="bg-sys-navy border border-sys-blue p-6 mb-8 rounded-sm">
            <h3 className="text-xs font-bold text-sys-accent mb-4 tracking-widest uppercase border-b border-sys-blue pb-2">ENTITY METADATA</h3>
            <div className="grid grid-cols-2 gap-y-4">
              <div>
                <span className="text-[10px] text-sys-muted uppercase tracking-widest block mb-1">IDENTIFIER</span>
                <span className="text-sm font-bold uppercase">{title || "UNKNOWN"}</span>
              </div>
              <div>
                <span className="text-[10px] text-sys-muted uppercase tracking-widest block mb-1">PRIMARY CLASS</span>
                <span className="text-sm font-bold uppercase">{classification}</span>
              </div>
              <div>
                <span className="text-[10px] text-sys-muted uppercase tracking-widest block mb-1">FINANCIAL TARGET</span>
                <span className="text-sm font-bold uppercase">${price.toFixed(2)}</span>
              </div>
              <div>
                <span className="text-[10px] text-sys-muted uppercase tracking-widest block mb-1">META TAGS</span>
                <span className="text-sm font-bold uppercase truncate pr-4">{tags || "N/A"}</span>
              </div>
            </div>
          </div>

          {/* Itemized Analysis */}
          <div className="mb-10">
            <h3 className="text-xs font-bold text-sys-accent mb-4 tracking-widest uppercase border-b border-sys-blue pb-2">ITEMIZED ANALYSIS LOG</h3>
            <div className="space-y-6">

              <div className="flex flex-col border-b border-dashed border-sys-navy pb-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-bold uppercase tracking-widest text-sys-text">01. BRAND IDENTITY EVALUATION</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 uppercase ${predictionData.title_status === 'WARNING' ? 'text-[#A3903B] border border-[#A3903B]' : 'text-sys-accent border border-sys-accent'}`}>
                    {predictionData.title_status}
                  </span>
                </div>
                <span className="text-xs text-sys-muted uppercase leading-relaxed">{predictionData.title_insight}</span>
              </div>

              <div className="flex flex-col border-b border-dashed border-sys-navy pb-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-bold uppercase tracking-widest text-sys-text">02. DEPLOYMENT WINDOW ANALYSIS</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 uppercase ${predictionData.date_status === 'WARNING' ? 'text-[#A3903B] border border-[#A3903B]' : 'text-sys-accent border border-sys-accent'}`}>
                    {predictionData.date_status}
                  </span>
                </div>
                <span className="text-xs text-sys-muted uppercase leading-relaxed">{predictionData.date_insight}</span>
              </div>

              <div className="flex flex-col border-b border-dashed border-sys-navy pb-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-bold uppercase tracking-widest text-sys-text">03. PRICE OPTIMIZATION CHECK</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 uppercase ${predictionData.price_status === 'WARNING' ? 'text-[#A3903B] border border-[#A3903B]' : 'text-sys-accent border border-sys-accent'}`}>
                    {predictionData.price_status}
                  </span>
                </div>
                <span className="text-xs text-sys-muted uppercase leading-relaxed">{predictionData.price_insight}</span>
              </div>

              <div className="flex flex-col border-b border-dashed border-sys-navy pb-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-bold uppercase tracking-widest text-sys-text">04. GENRE SATURATION REPORT</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 uppercase ${predictionData.genre_status === 'CRITICAL' ? 'text-[#ef4444] border border-[#ef4444]' : 'text-sys-accent border border-sys-accent'}`}>
                    {predictionData.genre_status}
                  </span>
                </div>
                <span className="text-xs text-sys-muted uppercase leading-relaxed">{predictionData.genre_insight}</span>
              </div>

            </div>
          </div>

          {/* Footer / Total */}
          <div className="mt-auto pt-6 border-t-2 border-sys-blue">
            <div className="flex justify-between items-end">
              <div>
                <p className="text-[10px] text-sys-muted font-bold tracking-widest uppercase mb-1">ANALYSIS STATUS: VERIFIED</p>
                <p className="text-[10px] text-sys-muted font-bold tracking-widest uppercase">SYSTEM: GAME_ORACLE_V2.1</p>
              </div>
              <div className="text-right bg-sys-navy p-6 border border-sys-accent rounded-sm">
                <p className="text-[10px] text-sys-accent font-bold uppercase tracking-widest mb-1">TOTAL SUCCESS PROBABILITY</p>
                <div className="text-5xl font-bold text-sys-accent tracking-tighter">
                  {predictionData.success_probability.toFixed(1)}<span className="text-2xl">%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main UI */}
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
          <div className="text-[10px] text-sys-muted font-bold tracking-widest uppercase">
            {isAnalyzing ? 'PROCESSING TELEMETRY...' : 'AWAITING INPUT...'}
          </div>
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
                    [01] ENTITY IDENTIFIER
                  </label>
                  <input
                    type="text"
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
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
                      <select
                        value={classification}
                        onChange={(e) => setClassification(e.target.value)}
                        className="w-full bg-sys-black border border-sys-blue p-4 text-sys-text focus:outline-none focus:border-sys-accent transition-colors uppercase font-mono text-sm appearance-none rounded-sm"
                      >
                        <option value="action">ACTION</option>
                        <option value="rpg">RPG</option>
                        <option value="strategy">STRATEGY</option>
                        <option value="simulation">SIMULATION</option>
                        <option value="adventure">ADVENTURE</option>
                        <option value="indie">INDIE</option>
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
                      value={price}
                      onChange={(e) => setPrice(parseFloat(e.target.value) || 0)}
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
                    required
                    value={tags}
                    onChange={(e) => setTags(e.target.value)}
                    placeholder="SINGLEPLAYER, STORY_RICH, ATMOSPHERIC"
                    className="w-full bg-sys-black border border-sys-blue p-4 text-sys-text placeholder-sys-navy focus:outline-none focus:border-sys-accent transition-colors uppercase font-mono text-sm rounded-sm"
                  />
                  <p className="text-[10px] text-sys-muted mt-2 font-mono uppercase">
                    FIRST TAG IS PRIORITIZED FOR MARKET MATCHING. SECONDARY TAGS INFLUENCE HEURISTICS.
                  </p>
                </div>

                <div>
                  <label className="block text-[11px] font-bold text-sys-muted mb-2 uppercase tracking-widest">
                    [05] ESTIMATED DEPLOYMENT
                  </label>
                  <input
                    type="date"
                    value={deploymentDate}
                    onChange={(e) => setDeploymentDate(e.target.value)}
                    className="w-full bg-sys-black border border-sys-blue p-4 text-sys-text focus:outline-none focus:border-sys-accent transition-colors uppercase font-mono text-sm rounded-sm [color-scheme:dark]"
                  />
                </div>
              </div>

              <div className="pt-8 border-t border-sys-blue">
                <button
                  type="submit"
                  disabled={isAnalyzing}
                  className={`w-full py-5 flex items-center justify-center transition-all ${isAnalyzing
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
          {showResult && predictionData ? (
            <div className="flex flex-col h-full">
              <div
                ref={resultsRef}
                className="cyno-panel p-8 flex-1 flex flex-col animate-in fade-in slide-in-from-right-4 relative"
              >
                <div className="absolute top-0 left-0 w-full h-1 bg-sys-accent" />
                <div className="flex items-start justify-between mb-8 border-b border-sys-blue pb-6">
                  <div className="flex items-center">
                    <CheckSquare className="w-6 h-6 text-sys-accent mr-3" />
                    <div>
                      <h3 className="font-bold text-sys-text uppercase tracking-widest text-sm">ANALYSIS COMPLETE</h3>
                      <p className="text-[10px] text-sys-muted font-bold tracking-widest mt-1">ENTITY: {title || "UNKNOWN"}</p>
                    </div>
                  </div>
                </div>

                <div className="space-y-8 flex-1">
                  <div>
                    <p className="text-[10px] text-sys-muted font-bold mb-2 uppercase tracking-widest">PREDICTED SUCCESS METRIC</p>
                    <div className="text-6xl font-bold text-sys-accent font-mono tracking-tighter">
                      {predictionData.success_probability.toFixed(1)}<span className="text-3xl">%</span>
                    </div>
                  </div>

                  <div className="space-y-4 pt-6 border-t border-sys-blue">
                    <div className={`bg-sys-black border p-4 rounded-sm ${predictionData.title_status === 'WARNING' ? 'border-[#A3903B]' : 'border-sys-blue'}`}>
                      <div className="flex justify-between items-center mb-3">
                        <span className={`text-xs font-bold uppercase tracking-widest flex items-center ${predictionData.title_status === 'WARNING' ? 'text-[#A3903B]' : 'text-sys-text'}`}>
                          {predictionData.title_status === 'WARNING' ? <AlertTriangle className="w-4 h-4 mr-2" /> : <Hash className="w-4 h-4 mr-2 text-sys-muted" />} BRAND IDENTITY
                        </span>
                        <span className={`text-[10px] font-bold px-2 py-0.5 ${predictionData.title_status === 'WARNING' ? 'text-sys-black bg-[#A3903B] animate-pulse' : 'text-sys-accent border border-sys-accent'}`}>
                          {predictionData.title_status}
                        </span>
                      </div>
                      <p className="text-xs text-sys-muted font-bold tracking-widest leading-relaxed uppercase font-mono">
                        {predictionData.title_insight}
                      </p>
                    </div>

                    <div className={`bg-sys-black border p-4 rounded-sm ${predictionData.date_status === 'WARNING' ? 'border-[#A3903B]' : 'border-sys-blue'}`}>
                      <div className="flex justify-between items-center mb-3">
                        <span className={`text-xs font-bold uppercase tracking-widest flex items-center ${predictionData.date_status === 'WARNING' ? 'text-[#A3903B]' : 'text-sys-text'}`}>
                          {predictionData.date_status === 'WARNING' ? <AlertTriangle className="w-4 h-4 mr-2" /> : <Calendar className="w-4 h-4 mr-2 text-sys-muted" />} DEPLOYMENT WINDOW
                        </span>
                        <span className={`text-[10px] font-bold px-2 py-0.5 ${predictionData.date_status === 'WARNING' ? 'text-sys-black bg-[#A3903B] animate-pulse' : 'text-sys-accent border border-sys-accent'}`}>
                          {predictionData.date_status}
                        </span>
                      </div>
                      <p className="text-xs text-sys-muted font-bold tracking-widest leading-relaxed uppercase font-mono">
                        {predictionData.date_insight}
                      </p>
                    </div>

                    <div className={`bg-sys-black border p-4 rounded-sm ${predictionData.price_status === 'WARNING' ? 'border-[#A3903B]' : 'border-sys-blue'}`}>
                      <div className="flex justify-between items-center mb-3">
                        <span className={`text-xs font-bold uppercase tracking-widest flex items-center ${predictionData.price_status === 'WARNING' ? 'text-[#A3903B]' : 'text-sys-text'}`}>
                          {predictionData.price_status === 'WARNING' ? <AlertTriangle className="w-4 h-4 mr-2" /> : <Binary className="w-4 h-4 mr-2 text-sys-muted" />} PRICE OPTIMIZATION
                        </span>
                        <span className={`text-[10px] font-bold px-2 py-0.5 ${predictionData.price_status === 'WARNING' ? 'text-sys-black bg-[#A3903B] animate-pulse' : 'text-sys-accent border border-sys-accent'}`}>
                          {predictionData.price_status}
                        </span>
                      </div>
                      <p className="text-xs text-sys-muted font-bold tracking-widest leading-relaxed uppercase font-mono">
                        {predictionData.price_insight}
                      </p>
                    </div>

                    <div className={`bg-sys-black border p-4 rounded-sm ${predictionData.genre_status === 'CRITICAL' ? 'border-[#ef4444]' : 'border-sys-blue'}`}>
                      <div className="flex justify-between items-center mb-3">
                        <span className={`text-xs font-bold uppercase tracking-widest flex items-center ${predictionData.genre_status === 'CRITICAL' ? 'text-[#ef4444]' : 'text-sys-text'}`}>
                          {predictionData.genre_status === 'CRITICAL' ? <AlertTriangle className="w-4 h-4 mr-2" /> : <Database className="w-4 h-4 mr-2 text-sys-muted" />} GENRE SATURATION
                        </span>
                        <span className={`text-[10px] font-bold px-2 py-0.5 ${predictionData.genre_status === 'CRITICAL' ? 'text-sys-black bg-[#ef4444] animate-pulse' : 'text-sys-accent border border-sys-accent'}`}>
                          {predictionData.genre_status}
                        </span>
                      </div>
                      <p className="text-xs text-sys-muted font-bold tracking-widest leading-relaxed uppercase font-mono">
                        {predictionData.genre_insight}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <button
                onClick={handleDownloadPdf}
                disabled={isGeneratingPdf}
                className={`w-full mt-4 py-4 flex items-center justify-center transition-all ${isGeneratingPdf ? 'bg-sys-black text-sys-muted border border-sys-navy cursor-not-allowed' : 'cyno-button'}`}
              >
                {isGeneratingPdf ? 'GENERATING PDF...' : 'DOWNLOAD FULL TELEMETRY'}
              </button>
            </div>
          ) : (
            <div className="cyno-panel p-8 h-full flex flex-col items-center justify-center text-center opacity-60 min-h-[500px]">
              <Database className="w-16 h-16 text-sys-blue mb-6" />
              <p className="text-xs text-sys-muted font-bold uppercase tracking-widest leading-loose">
                STANDBY MODE.<br />AWAITING ENTITY PARAMETERS<br />FOR NLP PROCESSING.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

