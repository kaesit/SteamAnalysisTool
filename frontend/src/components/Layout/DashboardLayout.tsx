import React from 'react';
import { Sidebar } from '../Sidebar/Sidebar';
import { Database, Search } from 'lucide-react';
import { ViewType } from '../../App';

interface DashboardLayoutProps {
  children: React.ReactNode;
  currentView: ViewType;
  setCurrentView: (view: ViewType) => void;
}

export function DashboardLayout({ children, currentView, setCurrentView }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-sys-black text-sys-text font-sans flex">
      {/* Sidebar */}
      <Sidebar currentView={currentView} setCurrentView={setCurrentView} />

      {/* Main Content Area */}
      <main className="flex-1 ml-[300px] min-h-screen flex flex-col relative z-10">

        {/* Top Header */}
        <header className="h-[88px] flex items-center justify-between px-10 border-b-2 border-sys-navy bg-sys-black/90 backdrop-blur-md sticky top-0 z-30">
          <div className="flex items-center w-[400px] relative">
            <Search className="w-5 h-5 text-sys-muted absolute left-4" />
            <input
              type="text"
              placeholder="SEARCH DATABASES..."
              className="w-full bg-sys-navy border-2 border-sys-blue rounded-[4px] py-2.5 pl-12 pr-4 text-sm font-mono tracking-wider text-sys-text placeholder-sys-muted focus:outline-none focus:border-sys-blue-light transition-all uppercase shadow-inner"
            />
          </div>

          <div className="flex items-center space-x-8">
            <div className="flex flex-col items-end border-r-2 border-sys-navy pr-8 hidden md:flex">
              <span className="text-xs text-sys-muted font-bold tracking-widest uppercase">Network Status</span>
              <span className="text-sm text-sys-accent font-mono tracking-widest font-bold">ONLINE / SECURE</span>
            </div>

            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 rounded-full bg-sys-navy border-2 border-sys-blue flex items-center justify-center">
                <Database className="w-5 h-5 text-sys-accent" />
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-bold uppercase tracking-wider">CYNOSURE DB</span>
                <span className="text-xs text-sys-muted font-mono tracking-widest">OP: SABUNCU</span>
              </div>
            </div>
          </div>
        </header>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto p-10 z-10 relative hide-scrollbar bg-[#090d16]">
          <div className="max-w-[1600px] mx-auto">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
}
