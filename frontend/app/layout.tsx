import "./../styles/globals.css";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

export const metadata = {
  title: 'FPL AI - Next Generation Fantasy Assistant',
  description: 'AI-powered FPL assistant with real-time insights and predictions',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="relative min-h-screen bg-[#0A0A0F]">
          {/* Animated gradient background */}
          <div className="fixed inset-0 overflow-hidden">
            <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
            <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-cyan-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-600 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float" style={{ animationDelay: '4s' }}></div>
          </div>

          {/* Main Layout */}
          <div className="relative z-10 flex h-screen">
            {/* Sidebar */}
            <Sidebar />
            
            {/* Content Area */}
            <div className="flex-1 flex flex-col">
              {/* Topbar */}
              <Topbar />
              
              {/* Page Content with Parallax */}
              <main className="flex-1 overflow-y-auto overflow-x-hidden">
                <div className="relative">
                  {/* Parallax Background Elements */}
                  <div className="parallax-container absolute inset-0 pointer-events-none">
                    <div className="parallax-layer opacity-5">
                      <div className="absolute top-20 left-20 w-64 h-64 border border-white/10 rounded-full"></div>
                      <div className="absolute bottom-40 right-40 w-96 h-96 border border-white/10 rounded-full"></div>
                    </div>
                  </div>
                  
                  {/* Content */}
                  <div className="relative z-10 p-8 max-w-[1400px] mx-auto">
                    {children}
                  </div>
                </div>
              </main>
            </div>
          </div>
        </div>
      </body>
    </html>
  );
}