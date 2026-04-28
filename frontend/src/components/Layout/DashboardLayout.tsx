import React from 'react';
import { Sidebar } from '../Sidebar/Sidebar';
import { Bell, Search, UserCircle } from 'lucide-react';

interface DashboardLayoutProps {
  children: React.ReactNode;
  currentView: 'overview' | 'analysis';
  setCurrentView: (view: 'overview' | 'analysis') => void;
}

export function DashboardLayout({ children, currentView, setCurrentView }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-[#0f1115] text-gray-200 font-sans selection:bg-violet-500/30 selection:text-white flex">
      {/* Sidebar - Fixed Position */}
      <Sidebar currentView={currentView} setCurrentView={setCurrentView} />

      {/* Main Content Area */}
      <main className="flex-1 ml-64 min-h-screen flex flex-col relative overflow-hidden">
        
        {/* Background Gradients for Glassmorphism */}
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-violet-900/20 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-cyan-900/10 rounded-full blur-[120px] pointer-events-none" />

        {/* Top Header */}
        <header className="h-16 flex items-center justify-between px-8 border-b border-white/5 backdrop-blur-md z-10 sticky top-0">
          <div className="flex items-center w-96 relative">
            <Search className="w-4 h-4 text-gray-500 absolute left-3" />
            <input 
              type="text" 
              placeholder="Search games, trends, or reports..." 
              className="w-full bg-white/[0.03] border border-white/[0.08] rounded-full py-1.5 pl-10 pr-4 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-violet-500/50 focus:bg-white/[0.05] transition-all"
            />
          </div>
          <div className="flex items-center space-x-4">
            <button className="p-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-full transition-colors relative">
              <Bell className="w-5 h-5" />
              <span className="absolute top-2 right-2 w-2 h-2 bg-rose-500 rounded-full border border-[#0f1115]" />
            </button>
            <div className="h-8 w-px bg-white/10" />
            <button className="flex items-center space-x-2 p-1 pr-2 rounded-full hover:bg-white/5 transition-colors border border-transparent hover:border-white/5">
              <UserCircle className="w-8 h-8 text-violet-400" />
              <span className="text-sm font-medium text-gray-300">Developer</span>
            </button>
          </div>
        </header>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto p-8 z-10 relative hide-scrollbar">
          {children}
        </div>
      </main>
    </div>
  );
}
