"use client";

import { Home, Calendar, Users, Eye, Sparkles, BarChart3, Settings, TrendingUp } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useEffect } from "react";

export default function Sidebar() {
  const pathname = usePathname();
  const [hoveredItem, setHoveredItem] = useState<string | null>(null);

  const navItems = [
    { name: "Dashboard", icon: Home, href: "/", badge: null },
    { name: "Calendar", icon: Calendar, href: "/calendar", badge: "GW3" },
    { name: "Squad", icon: Users, href: "/squad", badge: null },
    { name: "Watchlist", icon: Eye, href: "/watchlist", badge: "4" },
    { name: "AI Squad Builder", icon: Sparkles, href: "/builder", badge: "New" },
    { name: "Predictor", icon: BarChart3, href: "/predictor", badge: "Beta" },
    { name: "Settings", icon: Settings, href: "/settings", badge: null },
  ];

  return (
    <div className="w-72 h-screen glass-card border-r-0 rounded-none flex flex-col">
      {/* Logo Section */}
      <div className="p-8">
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-cyan-600 rounded-xl flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-accent rounded-full animate-pulse-glow"></div>
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-white to-white/80 bg-clip-text text-transparent">
              FPL AI
            </h1>
            <p className="text-xs text-gray-500">Next-Gen Assistant</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 pb-4">
        <ul className="space-y-2">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            const isHovered = hoveredItem === item.name;
            
            return (
              <li key={item.name} className="relative">
                <Link
                  href={item.href}
                  onMouseEnter={() => setHoveredItem(item.name)}
                  onMouseLeave={() => setHoveredItem(null)}
                  className={`
                    group relative flex items-center gap-3 px-4 py-3 rounded-xl
                    transition-all duration-300
                    ${isActive 
                      ? 'bg-gradient-to-r from-purple-600/20 to-cyan-600/20 text-white' 
                      : 'text-gray-400 hover:text-white hover:bg-white/5'
                    }
                  `}
                >
                  {/* Active indicator */}
                  {isActive && (
                    <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-gradient-to-b from-purple-600 to-cyan-600 rounded-r-full" />
                  )}
                  
                  {/* Icon */}
                  <div className={`
                    relative z-10 transition-transform duration-300
                    ${(isActive || isHovered) ? 'scale-110' : 'scale-100'}
                  `}>
                    <item.icon size={20} className={isActive ? 'text-white' : ''} />
                  </div>
                  
                  {/* Label */}
                  <span className="font-medium text-sm">{item.name}</span>
                  
                  {/* Badge */}
                  {item.badge && (
                    <span className={`
                      ml-auto text-xs px-2 py-1 rounded-full
                      ${item.badge === 'New' 
                        ? 'bg-gradient-to-r from-purple-600 to-cyan-600 text-white' 
                        : 'bg-white/10 text-gray-300'
                      }
                    `}>
                      {item.badge}
                    </span>
                  )}
                  
                  {/* Hover effect */}
                  {isHovered && !isActive && (
                    <div className="absolute inset-0 bg-gradient-to-r from-purple-600/10 to-cyan-600/10 rounded-xl -z-10" />
                  )}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Pro Section */}
      <div className="p-4">
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-600 to-cyan-600 p-[1px]">
          <div className="relative bg-[#12121A] rounded-2xl p-4">
            <div className="absolute top-0 right-0 w-24 h-24 bg-purple-600 rounded-full filter blur-3xl opacity-30"></div>
            <div className="relative z-10">
              <div className="flex items-center gap-2 mb-3">
                <TrendingUp size={20} className="text-purple-400" />
                <h3 className="font-semibold text-white">Upgrade to Pro</h3>
              </div>
              <p className="text-xs text-gray-400 mb-4">
                Get AI predictions, advanced analytics, and real-time insights
              </p>
              <button className="w-full py-2.5 bg-white/10 backdrop-blur-sm text-white text-sm font-medium rounded-xl hover:bg-white/20 transition-colors">
                Unlock Pro Features
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* User Section */}
      <div className="p-4 border-t border-white/5">
        <button className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-cyan-600 rounded-xl flex items-center justify-center">
            <span className="text-white font-semibold">JD</span>
          </div>
          <div className="flex-1 text-left">
            <p className="text-sm font-medium text-white">John Doe</p>
            <p className="text-xs text-gray-500">Team ID: 1234567</p>
          </div>
        </button>
      </div>
    </div>
  );
}