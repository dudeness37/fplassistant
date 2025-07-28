"use client";

import {
  Users,
  TrendingUp,
  DollarSign,
  AlertTriangle,
  Star,
  Target,
  Zap,
  Trophy,
  ArrowUp,
  ArrowDown,
  Clock,
  Newspaper,
  X,
  ExternalLink,
  Activity,
  BarChart3
} from "lucide-react";
import { useState } from "react";

// Utility function to handle conditional classes
const clsx = (...classes: (string | boolean | undefined | null)[]) => {
  return classes.filter(Boolean).join(' ');
};

export default function SquadPage() {
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [activeTab, setActiveTab] = useState('main');

  // Squad data
  const squad = {
    goalkeepers: [
      {
        id: 1,
        name: "Alisson",
        team: "LIV",
        price: 5.5,
        points: 12,
        selected: true,
        captain: false,
        viceCaptain: false,
        news: "Expected to start",
        status: "available",
        predictedPoints: 4.2,
        form: [2, 6, 4, 1, 3],
        ownership: 15.2
      },
      {
        id: 2,
        name: "Steele",
        team: "BHA",
        price: 4.0,
        points: 8,
        selected: false,
        captain: false,
        viceCaptain: false,
        news: "Backup keeper",
        status: "available",
        predictedPoints: 2.1,
        form: [1, 2, 1, 1, 2],
        ownership: 8.7
      }
    ],
    defenders: [
      {
        id: 3,
        name: "Trent Alexander-Arnold",
        team: "LIV",
        price: 7.0,
        points: 28,
        selected: true,
        captain: false,
        viceCaptain: false,
        news: "100% fit",
        status: "available",
        predictedPoints: 6.8,
        form: [6, 8, 2, 4, 8],
        ownership: 41.2
      },
      {
        id: 4,
        name: "Gabriel",
        team: "ARS",
        price: 6.0,
        points: 22,
        selected: true,
        captain: false,
        viceCaptain: false,
        news: "Minor knock",
        status: "doubt",
        predictedPoints: 5.4,
        form: [4, 6, 2, 6, 4],
        ownership: 28.9
      },
      {
        id: 5,
        name: "Saliba", 
        team: "ARS",
        price: 6.0,
        points: 18,
        selected: true,
        captain: false,
        viceCaptain: false,
        news: "Ready to play",
        status: "available",
        predictedPoints: 5.1,
        form: [3, 4, 6, 2, 3],
        ownership: 22.1
      },
      {
        id: 6,
        name: "Digne",
        team: "AVL",
        price: 4.5,
        points: 14,
        selected: false,
        captain: false,
        viceCaptain: false,
        news: "Rotation risk",
        status: "available",
        predictedPoints: 3.2,
        form: [2, 3, 4, 2, 3],
        ownership: 12.4
      },
      {
        id: 7,
        name: "Mykolenko",
        team: "EVE",
        price: 4.0,
        points: 8,
        selected: false,
        captain: false,
        viceCaptain: false,
        news: "Backup option",
        status: "available",
        predictedPoints: 2.8,
        form: [1, 2, 2, 1, 2],
        ownership: 5.8
      }
    ],
    midfielders: [
      {
        id: 8,
        name: "Mohamed Salah",
        team: "LIV",
        price: 12.5,
        points: 45,
        selected: true,
        captain: false,
        viceCaptain: true,
        news: "In great form",
        status: "available",
        predictedPoints: 8.9,
        form: [12, 6, 8, 9, 10],
        ownership: 45.3
      },
      {
        id: 9,
        name: "Bukayo Saka",
        team: "ARS",
        price: 8.5,
        points: 32,
        selected: true,
        captain: false,
        viceCaptain: false,
        news: "Fully fit",
        status: "available",
        predictedPoints: 7.2,
        form: [4, 8, 6, 6, 8],
        ownership: 38.7
      },
      {
        id: 10,
        name: "Palmer",
        team: "CHE",
        price: 10.5,
        points: 38,
        selected: true,
        captain: false,
        viceCaptain: false,
        news: "Flagged - 75%",
        status: "doubt",
        predictedPoints: 6.1,
        form: [8, 2, 10, 9, 9],
        ownership: 55.2
      },
      {
        id: 11,
        name: "Bruno Fernandes",
        team: "MUN",
        price: 8.0,
        points: 28,
        selected: true,
        captain: false,
        viceCaptain: false,
        news: "On penalties",
        status: "available",
        predictedPoints: 6.8,
        form: [6, 4, 6, 6, 6],
        ownership: 32.1
      },
      {
        id: 12,
        name: "Gordon",
        team: "NEW",
        price: 7.5,
        points: 24,
        selected: false,
        captain: false,
        viceCaptain: false,
        news: "Good fixtures",
        status: "available",
        predictedPoints: 5.9,
        form: [4, 6, 2, 6, 6],
        ownership: 18.9
      }
    ],
    forwards: [
      {
        id: 13,
        name: "Erling Haaland",
        team: "MCI",
        price: 14.0,
        points: 58,
        selected: true,
        captain: true,
        viceCaptain: false,
        news: "100% to start",
        status: "available",
        predictedPoints: 11.4,
        form: [15, 8, 10, 12, 13],
        ownership: 72.1
      },
      {
        id: 14,
        name: "Solanke",
        team: "BOU",
        price: 7.5,
        points: 18,
        selected: true,
        captain: false,
        viceCaptain: false,
        news: "Great value",
        status: "available",
        predictedPoints: 5.8,
        form: [4, 2, 6, 2, 4],
        ownership: 24.7
      },
      {
        id: 15,
        name: "Archer",
        team: "SHU",
        price: 4.5,
        points: 6,
        selected: false,
        captain: false,
        viceCaptain: false,
        news: "Bench fodder",
        status: "available",
        predictedPoints: 2.2,
        form: [1, 1, 2, 1, 1],
        ownership: 8.2
      }
    ]
  };

  // Low-cost haul potential players
  const lowCostHauls = [
    { id: 16, name: "Mitoma", team: "BHA", price: 6.5, predictedPoints: 7.8, reason: "Great fixtures", priceRise: 85 },
    { id: 17, name: "Mbeumo", team: "BRE", price: 5.5, predictedPoints: 6.9, reason: "On penalties", priceRise: 72 },
    { id: 18, name: "Rogers", team: "AVL", price: 5.0, predictedPoints: 6.2, reason: "Attacking returns", priceRise: 45 },
    { id: 19, name: "Welbeck", team: "BHA", price: 5.5, predictedPoints: 5.8, reason: "Home fixture", priceRise: 38 }
  ];

  // Popular transfer targets
  const transferTargets = [
    { id: 20, name: "Isak", team: "NEW", price: 8.5, predictedPoints: 7.9, priceRise: 78, ownership: 28.4 },
    { id: 21, name: "Watkins", team: "AVL", price: 9.0, predictedPoints: 7.2, priceRise: 65, ownership: 19.8 },
    { id: 22, name: "Maddison", team: "TOT", price: 7.5, predictedPoints: 6.8, priceRise: 52, ownership: 15.2 },
    { id: 23, name: "Diaz", team: "LIV", price: 7.5, predictedPoints: 6.5, priceRise: 44, ownership: 22.1 },
    { id: 24, name: "Bowen", team: "WHU", price: 7.0, predictedPoints: 6.1, priceRise: 38, ownership: 18.7 },
    { id: 25, name: "McNeil", team: "EVE", price: 5.0, predictedPoints: 5.9, priceRise: 71, ownership: 12.3 },
    { id: 26, name: "Cunha", team: "WOL", price: 6.5, predictedPoints: 5.7, priceRise: 29, ownership: 8.9 },
    { id: 27, name: "Havertz", team: "ARS", price: 8.0, predictedPoints: 5.4, priceRise: 22, ownership: 16.5 },
    { id: 28, name: "Jesus", team: "ARS", price: 7.0, predictedPoints: 5.2, priceRise: 18, ownership: 11.2 }
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'available': return 'border-green-500/30 bg-green-500/10';
      case 'doubt': return 'border-yellow-500/30 bg-yellow-500/10';
      case 'injured': return 'border-red-500/30 bg-red-500/10';
      default: return 'border-gray-500/30 bg-gray-500/10';
    }
  };

  const PlayerCard = ({ player, onSelect, size = 'normal' }) => (
    <div
      onClick={() => onSelect(player)}
      className={clsx(
        "relative cursor-pointer rounded-2xl border-2 transition-all duration-300 hover:scale-105",
        getStatusColor(player.status),
        player.selected ? "ring-2 ring-purple-500" : "",
        size === 'small' ? "p-3" : "p-4"
      )}
    >
      {/* Captain/Vice Captain badges */}
      {player.captain && (
        <div className="absolute -top-2 -right-2 w-6 h-6 bg-yellow-500 rounded-full flex items-center justify-center">
          <span className="text-xs font-bold text-black">C</span>
        </div>
      )}
      {player.viceCaptain && (
        <div className="absolute -top-2 -right-2 w-6 h-6 bg-gray-400 rounded-full flex items-center justify-center">
          <span className="text-xs font-bold text-black">V</span>
        </div>
      )}

      {/* Status indicator */}
      {player.status === 'doubt' && (
        <div className="absolute -top-1 -left-1">
          <AlertTriangle size={16} className="text-yellow-500" />
        </div>
      )}

      <div className="text-center">
        {/* Team badge placeholder */}
        <div className={clsx(
          "mx-auto mb-2 bg-gradient-to-br from-purple-600 to-cyan-600 rounded-xl flex items-center justify-center text-white font-bold",
          size === 'small' ? "w-10 h-10 text-xs" : "w-14 h-14 text-sm"
        )}>
          {player.team}
        </div>

        {/* Player name */}
        <div className={clsx(
          "font-semibold text-white mb-1 truncate",
          size === 'small' ? "text-xs" : "text-sm"
        )}>
          {player.name}
        </div>

        {/* Price and points */}
        <div className="flex justify-between items-center text-xs text-gray-400">
          <span>£{player.price}m</span>
          <span>{player.points}pts</span>
        </div>

        {/* Predicted points */}
        {player.predictedPoints && (
          <div className="mt-1 text-xs gradient-text font-bold">
            {player.predictedPoints} exp
          </div>
        )}
      </div>
    </div>
  );

  const PlayerModal = ({ player, onClose }) => {
    if (!player) return null;

    return (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div className="glass-card max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          {/* Modal Header */}
          <div className="flex items-center justify-between p-6 border-b border-white/10">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-cyan-600 rounded-2xl flex items-center justify-center text-white font-bold text-lg">
                {player.team}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">{player.name}</h2>
                <p className="text-gray-400">{player.team} • £{player.price}m • {player.points} points</p>
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
          <div className="p-6 space-y-6">
            {/* Stats Overview */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-white/5 rounded-xl">
                <div className="text-2xl font-bold gradient-text">{player.predictedPoints}</div>
                <div className="text-xs text-gray-500">Next GW</div>
              </div>
              <div className="text-center p-4 bg-white/5 rounded-xl">
                <div className="text-2xl font-bold text-white">{player.ownership}%</div>
                <div className="text-xs text-gray-500">Ownership</div>
              </div>
              <div className="text-center p-4 bg-white/5 rounded-xl">
                <div className="text-2xl font-bold text-white">{player.points}</div>
                <div className="text-xs text-gray-500">Total Points</div>
              </div>
              <div className="text-center p-4 bg-white/5 rounded-xl">
                <div className="text-2xl font-bold text-white">£{player.price}m</div>
                <div className="text-xs text-gray-500">Price</div>
              </div>
            </div>

            {/* Form */}
            <div className="bg-white/5 p-4 rounded-xl">
              <h3 className="text-lg font-semibold text-white mb-3">Recent Form</h3>
              <div className="flex gap-2">
                {player.form.map((points, idx) => (
                  <div key={idx} className="flex-1 text-center">
                    <div className={clsx(
                      "w-full h-8 rounded flex items-center justify-center text-sm font-bold",
                      points >= 8 ? "bg-green-500 text-white" :
                      points >= 4 ? "bg-yellow-500 text-black" :
                      "bg-red-500 text-white"
                    )}>
                      {points}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">GW{idx + 1}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* News Feed */}
            <div className="bg-white/5 p-4 rounded-xl">
              <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                <Newspaper className="w-5 h-5" />
                Latest News
              </h3>
              <div className="space-y-3">
                <div className="flex items-start gap-3 p-3 bg-white/5 rounded-lg">
                  <div className="w-2 h-2 bg-green-400 rounded-full mt-2 flex-shrink-0"></div>
                  <div>
                    <div className="text-white font-medium">Confirmed in training</div>
                    <div className="text-gray-400 text-sm">Expected to start against Brighton • 2 hours ago</div>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-3 bg-white/5 rounded-lg">
                  <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
                  <div>
                    <div className="text-white font-medium">Manager's press conference</div>
                    <div className="text-gray-400 text-sm">"He's in great form and ready to play" • 1 day ago</div>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-3 bg-white/5 rounded-lg">
                  <div className="w-2 h-2 bg-yellow-400 rounded-full mt-2 flex-shrink-0"></div>
                  <div>
                    <div className="text-white font-medium">Injury update</div>
                    <div className="text-gray-400 text-sm">Minor knock cleared, fit for selection • 2 days ago</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Transfer Actions */}
            <div className="flex gap-4">
              <button className="flex-1 btn btn-primary">
                Transfer Out
              </button>
              <button className="flex-1 btn btn-ghost">
                Make Captain
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <Users className="w-8 h-8 text-purple-400" />
            My Squad
          </h1>
          <p className="text-gray-400 mt-1">Gameweek 3 • £100.2M team value • 1 free transfer</p>
        </div>
        <div className="flex gap-3">
          <button className="btn btn-primary">
            Make Transfer
          </button>
          <button className="btn btn-ghost">
            Auto Pick
          </button>
        </div>
      </div>

      {/* Main Squad Formation */}
      <div className="glass-card p-8 rounded-3xl">
        <h2 className="text-xl font-bold text-white mb-6">Formation: 3-4-3</h2>
        
        <div className="space-y-8">
          {/* Goalkeepers */}
          <div>
            <h3 className="text-lg font-semibold text-purple-400 mb-4">Goalkeepers</h3>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              {squad.goalkeepers.map(player => (
                <PlayerCard key={player.id} player={player} onSelect={setSelectedPlayer} />
              ))}
            </div>
          </div>

          {/* Defenders */}
          <div>
            <h3 className="text-lg font-semibold text-purple-400 mb-4">Defenders</h3>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              {squad.defenders.map(player => (
                <PlayerCard key={player.id} player={player} onSelect={setSelectedPlayer} />
              ))}
            </div>
          </div>

          {/* Midfielders */}
          <div>
            <h3 className="text-lg font-semibold text-purple-400 mb-4">Midfielders</h3>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              {squad.midfielders.map(player => (
                <PlayerCard key={player.id} player={player} onSelect={setSelectedPlayer} />
              ))}
            </div>
          </div>

          {/* Forwards */}
          <div>
            <h3 className="text-lg font-semibold text-purple-400 mb-4">Forwards</h3>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              {squad.forwards.map(player => (
                <PlayerCard key={player.id} player={player} onSelect={setSelectedPlayer} />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Additional Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Low-Cost Haul Potential */}
        <div className="glass-card p-6">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-green-400" />
            Low-Cost Haul Potential
          </h2>
          <p className="text-gray-400 text-sm mb-6">Budget players who could deliver big returns this GW</p>
          
          <div className="grid grid-cols-2 gap-4">
            {lowCostHauls.map(player => (
              <div key={player.id} className="p-4 bg-white/5 rounded-xl hover:bg-white/10 transition-colors cursor-pointer">
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <div className="font-semibold text-white">{player.name}</div>
                    <div className="text-xs text-gray-400">{player.team} • £{player.price}m</div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold gradient-text">{player.predictedPoints}</div>
                    <div className="text-xs text-gray-500">exp pts</div>
                  </div>
                </div>
                <div className="text-xs text-green-400 mb-2">{player.reason}</div>
                <div className="flex items-center gap-2 text-xs">
                  <ArrowUp size={12} className="text-green-400" />
                  <span className="text-gray-400">{player.priceRise}% rise chance</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Assistant */}
        <div className="glass-card p-6 border border-purple-500/20">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-purple-400" />
            AI Assistant
          </h2>
          
          <div className="space-y-4">
            <div className="p-4 bg-gradient-to-r from-purple-600/10 to-cyan-600/10 rounded-xl border border-purple-500/20">
              <h3 className="font-semibold text-white mb-2">Squad Analysis</h3>
              <p className="text-sm text-gray-300 mb-3">
                Your current squad looks strong for GW3. The 3-4-3 formation maximizes attacking returns with Haaland (C) leading the line. 
              </p>
              <p className="text-sm text-gray-300">
                Consider Palmer's injury flag - Gordon could be a good replacement if he's ruled out.
              </p>
            </div>
            
            <div className="p-4 bg-gradient-to-r from-green-600/10 to-blue-600/10 rounded-xl border border-green-500/20">
              <h3 className="font-semibold text-white mb-2">Transfer Suggestion</h3>
              <p className="text-sm text-gray-300">
                If Palmer is ruled out, consider Gordon (NEW) for excellent fixtures or Mitoma (BHA) for his attacking potential at home.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Popular Transfer Targets */}
      <div className="glass-card p-6">
        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-cyan-400" />
          Popular Transfer Targets
        </h2>
        <p className="text-gray-400 text-sm mb-6">Most transferred-in players for GW3</p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {transferTargets.map(player => (
            <div key={player.id} className="p-4 bg-white/5 rounded-xl hover:bg-white/10 transition-colors cursor-pointer">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <div className="font-semibold text-white">{player.name}</div>
                  <div className="text-xs text-gray-400">{player.team} • {player.ownership}% owned</div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold gradient-text">{player.predictedPoints}</div>
                  <div className="text-xs text-gray-500">expected</div>
                </div>
              </div>
              
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-300">£{player.price}m</span>
                <div className="flex items-center gap-1">
                  <ArrowUp size={12} className="text-green-400" />
                  <span className="text-green-400">{player.priceRise}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Player Modal */}
      <PlayerModal player={selectedPlayer} onClose={() => setSelectedPlayer(null)} />
    </div>
  );
}