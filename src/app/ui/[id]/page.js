'use client';

import { useState, useEffect } from 'react';

export default function UIDisplay({ params }) {
  const [component, setComponent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [uiId, setUiId] = useState(null);

  useEffect(() => {
    const fetchComponent = async () => {
      try {
        const { id } = await params;
        setUiId(id);
        
        // Fetch component data
        const response = await fetch(`/api/ui?id=${id}`);
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to fetch component');
        }
        const data = await response.json();
        setComponent(data);

        // Fetch current state and set it globally before executing any JavaScript
        const stateResponse = await fetch(`/api/ui/state?id=${id}`);
        if (stateResponse.ok) {
          const stateData = await stateResponse.json();
          data.currentState = stateData.state || {};
          data.lastStateUpdate = new Date(stateData.lastUpdated);
        } else {
          data.currentState = {};
          data.lastStateUpdate = new Date();
        }
        
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchComponent();
  }, [params]);

  useEffect(() => {
    if (component) {
      try {
        let jsCode = '';
        
        // Handle separate JS field
        if (component.js) {
          jsCode = component.js;
        }
        
        // Handle inline JavaScript in content field
        if (component.content) {
          const scriptRegex = /<script[^>]*>([\s\S]*?)<\/script>/gi;
          let match;
          while ((match = scriptRegex.exec(component.content)) !== null) {
            jsCode += match[1] + '\n';
          }
        }
        
        // Execute JavaScript if any exists
        if (jsCode.trim()) {
          // Add state management functions to the global scope with pre-loaded state
          const stateManagementCode = `
            // Pre-loaded state from database
            window.uiId = '${uiId}';
            window.uiState = ${JSON.stringify(component.currentState || {})};
            window.lastStateUpdate = new Date('${component.lastStateUpdate || new Date().toISOString()}');
            
            console.log('🔄 UI initialized with state:', window.uiState);
            
            window.saveState = async function(newState) {
              try {
                console.log('💾 Saving state:', newState, 'to UI ID:', window.uiId);
                window.uiState = { ...window.uiState, ...newState };
                const response = await fetch('/api/ui/state', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ id: window.uiId, state: window.uiState })
                });
                const result = await response.json();
                console.log('💾 Save response:', result);
                if (!response.ok) {
                  throw new Error(result.error || 'Save failed');
                }
                window.lastStateUpdate = new Date();
              } catch (err) {
                console.error('❌ Failed to save state:', err);
              }
            };
            
            window.getState = function(key, defaultValue = null) {
              return window.uiState && window.uiState[key] !== undefined ? window.uiState[key] : defaultValue;
            };
            
            window.syncState = async function() {
              try {
                const response = await fetch('/api/ui/state?id=' + window.uiId);
                if (response.ok) {
                  const data = await response.json();
                  const serverUpdate = new Date(data.lastUpdated);
                  
                  if (serverUpdate > window.lastStateUpdate) {
                    console.log('✨ State changed! Updating UI...');
                    window.uiState = data.state || {};
                    window.lastStateUpdate = serverUpdate;
                    
                    // Trigger state sync event for UI updates
                    if (typeof window.onStateSync === 'function') {
                      window.onStateSync(window.uiState);
                    }
                  }
                }
              } catch (err) {
                console.error('❌ Failed to sync state:', err);
              }
            };
            
            // Start polling for state changes every 2 seconds
            setInterval(window.syncState, 2000);
            
            // Auto-initialize UI with pre-loaded state
            setTimeout(() => {
              if (typeof window.onStateSync === 'function') {
                window.onStateSync(window.uiState);
              }
            }, 100);
          `;
          
          const script = document.createElement('script');
          script.textContent = stateManagementCode + '\n' + jsCode;
          document.head.appendChild(script);

          // Cleanup function to remove script on unmount
          return () => {
            if (document.head.contains(script)) {
              document.head.removeChild(script);
            }
          };
        }
      } catch (err) {
        console.error('Error executing JavaScript:', err);
      }
    }
  }, [component]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-slate-600 text-lg">Loading UI Component...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-rose-50 flex items-center justify-center">
        <div className="text-center p-8 bg-white rounded-3xl shadow-premium max-w-md mx-4">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mb-2">Component Not Found</h1>
          <p className="text-slate-600 mb-6">{error}</p>
          <button 
            onClick={() => window.location.href = '/'}
            className="premium-gradient text-white px-6 py-3 rounded-full font-semibold hover:shadow-premium transition-all duration-300"
          >
            Go Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">

      {/* Component Display Area */}
      <div className="p-4">
        <div 
          className="w-full"
          dangerouslySetInnerHTML={{ 
            __html: component.content 
              ? component.content.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '') 
              : component.html 
          }}
        />
      </div>
    </div>
  );
} 