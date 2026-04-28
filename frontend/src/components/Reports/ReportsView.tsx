import { FileText, Download, ChevronRight, Lock } from 'lucide-react';

const mockReports = [
  { id: 'REP-77A', name: 'CYBERPUNK CHRONICLES OVERVIEW', date: '2023.10.15', sentiment: 'OPTIMAL', conf: '94.2%', size: '2.4MB' },
  { id: 'REP-77B', name: 'FARM SIMULATOR NLP BATCH', date: '2023.10.18', sentiment: 'NOMINAL', conf: '88.1%', size: '1.1MB' },
  { id: 'REP-77C', name: 'SPACE EXPLORER RISK ASSESS', date: '2023.10.22', sentiment: 'CRITICAL', conf: '98.9%', size: '4.7MB' },
  { id: 'REP-78A', name: 'MEDIEVAL DYNASTY PROJECTION', date: '2023.11.02', sentiment: 'OPTIMAL', conf: '91.5%', size: '3.3MB' },
  { id: 'REP-78B', name: 'PROJECT VELOCITY PRICING', date: '2023.11.05', sentiment: 'NOMINAL', conf: '84.0%', size: '1.8MB' },
  { id: 'REP-78C', name: 'Q3 MARKET SATURATION SCAN', date: '2023.11.10', sentiment: 'CRITICAL', conf: '96.4%', size: '8.9MB' },
];

export function ReportsView() {
  return (
    <div className="animate-in fade-in duration-300 max-w-[1400px] mx-auto">
      <div className="mb-10 flex justify-between items-end border-b-2 border-sys-blue pb-6">
        <div>
          <div className="flex items-center mb-2">
            <div className="w-6 h-6 bg-sys-text mr-3 flex items-center justify-center rounded-sm">
              <div className="w-2 h-2 bg-sys-black" />
            </div>
            <div className="text-sys-muted text-[10px] tracking-widest font-bold uppercase">MODULE: SECURE_LOGS_V3.0</div>
          </div>
          <h1 className="text-4xl font-bold text-sys-text tracking-widest uppercase">DATATERMINALS</h1>
        </div>
        <div className="text-right bg-sys-navy p-4 border border-sys-blue relative">
          <div className="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-sys-text" />
          <div className="absolute bottom-0 right-0 w-2 h-2 border-b-2 border-r-2 border-sys-text" />
          <div className="text-[10px] text-sys-muted font-bold tracking-widest uppercase">ACCESS: CLASSIFIED</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Main Reports List */}
        <div className="lg:col-span-2">
          <div className="cyno-panel p-8 md:p-10 min-h-[600px]">
            <div className="flex justify-between items-center mb-8 border-b border-sys-blue pb-4">
               <div className="flex items-center">
                 <FileText className="w-5 h-5 text-sys-accent mr-3" />
                 <h2 className="text-sm font-bold text-sys-text tracking-widest uppercase">ENCRYPTED NLP ARCHIVES</h2>
               </div>
               <div className="text-[10px] bg-sys-black border border-sys-blue px-3 py-1 text-sys-muted tracking-widest uppercase">INDEX: 6 LOGS</div>
            </div>
            
            <div className="space-y-4">
              {mockReports.map((report) => (
                <div key={report.id} className="bg-sys-black border border-sys-blue p-4 flex justify-between items-center group hover:border-sys-accent transition-colors rounded-sm cursor-pointer relative overflow-hidden">
                  <div className="absolute left-0 top-0 w-1 h-full bg-sys-blue group-hover:bg-sys-accent transition-colors" />
                  
                  <div className="flex items-center space-x-6 ml-2">
                    <div className="text-xs font-mono font-bold text-sys-muted tracking-widest">{report.id}</div>
                    <div>
                      <div className="text-sm font-bold text-sys-text uppercase tracking-widest group-hover:text-sys-accent transition-colors">{report.name}</div>
                      <div className="text-[10px] text-sys-muted font-mono tracking-widest mt-1 flex items-center">
                        <Lock className="w-3 h-3 mr-2 text-sys-blue-light" />
                        SECURE_KEY_REQ // {report.date}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-6">
                    <div className="text-right hidden md:block">
                      <div className={`text-[10px] font-bold tracking-widest uppercase ${
                        report.sentiment === 'OPTIMAL' ? 'text-sys-accent' :
                        report.sentiment === 'CRITICAL' ? 'text-[#ef4444]' : 'text-sys-text'
                      }`}>{report.sentiment}</div>
                      <div className="text-[10px] text-sys-muted font-mono tracking-widest mt-1">CONF: {report.conf}</div>
                    </div>
                    
                    <button className="cyno-button py-2 px-4 !text-[10px]">
                      <Download className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Selected Report Preview */}
        <div className="lg:col-span-1">
          <div className="cyno-panel p-8 h-full flex flex-col min-h-[600px] border-t-2 border-t-sys-accent">
            <div className="flex items-center mb-6 border-b border-sys-blue pb-4">
              <ChevronRight className="w-5 h-5 text-sys-accent mr-2" />
              <h2 className="text-sm font-bold text-sys-text tracking-widest uppercase">FILE INSPECTOR</h2>
            </div>
            
            <div className="flex-1 flex flex-col justify-center items-center text-center opacity-50">
              <FileText className="w-16 h-16 text-sys-blue mb-6" />
              <p className="text-xs text-sys-muted font-bold uppercase tracking-widest leading-loose">
                SELECT A REPORT<br/>FROM THE ARCHIVE<br/>TO DECRYPT CONTENTS.
              </p>
            </div>
            
            <div className="mt-auto pt-6 border-t border-sys-blue text-[10px] text-sys-muted font-mono tracking-widest uppercase text-center">
              AWAITING DECRYPTION KEY...
            </div>
          </div>
        </div>
        
      </div>
    </div>
  );
}
