import { TrendingUp, Activity, Gamepad2, AlertTriangle } from 'lucide-react';

export function KpiCards() {
  const kpis = [
    {
      title: "Total Games Analyzed",
      value: "14,205",
      change: "+12%",
      trend: "up",
      icon: Gamepad2,
      color: "from-violet-500 to-fuchsia-500",
      bgBase: "bg-violet-500/10"
    },
    {
      title: "Avg Success Predict",
      value: "68.4%",
      change: "+2.4%",
      trend: "up",
      icon: TrendingUp,
      color: "from-emerald-400 to-cyan-400",
      bgBase: "bg-emerald-500/10"
    },
    {
      title: "Market Sentiment",
      value: "Positive",
      change: "Stable",
      trend: "neutral",
      icon: Activity,
      color: "from-blue-400 to-indigo-500",
      bgBase: "bg-blue-500/10"
    },
    {
      title: "High Risk Genres",
      value: "3",
      change: "Action, MMO",
      trend: "down",
      icon: AlertTriangle,
      color: "from-rose-400 to-orange-400",
      bgBase: "bg-rose-500/10"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-8">
      {kpis.map((kpi, idx) => {
        const Icon = kpi.icon;
        return (
          <div key={idx} className="glass-panel p-6 relative group overflow-hidden transition-transform duration-300 hover:-translate-y-1">
            <div className={`absolute -right-6 -top-6 w-24 h-24 rounded-full blur-2xl opacity-20 bg-gradient-to-br ${kpi.color} group-hover:opacity-40 transition-opacity duration-500`} />
            
            <div className="flex justify-between items-start mb-4">
              <div>
                <p className="text-gray-400 text-sm font-medium mb-1">{kpi.title}</p>
                <h3 className="text-3xl font-bold text-gray-100 tracking-tight">{kpi.value}</h3>
              </div>
              <div className={`p-3 rounded-xl ${kpi.bgBase}`}>
                <Icon className={`w-6 h-6 text-transparent bg-clip-text bg-gradient-to-br ${kpi.color}`} style={{ color: 'white' }} />
              </div>
            </div>
            
            <div className="flex items-center text-sm">
              <span className={`font-medium ${
                kpi.trend === 'up' ? 'text-emerald-400' : 
                kpi.trend === 'down' ? 'text-rose-400' : 'text-gray-400'
              }`}>
                {kpi.change}
              </span>
              <span className="text-gray-500 ml-2">vs last month</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
