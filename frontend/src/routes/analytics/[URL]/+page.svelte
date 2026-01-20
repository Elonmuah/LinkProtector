<script>
  import { onMount } from "svelte";

  let currentURL = "";
  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");

  onMount(() =>{
    const url = new URL(window.location.href);
    
    // Remove the token parameter
    url.searchParams.delete("token");
    
    // Convert back to clean string (without ?token=...)
    currentURL = url.toString();

    // Optional: remove trailing ? or & if nothing else is left
    currentURL = currentURL.replace(/[?&]$/, '');
  });
</script>

<section class="w-full py-12 px-4 sm:px-6 lg:px-8">
  <div class="max-w-7xl mx-auto">

    <h1 class="text-3xl font-bold text-white text-center mb-12">
      Your Analytics Dashboard
    </h1>

    <!-- PERFECTLY EQUAL HEIGHT GRID -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 auto-rows-fr">
      <!-- auto-rows-fr = every row has the same height based on the tallest card -->

      <!-- 1. Clicks Over Time -->
      <a href="{currentURL}/clicks?token={token}" class="group block">
        <div class="h-full relative bg-slate-800/70 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-8 
                    shadow-2xl shadow-slate-950/40 overflow-hidden
                    transition-all duration-300 
                    hover:scale-[1.02] hover:shadow-purple-500/20 hover:border-purple-500/40">
          <div class="absolute inset-0 bg-gradient-to-br from-purple-600/10 to-indigo-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          
          <div class="relative z-10 flex flex-col h-full">
            <h3 class="text-2xl font-bold text-white mb-3">Clicks Over Time</h3>
            <p class="text-slate-400 mb-8">Track daily, weekly, and monthly trends</p>
            
            <div class="flex-1 flex items-end justify-center mb-6">
              <div class="w-full h-32 bg-gradient-to-r from-transparent via-purple-500/20 to-transparent rounded-lg flex items-end justify-between px-4 pb-4">
                {#each [20, 45, 30, 70, 55, 90, 75] as height}
                  <div 
                    class="w-8 bg-gradient-to-t from-purple-500 to-indigo-400 rounded-t-full transition-all duration-700 group-hover:h-[calc({height}%+10%)]"
                    style="height: {height}%"
                  ></div>
                {/each}
              </div>
            </div>
            
            <div class="text-right">
              <span class="inline-flex items-center gap-2 text-indigo-400 font-medium text-sm group-hover:text-indigo-300">
                View Details
                <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </span>
            </div>
          </div>
        </div>
      </a>

      <!-- 2. Redirect Success Rate -->
      <a href="/analytics/success-rate" class="group block">
        <div class="h-full relative bg-slate-800/70 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-8 
                    shadow-2xl shadow-slate-950/40 overflow-hidden
                    transition-all duration-300 
                    hover:scale-[1.02] hover:shadow-emerald-500/20 hover:border-emerald-500/40">
          <div class="absolute inset-0 bg-gradient-to-br from-emerald-600/10 to-cyan-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          
          <div class="relative z-10 flex flex-col h-full justify-between">
            <div>
              <h3 class="text-2xl font-bold text-white mb-3">Redirect Success Rate</h3>
              <p class="text-slate-400 mb-8">Successful vs blocked/hijacked attempts</p>
            </div>
            
            <div class="flex justify-center items-center flex-1">
              <div class="w-40 h-40 rounded-full bg-gradient-to-tr from-emerald-500 to-cyan-400 p-2">
                <div class="w-full h-full rounded-full bg-slate-800/90 flex items-center justify-center">
                  <span class="text-4xl font-bold text-emerald-400">94%</span>
                </div>
              </div>
            </div>
            
            <div class="text-right mt-6">
              <span class="inline-flex items-center gap-2 text-emerald-400 font-medium text-sm group-hover:text-emerald-300">
                View Details
                <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </span>
            </div>
          </div>
        </div>
      </a>

      <!-- 3. Money Saved -->
      <a href="/analytics/money-saved" class="group block">
        <div class="h-full relative bg-slate-800/70 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-8 
                    shadow-2xl shadow-slate-950/40 overflow-hidden
                    transition-all duration-300 
                    hover:scale-[1.02] hover:shadow-cyan-500/20 hover:border-cyan-500/40">
          <div class="absolute inset-0 bg-gradient-to-br from-cyan-600/10 to-blue-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
          
          <div class="relative z-10 flex flex-col h-full justify-between">
            <div>
              <h3 class="text-2xl font-bold text-white mb-3">Money Saved</h3>
              <p class="text-slate-400 mb-8">Commission protected from hijackers</p>
            </div>
            
            <div class="text-center flex-1 flex flex-col justify-center">
              <span class="text-5xl font-bold text-cyan-400">$11,420</span>
              <p class="text-slate-500 text-sm mt-2">This month</p>
            </div>
            
            <div class="text-right mt-6">
              <span class="inline-flex items-center gap-2 text-cyan-400 font-medium text-sm group-hover:text-cyan-300">
                View Breakdown
                <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </span>
            </div>
          </div>
        </div>
      </a>

      <!-- 4. Top Traffic Sources -->
      <a href="/analytics/traffic-sources" class="group block">
        <div class="h-full relative bg-slate-800/70 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-8 
                    shadow-2xl shadow-slate-950/40 overflow-hidden
                    transition-all duration-300 
                    hover:scale-[1.02] hover:shadow-violet-500/20 hover:border-violet-500/40">
          <div class="absolute inset-0 bg-gradient-to-br from-violet-600/10 to-purple-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
          
          <div class="relative z-10 flex flex-col h-full">
            <h3 class="text-2xl font-bold text-white mb-3">Top Traffic Sources</h3>
            <p class="text-slate-400 mb-8">Where your clicks are coming from</p>
            
            <div class="flex-1 space-y-4">
              {#each ["YouTube", "Twitter/X", "Instagram", "TikTok", "Discord"] as source, i}
                <div class="flex items-center justify-between">
                  <span class="text-slate-300 text-sm">{source}</span>
                  <div class="w-32 bg-slate-700 rounded-full h-3">
                    <div class="bg-gradient-to-r from-violet-500 to-purple-500 h-full rounded-full transition-all duration-500 group-hover:scale-x-110" 
                         style="width: {90 - i * 12}%"></div>
                  </div>
                </div>
              {/each}
            </div>
            
            <div class="text-right mt-6">
              <span class="inline-flex items-center gap-2 text-violet-400 font-medium text-sm group-hover:text-violet-300">
                View All Sources
                <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </span>
            </div>
          </div>
        </div>
      </a>

    </div>
  </div>
</section>