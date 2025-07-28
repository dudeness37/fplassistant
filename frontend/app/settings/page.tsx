"use client";

import { Settings, Moon, Bell, Database, User, Key, Smartphone, Globe, HelpCircle, Zap, Shield, CreditCard } from "lucide-react";
import { useState } from "react";

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState("account");
  const [notifications, setNotifications] = useState({
    deadline: true,
    priceChanges: true,
    injuries: true,
    aiSuggestions: false,
  });

  const sections = [
    { id: "account", name: "Account", icon: User },
    { id: "notifications", name: "Notifications", icon: Bell },
    { id: "appearance", name: "Appearance", icon: Moon },
    { id: "subscription", name: "Subscription", icon: CreditCard },
    { id: "data", name: "Data & Privacy", icon: Shield },
    { id: "help", name: "Help & Support", icon: HelpCircle },
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
      {/* Sidebar Navigation */}
      <div className="lg:col-span-1">
        <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl p-4 border border-gray-800">
          <nav className="space-y-1">
            {sections.map((section) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`
                  w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300
                  ${activeSection === section.id 
                    ? 'bg-gradient-to-r from-purple-600/20 to-pink-600/20 text-white border border-purple-500/30' 
                    : 'text-gray-400 hover:text-white hover:bg-gray-800/50'
                  }
                `}
              >
                <section.icon size={20} />
                <span className="font-medium text-sm">{section.name}</span>
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Settings Content */}
      <div className="lg:col-span-3 space-y-6">
        {/* Account Section */}
        {activeSection === "account" && (
          <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl p-8 border border-gray-800">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <User className="text-purple-400" />
              Account Settings
            </h2>

            <div className="space-y-6">
              {/* Profile Picture */}
              <div className="flex items-center gap-6">
                <div className="w-20 h-20 bg-gradient-to-br from-purple-600 to-pink-600 rounded-2xl flex items-center justify-center shadow-xl">
                  <span className="text-2xl font-bold text-white">JD</span>
                </div>
                <div>
                  <button className="px-6 py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-medium rounded-xl hover:opacity-90 transition-opacity mb-2">
                    Change Avatar
                  </button>
                  <p className="text-xs text-gray-500">JPG, PNG or GIF. Max 2MB</p>
                </div>
              </div>

              {/* Form Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="text-sm font-medium text-gray-300 mb-2 block">Username</label>
                  <input
                    type="text"
                    value="john_doe_fpl"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-purple-500 transition-colors"
                    readOnly
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-300 mb-2 block">Email</label>
                  <input
                    type="email"
                    value="john@example.com"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-purple-500 transition-colors"
                    readOnly
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-300 mb-2 block">FPL Team ID</label>
                  <input
                    type="text"
                    value="1234567"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-purple-500 transition-colors"
                    readOnly
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-300 mb-2 block">Team Name</label>
                  <input
                    type="text"
                    defaultValue="John's XI"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-purple-500 transition-colors"
                  />
                </div>
              </div>

              <button className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-medium rounded-xl hover:opacity-90 transition-opacity">
                Save Changes
              </button>
            </div>
          </div>
        )}

        {/* Notifications Section */}
        {activeSection === "notifications" && (
          <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl p-8 border border-gray-800">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <Bell className="text-purple-400" />
              Notification Preferences
            </h2>

            <div className="space-y-4">
              {Object.entries(notifications).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between p-5 bg-gray-800/50 rounded-xl border border-gray-700">
                  <div>
                    <p className="font-medium text-white capitalize">
                      {key.replace(/([A-Z])/g, ' $1').trim()}
                    </p>
                    <p className="text-sm text-gray-400 mt-1">
                      {key === 'deadline' && 'Get reminded before gameweek deadlines'}
                      {key === 'priceChanges' && 'Alert when player prices are about to change'}
                      {key === 'injuries' && 'Updates on player injuries and suspensions'}
                      {key === 'aiSuggestions' && 'AI-powered transfer recommendations'}
                    </p>
                  </div>
                  <button
                    onClick={() => setNotifications({ ...notifications, [key]: !value })}
                    className={`
                      relative w-14 h-8 rounded-full transition-colors duration-300
                      ${value ? 'bg-gradient-to-r from-purple-600 to-pink-600' : 'bg-gray-700'}
                    `}
                  >
                    <div className={`
                      absolute top-1 w-6 h-6 bg-white rounded-full transition-transform duration-300 shadow-lg
                      ${value ? 'translate-x-7' : 'translate-x-1'}
                    `} />
                  </button>
                </div>
              ))}
            </div>

            {/* Connect Services */}
            <div className="mt-8 p-6 bg-gradient-to-r from-blue-600/10 to-cyan-600/10 rounded-xl border border-blue-500/20">
              <div className="flex items-center gap-3 mb-4">
                <Smartphone className="text-blue-400" size={24} />
                <h3 className="text-lg font-semibold text-white">Connect Services</h3>
              </div>
              <p className="text-sm text-gray-300 mb-4">
                Get instant notifications on your phone and never miss important updates
              </p>
              <div className="flex gap-3">
                <button className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-medium rounded-xl hover:opacity-90 transition-opacity">
                  Connect Telegram
                </button>
                <button className="px-6 py-2.5 bg-gray-800 text-white font-medium rounded-xl hover:bg-gray-700 transition-colors border border-gray-700">
                  Connect Discord
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Appearance Section */}
        {activeSection === "appearance" && (
          <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl p-8 border border-gray-800">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <Moon className="text-purple-400" />
              Appearance Settings
            </h2>

            <div className="space-y-8">
              {/* Theme Selection */}
              <div>
                <h3 className="text-lg font-semibold text-white mb-4">Theme</h3>
                <div className="grid grid-cols-3 gap-4">
                  {['Dark', 'Light', 'Auto'].map((theme) => (
                    <button
                      key={theme}
                      className={`
                        p-6 rounded-xl border-2 transition-all bg-gray-800/50
                        ${theme === 'Dark' 
                          ? 'border-purple-500 bg-purple-500/10' 
                          : 'border-gray-700 hover:border-gray-600'
                        }
                      `}
                    >
                      <div className={`
                        w-full h-24 rounded-lg mb-3
                        ${theme === 'Dark' && 'bg-gradient-to-b from-gray-800 to-gray-900'}
                        ${theme === 'Light' && 'bg-gradient-to-b from-gray-100 to-white'}
                        ${theme === 'Auto' && 'bg-gradient-to-r from-gray-800 to-white'}
                      `} />
                      <p className="text-sm font-medium text-white">{theme}</p>
                    </button>
                  ))}
                </div>
              </div>

              {/* Accent Color */}
              <div>
                <h3 className="text-lg font-semibold text-white mb-4">Accent Color</h3>
                <div className="flex gap-3">
                  {[
                    'from-purple-600 to-pink-600',
                    'from-blue-600 to-cyan-600',
                    'from-green-600 to-emerald-600',
                    'from-orange-600 to-red-600',
                    'from-indigo-600 to-purple-600'
                  ].map((gradient, idx) => (
                    <button
                      key={idx}
                      className={`
                        w-12 h-12 rounded-xl bg-gradient-to-br ${gradient}
                        ring-2 ring-offset-2 ring-offset-gray-900
                        ${idx === 0 ? 'ring-white/50' : 'ring-transparent hover:ring-white/30'}
                        transition-all
                      `}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Subscription Section */}
        {activeSection === "subscription" && (
          <div className="space-y-6">
            {/* Current Plan */}
            <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl p-8 border border-gray-800">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white flex items-center gap-3">
                  <CreditCard className="text-purple-400" />
                  Subscription
                </h2>
                <span className="px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white text-sm font-medium rounded-full">
                  PRO ACTIVE
                </span>
              </div>

              <div className="p-6 bg-gradient-to-r from-purple-600/10 to-pink-600/10 rounded-xl border border-purple-500/20">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-white">FPL AI Pro</h3>
                    <p className="text-sm text-gray-400">Next billing date: January 15, 2025</p>
                  </div>
                  <p className="text-2xl font-bold text-white">£9.99<span className="text-sm text-gray-400">/mo</span></p>
                </div>
                <div className="flex gap-3">
                  <button className="px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors">
                    Change Plan
                  </button>
                  <button className="px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors">
                    Cancel Subscription
                  </button>
                </div>
              </div>
            </div>

            {/* Features */}
            <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl p-8 border border-gray-800">
              <h3 className="text-lg font-semibold text-white mb-4">Pro Features</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  'AI Transfer Predictions',
                  'Advanced Analytics',
                  'Price Change Alerts',
                  'Unlimited Watchlist',
                  'Custom Notifications',
                  'Priority Support'
                ].map((feature, idx) => (
                  <div key={idx} className="flex items-center gap-3">
                    <div className="w-5 h-5 rounded-full bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center">
                      <Zap size={12} className="text-white" />
                    </div>
                    <span className="text-gray-300">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Data & Privacy Section */}
        {activeSection === "data" && (
          <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl p-8 border border-gray-800">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <Shield className="text-purple-400" />
              Data & Privacy
            </h2>

            <div className="space-y-6">
              <div className="p-6 bg-gray-800/50 rounded-xl border border-gray-700">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="font-semibold text-white">Sync with FPL</h3>
                    <p className="text-sm text-gray-400">Last synced: 2 hours ago</p>
                  </div>
                  <button className="px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:opacity-90 transition-opacity">
                    Sync Now
                  </button>
                </div>
              </div>

              <div className="p-6 bg-gray-800/50 rounded-xl border border-gray-700">
                <h3 className="font-semibold text-white mb-4">Export Data</h3>
                <p className="text-sm text-gray-400 mb-4">Download your FPL data and analysis history</p>
                <div className="flex gap-3">
                  <button className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors">
                    Export CSV
                  </button>
                  <button className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors">
                    Export JSON
                  </button>
                </div>
              </div>

              <div className="p-6 bg-gray-800/50 rounded-xl border border-gray-700">
                <h3 className="font-semibold text-white mb-4">Delete Account</h3>
                <p className="text-sm text-gray-400 mb-4">Permanently delete your account and all associated data</p>
                <button className="px-4 py-2 bg-red-600/20 text-red-400 rounded-lg hover:bg-red-600/30 transition-colors border border-red-600/50">
                  Delete Account
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Help & Support Section */}
        {activeSection === "help" && (
          <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl p-8 border border-gray-800">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <HelpCircle className="text-purple-400" />
              Help & Support
            </h2>

            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button className="p-6 bg-gray-800/50 rounded-xl border border-gray-700 hover:border-purple-500/50 transition-all text-left">
                  <Globe className="w-8 h-8 text-purple-400 mb-3" />
                  <h3 className="font-semibold text-white mb-1">Documentation</h3>
                  <p className="text-sm text-gray-400">Browse our comprehensive guides</p>
                </button>
                <button className="p-6 bg-gray-800/50 rounded-xl border border-gray-700 hover:border-purple-500/50 transition-all text-left">
                  <Smartphone className="w-8 h-8 text-purple-400 mb-3" />
                  <h3 className="font-semibold text-white mb-1">Contact Support</h3>
                  <p className="text-sm text-gray-400">Get help from our team</p>
                </button>
              </div>

              <div className="p-6 bg-gray-800/50 rounded-xl border border-gray-700">
                <h3 className="font-semibold text-white mb-4">Frequently Asked Questions</h3>
                <div className="space-y-3">
                  <details className="group">
                    <summary className="cursor-pointer text-gray-300 hover:text-white transition-colors">
                      How do I connect my FPL account?
                    </summary>
                    <p className="mt-2 text-sm text-gray-400 pl-4">
                      Go to Settings → Account and enter your FPL Team ID to sync your data.
                    </p>
                  </details>
                  <details className="group">
                    <summary className="cursor-pointer text-gray-300 hover:text-white transition-colors">
                      What features are included in Pro?
                    </summary>
                    <p className="mt-2 text-sm text-gray-400 pl-4">
                      Pro includes AI predictions, advanced analytics, price alerts, and more.
                    </p>
                  </details>
                  <details className="group">
                    <summary className="cursor-pointer text-gray-300 hover:text-white transition-colors">
                      How accurate are the AI predictions?
                    </summary>
                    <p className="mt-2 text-sm text-gray-400 pl-4">
                      Our AI has 85% accuracy based on historical data and real-time analysis.
                    </p>
                  </details>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}