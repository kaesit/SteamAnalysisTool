import { useState } from 'react';
import { DashboardLayout } from './components/Layout/DashboardLayout';
import { Overview } from './components/Dashboard/Overview';
import { AnalysisForm } from './components/Analysis/AnalysisForm';

function App() {
  const [currentView, setCurrentView] = useState<'overview' | 'analysis'>('overview');

  return (
    <DashboardLayout currentView={currentView} setCurrentView={setCurrentView}>
      {currentView === 'overview' ? <Overview /> : <AnalysisForm />}
    </DashboardLayout>
  );
}

export default App;
