import { KpiCards } from './KpiCards';
import { MarketCharts } from './MarketCharts';
import { RecentAnalysisTable } from './RecentAnalysisTable';

export function Overview() {
  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-100 tracking-tight">Dashboard Overview</h1>
        <p className="text-gray-400 mt-1">Turkish Game Developers Market Analysis Platform</p>
      </div>
      
      <KpiCards />
      <MarketCharts />
      <RecentAnalysisTable />
    </div>
  );
}
