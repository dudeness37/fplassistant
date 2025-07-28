"use client";

import {
  CalendarDays,
  TrendingUp,
  Zap,
  Shield,
  Trophy,
  Users,
  AlertCircle,
  Newspaper,
  Repeat,
  Star,
  AlertTriangle,
  Target,
  Clock
} from "lucide-react";
import { useState } from "react";
// Utility function to handle conditional classes
const clsx = (...classes: (string | boolean | undefined | null)[]) => {
  return classes.filter(Boolean).join(' ');
};

export default function CalendarPage() {
  const [selectedGW, setSelectedGW] = useState<number | null>(null);
  const [highlightChip, setHighlightChip] = useState<string | null>(null);

  // Enhanced gameweek data with FDR-style information
  const gameweeksData = [
    { gw: 1, difficulty: 3, predictedPoints: 45, status: 'completed', chipRecommended: null, specialNote: null },
    { gw: 2, difficulty: 2, predictedPoints: 52, status: 'completed', chipRecommended: null, specialNote: null },
    { gw: 3, difficulty: 4, predictedPoints: 38, status: 'current', chipRecommended: null, specialNote: 'Derby Week' },
    { gw: 4, difficulty: 2, predictedPoints: 58, status: 'upcoming', chipRecommended: 'wildcard', specialNote: 'Great Fixtures' },
    { gw: 5, difficulty: 3, predictedPoints: 47, status: 'upcoming', chipRecommended: null, specialNote: null },
    { gw: 6, difficulty: 5, predictedPoints: 32, status: 'upcoming', chipRecommended: null, specialNote: 'Tough Week' },
    { gw: 7, difficulty: 3, predictedPoints: 49, status: 'upcoming', chipRecommended: null, specialNote: null },
    { gw: 8, difficulty: 1, predictedPoints: 65, status: 'upcoming', chipRecommended: 'triple-captain', specialNote: 'Double GW' },
    { gw: 9, difficulty: 4, predictedPoints: 41, status: 'upcoming', chipRecommended: null, specialNote: null },
    { gw: 10, difficulty: 2, predictedPoints: 54, status: 'upcoming', chipRecommended: null, specialNote: null },
    { gw: 11, difficulty: 3, predictedPoints: 46, status: 'upcoming', chipRecommended: null, specialNote: null },
    { gw: 12, difficulty: 2, predictedPoints: 61, status: 'upcoming', chipRecommended: 'bench-boost', specialNote: 'All Play' },
    { gw: 13, difficulty: 4, predictedPoints: 39, status: 'upcoming', chipRecommended: null, specialNote: null },
    { gw: 14, difficulty: 3, predictedPoints: 48, status: 'upcoming', chipRecommended: null, specialNote: null },
    { gw: 15, difficulty: 5, predictedPoints: 35, status: 'upcoming', chipRecommended: null, specialNote: 'Blank GW' },
    { gw: 16, difficulty: 2, predictedPoints: 55, status: 'upcoming', chipRecommended: null, specialNote: null },
    { gw: 17, difficulty: 3, predictedPoints: 44, status: 'upcoming', chipRecommended: null, specialNote: null },
    { gw: 18, difficulty: 1, predictedPoints: 28, status: 'upcoming', chipRecommended: 'free-hit', specialNote: 'Blank GW' },
    { gw: 19, difficulty: 4, predictedPoints: 42, status: 'upcoming', chipRecommended: null, specialNote: null },
  ];

  const fixtures = {
    3: [
      { home: "Arsenal", away: "Chelsea", difficultyHome: 4, difficultyAway: 4 },
      { home: "Liverpool", away: "Man City", difficultyHome: 5, difficultyAway: 5 },
      { home: "Newcastle", away: "Brighton", difficultyHome: 3, difficultyAway: 3 },
      { home: "Tottenham", away: "Man United", difficultyHome: 4, difficultyAway: 4 },
    ],
    4: [
      { home: "Aston Villa", away: "Brentford", difficultyHome: 3, difficultyAway: 2 },
      { home: "Crystal Palace", away: "Fulham", difficultyHome: 2, difficultyAway: 2 },
    ]
  };

  const chips = [
    {
      name: "Triple Captain",
      icon: Trophy,
      bestGW: "GW8",
      description: "Double gameweek with premium captain (Haaland).",
      color: "from-purple-500 to-pink-500",
      key: "triple-captain"
    },
    {
      name: "Bench Boost",
      icon: Users,
      bestGW: "GW12",
      description: "All 15 players with strong fixtures.",
      color: "from-blue-500 to-cyan-500",
      key: "bench-boost"
    },
    {
      name: "Free Hit",
      icon: Zap,
      bestGW: "GW18",
      description: "Best for navigating blank gameweeks.",
      color: "from-orange-500 to-red-500",
      key: "free-hit"
    },
    {
      name: "Wildcard",
      icon: Shield,
      bestGW: "GW4 or GW20",
      description: "Complete squad refresh during fixture swing.",
      color: "from-green-500 to-emerald-500",
      key: "wildcard"
    }
  ];

  const predictiveMatches = [
    { teams: "Liverpool vs Man City", winProb: "52%", over25: "68%" },
    { teams: "Arsenal vs Chelsea", winProb: "57%", over25: "61%" },
    { teams: "Tottenham vs Man United", winProb: "49%", over25: "72%" },
    { teams: "Newcastle vs Brighton", winProb: "55%", over25: "63%" }
  ];

  const transferSuggestions = [
    { player: "Haaland → Must Own", reason: "Facing weakest defense (xGC rank 20th)" },
    { player: "Salah → Explosive pick", reason: "Predicted 8.1 pts next GW" },
    { player: "Palmer → Differential", reason: "Penalty taker, strong xGI" }
  ];

  const getDifficultyColor = (difficulty: number) => {
    switch (difficulty) {
      case 1: return 'bg-green-500 text-white';
      case 2: return 'bg-green-400 text-black';
      case 3: return 'bg-yellow-400 text-black';  
      case 4: return 'bg-orange-500 text-white';
      case 5: return 'bg-red-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  const getStatusStyles = (status: string) => {
    switch (status) {
      case 'completed': return 'opacity-60 border-gray-600';
      case 'current': return 'ring-2 ring-purple-500 border-purple-400';
      case 'upcoming': return 'border-white/20';
      default: return 'border-white/20';
    }
  };

  const getChipIcon = (chipKey: string) => {
    const chip = chips.find(c => c.key === chipKey);
    return chip ? chip.icon : null;
  };

  return (
    <div className="space-y-8">
      {/* HEADER WITH CHIPS */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
          <CalendarDays className="w-8 h-8 text-purple-400" />
          Fixture Calendar
        </h1>

        <div className="flex gap-3">
          {chips.map((chip, idx) => (
            <button
              key={idx}
              onClick={() => setHighlightChip(highlightChip === chip.key ? null : chip.key)}
              className={clsx(
                "px-4 py-2 rounded-xl flex items-center gap-2 text-white font-medium text-sm bg-gradient-to-br hover:scale-105 transition-all",
                chip.color,
                highlightChip === chip.key && "ring-2 ring-white/50"
              )}
            >
              <chip.icon className="w-4 h-4" />
              {chip.name}
            </button>
          ))}
        </div>
      </div>

      {/* ENHANCED FDR-STYLE GAMEWEEK GRID */}
      <div className="glass-card p-8 rounded-3xl shadow-xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white mb-2">Gameweek Overview</h2>
          <p className="text-gray-400">Click on any gameweek to see detailed analysis</p>
        </div>

        {/* FDR Legend */}
        <div className="flex items-center gap-6 mb-8 p-4 bg-white/[0.02] rounded-xl">
          <span className="text-sm text-gray-400 font-medium">Difficulty:</span>
          {[1, 2, 3, 4, 5].map(diff => (
            <div key={diff} className="flex items-center gap-2">
              <div className={`w-6 h-6 rounded-lg ${getDifficultyColor(diff)} flex items-center justify-center text-xs font-bold`}>
                {diff}
              </div>
              <span className="text-xs text-gray-500">
                {diff === 1 ? 'Very Easy' : diff === 2 ? 'Easy' : diff === 3 ? 'Average' : diff === 4 ? 'Hard' : 'Very Hard'}
              </span>
            </div>
          ))}
        </div>

        {/* Enhanced Gameweek Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-7 gap-4">
          {gameweeksData.map((gwData) => {
            const ChipIcon = gwData.chipRecommended ? getChipIcon(gwData.chipRecommended) : null;
            const isHighlighted = highlightChip && gwData.chipRecommended === highlightChip;
            
            return (
              <div
                key={gwData.gw}
                onClick={() => setSelectedGW(gwData.gw === selectedGW ? null : gwData.gw)}
                className={clsx(
                  "relative group cursor-pointer rounded-2xl border-2 p-4 hover:scale-105 transition-all duration-300",
                  selectedGW === gwData.gw
                    ? "bg-gradient-to-br from-purple-600/20 to-cyan-600/20 border-purple-400 shadow-lg"
                    : "bg-white/[0.02] hover:bg-white/[0.05]",
                  getStatusStyles(gwData.status),
                  isHighlighted && "ring-4 ring-yellow-400/50 animate-pulse"
                )}
              >
                {/* Status indicator */}
                {gwData.status === 'current' && (
                  <div className="absolute -top-2 -right-2">
                    <div className="w-4 h-4 bg-purple-500 rounded-full animate-pulse"></div>
                  </div>
                )}

                {/* Chip recommendation */}
                {ChipIcon && (
                  <div className="absolute -top-2 -left-2">
                    <div className="w-6 h-6 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center">
                      <ChipIcon size={12} className="text-white" />
                    </div>
                  </div>
                )}

                {/* Special note indicator */}
                {gwData.specialNote && !ChipIcon && (
                  <div className="absolute -top-1 -right-1">
                    <AlertTriangle size={14} className="text-yellow-400" />
                  </div>
                )}

                <div className="text-center">
                  {/* GW Number */}
                  <div className="text-lg font-bold text-white mb-2">
                    GW {gwData.gw}
                  </div>

                  {/* Difficulty Rating */}
                  <div className={`
                    w-12 h-12 mx-auto mb-3 rounded-xl flex items-center justify-center text-lg font-bold
                    ${getDifficultyColor(gwData.difficulty)}
                    shadow-lg group-hover:scale-110 transition-transform
                  `}>
                    {gwData.difficulty}
                  </div>

                  {/* Predicted Points */}
                  <div className="mb-2">
                    <div className="text-2xl font-bold gradient-text">
                      {gwData.predictedPoints}
                    </div>
                    <div className="text-xs text-gray-500">predicted pts</div>
                  </div>

                  {/* Special Note */}
                  {gwData.specialNote && (
                    <div className="text-xs text-yellow-400 font-medium truncate">
                      {gwData.specialNote}
                    </div>
                  )}

                  {/* Status badge */}
                  <div className="mt-2">
                    {gwData.status === 'completed' && (
                      <span className="text-xs bg-gray-600 text-gray-300 px-2 py-1 rounded-full">
                        Done
                      </span>
                    )}
                    {gwData.status === 'current' && (
                      <span className="text-xs bg-purple-600 text-white px-2 py-1 rounded-full animate-pulse">
                        Live
                      </span>
                    )}
                  </div>
                </div>

                {/* Hover tooltip */}
                <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block z-10">
                  <div className="bg-black text-white text-xs rounded-lg px-3 py-2 whitespace-nowrap">
                    <div className="font-medium">Gameweek {gwData.gw}</div>
                    <div>Difficulty: {gwData.difficulty}/5</div>
                    <div>Predicted: {gwData.predictedPoints} pts</div>
                    {gwData.chipRecommended && (
                      <div className="text-yellow-400">
                        💡 {chips.find(c => c.key === gwData.chipRecommended)?.name}
                      </div>
                    )}
                    {gwData.specialNote && (
                      <div className="text-orange-400">⚠️ {gwData.specialNote}</div>
                    )}
                  </div>
                  <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-black"></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* EXPANDED GW DETAILS */}
      {selectedGW && (
        <div className="glass-card p-6 rounded-3xl space-y-6 animate-slide-up">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-white">
              Gameweek {selectedGW} Analysis
            </h2>
            <div className="flex items-center gap-4">
              {/* Difficulty badge */}
              <div className={`
                px-4 py-2 rounded-xl flex items-center gap-2
                ${getDifficultyColor(gameweeksData.find(gw => gw.gw === selectedGW)?.difficulty || 3)}
              `}>
                <Target size={16} />
                <span className="font-bold">
                  Difficulty: {gameweeksData.find(gw => gw.gw === selectedGW)?.difficulty}/5
                </span>
              </div>
              
              {/* Predicted points */}
              <div className="bg-gradient-to-r from-purple-600/20 to-cyan-600/20 px-4 py-2 rounded-xl border border-purple-500/30">
                <span className="text-sm text-gray-400">Predicted:</span>
                <span className="ml-2 text-xl font-bold gradient-text">
                  {gameweeksData.find(gw => gw.gw === selectedGW)?.predictedPoints} pts
                </span>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Fixtures */}
            <div className="bg-white/[0.02] p-4 rounded-xl border border-white/10">
              <h3 className="text-lg font-semibold text-purple-400 mb-3">Fixtures</h3>
              {fixtures[selectedGW as keyof typeof fixtures]?.map((fix, idx) => (
                <div
                  key={idx}
                  className="flex justify-between items-center py-3 border-b border-white/5 last:border-0"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-white font-medium">{fix.home}</span>
                    <div className={`w-6 h-6 rounded text-xs font-bold flex items-center justify-center ${getDifficultyColor(fix.difficultyHome)}`}>
                      {fix.difficultyHome}
                    </div>
                  </div>
                  <span className="text-gray-400 text-sm font-medium">vs</span>
                  <div className="flex items-center gap-2">
                    <div className={`w-6 h-6 rounded text-xs font-bold flex items-center justify-center ${getDifficultyColor(fix.difficultyAway)}`}>
                      {fix.difficultyAway}
                    </div>
                    <span className="text-white font-medium">{fix.away}</span>
                  </div>
                </div>
              )) || <p className="text-gray-500">Fixtures data coming soon...</p>}
            </div>

            {/* Top Predictive Matches */}
            <div className="bg-white/[0.02] p-4 rounded-xl border border-white/10">
              <h3 className="text-lg font-semibold text-purple-400 mb-3 flex items-center gap-2">
                <TrendingUp className="w-4 h-4" /> Top Predictive Matches
              </h3>
              {predictiveMatches.map((m, i) => (
                <div key={i} className="flex justify-between items-center py-2 text-sm">
                  <div>
                    <div className="text-white font-medium">{m.teams}</div>
                    <div className="text-gray-500 text-xs">Win: {m.winProb} • O2.5: {m.over25}</div>
                  </div>
                </div>
              ))}
            </div>

            {/* Squad Impact */}
            <div className="bg-white/[0.02] p-4 rounded-xl border border-white/10">
              <h3 className="text-lg font-semibold text-purple-400 mb-3 flex items-center gap-2">
                <Users className="w-4 h-4" /> Squad Impact
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Playing:</span>
                  <span className="text-green-400 font-medium">9/11 players</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Captain options:</span>
                  <span className="text-white font-medium">Haaland, Salah</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Bench strength:</span>
                  <span className="text-yellow-400 font-medium">Moderate</span>
                </div>
              </div>
            </div>

            {/* Transfer Suggestions */}
            <div className="bg-white/[0.02] p-4 rounded-xl border border-white/10">
              <h3 className="text-lg font-semibold text-purple-400 mb-3 flex items-center gap-2">
                <Repeat className="w-4 h-4" /> Best Transfers
              </h3>
              {transferSuggestions.map((t, i) => (
                <div key={i} className="py-2 border-b border-white/5 last:border-0">
                  <div className="text-sm font-medium text-white">{t.player}</div>
                  <div className="text-xs text-gray-400">{t.reason}</div>
                </div>
              ))}
            </div>

            {/* News */}
            <div className="bg-white/[0.02] p-4 rounded-xl border border-white/10 col-span-2">
              <h3 className="text-lg font-semibold text-purple-400 mb-3 flex items-center gap-2">
                <Newspaper className="w-4 h-4" /> GW News & Updates
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <div className="flex items-start gap-2">
                    <AlertTriangle size={14} className="text-yellow-400 mt-0.5 flex-shrink-0" />
                    <div className="text-sm">
                      <div className="text-white font-medium">Palmer flagged</div>
                      <div className="text-gray-500 text-xs">75% chance to miss</div>
                    </div>
                  </div>
                  <div className="flex items-start gap-2">
                    <Star size={14} className="text-green-400 mt-0.5 flex-shrink-0" />
                    <div className="text-sm">
                      <div className="text-white font-medium">Haaland confirmed</div>
                      <div className="text-gray-500 text-xs">Expected to start</div>
                    </div>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex items-start gap-2">
                    <Clock size={14} className="text-blue-400 mt-0.5 flex-shrink-0" />
                    <div className="text-sm">
                      <div className="text-white font-medium">Deadline reminder</div>
                      <div className="text-gray-500 text-xs">2 days, 14 hours left</div>
                    </div>
                  </div>
                  <div className="flex items-start gap-2">
                    <TrendingUp size={14} className="text-purple-400 mt-0.5 flex-shrink-0" />
                    <div className="text-sm">
                      <div className="text-white font-medium">Price changes</div>
                      <div className="text-gray-500 text-xs">3 players rising tonight</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}