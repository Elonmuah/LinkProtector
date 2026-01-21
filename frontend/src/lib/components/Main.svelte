<script>
  import { API_BASE } from '$lib/env';
  import HelpTool from '$lib/components/HelpTool.svelte';

  let userInputUrl = "";
  let responseMessage = "";
  let responseStatus = 0;
  let responseErrorCode = null;     // ← moved here + fixed typo + null instead of undefined

  async function submitForm() {
    try {
      const res = await fetch(`${API_BASE}/api/buttonClick`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: userInputUrl,
        })
      });

      const data = await res.json();

      responseStatus = data.error;
      responseMessage = data.message;

      if (responseStatus === 1) {
        responseErrorCode = data.errorCode;
      } else {
        responseErrorCode = null;
      }
    } catch (err) {
      responseStatus = 1;
      responseMessage = "Network error - please check your connection";
      console.error(err);
    }
  }
</script>

<div class="text-center justify-center flex flex-col items-center px-4 py-20" id="mainBlock">
  <!-- Heading -->
  <div>
    <p
      class="text-4xl md:text-6xl font-extrabold mb-6 text-transparent bg-clip-text
         bg-gradient-to-r from-cyan-400 via-indigo-400 to-purple-500
         drop-shadow-[0_0_10px_rgba(99,102,241,0.6)] animate-fadeIn
         leading-[1.2] pb-2 overflow-visible"
    >
      Crafted by you.<br />Perfected by us.
    </p>
  </div>

  <!--Input fields-->
  <!-- URL Input with Help Tooltip on the right -->
  <div class="mt-10 w-full max-w-md flex flex-col gap-4 text-left">
    <div class="relative flex items-center gap-3">
  <input
    type="text"
    placeholder="Your Affiliate URL"
    bind:value={userInputUrl}
    class="flex-1 px-6 py-4 text-lg rounded-xl
           bg-white/10 border border-gray-700
           text-gray-200 placeholder-gray-400
           focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400
           outline-none transition-all"
  />

  <!-- Icon on right → text appears on LEFT -->
  <HelpTool
    text="Paste your original affiliate link here (e.g. Amazon, eBay, Shopify with your tag). We will protect it from being replaced by browser extensions like Honey."
    position="right"       
    textposition="left"    
    size="xl"
    icon="❓"
  />
</div>

    <!-- Optional title input (commented out in your code) -->
    <!-- <input type="text" placeholder="Your Title For Your URL" ... /> -->
  </div>
  

  <!-- Creator Name Input, Should be title later on with real Databank, maybe try earlier too -->
  <!--<input
    type="text"
    placeholder="Your Title For Your URL"
    bind:value={userinputTitle}
    class="w-full px-6 py-4 text-lg rounded-xl 
             bg-white/10 border border-gray-700 
             text-gray-200 placeholder-gray-400
             focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 
             outline-none transition-all"
  /> -->

  <!-- Button -->
  <div class="mt-4">
    <button
    on:click={() => submitForm()}
    class="relative inline-flex items-center justify-center p-1 mb-3 me-2 overflow-hidden text-3xl font-semibold text-gray-900 rounded-xl group 
            bg-gradient-to-br from-green-400 to-blue-600 
            group-hover:from-green-400 group-hover:to-blue-600 
            hover:text-white dark:text-white 
            focus:ring-4 focus:outline-none focus:ring-green-200 dark:focus:ring-green-800 
            transition-all duration-300 scale-105 hover:scale-110 shadow-lg hover:shadow-xl"
    >
    <span
        class="relative px-8 py-4 transition-all ease-in duration-150 
            bg-white dark:bg-gray-900 rounded-lg 
            group-hover:bg-transparent group-hover:dark:bg-transparent"
    >
        Start Now
    </span>
  </button>
  <!-- Response feedback -->
  <div class="mt-6 w-full max-w-md transition-all duration-300">
    {#if responseStatus === 0}
      <!-- Success state -->
        
        {#if responseMessage.includes('Your protected url')}
          <div class="mt-4 p-3 bg-black/30 rounded-lg border border-emerald-800/50 font-mono text-sm text-emerald-200 break-all">
            {responseMessage.split(': ')[1] || responseMessage}
          </div>
        {/if}
    {:else}
      <!-- Error state -->
      <div class="p-5 bg-gradient-to-r from-red-900/40 to-rose-900/40 border border-red-700/50 rounded-xl shadow-lg shadow-red-900/20 animate-fade-in">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-8 h-8 rounded-full bg-red-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-red-300">Something went wrong</h3>
        </div>
        
        <p class="text-gray-300 mb-3">{responseMessage || "An unexpected error occurred."}</p>
        
        {#if responseErrorCode}
          <div class="inline-flex items-center gap-2 px-3 py-1.5 bg-red-950/60 rounded-md text-sm text-red-300 border border-red-800/50">
            <span class="font-mono">Error code: {responseErrorCode}</span>
          </div>
        
        <p class="mt-4 text-sm text-gray-400">
          Please contact our 
          <a href="#" class="text-red-300 hover:text-red-200 underline transition-colors">
            Support
          </a>
          with the error details above.
        </p>
        {/if}
      </div>
    {/if}
  </div>
  </div>

  <!-- Features -->
  <div class="pt-12 flex flex-wrap gap-10 justify-center max-w-6xl" id="wrapit">
    <div class="w-80 text-justify">
      <h2 class="pb-3 text-3xl md:text-4xl">
        <strong class="text-red-500 font-semibold drop-shadow-[0_0_6px_rgba(99,102,241,0.8)]">P</strong>rotect
      </h2>
      <p class="text-gray-300">
        Keep every link you share fully protected from hijackers and malicious actors. No complicated setup, no hidden fees — just a powerful system that automatically shields your URLs so your users can click safely. Focus on sharing, not worrying about attacks.
      </p>
    </div>

    <div class="w-80 text-justify">
      <h2 class="pb-3 text-3xl md:text-4xl">
        <strong class="text-red-500 font-semibold drop-shadow-[0_0_6px_rgba(99,102,241,0.8)]">P</strong>revent
      </h2>
      <p class="text-gray-300">
        Stop malicious redirects and link tampering before they ever happen. No confusing security rules, no unnecessary restrictions — just intelligent, automated protection that prevents hijacks in real time. Focus on your content, not cyber threats.
      </p>
    </div>

    <div class="w-80 text-justify">
      <h2 class="pb-3 text-3xl md:text-4xl">
        <strong class="text-red-500 font-semibold drop-shadow-[0_0_6px_rgba(99,102,241,0.8)]">P</strong>reserve
      </h2>
      <p class="text-gray-300">
        Maintain the integrity, trust, and reliability of every link you share. No interruptions, no broken redirects — just a system that ensures your users always reach exactly where you intended. Focus on growing your audience, not fixing problems.
      </p>
    </div>
  </div>
  <!-- Templates -->
<div class="pt-16 flex flex-col items-start self-start w-full max-w-6xl px-8">
  <h2 class="text-2xl font-semibold mb-6 text-gray-100">
    Choose a template to get started:
  </h2>

  <!-- Template previews -->
  <div class="overflow-x-auto w-full">
    <!-- Template cards will go here -->
  </div>
</div>
</div>
<style>
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  
  .animate-fade-in {
    animation: fadeIn 0.5s ease-out forwards;
  }
</style>