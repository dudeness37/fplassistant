"use client";

import {
  BarChart3,
  Target,
  TrendingUp,
  TrendingDown,
  Shield,
  Zap,
  Clock,
  Users,
  Star,
  ArrowRight,
  Activity,
  DollarSign,
  AlertTriangle,
  CheckCircle,
  Eye
} from "lucide-react";
import { useState } from "react";

// Utility function to handle conditional classes
const clsx = (...classes: (string | boolean | undefined | null)[]) => {
  return classes.filter(Boolean).join(' ');
};

export default function PredictorPage() {
  const [selectedGameweek, setSelectedGameweek] = useState(3);
  const [selectedFixture, setSelectedFixture] = useState(null);

  const gameweeks = [
    { gw: 1, status: 'completed' },
    { gw: 2, status: 'completed' },
    { gw: 3, status: 'current' },
    { gw: 4, status: 'upcoming' },
    { gw: 5, status: 'upcoming' },
  ];

  const fixtures = [
    {
      id: 1,
      homeTeam: "Arsenal",
      awayTeam: "Chelsea",
      homeTeamShort: "ARS",
      awayTeamShort: "CHE",
      kickoff: "2024-03-15T15:00:00",
      venue: "Emirates Stadium",
      difficulty: { home: 4, away: 4 },
      predictions: {
        homeWin: 42,
        draw: 28,
        awayWin: 30,
        over25Goals: 68,
        btts: 72,
        homeScore: 2.1,
        awayScore: 1.8
      },
      keyPlayers: {
        home: [
          { name: "Saka", position: "MID", price: 8.5, ownership: 38.7, predictedPoints: 7.2, form: [6, 8, 4, 9, 7] },
          { name: "Jesus", position: "FWD", price: 7.0, ownership: 16.2, predictedPoints: 6.8, form: [4, 6, 8, 2, 7] }
        ],
        away: [
          { name: "Palmer", position: "MID", price: 7.5, ownership: 28.3, predictedPoints: 6.9, form: [8, 2, 10, 9, 6] },
          { name: "Jackson", position: "FWD", price: 7.0, ownership: 12.8, predictedPoints: 5.4, form: [2, 6, 4, 8, 3] }
        ]
      },
      insights: [
        "Arsenal have scored 2+ goals in 4 of their last 5 home games",
        "Chelsea's away form shows 60% clean sheet rate",
        "Both teams to score occurred in 3 of last 5 H2H meetings"
      ]
    },
    {
      id: 2,
      homeTeam: "Liverpool",
      awayTeam: "Manchester City",
      homeTeamShort: "LIV",
      awayTeamShort: "MCI",
      kickoff: "2024-03-15T17:30:00",
      venue: "Anfield",
      difficulty: { home: 5, away: 5 },
      predictions: {
        homeWin: 38,
        draw: 24,
        awayWin: 38,
        over25Goals: 75,
        btts: 78,
        homeScore: 2.3,
        awayScore: 2.1
      },
      keyPlayers: {
        home: [
          { name: "Salah", position: "MID", price: 12.5, ownership: 45.3, predictedPoints: 8.9, form: [12, 6, 8, 9, 10] },
          { name: "Alexander-Arnold", position: "DEF", price: 7.0, ownership: 41.2, predictedPoints: 6.8, form: [6, 8, 2, 4, 8] }
        ],
        away: [
          { name: "Haaland", position: "FWD", price: 14.0, ownership: 72.1, predictedPoints: 11.4, form: [15, 8, 10, 12, 13] },
          { name: "De Bruyne", position: "MID", price: 9.5, ownership: 22.1, predictedPoints: 7.8, form: [4, 8, 6, 10, 7] }
        ]
      },
      insights: [
        "High-scoring fixture - avg 3.2 goals in last 6 meetings",
        "Haaland has 8 goals in 4 games vs Liverpool",
        "Anfield factor gives Liverpool 15% boost in goal probability"
      ]
    },
    {
      id: 3,
      homeTeam: "Newcastle",
      awayTeam: "Brighton",
      homeTeamShort: "NEW",
      awayTeamShort: "BHA",
      kickoff: "2024-03-16T14:00:00",
      venue: "St. James' Park",
      difficulty: { home: 3, away: 3 },
      predictions: {
        homeWin: 48,
        draw: 26,
        awayWin: 26,
        over25Goals: 58,
        btts: 65,
        homeScore: 1.9,
        awayScore: 1.4
      },
      keyPlayers: {
        home: [
          { name: "Isak", position: "FWD", price: 8.5, ownership: 28.4, predictedPoints: 7.9, form: [8, 4, 6, 9, 7] },
          { name: "Gordon", position: "MID", price: 6.5, ownership: 18.7, predictedPoints: 5.9, form: [4, 6, 2, 6, 6] }
        ],
        away: [
          { name: "Mitoma", position: "MID", price: 6.5, ownership: 15.2, predictedPoints: 6.2, form: [6, 3, 7, 4, 8] },
          { name: "Ferguson", position: "FWD", price: 4.5, ownership: 8.9, predictedPoints: 4.8, form: [2, 6, 3, 4, 5] }
        ]
      },
      insights: [
        "Newcastle's home record: 65% win rate this season",
        "Brighton struggle away - only 2 wins in last 8",
        "Under 2.5 goals hit in 60% of Newcastle home games"
      ]
    },
    {
      id: 4,
      homeTeam: "Tottenham",
      awayTeam: "Manchester United",
      homeTeamShort: "TOT",
      awayTeamShort: "MUN",
      kickoff: "2024-03-16T16:30:00",
      venue: "Tottenham Hotspur Stadium",
      difficulty: { home: 4, away: 4 },
      predictions: {
        homeWin: 44,
        draw: 28,
        awayWin: 28,
        over25Goals: 62,
        btts: 69,
        homeScore: 2.0,
        awayScore: 1.6
      },
      keyPlayers: {
        home: [
          { name: "Son", position: "FWD", price: 9.0, ownership: 24.5, predictedPoints: 7.1, form: [6, 8, 3, 7, 9] },
          { name: "Maddison", position: "MID", price: 7.5, ownership: 15.2, predictedPoints: 6.4, form: [4, 6, 8, 3, 7] }
        ],
        away: [
          { name: "Fernandes", position: "MID", price: 8.0, ownership: 32.1, predictedPoints: 6.8, form: [6, 4, 6, 6, 6] },
          { name: "Rashford", position: "FWD", price: 6.5, ownership: 18.9, predictedPoints: 5.9, form: [3, 7, 2, 6, 4] }
        ]
      },
      insights: [
        "Spurs unbeaten at home in last 6 league games",
        "Man United's away form: 45% win rate",
        "Historical H2H suggests goals - 72% BTTS rate"
      ]
    }
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

  const getFormColor = (form) => {
    const avg = form.reduce((a, b) => a + b, 0) / form.length;
    if (avg >= 7) return 'text-green-400';
    if (avg >= 4) return 'text-yellow-400';
    return 'text-red-400';
  };

  const formatKickoffTime = (kickoff) => {
    const date = new Date(kickoff);
    return date.toLocaleTimeString('en-GB', { 
      hour: '2-digit', 
      minute: '2-digit',
      weekday: 'short'
    });
  };

  const FixtureModal = ({ fixture, onClose }) => {
    if (!fixture) return null;

    return (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div className="glass-card max-w-6xl w-full max-h-[90vh] overflow-y-auto">
          {/* Modal Header */}
          <div className="flex items-center justify-between p-6 border-b border-white/10">
            <div className="flex items-center gap-6">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold">
                  {fixture.homeTeamShort}
                </div>
                <span className="text-2xl text-gray-400">vs</span>
                <div className="w-12 h-12 bg-gradient-to-br from-red-600 to-pink-600 rounded-xl flex items-center justify-center text-white font-bold">
                  {fixture.awayTeamShort}
                </div>
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">{fixture.homeTeam} vs {fixture.awayTeam}</h2>
                <p className="text-gray-400">{fixture.venue} • {formatKickoffTime(fixture.kickoff)}</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-white/10 rounded-xl transition-colors"
            >
              <X size={24} className="text-gray-400" />
            </button>
          </div>

          {/* Modal Content */}
          <div className="p-6 space-y-8">
            {/* Match Predictions */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Result Probabilities */}
              <div className="space-y-4">
                <h3 className="text-xl font-bold text-white mb-4">Match Outcome</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 bg-white/5 rounded-xl">
                    <span className="text-white">{fixture.homeTeam} Win</span>
                    <div className="flex items-center gap-2">
                      <div className="w-24 h-2 bg-white/10 rounded-full overflow-hidden">
                        <div className="h-full bg-green-500" style={{ width: `${fixture.predictions.homeWin}%` }}></div>
                      </div>
                      <span className="text-green-400 font-medium text-sm">{fixture.predictions.homeWin}%</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-white/5 rounded-xl">
                    <span className="text-white">Draw</span>
                    <div className="flex items-center gap-2">
                      <div className="w-24 h-2 bg-white/10 rounded-full overflow-hidden">
                        <div className="h-full bg-yellow-500" style={{ width: `${fixture.predictions.draw}%` }}></div>
                      </div>
                      <span className="text-yellow-400 font-medium text-sm">{fixture.predictions.draw}%</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-white/5 rounded-xl">
                    <span className="text-white">{fixture.awayTeam} Win</span>
                    <div className="flex items-center gap-2">
                      <div className="w-24 h-2 bg-white/10 rounded-full overflow-hidden">
                        <div className="h-full bg-red-500" style={{ width: `${fixture.predictions.awayWin}%` }}></div>
                      </div>
                      <span className="text-red-400 font-medium text-sm">{fixture.predictions.awayWin}%</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Goals & Scoring */}
              <div className="space-y-4">
                <h3 className="text-xl font-bold text-white mb-4">Goals Analysis</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-4 bg-white/5 rounded-xl">
                    <div className="text-2xl font-bold gradient-text">{fixture.predictions.homeScore}</div>
                    <div className="text-xs text-gray-500">Expected Goals (Home)</div>
                  </div>
                  <div className="text-center p-4 bg-white/5 rounded-xl">
                    <div className="text-2xl font-bold gradient-text">{fixture.predictions.awayScore}</div>
                    <div className="text-xs text-gray-500">Expected Goals (Away)</div>
                  </div>
                  <div className="text-center p-4 bg-white/5 rounded-xl">
                    <div className="text-2xl font-bold text-green-400">{fixture.predictions.over25Goals}%</div>
                    <div className="text-xs text-gray-500">Over 2.5 Goals</div>
                  </div>
                  <div className="text-center p-4 bg-white/5 rounded-xl">
                    <div className="text-2xl font-bold text-blue-400">{fixture.predictions.btts}%</div>
                    <div className="text-xs text-gray-500">Both Teams Score</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Key Players */}
            <div>
              <h3 className="text-xl font-bold text-white mb-6">Key FPL Players</h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Home Team Players */}
                <div>
                  <h4 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                    <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                    {fixture.homeTeam}
                  </h4>
                  <div className="space-y-3">
                    {fixture.keyPlayers.home.map((player, idx) => (
                      <div key={idx} className="p-4 bg-white/5 rounded-xl">
                        <div className="flex items-center justify-between mb-3">
                          <div>
                            <div className="font-semibold text-white">{player.name}</div>
                            <div className="text-xs text-gray-400">{player.position} • £{player.price}M • {player.ownership}% owned</div>
                          </div>
                          <div className="text-right">
                            <div className="text-lg font-bold gradient-text">{player.predictedPoints}</div>
                            <div className="text-xs text-gray-500">exp pts</div>
                          </div>
                        </div>
                        <div className="flex gap-1">
                          {player.form.map((points, formIdx) => (
                            <div key={formIdx} className={clsx(
                              "flex-1 h-6 rounded flex items-center justify-center text-xs font-bold",
                              points >= 8 ? "bg-green-500 text-white" :
                              points >= 4 ? "bg-yellow-500 text-black" :
                              "bg-red-500 text-white"
                            )}>
                              {points}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Away Team Players */}
                <div>
                  <h4 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    {fixture.awayTeam}
                  </h4>
                  <div className="space-y-3">
                    {fixture.keyPlayers.away.map((player, idx) => (
                      <div key={idx} className="p-4 bg-white/5 rounded-xl">
                        <div className="flex items-center justify-between mb-3">
                          <div>
                            <div className="font-semibold text-white">{player.name}</div>
                            <div className="text-xs text-gray-400">{player.position} • £{player.price}M • {player.ownership}% owned</div>
                          </div>
                          <div className="text-right">
                            <div className="text-lg font-bold gradient-text">{player.predictedPoints}</div>
                            <div className="text-xs text-gray-500">exp pts</div>
                          </div>
                        </div>
                        <div className="flex gap-1">
                          {player.form.map((points, formIdx) => (
                            <div key={formIdx} className={clsx(
                              "flex-1 h-6 rounded flex items-center justify-center text-xs font-bold",
                              points >= 8 ? "bg-green-500 text-white" :
                              points >= 4 ? "bg-yellow-500 text-black" :
                              "bg-red-500 text-white"
                            )}>
                              {points}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* AI Insights */}
            <div>
              <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <Zap className="w-5 h-5 text-purple-400" />
                AI Insights
              </h3>
              <div className="space-y-3">
                {fixture.insights.map((insight, idx) => (
                  <div key={idx} className="flex items-start gap-3 p-4 bg-gradient-to-r from-purple-600/10 to-cyan-600/10 rounded-xl border border-purple-500/20">
                    <CheckCircle size={16} className="text-purple-400 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-300">{insight}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between animate-slide-up">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <BarChart3 className="w-8 h-8 text-purple-400" />
            FPL Predictor
          </h1>
          <p className="text-gray-400 mt-1">AI-powered fixture analysis and player predictions</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-600/20 to-cyan-600/20 rounded-xl border border-purple-600/30">
          <Target size={16} className="text-purple-400" />
          <span className="text-sm font-medium text-purple-300">Beta</span>
        </div>
      </div>

      {/* Gameweek Selector */}
      <div className="glass-card p-6 animate-scale-in">
        <h2 className="text-xl font-bold text-white mb-4">Select Gameweek</h2>
        <div className="flex gap-3">
          {gameweeks.map((gw) => (
            <button
              key={gw.gw}
              onClick={() => setSelectedGameweek(gw.gw)}
              className={clsx(
                "px-6 py-3 rounded-xl font-medium transition-all",
                selectedGameweek === gw.gw
                  ? "bg-gradient-to-r from-purple-600 to-cyan-600 text-white"
                  : "bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white",
                gw.status === 'completed' && "opacity-60",
                gw.status === 'current' && "ring-2 ring-purple-500/50"
              )}
            >
              <div className="text-center">
                <div>GW {gw.gw}</div>
                <div className="text-xs mt-1 capitalize">{gw.status}</div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Fixtures Grid */}
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-white">Gameweek {selectedGameweek} Fixtures</h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {fixtures.map((fixture, idx) => (
            <div
              key={fixture.id}
              onClick={() => setSelectedFixture(fixture)}
              className="glass-card p-6 hover-lift animate-scale-in cursor-pointer border border-white/5 group"
              style={{ animationDelay: `${idx * 0.1}s` }}
            >
              {/* Match Header */}
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold text-sm">
                      {fixture.homeTeamShort}
                    </div>
                    <span className="text-gray-400 font-medium">vs</span>
                    <div className="w-10 h-10 bg-gradient-to-br from-red-600 to-pink-600 rounded-xl flex items-center justify-center text-white font-bold text-sm">
                      {fixture.awayTeamShort}
                    </div>
                  </div>
                  <div>
                    <div className="font-semibold text-white">{fixture.homeTeam} vs {fixture.awayTeam}</div>
                    <div className="text-xs text-gray-500">{formatKickoffTime(fixture.kickoff)} • {fixture.venue}</div>
                  </div>
                </div>
                <ArrowRight size={20} className="text-gray-400 group-hover:text-purple-400 transition-colors" />
              </div>

              {/* Difficulty Ratings */}
              <div className="flex items-center gap-4 mb-4">
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-400">Difficulty:</span>
                  <div className={`px-2 py-1 rounded text-xs font-bold ${getDifficultyColor(fixture.difficulty.home)}`}>
                    {fixture.difficulty.home}
                  </div>
                  <span className="text-gray-500">-</span>
                  <div className={`px-2 py-1 rounded text-xs font-bold ${getDifficultyColor(fixture.difficulty.away)}`}>
                    {fixture.difficulty.away}
                  </div>
                </div>
              </div>

              {/* Quick Predictions */}
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div className="text-center p-3 bg-white/5 rounded-xl">
                  <div className="text-lg font-bold text-green-400">{fixture.predictions.homeWin}%</div>
                  <div className="text-xs text-gray-500">Home Win</div>
                </div>
                <div className="text-center p-3 bg-white/5 rounded-xl">
                  <div className="text-lg font-bold text-yellow-400">{fixture.predictions.draw}%</div>
                  <div className="text-xs text-gray-500">Draw</div>
                </div>
                <div className="text-center p-3 bg-white/5 rounded-xl">
                  <div className="text-lg font-bold text-red-400">{fixture.predictions.awayWin}%</div>
                  <div className="text-xs text-gray-500">Away Win</div>
                </div>
              </div>

              {/* Top Players Preview */}
              <div className="border-t border-white/10 pt-4">
                <div className="text-sm text-gray-400 mb-2">Top FPL Picks:</div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    {fixture.keyPlayers.home.slice(0, 1).map((player, pIdx) => (
                      <div key={pIdx} className="flex items-center gap-1">
                        <span className="text-white text-sm font-medium">{player.name}</span>
                        <span className={`text-xs ${getFormColor(player.form)}`}>({player.predictedPoints})</span>
                      </div>
                    ))}
                  </div>
                  <div className="flex items-center gap-2">
                    {fixture.keyPlayers.away.slice(0, 1).map((player, pIdx) => (
                      <div key={pIdx} className="flex items-center gap-1">
                        <span className="text-white text-sm font-medium">{player.name}</span>
                        <span className={`text-xs ${getFormColor(player.form)}`}>({player.predictedPoints})</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* AI Summary */}
      <div className="glass-card p-8 animate-slide-up border border-purple-500/20">
        <div className="flex items-start gap-6">
          <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-cyan-600 rounded-2xl flex items-center justify-center flex-shrink-0 animate-pulse-glow shadow-xl">
            <Eye className="w-8 h-8 text-white" />
          </div>
          <div className="flex-1">
            <h3 className="text-2xl font-bold text-white mb-3">AI Gameweek Summary</h3>
            <p className="text-gray-300 mb-4 max-w-3xl">
              Gameweek {selectedGameweek} features several high-scoring fixtures with Liverpool vs Manchester City 
              standing out as the premium captain choice battleground. Arsenal's home advantage against Chelsea 
              offers differential opportunities, while Newcastle vs Brighton presents the safest defensive options.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-gradient-to-r from-green-600/10 to-emerald-600/10 rounded-xl border border-green-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <Star size={16} className="text-green-400" />
                  <span className="text-sm font-medium text-green-400">Top Captain Pick</span>
                </div>
                <div className="text-white font-semibold">Haaland vs Liverpool</div>
              </div>
              <div className="p-4 bg-gradient-to-r from-blue-600/10 to-cyan-600/10 rounded-xl border border-blue-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <Target size={16} className="text-blue-400" />
                  <span className="text-sm font-medium text-blue-400">Best Differential</span>
                </div>
                <div className="text-white font-semibold">Palmer vs Arsenal</div>
              </div>
              <div className="p-4 bg-gradient-to-r from-purple-600/10 to-pink-600/10 rounded-xl border border-purple-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <Shield size={16} className="text-purple-400" />
                  <span className="text-sm font-medium text-purple-400">Safe Option</span>
                </div>
                <div className="text-white font-semibold">Newcastle Defence</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Fixture Modal */}
      <FixtureModal fixture={selectedFixture} onClose={() => setSelectedFixture(null)} />
    </div>
  );
}