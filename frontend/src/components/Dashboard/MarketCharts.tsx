import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar, Legend
} from 'recharts';

const sentimentData = [
  { name: 'T-6', pos: 4000, neg: 2400 },
  { name: 'T-5', pos: 3000, neg: 1398 },
  { name: 'T-4', pos: 2000, neg: 9800 },
  { name: 'T-3', pos: 2780, neg: 3908 },
  { name: 'T-2', pos: 1890, neg: 4800 },
  { name: 'T-1', pos: 2390, neg: 3800 },
  { name: 'NOW', pos: 3490, neg: 4300 },
];

const genreData = [
  { name: 'ACT', active: 400, load: 240 },
  { name: 'RPG', active: 300, load: 456 },
  { name: 'STR', active: 200, load: 139 },
  { name: 'SIM', active: 278, load: 390 },
  { name: 'IND', active: 589, load: 280 },
];

export function MarketCharts() {
  return (
    <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-10">
      {/* Sentiment Analysis Chart */}
      <div className="cyno-panel p-6 flex flex-col min-h-[420px]">
        <div className="flex justify-between items-center mb-6 border-b border-sys-blue pb-4">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-sys-accent mr-3 rounded-sm" />
            <div>
              <h3 className="text-sm font-bold text-sys-text uppercase tracking-widest">
                NLP SENTIMENT TELEMETRY
              </h3>
              <p className="text-[10px] text-sys-muted font-bold tracking-widest mt-1 uppercase">MODULE: STEAM_REVIEWS_v2.4</p>
            </div>
          </div>
          <div className="text-[10px] text-sys-accent font-bold tracking-widest bg-sys-black border border-sys-blue px-3 py-1 rounded-sm">LIVE</div>
        </div>
        <div className="flex-1 w-full font-mono text-xs">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={sentimentData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorPos" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--color-sys-accent)" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="var(--color-sys-accent)" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorNeg" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-sys-blue)" vertical={true} />
              <XAxis dataKey="name" stroke="var(--color-sys-muted)" fontSize={10} tickLine={false} axisLine={false} />
              <YAxis stroke="var(--color-sys-muted)" fontSize={10} tickLine={false} axisLine={false} tickFormatter={(value) => `${value / 1000}k`} />
              <Tooltip 
                contentStyle={{ backgroundColor: 'var(--color-sys-black)', border: '1px solid var(--color-sys-blue)', borderRadius: '4px', color: 'var(--color-sys-text)' }}
                itemStyle={{ fontSize: '12px', fontFamily: 'monospace', fontWeight: 'bold' }}
              />
              <Area type="monotone" dataKey="pos" stroke="var(--color-sys-accent)" strokeWidth={2} fillOpacity={1} fill="url(#colorPos)" />
              <Area type="monotone" dataKey="neg" stroke="#ef4444" strokeWidth={2} fillOpacity={1} fill="url(#colorNeg)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Genre Distribution Chart */}
      <div className="cyno-panel p-6 flex flex-col min-h-[420px]">
        <div className="flex justify-between items-center mb-6 border-b border-sys-blue pb-4">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-sys-text mr-3 rounded-sm" />
            <div>
              <h3 className="text-sm font-bold text-sys-text uppercase tracking-widest">
                GENRE SECTOR LOAD
              </h3>
              <p className="text-[10px] text-sys-muted font-bold tracking-widest mt-1 uppercase">MODULE: STEAM_DB_SYNC</p>
            </div>
          </div>
          <div className="text-[10px] text-sys-muted font-bold tracking-widest bg-sys-black border border-sys-blue px-3 py-1 rounded-sm">CACHED</div>
        </div>
        <div className="flex-1 w-full font-mono text-xs">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={genreData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-sys-blue)" vertical={false} />
              <XAxis dataKey="name" stroke="var(--color-sys-muted)" fontSize={10} tickLine={false} axisLine={false} />
              <YAxis stroke="var(--color-sys-muted)" fontSize={10} tickLine={false} axisLine={false} />
              <Tooltip 
                cursor={{ fill: 'rgba(0, 0, 0, 0.05)' }}
                contentStyle={{ backgroundColor: 'var(--color-sys-black)', border: '1px solid var(--color-sys-blue)', borderRadius: '4px', color: 'var(--color-sys-text)' }}
                itemStyle={{ fontSize: '12px', fontFamily: 'monospace', fontWeight: 'bold' }}
              />
              <Legend wrapperStyle={{ paddingTop: '10px', fontSize: '11px', fontWeight: 'bold' }} iconType="square" />
              <Bar dataKey="active" name="ACTIVE NODES" fill="var(--color-sys-accent)" radius={[2, 2, 0, 0]} />
              <Bar dataKey="load" name="SECTOR LOAD" fill="var(--color-sys-muted)" radius={[2, 2, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
