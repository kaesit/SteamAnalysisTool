import { LayoutDashboard, PlusCircle, FileText, BarChart3, Database } from 'lucide-react';
import { ViewType } from '../../App';

interface SidebarProps {
  currentView: ViewType;
  setCurrentView: (view: ViewType) => void;
}

export function Sidebar({ currentView, setCurrentView }: SidebarProps) {
  const menuItems = [
    { id: 'overview', label: 'SECTOR OVERVIEW', icon: LayoutDashboard },
    { id: 'analysis', label: 'NEW ANALYSIS UPLINK', icon: PlusCircle },
    { id: 'reports', label: 'DATATERMINALS', icon: FileText },
    { id: 'market', label: 'MARKET TELEMETRY', icon: BarChart3 },
    { id: 'data', label: 'SECURE NODES', icon: Database },
  ];

  return (
    <aside className="w-[300px] h-screen bg-sys-black border-r-2 border-sys-navy flex flex-col fixed left-0 top-0 z-20">
      
      <div className="h-[88px] flex items-center px-8 border-b-2 border-sys-navy">
        <div className="w-12 h-12 bg-sys-navy border-2 border-sys-blue flex items-center justify-center mr-4 rounded-[4px]">
          <div className="w-6 h-6 border-2 border-sys-accent rounded-full flex items-center justify-center">
            <div className="w-2 h-2 bg-sys-accent rounded-full" />
          </div>
        </div>
        <div>
          <span className="text-xl font-bold text-sys-text tracking-[0.1em] uppercase">CYNOSURE</span>
          <div className="text-[10px] text-sys-muted font-bold tracking-[0.2em] uppercase mt-1">ANALYSIS SYSTEM</div>
        </div>
      </div>
      
      <div className="flex-1 py-8 px-6 pl-8 space-y-3">
        <div className="text-xs font-bold text-sys-muted uppercase tracking-[0.2em] mb-6">Navigation Control</div>
        
        {menuItems.map((item, idx) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id as ViewType)}
              className={`w-full flex items-center px-4 py-3.5 transition-all duration-200 group relative ${
                isActive 
                  ? 'bg-sys-navy text-sys-accent border-l-4 border-sys-accent' 
                  : 'bg-transparent text-sys-muted border-l-4 border-transparent hover:bg-sys-navy hover:text-sys-text hover:border-sys-blue'
              }`}
            >
              <div className="flex items-center w-full">
                <Icon className={`w-5 h-5 mr-4 ${isActive ? 'text-sys-accent' : 'text-sys-muted group-hover:text-sys-text'}`} />
                <span className="font-bold text-xs tracking-widest uppercase">{item.label}</span>
              </div>
            </button>
          );
        })}
      </div>

      <div className="p-8 border-t-2 border-sys-navy">
        <div className="sys-panel p-4 flex flex-col items-center justify-center text-center">
          <span className="text-[10px] text-sys-muted font-bold uppercase tracking-[0.2em] mb-2">System Load</span>
          <div className="w-full bg-sys-black border border-sys-blue h-3 rounded-sm mb-2">
             <div className="bg-sys-accent h-full w-[35%]" />
          </div>
          <span className="text-xs font-mono font-bold text-sys-text tracking-widest">35.0% NOMINAL</span>
        </div>
      </div>
    </aside>
  );
}
