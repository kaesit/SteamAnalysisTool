import { BarChart3, LayoutDashboard, PlusCircle, Settings, FileText, Database, Compass } from 'lucide-react';

interface SidebarProps {
  currentView: 'overview' | 'analysis';
  setCurrentView: (view: 'overview' | 'analysis') => void;
}

export function Sidebar({ currentView, setCurrentView }: SidebarProps) {
  const menuItems = [
    { id: 'overview', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'analysis', label: 'New Analysis', icon: PlusCircle },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'market', label: 'Market Trends', icon: BarChart3 },
    { id: 'data', label: 'Data Sources', icon: Database },
  ];

  return (
    <aside className="w-64 h-screen border-r border-white/5 bg-[#0a0c10]/80 backdrop-blur-3xl flex flex-col fixed left-0 top-0">
      <div className="h-16 flex items-center px-6 border-b border-white/5">
        <Compass className="w-6 h-6 text-violet-400 mr-2" />
        <span className="text-lg font-bold text-gradient tracking-wide">Game Oracle</span>
      </div>
      
      <div className="flex-1 py-6 px-4 space-y-2">
        <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4 px-2">Menu</div>
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => (item.id === 'overview' || item.id === 'analysis') && setCurrentView(item.id as any)}
              className={`w-full flex items-center px-3 py-2.5 rounded-xl transition-all duration-200 group ${
                isActive 
                  ? 'bg-violet-500/10 text-violet-300' 
                  : 'text-gray-400 hover:bg-white/5 hover:text-gray-200'
              }`}
            >
              <Icon className={`w-5 h-5 mr-3 transition-colors ${isActive ? 'text-violet-400' : 'text-gray-500 group-hover:text-gray-400'}`} />
              <span className="font-medium text-sm">{item.label}</span>
              {isActive && (
                <div className="ml-auto w-1.5 h-1.5 rounded-full bg-violet-400 shadow-[0_0_8px_rgba(167,139,250,0.8)]" />
              )}
            </button>
          );
        })}
      </div>

      <div className="p-4 border-t border-white/5">
        <button className="w-full flex items-center px-3 py-2.5 rounded-xl text-gray-400 hover:bg-white/5 hover:text-gray-200 transition-all duration-200">
          <Settings className="w-5 h-5 mr-3 text-gray-500" />
          <span className="font-medium text-sm">Settings</span>
        </button>
      </div>
    </aside>
  );
}
