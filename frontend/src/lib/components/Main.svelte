<script>
  let userInputUrl = "";
  let userinputTitle = "";
  let responseMessage = "";
  let responseStatus = undefined;
  let responseErrorCode = null;     // ← moved here + fixed typo + null instead of undefined

  async function submitForm() {
    try {
      const res = await fetch("http://192.168.2.101:5000/api/buttonClick", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: userInputUrl,
          title: userinputTitle
        })
      });

      const data = await res.json();

      responseStatus = data.error;
      responseMessage = data.message;

      if (data.errorCode) {
        responseErrorCode = data.errorCode;    // ← no 'let' here!
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
  <div class="mt-10 w-full max-w-md flex flex-col gap-4 text-left">

  <!-- URL Input -->
  <input
    type="text"
    placeholder="Your Affilate URL"
    bind:value={userInputUrl}
    class="w-full px-6 py-4 text-lg rounded-xl 
             bg-white/10 border border-gray-700 
             text-gray-200 placeholder-gray-400
             focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 
             outline-none transition-all"
  />
  

  <!-- Creator Name Input, Should be title later on with real Databank, maybe try earlier too -->
  <input
    type="text"
    placeholder="Your Title For Your URL"
    bind:value={userinputTitle}
    class="w-full px-6 py-4 text-lg rounded-xl 
             bg-white/10 border border-gray-700 
             text-gray-200 placeholder-gray-400
             focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 
             outline-none transition-all"
  />
  </div>

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
      <div class="p-5 bg-gradient-to-r from-emerald-900/40 to-teal-900/40 border border-emerald-700/50 rounded-xl shadow-lg shadow-emerald-900/20 animate-fade-in">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-emerald-300">Success!</h3>
        </div>
        <p class="text-gray-300 leading-relaxed">{responseMessage}</p>
        
        {#if responseMessage.includes('Your protected url')}
          <div class="mt-4 p-3 bg-black/30 rounded-lg border border-emerald-800/50 font-mono text-sm text-emerald-200 break-all">
            {responseMessage.split(': ')[1] || responseMessage}
          </div>
        {/if}
      </div>
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
        
        {#if reponseErrorCode}
          <div class="inline-flex items-center gap-2 px-3 py-1.5 bg-red-950/60 rounded-md text-sm text-red-300 border border-red-800/50">
            <span class="font-mono">Error code: {reponseErrorCode}</span>
          </div>
        {/if}
        
        <p class="mt-4 text-sm text-gray-400">
          Please contact our 
          <a href="#" class="text-red-300 hover:text-red-200 underline transition-colors">
            Support
          </a>
          with the error details above.
        </p>
      </div>
    {/if}
  </div>
  </div>

  <!-- Features -->
  <div class="pt-12 flex flex-wrap gap-10 justify-center max-w-6xl" id="wrapit">
    <div class="w-80 text-justify">
      <h2 class="pb-3 text-3xl md:text-4xl">
        <strong class="text-red-500 font-semibold drop-shadow-[0_0_6px_rgba(99,102,241,0.8)]">F</strong>ree
      </h2>
      <p class="text-gray-300">
        Build your professional résumé without limits. No paywalls, no hidden catches — just powerful tools that let you design, customize, and download your résumé for free. Focus on your career, not your credit card.
      </p>
    </div>

    <div class="w-80 text-justify">
      <h2 class="pb-3 text-3xl md:text-4xl">
        <strong class="text-red-500 font-semibold drop-shadow-[0_0_6px_rgba(99,102,241,0.8)]">F</strong>ast
      </h2>
      <p class="text-gray-300">
        From start to finish in minutes. Our intuitive builder helps you generate, edit, and polish your résumé in real-time — no loading screens, no wasted effort. Just instant results that move as quickly as you do.
      </p>
    </div>

    <div class="w-80 text-justify">
      <h2 class="pb-3 text-3xl md:text-4xl">
        <strong class="text-red-500 font-semibold drop-shadow-[0_0_6px_rgba(99,102,241,0.8)]">F</strong>ormatted
      </h2>
      <p class="text-gray-300">
        Your résumé, perfectly aligned every time. With smart templates and adaptive layouts, every section looks clean, consistent, and ready for recruiters. Designed for precision — because presentation matters.
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