<!-- NavActions.svelte -->
<script>
  let menuOpen = false;
  
  const toggleMenu = () => {
    menuOpen = !menuOpen;
  };

  const closeMenu = () => {
    menuOpen = false;
  };
</script>

<div class="flex items-center">
  <!-- Mobile menu button -->
  <button
    class="lg:hidden p-4 rounded-xl bg-slate-800/50 hover:bg-slate-700/50 border border-slate-700/50 transition-all duration-200 flex items-center justify-center"
    on:click={toggleMenu}
    aria-label="Open navigation menu"
  >
    <svg class="w-6 h-6 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  </button>

  <!-- Desktop navigation anchors -->
  <div class="hidden lg:flex items-center gap-4">
    <a
      href="/"
      class="px-8 py-3 text-base font-medium text-slate-300 bg-slate-800/50 hover:bg-slate-700/50 rounded-xl border border-slate-700/50 transition-all duration-200"
      on:click={closeMenu}
    >
      Log in
    </a>
    
    <a
      href="/"
      class="px-8 py-3 text-base font-medium text-slate-300 bg-slate-800/50 hover:bg-slate-700/50 rounded-xl border border-slate-700/50 transition-all duration-200"
      on:click={closeMenu}
    >
      Sign up
    </a>
    
    <div class="flex items-center gap-4">
      <a
        href="/"
        class="px-10 py-3 text-base font-semibold text-white bg-gradient-to-r from-indigo-600 to-purple-700 rounded-xl shadow-lg hover:shadow-indigo-500/25 hover:scale-105 transition-all duration-200"
        on:click={closeMenu}
      >
        Go Premium
      </a>
      
      <a
        href="/analytics"
        class="px-8 py-3 text-base font-semibold text-white bg-gradient-to-r from-indigo-600 to-purple-700 rounded-xl shadow-lg hover:shadow-indigo-500/25 hover:scale-105 transition-all duration-200"
        on:click={closeMenu}
      >
        Analytics
      </a>
    </div>
  </div>

  <!-- Mobile dropdown menu with anchor tags -->
  {#if menuOpen}
    <div class="lg:hidden fixed inset-x-0 top-28 z-50">
      <div class="relative mx-auto w-full max-w-md bg-slate-800/95 backdrop-blur-xl border border-slate-700/50 rounded-2xl shadow-2xl shadow-slate-950/50 p-8 animate-in slide-in-from-top-2 duration-200 mx-4">
        <ul class="space-y-4">
          <li>
            <a
              href="/"
              class="block w-full text-left px-6 py-4 rounded-xl bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 transition-all duration-200 flex items-center gap-4"
              on:click={closeMenu}
            >
              <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Log in
            </a>
          </li>
          <li>
            <a
              href="/"
              class="block w-full text-left px-6 py-4 rounded-xl bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 transition-all duration-200 flex items-center gap-4"
              on:click={closeMenu}
            >
              <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
              Sign up
            </a>
          </li>
          <li>
            <a
              href="/"
              class="block w-full px-6 py-4 bg-gradient-to-r from-indigo-600 to-purple-700 text-white rounded-xl shadow-lg hover:shadow-indigo-500/25 hover:scale-105 transition-all duration-200"
              on:click={closeMenu}
            >
              Go Premium
            </a>
          </li>
          <li>
            <a
              href="/analytics"
              class="block w-full px-6 py-4 bg-gradient-to-r from-indigo-600 to-purple-700 text-white rounded-xl shadow-lg hover:shadow-indigo-500/25 hover:scale-105 transition-all duration-200"
              on:click={closeMenu}
            >
              Analytics
            </a>
          </li>
        </ul>
      </div>
    </div>
  {/if}
</div>