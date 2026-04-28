import { useEffect, useState } from 'react';
import { Database, Server, Terminal as TerminalIcon, Wifi, RefreshCw } from 'lucide-react';

export function DataNodes() {
  const [logs, setLogs] = useState<string[]>([
    "[10:42:01] SYS_INIT // SECURE NODE PROTOCOL",
    "[10:42:02] AUTH_KEY_VALIDATED // STEAM_WEB_API",
    "[10:42:05] ESTABLISHING_UPLINK... OK",
  ]);

  useEffect(() => {
    const newLogs = [
      "FETCHING_BATCH: APP_ID_730 // OK",
      "PARSE_JSON: REVIEWS_NODE // 1420B PROCESSED",
      "STEAM_SPY_SYNC: ACTIVE // LATENCY 45MS",
      "WARNING: NLP_QUEUE_HIGH // BALANCING LOAD...",
      "FETCHING_BATCH: APP_ID_271590 // OK",
      "DB_INSERT: SUCCESS // 240 ROWS",
      "PING: STEAM_API // 12MS",
    ];
    let i = 0;
    const interval = setInterval(() => {
      setLogs(prev => [...prev, `[10:${42 + Math.floor(i/2)}:${(15 + i*12)%60}] ` + newLogs[i % newLogs.length]]);
      i++;
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="animate-in fade-in duration-300 max-w-[1400px] mx-auto">
      <div className="mb-10 flex justify-between items-end border-b-2 border-sys-blue pb-6">
        <div>
          <div className="flex items-center mb-2">
            <div className="w-6 h-6 bg-sys-text mr-3 flex items-center justify-center rounded-sm">
              <div className="w-2 h-2 bg-sys-black" />
            </div>
            <div className="text-sys-muted text-[10px] tracking-widest font-bold uppercase">MODULE: NODE_CONTROL_V4.2</div>
          </div>
          <h1 className="text-4xl font-bold text-sys-text tracking-widest uppercase">SECURE NODES</h1>
        </div>
        <div className="text-right bg-sys-navy p-4 border border-sys-blue relative">
          <div className="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-sys-text" />
          <div className="absolute bottom-0 right-0 w-2 h-2 border-b-2 border-r-2 border-sys-text" />
          <div className="text-[10px] text-sys-accent font-bold tracking-widest uppercase flex items-center">
            <Wifi className="w-3 h-3 mr-2 animate-pulse" />
            CONNECTION LIVE
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Node Status Cards */}
        <div className="space-y-6">
          <div className="cyno-panel p-8">
            <div className="flex justify-between items-start mb-6 border-b border-sys-blue pb-4">
               <div className="flex items-center">
                 <Server className="w-5 h-5 text-sys-accent mr-3" />
                 <div>
                   <h2 className="text-sm font-bold text-sys-text tracking-widest uppercase">STEAM_WEB_API</h2>
                   <div className="text-[10px] text-sys-muted font-bold tracking-widest uppercase mt-1">PRIMARY INGESTION NODE</div>
                 </div>
               </div>
               <div className="flex items-center text-[10px] font-bold text-[#4ade80] tracking-widest uppercase bg-[#4ade80]/10 border border-[#4ade80] px-3 py-1">
                 <div className="w-1.5 h-1.5 bg-[#4ade80] rounded-full mr-2 animate-pulse" />
                 ONLINE
               </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-sys-black border border-sys-blue p-4">
                <div className="text-[10px] text-sys-muted font-bold tracking-widest uppercase mb-1">LATENCY</div>
                <div className="text-xl font-mono text-sys-text font-bold">12ms</div>
              </div>
              <div className="bg-sys-black border border-sys-blue p-4">
                <div className="text-[10px] text-sys-muted font-bold tracking-widest uppercase mb-1">DATA PROCESSED (24H)</div>
                <div className="text-xl font-mono text-sys-text font-bold">4.2 GB</div>
              </div>
            </div>
            
            <button className="cyno-button w-full mt-6 py-3 text-[10px] flex items-center justify-center">
              <RefreshCw className="w-3 h-3 mr-2" /> FORCE MANUAL SYNC
            </button>
          </div>

          <div className="cyno-panel p-8 border-t-2 border-[#ef4444]">
            <div className="flex justify-between items-start mb-6 border-b border-sys-blue pb-4">
               <div className="flex items-center">
                 <Database className="w-5 h-5 text-[#ef4444] mr-3" />
                 <div>
                   <h2 className="text-sm font-bold text-sys-text tracking-widest uppercase">STEAM_SPY_API</h2>
                   <div className="text-[10px] text-sys-muted font-bold tracking-widest uppercase mt-1">SECONDARY METRICS NODE</div>
                 </div>
               </div>
               <div className="flex items-center text-[10px] font-bold text-[#f59e0b] tracking-widest uppercase bg-[#f59e0b]/10 border border-[#f59e0b] px-3 py-1">
                 <div className="w-1.5 h-1.5 bg-[#f59e0b] rounded-full mr-2 animate-pulse" />
                 DEGRADED
               </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-sys-black border border-[#ef4444]/50 p-4">
                <div className="text-[10px] text-sys-muted font-bold tracking-widest uppercase mb-1">LATENCY</div>
                <div className="text-xl font-mono text-[#ef4444] font-bold">485ms</div>
              </div>
              <div className="bg-sys-black border border-sys-blue p-4">
                <div className="text-[10px] text-sys-muted font-bold tracking-widest uppercase mb-1">RATE LIMIT</div>
                <div className="text-xl font-mono text-sys-text font-bold">45/60</div>
              </div>
            </div>
            
            <div className="mt-4 text-[10px] text-[#ef4444] font-mono tracking-widest uppercase">
              WARNING: ELEVATED RESPONSE TIMES DETECTED.
            </div>
          </div>
        </div>

        {/* Live Terminal Log */}
        <div className="cyno-panel p-6 flex flex-col h-[650px]">
          <div className="flex items-center mb-4 border-b border-sys-blue pb-4">
             <TerminalIcon className="w-4 h-4 text-sys-accent mr-3" />
             <h2 className="text-sm font-bold text-sys-text tracking-widest uppercase">LIVE INGESTION STREAM</h2>
          </div>
          
          <div className="flex-1 bg-[#010204] border border-sys-blue p-4 overflow-y-auto font-mono text-[11px] leading-loose">
            {logs.map((log, i) => (
              <div key={i} className={`${log.includes('WARNING') || log.includes('DEGRADED') ? 'text-[#ef4444]' : 'text-[#60a5fa]'} opacity-90`}>
                {log}
              </div>
            ))}
            <div className="text-sys-muted animate-pulse mt-2">_</div>
          </div>
        </div>
      </div>
    </div>
  );
}
