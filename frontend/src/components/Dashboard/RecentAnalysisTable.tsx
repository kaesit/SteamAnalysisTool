import { Terminal, Download, FileJson } from 'lucide-react';

const recentAnalyses = [
  { id: 'TRX-01', name: 'CYBERPUNK CHRONICLES', genre: 'ACTION RPG', success: 82, sentiment: 'OPTIMAL', date: 'T-2H', status: 'COMPLETE' },
  { id: 'TRX-02', name: 'FARM SIMULATOR 2024', genre: 'SIMULATION', success: 65, sentiment: 'NOMINAL', date: 'T-5H', status: 'COMPLETE' },
  { id: 'TRX-03', name: 'SPACE EXPLORER VR', genre: 'ACTION VR', success: 41, sentiment: 'CRITICAL', date: 'T-24H', status: 'COMPLETE' },
  { id: 'TRX-04', name: 'MEDIEVAL DYNASTY', genre: 'STRATEGY', success: 91, sentiment: 'OPTIMAL', date: 'T-48H', status: 'COMPLETE' },
  { id: 'TRX-05', name: 'PROJECT VELOCITY', genre: 'RACING', success: 0, sentiment: 'CALCULATING', date: 'NOW', status: 'PROCESSING' },
];

export function RecentAnalysisTable() {
  return (
    <div className="cyno-panel p-8">
      <div className="flex justify-between items-center mb-6 border-b border-sys-blue pb-4">
        <div>
          <h3 className="text-lg font-bold text-sys-text uppercase tracking-widest flex items-center">
            RECENT DATA UPLINKS
          </h3>
          <p className="text-[10px] text-sys-muted font-bold tracking-widest mt-1 uppercase">LOGGED TRANSACTIONS IN SECURE SECTOR</p>
        </div>
        <button className="cyno-button py-2 px-6">
          VIEW ALL LOGS
        </button>
      </div>

      <div className="overflow-x-auto pb-2">
        <table className="w-full text-left border-collapse min-w-[800px]">
          <thead>
            <tr className="border-b-2 border-sys-blue text-sys-muted text-[10px] font-bold uppercase tracking-widest bg-sys-black">
              <th className="py-4 px-4 whitespace-nowrap">ID</th>
              <th className="py-4 px-4 whitespace-nowrap">ENTITY_NAME</th>
              <th className="py-4 px-4 whitespace-nowrap">CLASS</th>
              <th className="py-4 px-4 whitespace-nowrap">PROBABILITY</th>
              <th className="py-4 px-4 whitespace-nowrap">STATUS</th>
              <th className="py-4 px-4 whitespace-nowrap">TIMESTAMP</th>
              <th className="py-4 px-4 text-right whitespace-nowrap">EXEC</th>
            </tr>
          </thead>
          <tbody className="text-[12px] font-mono tracking-wider font-bold">
            {recentAnalyses.map((item) => (
              <tr key={item.id} className="border-b border-sys-navy hover:bg-sys-blue/20 transition-colors group">
                <td className="py-4 px-4 text-sys-muted">{item.id}</td>
                <td className="py-4 px-4">
                  <div className="flex items-center space-x-3">
                    <Terminal className="w-4 h-4 text-sys-accent shrink-0" />
                    <span className="text-sys-text group-hover:text-sys-accent transition-colors whitespace-nowrap">{item.name}</span>
                  </div>
                </td>
                <td className="py-4 px-4 text-sys-muted whitespace-nowrap">{item.genre}</td>
                <td className="py-4 px-4 w-[200px]">
                  {item.status === 'PROCESSING' ? (
                    <div className="flex items-center space-x-3 text-xs">
                      <div className="w-full bg-sys-black border border-sys-blue h-3 max-w-[120px] overflow-hidden rounded-[2px]">
                        <div className="h-full bg-sys-text w-full animate-pulse" />
                      </div>
                      <span className="text-sys-text animate-pulse">CALC...</span>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-3 text-xs">
                      <div className="w-full bg-sys-black border border-sys-blue h-3 max-w-[120px] rounded-[2px]">
                        <div 
                          className={`h-full ${
                            item.success >= 80 ? 'bg-sys-accent' : item.success >= 60 ? 'bg-sys-muted' : 'bg-[#ef4444]'
                          }`}
                          style={{ width: `${item.success}%` }}
                        />
                      </div>
                      <span className={`${item.success >= 80 ? 'text-sys-accent' : item.success >= 60 ? 'text-sys-text' : 'text-[#ef4444]'}`}>{item.success}%</span>
                    </div>
                  )}
                </td>
                <td className="py-4 px-4">
                  <span className={`px-3 py-1 text-[10px] font-bold tracking-widest border rounded-[2px] ${
                    item.sentiment === 'OPTIMAL' ? 'text-sys-accent border-sys-accent bg-sys-accent/10' :
                    item.sentiment === 'CRITICAL' ? 'text-[#ef4444] border-[#ef4444] bg-[#ef4444]/10' :
                    item.sentiment === 'NOMINAL' ? 'text-sys-text border-sys-text bg-sys-text/10' :
                    'text-sys-muted border-sys-muted bg-sys-muted/10'
                  }`}>
                    {item.sentiment}
                  </span>
                </td>
                <td className="py-4 px-4 text-sys-muted whitespace-nowrap">{item.date}</td>
                <td className="py-4 px-4">
                  <div className="flex items-center justify-end space-x-2">
                    <button className="p-2 text-sys-muted hover:text-sys-accent hover:bg-sys-navy border border-transparent hover:border-sys-accent transition-colors rounded-[2px]" title="DOWNLOAD_LOG">
                      <Download className="w-4 h-4" />
                    </button>
                    <button className="p-2 text-sys-muted hover:text-sys-text hover:bg-sys-navy border border-transparent hover:border-sys-text transition-colors rounded-[2px]" title="VIEW_JSON">
                      <FileJson className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
