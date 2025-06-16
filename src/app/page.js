import Image from "next/image";

export default function Home() {
  const industries = [
    'E-commerce',
    'Travel & Hospitality',
    'Real Estate',
    'Financial Services',
    'Healthcare',
    'Food & Delivery',
    'Entertainment',
    'Automotive',
    'Education',
    'Fashion & Beauty',
    'Other'
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-indigo-50/40 to-purple-50/40 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-100/30 via-purple-100/30 to-amber-100/30"></div>
        <div className="absolute top-0 left-0 w-full h-full">
          <div className="absolute top-20 left-20 w-32 h-32 bg-gradient-to-br from-indigo-400/20 to-purple-400/20 rounded-full blur-xl"></div>
          <div className="absolute bottom-40 right-32 w-24 h-24 bg-gradient-to-br from-amber-400/20 to-orange-400/20 rounded-full blur-lg"></div>
          <div className="absolute top-1/2 right-20 w-16 h-16 bg-gradient-to-br from-emerald-400/20 to-teal-400/20 rounded-full blur-md"></div>
        </div>
        
        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="mb-6">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 border border-indigo-200/50 mb-8">
              <span className="text-sm font-semibold text-indigo-700">🚀 The Future of Commerce is Here</span>
            </div>
          </div>
          
          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-bold text-slate-900 mb-6 leading-tight">
            Bringing the <span className="gradient-text">Web</span><br />
            Where Users <span className="gradient-text">Already Are</span>
          </h1>
          
          <p className="text-xl sm:text-2xl text-slate-600 max-w-4xl mx-auto mb-8 leading-relaxed">
            The world is moving to chat agents. We're building the UI layer that makes commerce seamless inside conversations.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <a href="#demo" className="premium-gradient text-white px-8 py-4 rounded-2xl font-semibold hover:shadow-premium transition-all duration-300 transform hover:scale-105">
              Watch Demo
            </a>
            <a href="#waitlist" className="bg-white/80 backdrop-blur-sm text-slate-700 px-8 py-4 rounded-2xl font-semibold border border-slate-200 hover:border-indigo-300 transition-all duration-300 hover:shadow-lg">
              Join Early Access
            </a>
          </div>
          
          <div className="flex justify-center items-center space-x-8 text-slate-500">
            <div className="text-center">
              <div className="text-2xl font-bold text-slate-700">💬</div>
              <div className="text-sm text-slate-600">Chat Native</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-slate-700">🖱️</div>
              <div className="text-sm text-slate-600">Full UI</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-slate-700">🛍️</div>
              <div className="text-sm text-slate-600">Multi-Brand</div>
            </div>
          </div>
        </div>
      </section>

      {/* Demo Video Section */}
      <section id="demo" className="py-16 sm:py-20 lg:py-24 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-slate-900 mb-6">
              See <span className="gradient-text">UI4Chat</span> in Action
            </h2>
            <p className="text-xl text-slate-600 max-w-3xl mx-auto">
              Watch how our agent seamlessly generates a shopping interface inside a chat conversation
            </p>
          </div>

          <div className="flex justify-center">
            <div className="relative max-w-sm mx-auto bg-gradient-to-br from-slate-100 to-indigo-50 p-4 rounded-3xl shadow-premium border border-indigo-100">
              <div className="relative bg-black rounded-2xl overflow-hidden shadow-lg" style={{ aspectRatio: '9/16' }}>
                <video 
                  className="w-full h-full object-cover"
                  controls
                  autoPlay
                  muted
                  loop
                  playsInline
                  poster="/api/placeholder/300/533"
                  style={{ aspectRatio: '9/16' }}
                >
                  <source src="https://d3d9moyly3ug5v.cloudfront.net/public/demo_ui4chat.mp4" type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
                
                {/* Play button overlay */}
                <div className="absolute inset-0 flex items-center justify-center bg-black/30 opacity-0 hover:opacity-100 transition-opacity duration-300 pointer-events-none">
                  <div className="w-16 h-16 bg-white/90 rounded-full flex items-center justify-center">
                    <div className="w-0 h-0 border-l-8 border-l-slate-700 border-t-4 border-t-transparent border-b-4 border-b-transparent ml-1"></div>
                  </div>
                </div>
              </div>
              
              {/* Phone frame decoration */}
              <div className="absolute -top-2 left-1/2 transform -translate-x-1/2 w-16 h-1 bg-slate-800 rounded-full"></div>
              <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-12 h-1 bg-slate-800 rounded-full"></div>
            </div>
          </div>
          
          <div className="text-center mt-12">
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Experience commerce like never before - no app switching, no website redirects, just pure conversation-driven shopping.
            </p>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section id="learn-more" className="py-16 sm:py-20 lg:py-24" style={{ backgroundColor: '#ffffff' }}>
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-slate-900 mb-6">
              The <span className="gradient-text">Revolution</span> is Here
            </h2>
            <p className="text-xl text-slate-600 max-w-3xl mx-auto">
              MCP servers are becoming the new standard. Soon, every company will let users access their services directly through chat agents instead of outdated websites.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="bg-gradient-to-br from-red-50 to-orange-50 p-6 rounded-3xl border border-red-100">
                <div className="text-3xl mb-4">😔</div>
                <h3 className="text-xl font-bold text-slate-900 mb-3">Chat Alone Isn't Enough</h3>
                <p className="text-slate-700">People still need UI to compare, interact, and make decisions. Just not outside the conversation.</p>
              </div>
              
              <div className="bg-gradient-to-br from-amber-50 to-yellow-50 p-6 rounded-3xl border border-amber-100">
                <div className="text-3xl mb-4">🔄</div>
                <h3 className="text-xl font-bold text-slate-900 mb-3">Constant Context Switching</h3>
                <p className="text-slate-700">Users jump between chat, websites, and apps. It's fragmented and frustrating.</p>
              </div>
            </div>

            <div className="bg-gradient-to-br from-emerald-50 to-teal-50 p-8 rounded-3xl border border-emerald-100">
              <div className="text-4xl mb-6 text-center">💡</div>
              <h3 className="text-2xl font-bold text-slate-900 mb-4 text-center">Our Solution</h3>
              <p className="text-slate-700 text-center text-lg">
                We built an agent that generates a full UI inside the chat, powered with data from many companies' MCP servers.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 sm:py-20 lg:py-24 bg-gradient-to-br from-slate-50 via-indigo-50/20 to-purple-50/20">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-slate-900 mb-6">
              See It in <span className="gradient-text">Action</span>
            </h2>
            <p className="text-xl text-slate-600 max-w-3xl mx-auto">
              Imagine you're in a Telegram group chatting about replacing a sofa 🛋️
            </p>
          </div>

          <div className="space-y-8">
            <div className="bg-white/80 backdrop-blur-sm p-8 rounded-3xl shadow-premium border border-indigo-100/50">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="text-center">
                  <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-2xl flex items-center justify-center">
                    <span className="text-2xl">🎯</span>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 mb-3">Smart Detection</h3>
                  <p className="text-slate-700">Our agent detects context in your conversation and understands what you need.</p>
                </div>
                
                <div className="text-center">
                  <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-emerald-100 to-teal-100 rounded-2xl flex items-center justify-center">
                    <span className="text-2xl">🔄</span>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 mb-3">Multi-Source Fetch</h3>
                  <p className="text-slate-700">Fetches options from different brands using their own MCP servers.</p>
                </div>
                
                <div className="text-center">
                  <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-amber-100 to-orange-100 rounded-2xl flex items-center justify-center">
                    <span className="text-2xl">🖥️</span>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 mb-3">Unified Interface</h3>
                  <p className="text-slate-700">Builds one simple interface inside the chat for seamless interaction.</p>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-indigo-50 to-purple-50 p-8 rounded-3xl border border-indigo-100">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-slate-900 mb-3">🛍️ The Result</h3>
                <p className="text-lg text-slate-700 max-w-2xl mx-auto">
                  Compare sofas, interact with services from multiple companies, and buy from all of them through one unified UI. All powered by their own MCPs.
                </p>
              </div>
              
              <div className="flex justify-center space-x-8 text-slate-700">
                <div className="text-center">
                  <div className="text-xl font-semibold">❌</div>
                  <div className="text-sm">No websites</div>
                </div>
                <div className="text-center">
                  <div className="text-xl font-semibold">❌</div>
                  <div className="text-sm">No switching</div>
                </div>
                <div className="text-center">
                  <div className="text-xl font-semibold">✅</div>
                  <div className="text-sm">Pure convenience</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Vision Section */}
      <section className="py-16 sm:py-20 lg:py-24" style={{ backgroundColor: '#ffffff' }}>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="bg-gradient-to-br from-indigo-50 to-purple-50 p-8 sm:p-12 rounded-3xl border border-indigo-100">
            <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-6">
              We're Not Replacing the Web
            </h2>
            <p className="text-xl sm:text-2xl text-slate-700 mb-8 leading-relaxed">
              We're bringing it where users <span className="gradient-text font-semibold">already are</span> 💡
            </p>
            <div className="flex justify-center">
              <div className="inline-flex items-center px-6 py-3 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 border border-indigo-200/50">
                <span className="text-indigo-700 font-semibold">Built by Vincent Wargnier & Marcin Gendek</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Join Waiting List Section */}
      <section id="waitlist" className="py-12 sm:py-16 lg:py-20 bg-gradient-to-br from-slate-50 via-indigo-50/30 to-purple-50/30 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-100/20 via-purple-100/20 to-amber-100/20"></div>
        <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8 sm:mb-12">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-slate-900 mb-3 sm:mb-4">
              Join the <span className="gradient-text">Revolution</span>
            </h2>
            <p className="text-lg sm:text-xl text-slate-600 max-w-2xl mx-auto px-4">
              Be among the first to experience commerce reimagined. Get early access to UI4chat and transform how your customers shop.
            </p>
          </div>

          <div className="max-w-2xl mx-auto">
            <div className="bg-white/80 backdrop-blur-sm p-6 sm:p-8 rounded-3xl shadow-premium hover:shadow-gold transition-all duration-500 border border-indigo-100/50">
              <form action="/api/waitlist" method="POST" className="space-y-4 sm:space-y-6">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                  <div>
                    <label htmlFor="name" className="block text-sm font-semibold text-slate-700 mb-2">
                      Full Name *
                    </label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      required
                      className="w-full px-4 py-3 rounded-2xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-300 text-slate-900 bg-white/90 backdrop-blur-sm"
                      placeholder="Enter your full name"
                    />
                  </div>
                  
                  <div>
                    <label htmlFor="email" className="block text-sm font-semibold text-slate-700 mb-2">
                      Email Address *
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      required
                      className="w-full px-4 py-3 rounded-2xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-300 text-slate-900 bg-white/90 backdrop-blur-sm"
                      placeholder="Enter your email"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="industry" className="block text-sm font-semibold text-slate-700 mb-2">
                    Industry *
                  </label>
                  <select
                    id="industry"
                    name="industry"
                    required
                    className="w-full px-4 py-3 rounded-2xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-300 text-slate-900 bg-white/90 backdrop-blur-sm"
                  >
                    <option value="">Select your industry</option>
                    {industries.map((industry) => (
                      <option key={industry} value={industry}>
                        {industry}
                      </option>
                    ))}
                  </select>
                </div>

                <button
                  type="submit"
                  className="w-full premium-gradient text-white px-6 py-4 rounded-2xl font-semibold hover:shadow-premium transition-all duration-300 transform hover:scale-105"
                >
                  Join Early Access
                </button>
              </form>

              <div className="mt-6 text-center">
                <p className="text-sm text-slate-500">
                  We respect your privacy. No spam, just updates about our revolutionary platform.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
}
