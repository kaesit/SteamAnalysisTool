import { KpiCards } from './KpiCards';
import { MarketCharts } from './MarketCharts';
import { RecentAnalysisTable } from './RecentAnalysisTable';

export function Overview() {
  return (
    <div className="animate-in fade-in duration-300">
      <div className="mb-10 flex justify-between items-end border-b-4 border-sys-navy pb-6">
        <div>
          <div className="flex items-center mb-2">
            <div className="w-6 h-6 bg-sys-accent mr-3 flex items-center justify-center">
              <div className="w-2 h-2 bg-sys-black" />
            </div>
            <div className="text-sys-muted text-[10px] tracking-[0.3em] font-bold uppercase">MODULE: DASH_OVERVIEW_V1.0</div>
          </div>
          <h1 className="text-4xl font-bold text-sys-text tracking-[0.15em] uppercase">SECTOR OVERVIEW</h1>
        </div>
        <div className="text-right bg-sys-navy p-4 border-2 border-sys-blue relative">
          <div className="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-sys-accent" />
          <div className="absolute bottom-0 right-0 w-2 h-2 border-b-2 border-r-2 border-sys-accent" />
          <div className="text-[10px] text-sys-muted font-bold tracking-[0.2em] uppercase mb-1">ENCRYPTION: CYNOSURE-AES</div>
          <div className="text-xs text-sys-accent tracking-widest font-bold uppercase flex items-center justify-end">
            <span className="w-2 h-2 bg-sys-accent mr-2 animate-pulse" />
            STATUS: SECURE
          </div>
        </div>
      </div>
      
      <KpiCards />
      <MarketCharts />
      <RecentAnalysisTable />
    </div>
  );
}
