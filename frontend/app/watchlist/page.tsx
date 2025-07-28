"use client";

import { 
  Eye, 
  Plus, 
  TrendingUp, 
  TrendingDown, 
  Star, 
  Filter, 
  ChevronUp, 
  ChevronDown, 
  Zap,
  X,
  Trash2,
  Clock,
  Newspaper,
  Target,
  AlertTriangle,
  Search
} from "lucide-react";
import { useState, useEffect } from "react";

export default function WatchlistPage() {
  const [filterPosition, setFilterPosition] = useState("all");
  const [sortBy, setSortBy] = useState("form");
  const [timeToNextScout, setTimeToNextScout] = useState({
    hours: 7,
    minutes: 23,
    seconds: 45
  });
  
  // Scout timer countdown
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeToNextScout(prev => {
        if (prev.seconds > 0) {
          return { ...prev, seconds: prev.seconds - 1 };
        } else if (prev.minutes > 0) {
          return { ...prev, minutes: prev.minutes - 1, seconds: 59 };
        } else if (prev.hours > 0) {
          return { ...prev, hours: prev.hours - 1, minutes: 59, seconds: 59 };
        } else {
          // Reset to 12 hours when timer reaches 0
          return { hours: 12, minutes: 0, seconds: 0 };
        }
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const [players, setPlayers] = useState([
    { 
      id: 1,
      name: "Cole Palmer", 
      team: "CHE", 
      position: "MID", 
      price: 7.5,
      priceChange: 0.1,
      ownership: 28.3,
      form: 8.2,
      nextFixtures: ["bou (H)", "WOL (A)", "cry (H)"],
      difficulty: [2, 2, 3],
      expectedPoints: 28,
      trend: "up",
      aiScore: 94,
      priceRiseProbability: 85,
      latestNews: "Confirmed fit after minor knock, expected to start vs Bournemouth"
    },
    { 
      id: 2,
      name: "Darwin Núñez", 
      team: "LIV", 
      position: "FWD", 
      price: 7.0,
      priceChange: -0.1,
      ownership: 15.2,
      form: 6.5,
      nextFixtures: ["MCI (A)", "che (H)", "ARS (A)"],
      difficulty: [5, 4, 4],
      expectedPoints: 18,
      trend: "down",
      aiScore: 72,
      priceRiseProbability: 25,
      latestNews: "Klopp hints at rotation, but likely to feature against City"
    },
    { 
      id: 3,
      name: "Pedro Porro", 
      team: "TOT", 
      position: "DEF", 
      price: 5.5,
      priceChange: 0.0,
      ownership: 12.8,
      form: 7.1,
      nextFixtures: ["new (H)", "EVE (A)", "bha (H)"],
      difficulty: [3, 2, 2],
      expectedPoints: 22,
      trend: "up",
      aiScore: 85,
      priceRiseProbability: 65,
      latestNews: "Impressed in training, Postecoglou praises defensive work"
    },
    { 
      id: 4,
      name: "Bruno Guimarães", 
      team: "NEW", 
      position: "MID", 
      price: 6.0,
      priceChange: 0.2,
      ownership: 18.9,
      form: 7.8,
      nextFixtures: ["tot (A)", "BUR (H)", "whu (H)"],
      difficulty: [4, 2, 2],
      expectedPoints: 25,
      trend: "up",
      aiScore: 88,
      priceRiseProbability: 78,
      latestNews: "Captain armband secured, penalty duties confirmed"
    },
  ]);

  const positions = [
    { value: "all", label: "All Positions" },
    { value: "GK", label: "Goalkeepers" },
    { value: "DEF", label: "Defenders" },
    { value: "MID", label: "Midfielders" },
    { value: "FWD", label: "Forwards" },
  ];

  const removePlayer = (playerId) => {
    setPlayers(players.filter(p => p.id !== playerId));
  };

  const filteredPlayers = filterPosition === "all" 
    ? players 
    : players.filter(p => p.position === filterPosition);

  const sortedPlayers = [...filteredPlayers].sort((a, b) => {
    if (sortBy === "form") return b.form - a.form;
    if (sortBy === "price") return b.price - a.price;
    if (sortBy === "ai") return b.aiScore - a.aiScore;
    return 0;
  });

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 animate-slide-up">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Player Watchlist</h1>
          <p className="text-gray-400">Track and analyze potential transfer targets</p>
        </div>
        <div className="flex gap-3">
          {/* Scout Timer */}
          <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-cyan-600/20 to-blue-600/20 rounded-xl border border-cyan-600/30">
            <Search size={16} className="text-cyan-400" />
            <div className="text-sm">
              <span className="text-gray-400">Next Scout: </span>
              <span className="font-mono font-medium text-cyan-300">
                {String(timeToNextScout.hours).padStart(2, '0')}:
                {String(timeToNextScout.minutes).padStart(2, '0')}:
                {String(timeToNextScout.seconds).padStart(2, '0')}
              </span>
            </div>
          </div>
          <button className="btn btn-primary flex items-center gap-2">
            <Plus size={18} />
            Add Player
          </button>
        </div>
      </div>

      {/* Filters and Sort */}
      <div className="glass-card p-5 animate-slide-up">
        <div className="flex flex-col lg:flex-row gap-4">
          {/* Position Filter */}
          <div className="flex items-center gap-3 flex-1">
            <Filter size={18} className="text-gray-400" />
            <div className="flex gap-2 overflow-x-auto">
              {positions.map((pos) => (
                <button
                  key={pos.value}
                  onClick={() => setFilterPosition(pos.value)}
                  className={`
                    px-4 py-2 rounded-xl text-sm font-medium whitespace-nowrap transition-all
                    ${filterPosition === pos.value 
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white' 
                      : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
                    }
                  `}
                >
                  {pos.label}
                </button>
              ))}
            </div>
          </div>

          {/* Sort Options */}
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-400">Sort by:</span>
            <select 
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 bg-white/5 border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500"
            >
              <option value="form">Form</option>
              <option value="price">Price</option>
              <option value="ai">AI Score</option>
            </select>
          </div>
        </div>
      </div>

      {/* Players Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {sortedPlayers.map((player, idx) => (
          <div 
            key={player.id}
            className="glass-card p-6 hover-lift animate-scale-in group border border-white/5"
            style={{ animationDelay: `${idx * 0.1}s` }}
          >
            {/* Header with Delete Button */}
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-4">
                <div className={`
                  w-14 h-14 rounded-xl flex items-center justify-center text-sm font-bold shadow-lg
                  ${player.position === 'GK' && 'bg-gradient-to-br from-amber-600 to-orange-600'}
                  ${player.position === 'DEF' && 'bg-gradient-to-br from-emerald-600 to-green-600'}
                  ${player.position === 'MID' && 'bg-gradient-to-br from-blue-600 to-indigo-600'}
                  ${player.position === 'FWD' && 'bg-gradient-to-br from-purple-600 to-pink-600'}
                `}>
                  <span className="text-white">{player.position}</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">{player.name}</h3>
                  <p className="text-sm text-gray-400">{player.team} • £{player.price}M</p>
                </div>
              </div>
              <div className="flex gap-2">
                <button className="p-2 rounded-lg hover:bg-white/10 transition-colors">
                  <Star size={18} className="text-gray-400 hover:text-yellow-400" />
                </button>
                <button 
                  onClick={() => removePlayer(player.id)}
                  className="p-2 rounded-lg hover:bg-red-500/20 transition-colors group"
                >
                  <Trash2 size={18} className="text-gray-400 group-hover:text-red-400" />
                </button>
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-white">{player.form}</p>
                <p className="text-xs text-gray-500">Form</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold gradient-text">{player.expectedPoints}</p>
                <p className="text-xs text-gray-500">xPts</p>
              </div>
              <div className="text-center">
                <div className="flex items-center justify-center gap-1">
                  <span className="text-2xl font-bold text-white">{player.ownership}%</span>
                  {player.trend === 'up' ? (
                    <TrendingUp size={16} className="text-green-400" />
                  ) : (
                    <TrendingDown size={16} className="text-red-400" />
                  )}
                </div>
                <p className="text-xs text-gray-500">Owned</p>
              </div>
            </div>

            {/* Price Change & Rise Probability */}
            <div className="grid grid-cols-2 gap-3 mb-4">
              <div className="flex items-center justify-between p-3 bg-white/5 rounded-xl">
                <span className="text-xs text-gray-400">Price Change</span>
                <div className="flex items-center gap-1">
                  {player.priceChange > 0 ? (
                    <>
                      <ChevronUp size={14} className="text-green-400" />
                      <span className="text-green-400 font-medium text-sm">+£{player.priceChange}M</span>
                    </>
                  ) : player.priceChange < 0 ? (
                    <>
                      <ChevronDown size={14} className="text-red-400" />
                      <span className="text-red-400 font-medium text-sm">-£{Math.abs(player.priceChange)}M</span>
                    </>
                  ) : (
                    <span className="text-gray-400 text-sm">—</span>
                  )}
                </div>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-white/5 rounded-xl">
                <span className="text-xs text-gray-400">Rise Chance</span>
                <div className="flex items-center gap-1">
                  <Target size={12} className={player.priceRiseProbability > 70 ? "text-green-400" : player.priceRiseProbability > 40 ? "text-yellow-400" : "text-red-400"} />
                  <span className={`font-medium text-sm ${player.priceRiseProbability > 70 ? "text-green-400" : player.priceRiseProbability > 40 ? "text-yellow-400" : "text-red-400"}`}>
                    {player.priceRiseProbability}%
                  </span>
                </div>
              </div>
            </div>

            {/* Latest News */}
            <div className="p-3 bg-white/5 rounded-xl mb-4">
              <div className="flex items-center gap-2 mb-2">
                <Newspaper size={14} className="text-blue-400" />
                <span className="text-xs font-medium text-blue-400">Latest News</span>
              </div>
              <p className="text-xs text-gray-300 leading-relaxed">{player.latestNews}</p>
            </div>

            {/* Fixtures */}
            <div className="mb-4">
              <p className="text-sm text-gray-400 mb-2">Next 3 Fixtures</p>
              <div className="flex gap-2">
                {player.nextFixtures.map((fixture, i) => (
                  <div
                    key={i}
                    className={`
                      flex-1 px-3 py-2 rounded-lg text-center text-xs font-medium text-white
                      fdr-${player.difficulty[i]}
                    `}
                  >
                    {fixture}
                  </div>
                ))}
              </div>
            </div>

            {/* AI Score */}
            <div className="p-4 bg-gradient-to-r from-purple-600/10 to-pink-600/10 rounded-xl border border-purple-500/20">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Zap size={16} className="text-purple-400" />
                  <span className="text-sm font-medium text-purple-300">AI Score</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-24 h-2 bg-white/10 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500"
                      style={{ width: `${player.aiScore}%` }}
                    />
                  </div>
                  <span className="text-sm font-bold text-purple-300">{player.aiScore}</span>
                </div>
              </div>
            </div>

            {/* Action */}
            <button className="w-full mt-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-sm font-medium text-white transition-all opacity-0 group-hover:opacity-100">
              View Detailed Analysis
            </button>
          </div>
        ))}
      </div>

      {/* Watchlist News & AI Insights */}
      <div className="glass-card p-8 animate-slide-up">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-xl flex items-center justify-center animate-pulse-glow shadow-xl">
            <Newspaper className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="text-2xl font-bold text-white">Watchlist Intelligence</h3>
            <p className="text-gray-400">Latest news and AI insights for your tracked players</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* News Feed */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-white flex items-center gap-2">
              <Clock size={18} className="text-blue-400" />
              Recent Updates
            </h4>
            
            {players.slice(0, 3).map((player, idx) => (
              <div key={player.id} className="p-4 bg-white/5 rounded-xl border border-white/10">
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-cyan-600 rounded-lg flex items-center justify-center text-xs font-bold text-white flex-shrink-0">
                    {player.team}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <h5 className="font-semibold text-white">{player.name}</h5>
                      <span className="text-xs text-gray-500">{idx === 0 ? '2h ago' : idx === 1 ? '4h ago' : '6h ago'}</span>
                    </div>
                    <p className="text-sm text-gray-300 mb-2">{player.latestNews}</p>
                    <div className="flex items-center gap-4 text-xs">
                      <span className="text-gray-400">Expected: <span className="text-white font-medium">{player.expectedPoints} pts</span></span>
                      <span className="text-gray-400">Rise: <span className={`font-medium ${player.priceRiseProbability > 70 ? "text-green-400" : player.priceRiseProbability > 40 ? "text-yellow-400" : "text-red-400"}`}>{player.priceRiseProbability}%</span></span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* AI Predictions */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-white flex items-center gap-2">
              <Zap size={18} className="text-purple-400" />
              AI Predictions
            </h4>

            {/* Top Pick */}
            <div className="p-4 bg-gradient-to-r from-green-600/10 to-emerald-600/10 rounded-xl border border-green-500/20">
              <div className="flex items-center gap-2 mb-2">
                <Star size={16} className="text-green-400" />
                <span className="text-sm font-medium text-green-400">Top Pick This Week</span>
              </div>
              <div className="text-white font-semibold">{players[0]?.name} ({players[0]?.team})</div>
              <div className="text-sm text-gray-300 mt-1">
                {players[0]?.expectedPoints} expected points • {players[0]?.priceRiseProbability}% price rise chance
              </div>
            </div>

            {/* Price Alert */}
            <div className="p-4 bg-gradient-to-r from-yellow-600/10 to-orange-600/10 rounded-xl border border-yellow-500/20">
              <div className="flex items-center gap-2 mb-2">
                <AlertTriangle size={16} className="text-yellow-400" />
                <span className="text-sm font-medium text-yellow-400">Price Rise Alert</span>
              </div>
              <div className="text-white font-semibold">
                {players.filter(p => p.priceRiseProbability > 70).length} players likely to rise
              </div>
              <div className="text-sm text-gray-300 mt-1">
                Consider transferring in: {players.filter(p => p.priceRiseProbability > 70).map(p => p.name).join(', ')}
              </div>
            </div>

            {/* Form Alert */}
            <div className="p-4 bg-gradient-to-r from-purple-600/10 to-pink-600/10 rounded-xl border border-purple-500/20">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp size={16} className="text-purple-400" />
                <span className="text-sm font-medium text-purple-400">Form Watch</span>
              </div>
              <div className="text-white font-semibold">
                {players.filter(p => p.form > 7.5).length} players in excellent form
              </div>
              <div className="text-sm text-gray-300 mt-1">
                Average predicted points: {Math.round(players.reduce((sum, p) => sum + p.expectedPoints, 0) / players.length)} per player
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* AI Recommendation Banner */}
      <div className="relative overflow-hidden glass-card p-8 animate-slide-up">
        <div className="absolute top-0 right-0 w-64 h-64 bg-purple-600 rounded-full filter blur-3xl opacity-20"></div>
        <div className="relative z-10 flex items-start gap-6">
          <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-pink-600 rounded-2xl flex items-center justify-center flex-shrink-0 animate-pulse-glow shadow-xl">
            <Eye className="w-8 h-8 text-white" />
          </div>
          <div className="flex-1">
            <h3 className="text-2xl font-bold text-white mb-3">AI Transfer Recommendation</h3>
            <p className="text-gray-300 mb-4 max-w-2xl">
              Based on form, fixtures, and ownership trends, <span className="font-semibold text-white">Cole Palmer</span> presents 
              the best value for immediate transfer. His low ownership (28.3%) combined with excellent upcoming fixtures 
              make him an ideal differential pick for the next 3 gameweeks.
            </p>
            <div className="flex items-center gap-4">
              <button className="btn btn-primary">
                Add to Transfer List
              </button>
              <button className="text-sm font-medium text-purple-400 hover:text-purple-300">
                View Full Analysis →
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}