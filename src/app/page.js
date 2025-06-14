import Image from "next/image";

export default function Home() {
  const industries = [
    'Technology',
    'Healthcare',
    'Finance',
    'E-commerce',
    'Education',
    'Manufacturing',
    'Real Estate',
    'Media & Entertainment',
    'Government',
    'Non-profit',
    'Other'
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="fixed top-0 w-full z-50 glass border-b border-white/10 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-14 sm:h-16">
            <div className="flex items-center">
              <div className="text-lg sm:text-2xl font-bold gradient-text">mcpmyapi.com</div>
            </div>
            <nav className="hidden md:flex space-x-6 lg:space-x-8">
              <a href="#features" className="text-slate-700 hover:text-indigo-600 transition-all duration-300 font-medium text-sm lg:text-base">Features</a>
              <a href="#how-it-works" className="text-slate-700 hover:text-indigo-600 transition-all duration-300 font-medium text-sm lg:text-base">How it Works</a>
              <a href="#pricing" className="text-slate-700 hover:text-indigo-600 transition-all duration-300 font-medium text-sm lg:text-base">Pricing</a>
            </nav>
            <div className="flex items-center space-x-2 sm:space-x-4">
              <button className="premium-gradient text-white px-4 py-2 sm:px-6 sm:py-2 rounded-full hover:shadow-premium transition-all duration-300 font-semibold text-sm sm:text-base transform hover:scale-105">
                Get Started
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-16 sm:pt-20 lg:pt-24 pb-12 sm:pb-16 lg:pb-20 hero-gradient relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/30 via-purple-900/30 to-violet-900/30"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="animate-float">
            <h1 className="text-3xl sm:text-5xl lg:text-7xl font-bold text-white mb-4 sm:mb-6 leading-tight">
              Transform Your APIs into
              <span className="block bg-gradient-to-r from-amber-400 via-orange-400 to-yellow-400 bg-clip-text text-transparent mt-2">
                MCP Servers
              </span>
            </h1>
          </div>
          <p className="text-base sm:text-xl lg:text-2xl text-white/90 mb-6 sm:mb-8 max-w-3xl mx-auto leading-relaxed px-4">
            Seamlessly convert your APIs into MCP servers. Run directly on your servers or use our SaaS platform with FastAPI integration.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center items-center mb-8 sm:mb-12 px-4">
            <button className="w-full sm:w-auto bg-white text-indigo-600 px-6 sm:px-8 py-3 sm:py-4 rounded-full font-semibold hover:bg-gray-50 transition-all transform hover:scale-105 shadow-premium hover:shadow-gold duration-300">
              Download FastAPI Package
            </button>
            <button className="w-full sm:w-auto glass text-white px-6 sm:px-8 py-3 sm:py-4 rounded-full font-semibold hover:bg-white/20 transition-all border border-white/20 hover:border-white/40 duration-300">
              Try SaaS Platform
            </button>
          </div>
          <div className="text-center">
            <div className="inline-flex items-center gold-gradient text-white px-4 sm:px-6 py-2 sm:py-3 rounded-full font-bold text-sm sm:text-lg animate-pulse-slow shadow-gold hover:shadow-xl transition-all duration-300">
              ✨ COMING SOON
            </div>
          </div>
        </div>
        
        {/* Premium Floating Elements */}
        <div className="absolute top-20 left-4 sm:left-10 w-12 sm:w-20 h-12 sm:h-20 bg-indigo-400/20 rounded-full animate-float blur-sm"></div>
        <div className="absolute top-32 sm:top-40 right-4 sm:right-20 w-10 sm:w-16 h-10 sm:h-16 bg-purple-400/20 rounded-full animate-float blur-sm" style={{animationDelay: '2s'}}></div>
        <div className="absolute bottom-16 sm:bottom-20 left-1/4 w-8 sm:w-12 h-8 sm:h-12 bg-amber-400/20 rounded-full animate-float blur-sm" style={{animationDelay: '4s'}}></div>
        <div className="absolute top-1/2 right-1/4 w-6 sm:w-8 h-6 sm:h-8 bg-violet-400/20 rounded-full animate-float blur-sm" style={{animationDelay: '1s'}}></div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-12 sm:py-16 lg:py-20 bg-gradient-to-br from-slate-50 to-indigo-50/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-slate-900 mb-3 sm:mb-4">
              Why Choose <span className="gradient-text">mcpmyapi.com</span>?
            </h2>
            <p className="text-lg sm:text-xl text-slate-600 max-w-3xl mx-auto px-4">
              The fastest and most reliable way to transform your existing APIs into powerful MCP servers
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
            <div className="bg-white/80 backdrop-blur-sm p-6 sm:p-8 rounded-3xl shadow-premium hover:shadow-gold transition-all duration-500 border border-indigo-100/50 group transform hover:-translate-y-2">
              <div className="w-12 sm:w-16 h-12 sm:h-16 premium-gradient rounded-2xl flex items-center justify-center mb-4 sm:mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                <svg className="w-6 sm:w-8 h-6 sm:h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mb-3 sm:mb-4">Lightning Fast</h3>
              <p className="text-slate-600 leading-relaxed text-sm sm:text-base">
                Convert your APIs in seconds, not hours. Our automated system handles the heavy lifting while you focus on building.
              </p>
            </div>
            
            <div className="bg-white/80 backdrop-blur-sm p-6 sm:p-8 rounded-3xl shadow-premium hover:shadow-gold transition-all duration-500 border border-purple-100/50 group transform hover:-translate-y-2">
              <div className="w-12 sm:w-16 h-12 sm:h-16 bg-gradient-to-br from-purple-600 to-violet-600 rounded-2xl flex items-center justify-center mb-4 sm:mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                <svg className="w-6 sm:w-8 h-6 sm:h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mb-3 sm:mb-4">Secure & Reliable</h3>
              <p className="text-slate-600 leading-relaxed text-sm sm:text-base">
                Enterprise-grade security with your credentials safely managed. Run on your infrastructure or ours.
              </p>
            </div>
            
            <div className="bg-white/80 backdrop-blur-sm p-6 sm:p-8 rounded-3xl shadow-premium hover:shadow-gold transition-all duration-500 border border-amber-100/50 group transform hover:-translate-y-2">
              <div className="w-12 sm:w-16 h-12 sm:h-16 gold-gradient rounded-2xl flex items-center justify-center mb-4 sm:mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                <svg className="w-6 sm:w-8 h-6 sm:h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
              <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mb-3 sm:mb-4">Developer Friendly</h3>
              <p className="text-slate-600 leading-relaxed text-sm sm:text-base">
                Simple FastAPI integration with comprehensive documentation. Get started in minutes, not days.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-12 sm:py-16 lg:py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-slate-900 mb-3 sm:mb-4">
              How It <span className="gradient-text">Works</span>
            </h2>
            <p className="text-lg sm:text-xl text-slate-600 max-w-3xl mx-auto px-4">
              Three simple ways to get your APIs running as MCP servers
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-center">
            <div className="space-y-6 sm:space-y-8 order-2 lg:order-1">
              <div className="flex items-start space-x-3 sm:space-x-4 group">
                <div className="w-10 sm:w-12 h-10 sm:h-12 premium-gradient text-white rounded-full flex items-center justify-center font-bold text-base sm:text-lg shadow-premium group-hover:scale-110 transition-all duration-300 flex-shrink-0">1</div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mb-2">FastAPI Package</h3>
                  <p className="text-slate-600 leading-relaxed text-sm sm:text-base">
                    Download our FastAPI package and integrate it directly into your existing codebase. Full control, runs on your infrastructure.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3 sm:space-x-4 group">
                <div className="w-10 sm:w-12 h-10 sm:h-12 bg-gradient-to-br from-purple-600 to-violet-600 text-white rounded-full flex items-center justify-center font-bold text-base sm:text-lg shadow-premium group-hover:scale-110 transition-all duration-300 flex-shrink-0">2</div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mb-2">Swagger Scraping</h3>
                  <p className="text-slate-600 leading-relaxed text-sm sm:text-base">
                    Provide your Swagger/OpenAPI documentation and we'll automatically generate your MCP server configuration.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3 sm:space-x-4 group">
                <div className="w-10 sm:w-12 h-10 sm:h-12 gold-gradient text-white rounded-full flex items-center justify-center font-bold text-base sm:text-lg shadow-gold group-hover:scale-110 transition-all duration-300 flex-shrink-0">3</div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mb-2">SaaS Platform</h3>
                  <p className="text-slate-600 leading-relaxed text-sm sm:text-base">
                    Use our cloud platform to manage environment variables, credentials, and run your MCP servers seamlessly.
                  </p>
                </div>
              </div>
            </div>
            
            <div className="relative order-1 lg:order-2">
              <div className="bg-gradient-to-br from-indigo-50 via-purple-50 to-amber-50 p-6 sm:p-8 rounded-3xl shadow-premium hover:shadow-gold transition-all duration-500 transform hover:-translate-y-1">
                <div className="bg-white/90 backdrop-blur-sm p-4 sm:p-6 rounded-2xl shadow-lg mb-4 border border-indigo-100 hover:border-indigo-200 transition-all duration-300">
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="w-2 sm:w-3 h-2 sm:h-3 bg-red-500 rounded-full"></div>
                    <div className="w-2 sm:w-3 h-2 sm:h-3 bg-amber-500 rounded-full"></div>
                    <div className="w-2 sm:w-3 h-2 sm:h-3 bg-green-500 rounded-full"></div>
                  </div>
                  <div className="space-y-2">
                    <div className="h-2 sm:h-3 bg-slate-200 rounded w-3/4"></div>
                    <div className="h-2 sm:h-3 bg-indigo-200 rounded w-1/2"></div>
                    <div className="h-2 sm:h-3 bg-slate-200 rounded w-5/6"></div>
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-2xl sm:text-4xl mb-2">⚡</div>
                  <p className="text-slate-700 font-semibold text-sm sm:text-base">Your API → MCP Server</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 sm:py-16 lg:py-20 premium-gradient relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/20 via-purple-900/20 to-violet-900/20"></div>
        <div className="relative max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-4 sm:mb-6">
            Ready to Transform Your APIs?
          </h2>
          <p className="text-lg sm:text-xl text-white/90 mb-6 sm:mb-8 leading-relaxed">
            Join thousands of developers who are already using mcpmyapi.com to power their applications
          </p>
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
            <button className="w-full sm:w-auto bg-white text-indigo-600 px-6 sm:px-8 py-3 sm:py-4 rounded-full font-semibold hover:bg-gray-50 transition-all transform hover:scale-105 shadow-premium hover:shadow-gold duration-300">
              Get Early Access
            </button>
            <button className="w-full sm:w-auto glass text-white px-6 sm:px-8 py-3 sm:py-4 rounded-full font-semibold hover:bg-white/20 transition-all border border-white/20 hover:border-white/40 duration-300">
              View Documentation
            </button>
          </div>
        </div>
      </section>

      {/* Join Waiting List Section */}
      <section id="waitlist" className="py-12 sm:py-16 lg:py-20 bg-gradient-to-br from-slate-50 via-indigo-50/30 to-purple-50/30 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-100/20 via-purple-100/20 to-amber-100/20"></div>
        <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8 sm:mb-12">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-slate-900 mb-3 sm:mb-4">
              Join the <span className="gradient-text">Waiting List</span>
            </h2>
            <p className="text-lg sm:text-xl text-slate-600 max-w-2xl mx-auto px-4">
              Be the first to know when mcpmyapi.com launches. Get early access and exclusive updates.
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
                  Join Waiting List
                </button>
              </form>

              <div className="mt-6 text-center">
                <p className="text-sm text-slate-500">
                  We respect your privacy. No spam, just updates about our launch.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-white py-12 sm:py-16 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-indigo-900/50 to-purple-900/30"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
            <div className="col-span-1 sm:col-span-2">
              <div className="text-xl sm:text-2xl font-bold gradient-text mb-3 sm:mb-4">mcpmyapi.com</div>
              <p className="text-slate-400 mb-4 sm:mb-6 max-w-md text-sm sm:text-base">
                The fastest way to transform your APIs into MCP servers. Built for developers, by developers.
              </p>
              <div className="flex space-x-4">
                <a href="#" className="text-slate-400 hover:text-amber-400 transition-all duration-300 transform hover:scale-110">
                  <svg className="w-5 sm:w-6 h-5 sm:h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                  </svg>
                </a>
                <a href="#" className="text-slate-400 hover:text-amber-400 transition-all duration-300 transform hover:scale-110">
                  <svg className="w-5 sm:w-6 h-5 sm:h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.174-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.099.12.112.225.085.345-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.402.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.357-.629-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24.009 12.017 24.009c6.624 0 11.99-5.367 11.99-11.988C24.007 5.367 18.641.001.012.001z"/>
                  </svg>
                </a>
                <a href="#" className="text-slate-400 hover:text-amber-400 transition-all duration-300 transform hover:scale-110">
                  <svg className="w-5 sm:w-6 h-5 sm:h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12.007 0C5.383 0 .007 5.376.007 12s5.376 12 12 12 12-5.376 12-12S18.631.007 12.007.007zM8.442 18.664c-4.664 0-7.348-3.71-7.348-6.912 0-.576.043-1.152.129-1.705C2.498 6.842 6.505 4.807 12.007 4.807c2.133 0 4.096.576 5.616 1.536l-2.304 2.218c-.662-.384-1.459-.576-2.304-.576-2.133 0-3.84 1.728-3.84 3.84s1.707 3.84 3.84 3.84c1.92 0 3.326-1.344 3.67-3.072h-3.67v-2.88h6.912c.086.48.129.96.129 1.536 0 5.184-3.456 8.832-8.832 8.832z"/>
                  </svg>
                </a>
              </div>
            </div>
            
            <div>
              <h3 className="text-base sm:text-lg font-semibold mb-3 sm:mb-4 text-white">Product</h3>
              <ul className="space-y-2 text-slate-400 text-sm sm:text-base">
                <li><a href="#" className="hover:text-amber-400 transition-all duration-300">Features</a></li>
                <li><a href="#" className="hover:text-amber-400 transition-all duration-300">Pricing</a></li>
                <li><a href="#" className="hover:text-amber-400 transition-all duration-300">Documentation</a></li>
                <li><a href="#" className="hover:text-amber-400 transition-all duration-300">API Reference</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-base sm:text-lg font-semibold mb-3 sm:mb-4 text-white">Company</h3>
              <ul className="space-y-2 text-slate-400 text-sm sm:text-base">
                <li><a href="#" className="hover:text-amber-400 transition-all duration-300">About</a></li>
                <li><a href="#" className="hover:text-amber-400 transition-all duration-300">Blog</a></li>
                <li><a href="#" className="hover:text-amber-400 transition-all duration-300">Careers</a></li>
                <li><a href="#" className="hover:text-amber-400 transition-all duration-300">Contact</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-slate-700 mt-8 sm:mt-12 pt-6 sm:pt-8 text-center text-slate-400 text-sm sm:text-base">
            <p>&copy; 2024 mcpmyapi.com. All rights reserved. Coming Soon.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
