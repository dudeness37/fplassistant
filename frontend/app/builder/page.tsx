"use client";

import { Trophy, Sparkles, Shield, Target, Zap, RefreshCw, TrendingUp, DollarSign } from "lucide-react";
import { useState } from "react";

export default function AISquadBuilderPage() {
  const [budget, setBudget] = useState(100);
  const [riskLevel, setRiskLevel] = useState("balanced");
  const [formation, setFormation] = useState("3-4-3");
  const [isGenerating, setIsGenerating] = useState(false);
  const [showSquad, setShowSquad] = useState(true);

  const riskLevels = [
    { 
      id: "conservative", 
      name: "Conservative", 
      description: "Proven players with consistent returns",
      icon: Shield,
      gradient: "from-blue-600 to-cyan-600"
    },
    { 
      id: "balanced", 
      name: "Balanced", 
      description: "Mix of premium and value picks",
      icon: Target,
      gradient: "from-emerald-600 to-green-600"
    },
    { 
      id: "aggressive", 
      name: "Aggressive", 
      description: "High-risk differentials for big gains",
      icon: Zap,
      gradient: "from-orange-600 to-red-600"
    },
  ];

  const formations = ["3-4-3", "3-5-2", "4-3-3", "4-4-2", "4-5-1", "5-3-2", "5-4-1"];

  const suggestedSquad = {
    totalValue: 99.5,
    projectedValueGW5: 102.8,
    goalkeepers: [
      { name: "Alisson", team: "LIV", price: 5.5, ownership: 18.2, xPoints: 180, projectedPrice: 5.6 },
      { name: "Raya", team: "ARS", price: 4.5, ownership: 22.1, xPoints: 150, projectedPrice: 4.5 },
    ],
    defenders: [
      { name: "Alexander-Arnold", team: "LIV", price: 7.0, ownership: 41.2, xPoints: 185, projectedPrice: 7.2 },
      { name: "Saliba", team: "ARS", price: 6.0, ownership: 35.6, xPoints: 165, projectedPrice: 6.1 },
      { name: "Trippier", team: "NEW", price: 5.5, ownership: 28.9, xPoints: 155, projectedPrice: 5.4 },
      { name: "Gvardiol", team: "MCI", price: 6.0, ownership: 15.3, xPoints: 160, projectedPrice: 6.2 },
      { name: "White", team: "ARS", price: 4.5, ownership: 12.1, xPoints: 140, projectedPrice: 4.4 },
    ],
    midfielders: [
      { name: "Salah", team: "LIV", price: 12.5, ownership: 45.3, xPoints: 260, projectedPrice: 12.8 },
      { name: "Saka", team: "ARS", price: 8.5, ownership: 38.7, xPoints: 210, projectedPrice: 8.7 },
      { name: "Palmer", team: "CHE", price: 7.5, ownership: 28.3, xPoints: 190, projectedPrice: 7.8 },
      { name: "Ødegaard", team: "ARS", price: 8.0, ownership: 31.2, xPoints: 195, projectedPrice: 8.1 },
      { name: "Gordon", team: "NEW", price: 6.5, ownership: 18.7, xPoints: 170, projectedPrice: 6.7 },
    ],
    forwards: [
      { name: "Haaland", team: "MCI", price: 14.0, ownership: 72.1, xPoints: 280, projectedPrice: 14.3 },
      { name: "Watkins", team: "AVL", price: 9.0, ownership: 24.5, xPoints: 185, projectedPrice: 9.2 },
      { name: "Wissa", team: "BRE", price: 6.0, ownership: 8.9, xPoints: 145, projectedPrice: 6.1 },
    ],
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    setShowSquad(false);
    setTimeout(() => {
      setIsGenerating(false);
      setShowSquad(true);
    }, 2000);
  };

  const PlayerCard = ({ player, position }) => (
    <div className="p-4 bg-white/5 rounded-xl hover:bg-white/10 transition-all border border-white/5 group">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className={`
            w-10 h-10 rounded-xl flex items-center justify-center text-xs font-bold text-white shadow-lg
            ${position === 'GK' && 'bg-gradient-to-br from-amber-600 to-orange-600'}
            ${position === 'DEF' && 'bg-gradient-to-br from-emerald-600 to-green-600'}
            ${position === 'MID' && 'bg-gradient-to-br from-blue-600 to-indigo-600'}
            ${position === 'FWD' && 'bg-gradient-to-br from-purple-600 to-pink-600'}
          `}>
            {player.team}
          </div>
          <div>
            <p className="font-semibold text-white">{player.name}</p>
            <p className="text-xs text-gray-400">{player.team} • £{player.price}M</p>
          </div>
        </div>
        <div className="text-right">
          <div className="flex items-center gap-1">
            <TrendingUp size={14} className="text-green-400" />
            <span className="text-xs text-green-400 font-medium">
              +£{(player.projectedPrice - player.price).toFixed(1)}M
            </span>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-3 text-xs">
        <div className="text-center p-2 bg-white/5 rounded-lg">
          <div className="text-white font-medium">{player.ownership}%</div>
          <div className="text-gray-500">Ownership</div>
        </div>
        <div className="text-center p-2 bg-white/5 rounded-lg">
          <div className="gradient-text font-medium">{player.xPoints}</div>
          <div className="text-gray-500">xPoints</div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center animate-slide-up">
        <div className="flex items-center justify-center gap-3 mb-4">
          <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-pink-600 rounded-2xl flex items-center justify-center shadow-xl">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
        </div>
        <h1 className="text-4xl font-bold text-white mb-4">AI Squad Builder</h1>
        <p className="text-gray-400 max-w-2xl mx-auto text-lg">
          Let our advanced AI create the perfect starting squad based on historical data, 
          fixture analysis, and ownership trends.
        </p>
      </div>

      {/* Configuration */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Risk Level */}
        <div className="glass-card p-6 animate-scale-in">
          <h2 className="text-xl font-semibold text-white mb-6">Risk Level</h2>
          <div className="space-y-4">
            {riskLevels.map((level) => (
              <button
                key={level.id}
                onClick={() => setRiskLevel(level.id)}
                className={`
                  w-full p-5 rounded-xl transition-all duration-300 border
                  ${riskLevel === level.id 
                    ? 'bg-white/10 border-purple-500' 
                    : 'bg-white/5 border-white/5 hover:bg-white/10'
                  }
                `}
              >
                <div className="flex items-center gap-4">
                  <div className={`
                    w-14 h-14 rounded-xl bg-gradient-to-br ${level.gradient} 
                    flex items-center justify-center shadow-lg
                  `}>
                    <level.icon size={26} className="text-white" />
                  </div>
                  <div className="text-left flex-1">
                    <p className="font-semibold text-white text-lg">{level.name}</p>
                    <p className="text-sm text-gray-400">{level.description}</p>
                  </div>
                  {riskLevel === level.id && (
                    <div className="w-6 h-6 rounded-full bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center">
                      <div className="w-3 h-3 bg-white rounded-full"></div>
                    </div>
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Formation & Budget */}
        <div className="glass-card p-6 animate-scale-in stagger-1">
          <h2 className="text-xl font-semibold text-white mb-6">Configuration</h2>
          
          {/* Budget Slider */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-3">
              <label className="text-sm font-medium text-gray-300">Starting Budget</label>
              <span className="text-xl font-bold text-white">£{budget}M</span>
            </div>
            <input
              type="range"
              min="90"
              max="110"
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
              className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer slider"
              style={{
                background: `linear-gradient(to right, #8B5CF6 0%, #8B5CF6 ${((budget - 90) / 20) * 100}%, rgba(255,255,255,0.1) ${((budget - 90) / 20) * 100}%, rgba(255,255,255,0.1) 100%)`
              }}
            />
            <div className="flex justify-between text-xs text-gray-500 mt-2">
              <span>£90M</span>
              <span>£110M</span>
            </div>
          </div>

          {/* Formation Grid */}
          <div className="mb-8">
            <label className="text-sm font-medium text-gray-300 mb-3 block">Formation</label>
            <div className="grid grid-cols-4 gap-2">
              {formations.map((f) => (
                <button
                  key={f}
                  onClick={() => setFormation(f)}
                  className={`
                    py-2.5 rounded-lg font-medium transition-all text-sm
                    ${formation === f 
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white' 
                      : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
                    }
                  `}
                >
                  {f}
                </button>
              ))}
            </div>
          </div>

          {/* Generate Button */}
          <button 
            onClick={handleGenerate}
            disabled={isGenerating}
            className="w-full py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold rounded-xl hover:opacity-90 transition-all disabled:opacity-50 flex items-center justify-center gap-3"
          >
            {isGenerating ? (
              <>
                <RefreshCw className="animate-spin" size={20} />
                Analyzing Players...
              </>
            ) : (
              <>
                <Sparkles size={20} />
                Generate Squad
              </>
            )}
          </button>
        </div>
      </div>

      {/* AI Insights */}
      {showSquad && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-scale-in">
          {[
            {
              icon: Shield,
              title: "Key Differentials",
              description: "Palmer (28.3%) and Gordon (18.7%) offer excellent value with low ownership",
              gradient: "from-blue-600 to-cyan-600"
            },
            {
              icon: Target,
              title: "Captain Strategy",
              description: "Rotate between Haaland and Salah based on home fixtures",
              gradient: "from-emerald-600 to-green-600"
            },
            {
              icon: Sparkles,
              title: "Rotation Strategy",
              description: "Strong rotation options with Gvardiol and Gordon for flexibility",
              gradient: "from-purple-600 to-pink-600"
            },
            {
              icon: DollarSign,
              title: "Price Projection",
              description: `Squad value could reach £${suggestedSquad.projectedValueGW5}M by GW5 (+£${(suggestedSquad.projectedValueGW5 - suggestedSquad.totalValue).toFixed(1)}M)`,
              gradient: "from-orange-600 to-red-600"
            }
          ].map((insight, idx) => (
            <div 
              key={idx} 
              className="glass-card p-6 hover-lift border border-white/5"
              style={{ animationDelay: `${idx * 0.1}s` }}
            >
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${insight.gradient} flex items-center justify-center mb-4 shadow-lg`}>
                <insight.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="font-semibold text-white mb-2">{insight.title}</h3>
              <p className="text-sm text-gray-400">{insight.description}</p>
            </div>
          ))}
        </div>
      )}

      {/* Generated Squad */}
      {showSquad && (
        <div className="glass-card p-8 animate-scale-in">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-2xl font-bold text-white">AI Generated Squad</h2>
              <p className="text-sm text-gray-400 mt-1">Optimized for maximum points potential • Formation: {formation}</p>
            </div>
            <div className="text-right">
              <div className="flex items-center gap-6">
                <div>
                  <p className="text-sm text-gray-400">Current Value</p>
                  <p className="text-2xl font-bold gradient-text">£{suggestedSquad.totalValue}M</p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Projected GW5</p>
                  <p className="text-xl font-bold text-green-400">£{suggestedSquad.projectedValueGW5}M</p>
                </div>
              </div>
            </div>
          </div>

          {/* Squad Formation Layout */}
          <div className="space-y-8">
            {/* Goalkeepers */}
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-3 h-3 bg-amber-500 rounded-full"></div>
                <h3 className="text-lg font-semibold text-white">Goalkeepers</h3>
                <span className="text-sm text-gray-500">({suggestedSquad.goalkeepers.length})</span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {suggestedSquad.goalkeepers.map((player, idx) => (
                  <PlayerCard key={idx} player={player} position="GK" />
                ))}
              </div>
            </div>

            {/* Defenders */}
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-3 h-3 bg-emerald-500 rounded-full"></div>
                <h3 className="text-lg font-semibold text-white">Defenders</h3>
                <span className="text-sm text-gray-500">({suggestedSquad.defenders.length})</span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {suggestedSquad.defenders.map((player, idx) => (
                  <PlayerCard key={idx} player={player} position="DEF" />
                ))}
              </div>
            </div>

            {/* Midfielders */}
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                <h3 className="text-lg font-semibold text-white">Midfielders</h3>
                <span className="text-sm text-gray-500">({suggestedSquad.midfielders.length})</span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {suggestedSquad.midfielders.map((player, idx) => (
                  <PlayerCard key={idx} player={player} position="MID" />
                ))}
              </div>
            </div>

            {/* Forwards */}
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                <h3 className="text-lg font-semibold text-white">Forwards</h3>
                <span className="text-sm text-gray-500">({suggestedSquad.forwards.length})</span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {suggestedSquad.forwards.map((player, idx) => (
                  <PlayerCard key={idx} player={player} position="FWD" />
                ))}
              </div>
            </div>
          </div>

          {/* Single Action Button */}
          <div className="mt-8">
            <button className="w-full py-4 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-bold rounded-xl hover:opacity-90 transition-all flex items-center justify-center gap-3">
              <Trophy size={20} />
              Open in Squad
            </button>
          </div>
        </div>
      )}
    </div>
  );
}