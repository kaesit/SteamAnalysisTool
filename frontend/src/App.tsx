import { useState } from 'react';
import { DashboardLayout } from './components/Layout/DashboardLayout';
import { Overview } from './components/Dashboard/Overview';
import { AnalysisForm } from './components/Analysis/AnalysisForm';
import { ReportsView } from './components/Reports/ReportsView';
import { MarketTelemetry } from './components/Market/MarketTelemetry';
import { DataNodes } from './components/DataSources/DataNodes';

export type ViewType = 'overview' | 'analysis' | 'reports' | 'market' | 'data';

function App() {
  const [currentView, setCurrentView] = useState<ViewType>('overview');

  const renderView = () => {
    switch (currentView) {
      case 'overview': return <Overview />;
      case 'analysis': return <AnalysisForm />;
      case 'reports': return <ReportsView />;
      case 'market': return <MarketTelemetry />;
      case 'data': return <DataNodes />;
      default: return <Overview />;
    }
  };

  return (
    <DashboardLayout currentView={currentView} setCurrentView={setCurrentView}>
      {renderView()}
    </DashboardLayout>
  );
}

export default App;
