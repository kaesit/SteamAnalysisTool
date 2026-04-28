import { MoreHorizontal, Download, PlayCircle } from 'lucide-react';

const recentAnalyses = [
  { id: '1', name: 'Cyberpunk Chronicles', genre: 'Action RPG', success: 82, sentiment: 'Highly Positive', date: '2 hrs ago', status: 'Completed' },
  { id: '2', name: 'Farm Simulator 2024', genre: 'Simulation', success: 65, sentiment: 'Mixed', date: '5 hrs ago', status: 'Completed' },
  { id: '3', name: 'Space Explorer VR', genre: 'Action, VR', success: 41, sentiment: 'Negative', date: '1 day ago', status: 'Completed' },
  { id: '4', name: 'Medieval Dynasty', genre: 'Strategy', success: 91, sentiment: 'Overwhelmingly Positive', date: '2 days ago', status: 'Completed' },
  { id: '5', name: 'Project Velocity', genre: 'Racing', success: 0, sentiment: 'Pending Processing', date: 'Just now', status: 'Processing' },
];

export function RecentAnalysisTable() {
  return (
    <div className="glass-panel p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-100">Recent AI Analyses</h3>
          <p className="text-sm text-gray-400">Latest predictions processed by NLP models</p>
        </div>
        <button className="text-sm text-violet-400 hover:text-violet-300 font-medium transition-colors">
          View All
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-white/5 text-gray-400 text-sm">
              <th className="pb-3 font-medium px-4">Game Name</th>
              <th className="pb-3 font-medium px-4">Genre</th>
              <th className="pb-3 font-medium px-4">Predicted Success</th>
              <th className="pb-3 font-medium px-4">Market Sentiment</th>
              <th className="pb-3 font-medium px-4">Date</th>
              <th className="pb-3 font-medium px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="text-sm">
            {recentAnalyses.map((item) => (
              <tr key={item.id} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors group">
                <td className="py-4 px-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center border border-white/10 group-hover:border-violet-500/30 transition-colors">
                      <PlayCircle className="w-4 h-4 text-gray-400 group-hover:text-violet-400" />
                    </div>
                    <span className="font-medium text-gray-200">{item.name}</span>
                  </div>
                </td>
                <td className="py-4 px-4 text-gray-400">{item.genre}</td>
                <td className="py-4 px-4">
                  {item.status === 'Processing' ? (
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-amber-400 rounded-full animate-pulse" />
                      <span className="text-amber-400/80">Processing NLP...</span>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-2">
                      <div className="w-full bg-white/5 rounded-full h-1.5 max-w-[100px]">
                        <div 
                          className={`h-1.5 rounded-full ${
                            item.success >= 80 ? 'bg-emerald-400' : item.success >= 60 ? 'bg-amber-400' : 'bg-rose-400'
                          }`}
                          style={{ width: `${item.success}%` }}
                        />
                      </div>
                      <span className="text-gray-300 font-medium">{item.success}%</span>
                    </div>
                  )}
                </td>
                <td className="py-4 px-4">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-medium border ${
                    item.sentiment.includes('Positive') ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                    item.sentiment.includes('Negative') ? 'bg-rose-500/10 text-rose-400 border-rose-500/20' :
                    item.sentiment.includes('Mixed') ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' :
                    'bg-gray-500/10 text-gray-400 border-gray-500/20'
                  }`}>
                    {item.sentiment}
                  </span>
                </td>
                <td className="py-4 px-4 text-gray-500">{item.date}</td>
                <td className="py-4 px-4">
                  <div className="flex items-center justify-end space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button className="p-1.5 text-gray-400 hover:text-white hover:bg-white/10 rounded-md transition-colors" title="Download Report">
                      <Download className="w-4 h-4" />
                    </button>
                    <button className="p-1.5 text-gray-400 hover:text-white hover:bg-white/10 rounded-md transition-colors">
                      <MoreHorizontal className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
