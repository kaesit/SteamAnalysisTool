import { Crosshair, ActivitySquare, Cpu, AlertTriangle } from 'lucide-react';

export function KpiCards() {
  const kpis = [
    {
      id: "ALPHA",
      title: "TOTAL DATA PROCESSED",
      value: "14,205",
      change: "+12.4%",
      trend: "up",
      icon: Cpu,
      color: "text-sys-accent",
    },
    {
      id: "BRAVO",
      title: "PREDICTIVE SUCCESS",
      value: "68.4%",
      change: "+2.4%",
      trend: "up",
      icon: Crosshair,
      color: "text-sys-text",
    },
    {
      id: "SIERRA",
      title: "GLOBAL SENTIMENT",
      value: "STABLE",
      change: "0.0%",
      trend: "neutral",
      icon: ActivitySquare,
      color: "text-sys-text",
    },
    {
      id: "VICTOR",
      title: "CRITICAL RISK ZONES",
      value: "3",
      change: "MMO, ACT",
      trend: "down",
      icon: AlertTriangle,
      color: "text-[#ef4444]",
    }
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-4 gap-6 mb-10">
      {kpis.map((kpi, idx) => {
        const Icon = kpi.icon;
        return (
          <div key={idx} className="cyno-panel p-6 flex flex-col justify-between min-h-[140px] group transition-transform hover:-translate-y-1">
            <div className="flex justify-between items-start mb-4 gap-2">
              <div className="flex items-center">
                <div className="w-8 h-8 bg-sys-black border border-sys-blue flex items-center justify-center mr-3 shrink-0 rounded-sm">
                  <Icon className={`w-4 h-4 ${kpi.color}`} />
                </div>
                <div className="text-xs text-sys-muted font-bold tracking-widest uppercase leading-snug">{kpi.title}</div>
              </div>
              <div className="text-[10px] text-sys-muted font-bold tracking-widest bg-sys-black px-2 py-1 border border-sys-blue shrink-0 rounded-sm">
                {kpi.id}
              </div>
            </div>
            
            <div className="flex items-center justify-between mt-auto">
              <h3 className="text-3xl font-bold text-sys-text tracking-wider font-mono">{kpi.value}</h3>
              <div className="flex items-center text-xs font-mono tracking-wider font-bold bg-sys-black px-2 py-1 border border-sys-blue rounded-sm">
                <span className={`${
                  kpi.trend === 'up' ? 'text-sys-accent' : 
                  kpi.trend === 'down' ? 'text-[#ef4444]' : 'text-sys-muted'
                }`}>
                  {kpi.trend === 'up' ? '▲' : kpi.trend === 'down' ? '▼' : '■'} {kpi.change}
                </span>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
