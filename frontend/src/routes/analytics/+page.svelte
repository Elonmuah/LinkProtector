<script>
  import { onMount } from "svelte";
  import { API_BASE } from '$lib/env';

  let message = "";
  let noUserURLs = false;
  let userData = [];

  onMount(async () => {
  try {
    const res = await fetch(`${API_BASE}/api/getUserUrls`, {
      method: "POST"
    });
    const data = await res.json();

    if (data.error === 1) {
      message = "You have no urls protected yet...";
      noUserURLs = true;
    } else {
      message = "Your Protected URLs";
      noUserURLs = false;
      userData = data.IDs.map((id, i) => ({
        ID: id,
        URL: data.URLs[i],
        title: data.titles[i].replace(" ", "-") || `URL ${id}`,
        token: data.tokens[i]
      }));
    }
  } catch (err) {
    console.error("Fetch failed:", err);
    message = "Could not connect to backend" + err;
    noUserURLs = true;
  }
});
</script>

<!-- Consistent site padding – use this everywhere! -->
<section class="w-full py-16 px-4 sm:px-6 lg:px-8">
  <div class="max-w-7xl mx-auto">

    <h1 class="text-4xl font-bold text-white text-center mb-12">
      {message || "Loading..."}
    </h1>

    {#if noUserURLs}
      <div class="flex justify-center">
        <a href="/protect">
          <button class="relative px-10 py-4 rounded-2xl font-bold text-white
                         bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500
                         shadow-2xl shadow-purple-500/40 hover:shadow-purple-500/60
                         hover:scale-105 transition-all duration-300 backdrop-blur-md
                         border border-white/20 text-lg">
            Start Protecting URLs Now
          </button>
        </a>
      </div>
    {:else}
      <div class="space-y-8">
        {#each userData as data}
          <div class="bg-slate-800/70 backdrop-blur-xl border border-slate-700/50 
                      rounded-2xl p-8 shadow-2xl shadow-slate-950/40
                      transition-all duration-300 hover:border-purple-500/40 hover:shadow-purple-500/20">
            
            <div class="flex items-center justify-between mb-6">
              <span class="text-lg font-semibold text-slate-300">URL #{data.ID}</span>
            </div>

            <div class="space-y-6">
              <h2 class="text-2xl font-bold text-white leading-tight">
                {data.title}
              </h2>

              <p class="text-slate-400">
                <span class="font-mono text-sm bg-slate-700/60 px-5 py-3 rounded-xl 
                             border border-slate-600/50 block break-all">
                  {data.URL}
                </span>
              </p>
            </div>

            <div class="mt-8">
              <a href="/analytics/{encodeURIComponent(data.title)}?token={data.token}">
                <button class="w-full py-4 px-8 bg-gradient-to-r from-indigo-600 to-purple-700 
                                text-white font-semibold rounded-xl shadow-lg
                                hover:shadow-indigo-500/30 hover:scale-105 
                                transition-all duration-300 text-base">
                  See Analytics →
                </button>
              </a>
            </div>
          </div>
        {/each}
      </div>
    {/if}

  </div>
</section>