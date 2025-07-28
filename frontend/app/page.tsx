"use client";

import { 
  TrendingUp, 
  Trophy, 
  DollarSign, 
  Users, 
  ArrowUp, 
  ArrowDown, 
  Zap, 
  AlertTriangle, 
  Star, 
  Target, 
  Activity, 
  Clock,
  Calendar,
  Eye,
  Sparkles,
  BarChart3,
  ArrowRight,
  Shield,
  TrendingDown
} from "lucide-react";
import { useState, useEffect } from "react";

export default function Dashboard() {
  const [selectedStat, setSelectedStat] = useState(0);
  const [animateValues, setAnimateValues] = useState(false);
  
  useEffect(() => {
    setAnimateValues(true);
  }, []);
  
  const stats = [
    {
      label: "Total Points",
      value: 247,
      displayValue: "247",
      change: "+12",
      trend: "up",
      icon: Trophy,
      gradient: "from-purple-600 to-pink-600",
      description: "Top 15% globally"
    },
    {
      label: "Overall Rank",
      value: 124521,
      displayValue: "124.5K",
      change: "↑ 15,243",
      trend: "up",
      icon: TrendingUp,
      gradient: "from-cyan-600 to-blue-600",
      description: "Rising fast"
    },
    {
      label: "Team Value",
      value: 101.2,
      displayValue: "£101.2M",
      change: "+£0.3M",
      trend: "up",
      icon: DollarSign,
      gradient: "from-green-600 to-emerald-600",
      description: "Above average"
    },
    {
      label: "Points Bench",
      value: 18,
      displayValue: "18",
      change: "+6",
      trend: "up",
      icon: Users,
      gradient: "from-orange-600 to-red-600",
      description: "Well selected"
    }
  ];

  const topPerformers = [
    { name: "Erling Haaland", team: "MCI", points: 15, ownership: 72.1, price: 14.0, position: "FWD", trend: "up" },
    { name: "Mohamed Salah", team: "LIV", points: 12, ownership: 45.3, price: 12.5, position: "MID", trend: "up" },
    { name: "Bukayo Saka", team: "ARS", points: 10, ownership: 38.7, price: 8.5, position: "MID", trend: "down" },
    { name: "Trent Alexander-Arnold", team: "LIV", points: 9, ownership: 41.2, price: 7.0, position: "DEF", trend: "up" },
  ];

  const liveMatches = [
    { home: "Arsenal", away: "Chelsea", score: "2-1", time: "67'", isLive: true },
    { home: "Liverpool", away: "Man City", score: "0-0", time: "HT", isLive: true },
    { home: "Newcastle", away: "Brighton", score: "-", time: "15:00", isLive: false },
  ];

  const upcomingFixtures = [
    { team: "Arsenal", opponent: "Brighton", difficulty: 2, venue: "H" },
    { team: "Liverpool", opponent: "Crystal Palace", difficulty: 2, venue: "A" },
    { team: "Man City", opponent: "Bournemouth", difficulty: 1, venue: "H" },
  ];

  const watchlistHighlights = [
    { name: "Palmer", team: "CHE", price: 7.5, priceRise: 85, reason: "Great fixtures" },
    { name: "Isak", team: "NEW", price: 8.5, priceRise: 78, reason: "On form" },
    { name: "Gordon", team: "NEW", price: 6.5, priceRise: 65, reason: "Value pick" },
  ];

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 1: return 'bg-green-500 text-white';
      case 2: return 'bg-green-400 text-black';
      case 3: return 'bg-yellow-400 text-black';  
      case 4: return 'bg-orange-500 text-white';
      case 5: return 'bg-red-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  const quickActions = [
    { 
      title: "Plan Transfers", 
      description: "GW3 deadline in 2 days",
      icon: Calendar,
      gradient: "from-purple-600 to-pink-600",
      action: "View Calendar",
      href: "/calendar"
    },
    { 
      title: "Squad Analysis", 
      description: "9/11 players starting",
      icon: Users,
      gradient: "from-green-600 to-emerald-600",
      action: "View Squad",
      href: "/squad"
    },
    { 
      title: "Build New Squad", 
      description: "AI-powered team builder",
      icon: Sparkles,
      gradient: "from-orange-600 to-red-600",
      action: "Try AI Builder",
      href: "/builder"
    },
    { 
      title: "Fixture Predictor", 
      description: "GW3 match predictions",
      icon: BarChart3,
      gradient: "from-blue-600 to-cyan-600",
      action: "View Predictions",
      href: "/predictor"
    }
  ];

  return (
    <div className="space-y-8">
      {/* Header with live indicator */}
      <div className="flex items-center justify-between animate-slide-up">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">Welcome back, John</h1>
          <p className="text-gray-400 text-lg">Here's your FPL performance overview</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-5 py-3 glass-card">
            <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium text-gray-300">Live Gameweek</span>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-600/20 to-cyan-600/20 rounded-xl border border-purple-600/30">
            <Zap size={16} className="text-purple-400" />
            <span className="text-sm font-medium text-purple-300">AI Active</span>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, idx) => (
          <div
            key={idx}
            onClick={() => setSelectedStat(idx)}
            className={`
              glass-card p-6 cursor-pointer hover-lift animate-scale-in
              ${selectedStat === idx ? 'ring-2 ring-purple-500/50' : ''}
            `}
            style={{ animationDelay: `${idx * 0.1}s` }}
          >
            {/* Gradient background */}
            <div className={`absolute inset-0 bg-gradient-to-br ${stat.gradient} opacity-5 rounded-[20px]`} />
            
            {/* Content */}
            <div className="relative z-10">
              <div className="flex items-start justify-between mb-4">
                <div className={`
                  w-14 h-14 rounded-2xl bg-gradient-to-br ${stat.gradient} 
                  flex items-center justify-center transform rotate-3 hover:rotate-6 transition-transform
                  shadow-lg
                `}>
                  <stat.icon size={26} className="text-white" />
                </div>
                <div className={`
                  flex items-center gap-1 text-sm font-semibold
                  ${stat.trend === 'up' ? 'text-green-400' : 'text-red-400'}
                `}>
                  {stat.change}
                  {stat.trend === 'up' ? <ArrowUp size={14} /> : <ArrowDown size={14} />}
                </div>
              </div>
              
              <h3 className="text-gray-400 text-sm font-medium mb-1">{stat.label}</h3>
              <p className="text-3xl font-bold text-white mb-2">
                {animateValues ? stat.displayValue : '0'}
              </p>
              <p className="text-xs text-gray-500">{stat.description}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {quickActions.map((action, idx) => (
          <div
            key={idx}
            className="glass-card p-6 hover-lift animate-scale-in cursor-pointer group"
            style={{ animationDelay: `${idx * 0.1}s` }}
          >
            <div className="flex items-start justify-between mb-4">
              <div className={`
                w-12 h-12 rounded-xl bg-gradient-to-br ${action.gradient} 
                flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform
              `}>
                <action.icon size={24} className="text-white" />
              </div>
              <ArrowRight size={16} className="text-gray-400 group-hover:text-purple-400 transition-colors" />
            </div>
            
            <h3 className="font-semibold text-white mb-2 group-hover:text-purple-300 transition-colors">
              {action.title}
            </h3>
            <p className="text-sm text-gray-400 mb-3">{action.description}</p>
            <button className="text-xs font-medium text-purple-400 hover:text-purple-300 transition-colors">
              {action.action} →
            </button>
          </div>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column - 2/3 width */}
        <div className="lg:col-span-2 space-y-6">
          {/* Top Performers */}
          <div className="glass-card p-6 animate-slide-up stagger-1">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold text-white">Top Performers</h2>
                <p className="text-sm text-gray-500 mt-1">Gameweek 3 standouts</p>
              </div>
              <button className="text-sm font-medium text-purple-400 hover:text-purple-300 transition-colors">
                View Squad →
              </button>
            </div>
            
            <div className="space-y-3">
              {topPerformers.map((player, idx) => (
                <div 
                  key={idx} 
                  className="group relative p-5 bg-white/[0.02] rounded-xl hover:bg-white/[0.05] transition-all duration-300 cursor-pointer border border-white/5"
                >
                  {/* Hover gradient */}
                  <div className="absolute inset-0 bg-gradient-to-r from-purple-600/0 via-purple-600/10 to-purple-600/0 opacity-0 group-hover:opacity-100 transition-opacity rounded-xl" />
                  
                  <div className="relative flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      {/* Rank badge */}
                      <div className="relative">
                        <div className="w-14 h-14 bg-gradient-to-br from-purple-600 to-pink-600 rounded-2xl flex items-center justify-center shadow-xl">
                          <span className="text-white font-bold text-lg">{idx + 1}</span>
                        </div>
                        {idx === 0 && (
                          <div className="absolute -top-2 -right-2">
                            <Star size={18} className="text-yellow-400 fill-yellow-400 drop-shadow-lg" />
                          </div>
                        )}
                      </div>
                      
                      {/* Player info */}
                      <div>
                        <p className="font-semibold text-white text-lg group-hover:text-purple-300 transition-colors">
                          {player.name}
                        </p>
                        <div className="flex items-center gap-3 text-sm mt-1">
                          <span className="text-gray-400">{player.team}</span>
                          <span className="text-gray-600">•</span>
                          <span className="text-gray-400">£{player.price}m</span>
                          <span className="text-gray-600">•</span>
                          <span className="text-gray-400">{player.ownership}%</span>
                        </div>
                      </div>
                    </div>
                    
                    {/* Points */}
                    <div className="text-right">
                      <p className="text-4xl font-bold gradient-text">{player.points}</p>
                      <p className="text-xs text-gray-500 uppercase tracking-wider">points</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* This Gameweek */}
          <div className="glass-card p-6 animate-slide-up stagger-2">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                  <h2 className="text-2xl font-bold text-white">This Gameweek</h2>
                </div>
                <span className="text-xs text-gray-500 bg-white/5 px-3 py-1 rounded-full">Your players highlighted</span>
              </div>
              <button className="text-sm font-medium text-purple-400 hover:text-purple-300 transition-colors">
                View Predictor →
              </button>
            </div>
            
            <div className="space-y-4">
              {liveMatches.map((match, idx) => (
                <div key={idx} className="p-5 bg-white/[0.02] rounded-xl border border-white/5 hover:bg-white/[0.05] transition-all">
                  <div className="flex items-center justify-between">
                    <div className="flex-1 text-right">
                      <p className="font-semibold text-white text-lg">{match.home}</p>
                    </div>
                    <div className="px-8 text-center">
                      {match.isLive ? (
                        <div>
                          <p className="text-3xl font-bold text-white">{match.score}</p>
                          <p className="text-xs text-green-400 animate-pulse mt-1">{match.time}</p>
                        </div>
                      ) : (
                        <p className="text-sm text-gray-400">{match.time}</p>
                      )}
                    </div>
                    <div className="flex-1">
                      <p className="font-semibold text-white text-lg">{match.away}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column - 1/3 width */}
        <div className="space-y-6">
          {/* AI Insights */}
          <div className="glass-card p-6 border border-purple-500/20 animate-slide-up stagger-3">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-pink-600 rounded-xl flex items-center justify-center animate-pulse-glow shadow-xl">
                <Zap size={24} className="text-white" />
              </div>
              <h3 className="text-xl font-bold text-white">AI Insights</h3>
            </div>
            
            <div className="space-y-4">
              {/* Transfer Suggestion */}
              <div className="p-4 bg-gradient-to-r from-purple-600/10 to-pink-600/10 rounded-xl border border-purple-500/20">
                <div className="flex items-start gap-3">
                  <Target size={20} className="text-purple-400 mt-0.5 flex-shrink-0" />
                  <div className="flex-1">
                    <h4 className="font-semibold text-white mb-1">Transfer Alert</h4>
                    <p className="text-sm text-gray-400 mb-3">
                      Palmer → Saka recommended. Better fixtures ahead.
                    </p>
                    <div className="flex items-center justify-between">
                      <button className="text-xs font-medium text-purple-400 hover:text-purple-300 transition-colors">
                        View Analysis →
                      </button>
                      <span className="text-xs text-gray-500 bg-white/5 px-2 py-1 rounded-full">85% confidence</span>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Captain Pick */}
              <div className="p-4 bg-gradient-to-r from-cyan-600/10 to-blue-600/10 rounded-xl border border-cyan-500/20">
                <div className="flex items-start gap-3">
                  <Trophy size={20} className="text-cyan-400 mt-0.5 flex-shrink-0" />
                  <div className="flex-1">
                    <h4 className="font-semibold text-white mb-1">Captain Choice</h4>
                    <p className="text-sm text-gray-400 mb-3">
                      Haaland (C) vs BOU - Premium pick
                    </p>
                    <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-500" style={{ width: '89%' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Upcoming Fixtures */}
          <div className="glass-card p-6 animate-slide-up stagger-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-white">Next Fixtures</h3>
              <button className="text-sm font-medium text-purple-400 hover:text-purple-300 transition-colors">
                View Calendar →
              </button>
            </div>
            <div className="space-y-3">
              {upcomingFixtures.map((fixture, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-white/5 rounded-xl">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-cyan-600 rounded-lg flex items-center justify-center text-xs font-bold text-white">
                      {fixture.team.slice(0,3)}
                    </div>
                    <div>
                      <div className="text-white text-sm font-medium">{fixture.opponent} ({fixture.venue})</div>
                    </div>
                  </div>
                  <div className={`px-2 py-1 rounded text-xs font-bold ${getDifficultyColor(fixture.difficulty)}`}>
                    {fixture.difficulty}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Watchlist Highlights */}
          <div className="glass-card p-6 animate-slide-up stagger-4">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Eye size={20} className="text-cyan-400" />
                <h3 className="text-xl font-bold text-white">Watchlist</h3>
              </div>
              <button className="text-sm font-medium text-purple-400 hover:text-purple-300 transition-colors">
                View All →
              </button>
            </div>
            <div className="space-y-3">
              {watchlistHighlights.map((player, idx) => (
                <div key={idx} className="p-3 bg-white/5 rounded-xl">
                  <div className="flex items-center justify-between mb-2">
                    <div>
                      <div className="text-white font-medium text-sm">{player.name}</div>
                      <div className="text-xs text-gray-400">{player.team} • £{player.price}M</div>
                    </div>
                    <div className="text-right">
                      <div className={`text-xs font-medium ${player.priceRise > 70 ? "text-green-400" : "text-yellow-400"}`}>
                        {player.priceRise}% rise
                      </div>
                    </div>
                  </div>
                  <div className="text-xs text-gray-500">{player.reason}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Alerts */}
          <div className="glass-card p-6 animate-slide-up stagger-4">
            <div className="flex items-center gap-2 mb-4">
              <AlertTriangle size={20} className="text-yellow-500" />
              <h3 className="text-xl font-bold text-white">Alerts</h3>
            </div>
            <div className="space-y-3">
              <div className="p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-xl">
                <p className="text-sm text-yellow-300 font-medium">Palmer flagged - 75% chance</p>
              </div>
              <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-xl">
                <p className="text-sm text-green-300 font-medium">Haaland price rise tonight</p>
              </div>
              <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-xl">
                <p className="text-sm text-blue-300 font-medium">GW3 deadline: 2 days left</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}