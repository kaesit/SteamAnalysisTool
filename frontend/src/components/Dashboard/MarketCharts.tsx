import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar, Legend
} from 'recharts';

const sentimentData = [
  { name: 'Jan', positive: 4000, negative: 2400 },
  { name: 'Feb', positive: 3000, negative: 1398 },
  { name: 'Mar', positive: 2000, negative: 9800 },
  { name: 'Apr', positive: 2780, negative: 3908 },
  { name: 'May', positive: 1890, negative: 4800 },
  { name: 'Jun', positive: 2390, negative: 3800 },
  { name: 'Jul', positive: 3490, negative: 4300 },
];

const genreData = [
  { name: 'Action', games: 400, revenue: 240 },
  { name: 'RPG', games: 300, revenue: 456 },
  { name: 'Strategy', games: 200, revenue: 139 },
  { name: 'Simulation', games: 278, revenue: 390 },
  { name: 'Indie', games: 589, revenue: 280 },
];

export function MarketCharts() {
  return (
    <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-8">
      {/* Sentiment Analysis Chart */}
      <div className="glass-panel p-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-100">Market Sentiment Analysis</h3>
            <p className="text-sm text-gray-400">NLP processed Steam reviews over time</p>
          </div>
        </div>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={sentimentData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorPos" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorNeg" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#f43f5e" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis dataKey="name" stroke="#6b7280" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis stroke="#6b7280" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `${value / 1000}k`} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#111827', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                itemStyle={{ fontSize: '14px' }}
              />
              <Area type="monotone" dataKey="positive" stroke="#8b5cf6" strokeWidth={3} fillOpacity={1} fill="url(#colorPos)" />
              <Area type="monotone" dataKey="negative" stroke="#f43f5e" strokeWidth={3} fillOpacity={1} fill="url(#colorNeg)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Genre Distribution Chart */}
      <div className="glass-panel p-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-100">Genre Distribution vs Revenue</h3>
            <p className="text-sm text-gray-400">Comparing active games and avg revenue</p>
          </div>
        </div>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={genreData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis dataKey="name" stroke="#6b7280" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis stroke="#6b7280" fontSize={12} tickLine={false} axisLine={false} />
              <Tooltip 
                cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                contentStyle={{ backgroundColor: '#111827', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
              />
              <Legend wrapperStyle={{ paddingTop: '10px' }} />
              <Bar dataKey="games" name="Total Games" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
              <Bar dataKey="revenue" name="Avg Revenue (k)" fill="#a855f7" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
