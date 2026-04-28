import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Cell } from 'recharts';
import { LineChart, Line } from 'recharts';
import { BarChart3, TrendingUp, DollarSign } from 'lucide-react';

const scatterData = [
  { name: 'Game A', price: 19.99, reviews: 85, success: 1 },
  { name: 'Game B', price: 9.99, reviews: 60, success: 0 },
  { name: 'Game C', price: 29.99, reviews: 92, success: 1 },
  { name: 'Game D', price: 59.99, reviews: 45, success: -1 },
  { name: 'Game E', price: 14.99, reviews: 78, success: 1 },
  { name: 'Game F', price: 39.99, reviews: 65, success: 0 },
  { name: 'Game G', price: 4.99, reviews: 88, success: 1 },
  { name: 'Game H', price: 24.99, reviews: 30, success: -1 },
  { name: 'Game I', price: 19.99, reviews: 72, success: 0 },
  { name: 'Game J', price: 34.99, reviews: 95, success: 1 },
];

const trendData = [
  { month: '01', tags: 400 },
  { month: '02', tags: 300 },
  { month: '03', tags: 550 },
  { month: '04', tags: 480 },
  { month: '05', tags: 600 },
  { month: '06', tags: 800 },
];

export function MarketTelemetry() {
  return (
    <div className="animate-in fade-in duration-300 max-w-[1400px] mx-auto">
      <div className="mb-10 flex justify-between items-end border-b-2 border-sys-blue pb-6">
        <div>
          <div className="flex items-center mb-2">
            <div className="w-6 h-6 bg-sys-text mr-3 flex items-center justify-center rounded-sm">
              <div className="w-2 h-2 bg-sys-black" />
            </div>
            <div className="text-sys-muted text-[10px] tracking-widest font-bold uppercase">MODULE: STEAM_RADAR_V1.4</div>
          </div>
          <h1 className="text-4xl font-bold text-sys-text tracking-widest uppercase">MARKET TELEMETRY</h1>
        </div>
        <div className="text-right bg-sys-navy p-4 border border-sys-blue relative">
          <div className="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-sys-text" />
          <div className="absolute bottom-0 right-0 w-2 h-2 border-b-2 border-r-2 border-sys-text" />
          <div className="text-[10px] text-sys-muted font-bold tracking-widest uppercase">DB SYNC: 12ms AGO</div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-8">
        
        {/* Scatter Plot: Price vs Reviews */}
        <div className="cyno-panel p-8 min-h-[450px] flex flex-col">
          <div className="flex justify-between items-center mb-8 border-b border-sys-blue pb-4">
             <div className="flex items-center">
               <DollarSign className="w-5 h-5 text-sys-accent mr-3" />
               <h2 className="text-sm font-bold text-sys-text tracking-widest uppercase">PRICE VS. POSITIVE REVIEWS</h2>
             </div>
             <div className="text-[10px] bg-sys-black border border-sys-blue px-3 py-1 text-sys-muted tracking-widest uppercase">SECTOR: ACTION RPG</div>
          </div>
          
          <div className="flex-1 w-full font-mono text-xs">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: -20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1a2c47" />
                <XAxis type="number" dataKey="price" name="Price USD" unit="$" stroke="#94a3b8" fontSize={10} tickLine={false} axisLine={false} />
                <YAxis type="number" dataKey="reviews" name="Positive %" unit="%" stroke="#94a3b8" fontSize={10} tickLine={false} axisLine={false} />
                <RechartsTooltip 
                  cursor={{ strokeDasharray: '3 3' }} 
                  contentStyle={{ backgroundColor: '#020408', border: '1px solid #1a2c47', borderRadius: '4px', color: '#f1f5f9' }}
                  itemStyle={{ fontSize: '12px', fontFamily: 'monospace', fontWeight: 'bold' }}
                />
                <Scatter name="Games" data={scatterData}>
                  {scatterData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.success === 1 ? '#60a5fa' : entry.success === -1 ? '#ef4444' : '#94a3b8'} />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Line Chart: Trending Tags */}
        <div className="cyno-panel p-8 min-h-[450px] flex flex-col">
          <div className="flex justify-between items-center mb-8 border-b border-sys-blue pb-4">
             <div className="flex items-center">
               <TrendingUp className="w-5 h-5 text-[#ef4444] mr-3" />
               <h2 className="text-sm font-bold text-sys-text tracking-widest uppercase">TAG FREQUENCY VELOCITY</h2>
             </div>
             <div className="text-[10px] bg-[#ef4444]/10 border border-[#ef4444] px-3 py-1 text-[#ef4444] tracking-widest uppercase font-bold animate-pulse">HOT: CYBERPUNK</div>
          </div>
          
          <div className="flex-1 w-full font-mono text-xs">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData} margin={{ top: 20, right: 20, bottom: 20, left: -20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1a2c47" vertical={false} />
                <XAxis dataKey="month" stroke="#94a3b8" fontSize={10} tickLine={false} axisLine={false} />
                <YAxis stroke="#94a3b8" fontSize={10} tickLine={false} axisLine={false} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#020408', border: '1px solid #1a2c47', borderRadius: '4px', color: '#f1f5f9' }}
                  itemStyle={{ fontSize: '12px', fontFamily: 'monospace', fontWeight: 'bold' }}
                />
                <Line type="monotone" dataKey="tags" stroke="#ef4444" strokeWidth={3} dot={{ r: 4, fill: '#ef4444', strokeWidth: 0 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
