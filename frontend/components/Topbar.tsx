"use client";

import { Search, Bell, RefreshCw, Zap, Clock, ChevronDown } from "lucide-react";
import { useState, useEffect } from "react";
import { usePathname } from "next/navigation";

export default function Topbar() {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const pathname = usePathname();
  
  const pageConfig = {
    '/': { title: 'Dashboard', subtitle: 'Track your FPL performance' },
    '/calendar': { title: 'Fixture Calendar', subtitle: 'Plan your transfers ahead' },
    '/squad': { title: 'My Squad', subtitle: 'Manage your team' },
    '/watchlist': { title: 'Player Watchlist', subtitle: 'Monitor key targets' },
    '/preseason': { title: 'Squad Builder', subtitle: 'AI-powered team creation' },
    '/settings': { title: 'Settings', subtitle: 'Customize your experience' },
  }[pathname] || { title: 'Dashboard', subtitle: '' };

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 1000);
  };

  return (
    <header className="glass-card border-x-0 border-t-0 rounded-none px-8 py-6">
      <div className="flex items-center justify-between">
        {/* Left Section */}
        <div className="flex-1">
          <div className="animate-slide-up">
            <h1 className="text-2xl font-bold text-white mb-1">{pageConfig.title}</h1>
            <p className="text-sm text-gray-500">{pageConfig.subtitle}</p>
          </div>
        </div>

        {/* Center - Live Status */}
        <div className="hidden lg:flex items-center gap-6 animate-fade-in">
          <div className="flex items-center gap-3 px-4 py-2 bg-white/5 rounded-xl">
            <Clock size={16} className="text-gray-400" />
            <div className="text-sm">
              <span className="text-gray-500">GW3 Deadline: </span>
              <span className="font-medium gradient-text">12d 6h 42m</span>
            </div>
          </div>
          
          <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-600/20 to-cyan-600/20 rounded-xl border border-purple-600/30">
            <Zap size={16} className="text-purple-400" />
            <span className="text-sm font-medium text-purple-300">AI Active</span>
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-4">
          {/* Search */}
          <div className="relative hidden lg:block">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
            <input
              type="text"
              placeholder="Search players..."
              className="input pl-10 w-64 bg-white/5 border-white/10 placeholder-gray-600 focus:bg-white/10"
            />
          </div>

          {/* Actions */}
          <button
            onClick={handleRefresh}
            className={`
              p-3 glass-card hover:bg-white/5 transition-all
              ${isRefreshing ? 'animate-spin' : ''}
            `}
          >
            <RefreshCw size={18} className="text-gray-400" />
          </button>

          <button className="relative p-3 glass-card hover:bg-white/5 transition-all">
            <Bell size={18} className="text-gray-400" />
            <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
          </button>

          {/* Profile */}
          <button className="flex items-center gap-3 pl-3 pr-4 py-2 glass-card hover:bg-white/5 transition-all">
            <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-cyan-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-sm font-semibold">JD</span>
            </div>
            <ChevronDown size={16} className="text-gray-400" />
          </button>
        </div>
      </div>
    </header>
  );
}