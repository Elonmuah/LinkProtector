<!-- src/lib/components/HelpTooltip.svelte -->
<script>
  export let text = "Explain what this step is about...";
  export let position = "top";       // where the icon tooltip appears relative to trigger
  export let textposition = "auto";  // where the text bubble appears relative to icon
  export let size = "xl";
  export let icon = "❓";
</script>

<div class="relative inline-flex items-center group">
  <!-- Trigger icon -->
  <button type="button" aria-label="Help" class="focus:outline-none transition-transform duration-200 hover:scale-110">
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    class="text-white/90 transition-all duration-300 group-hover:text-white group-hover:scale-110 drop-shadow-[0_1px_4px_rgba(255,255,255,0.3)]"
  >
    <defs>
      <linearGradient id="imp-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#ffffff" />
        <stop offset="50%" stop-color="#e0e0e0" />
        <stop offset="100%" stop-color="#c7c7c7" />
      </linearGradient>
    </defs>

    <path d="M12 4C9.23858 4 7 6.23858 7 9C7 9.82843 7.67157 10.5 8.5 10.5C9.32843 10.5 10 9.82843 10 9C10 7.34315 11.3431 6 12 6C13.6569 6 15 7.34315 15 9C15 10.1046 14.1046 11 13 11C12.4477 11 12 11.4477 12 12V13C12 13.5523 12.4477 14 13 14C13.5523 14 14 13.5523 14 13V12.5C15.6569 12.1569 17 10.6569 17 9C17 6.23858 14.7614 4 12 4Z" fill="url(#imp-grad)"/>
    <circle cx="12" cy="18" r="1.8" fill="#ffffff"/>
  </svg>
</button>

  <!-- Tooltip bubble – square corners, sharp edges -->
  <div
    class="absolute z-50 invisible group-hover:visible opacity-0 group-hover:opacity-100
           transition-all duration-200 pointer-events-none whitespace-pre-wrap"
    class:tt-top={textposition === "top" || (textposition === "auto" && position === "bottom")}
    class:tt-bottom={textposition === "bottom" || (textposition === "auto" && position === "top")}
    class:tt-left={textposition === "left" || (textposition === "auto" && position === "right")}
    class:tt-right={textposition === "right" || (textposition === "auto" && position === "left")}
  >
    <div
      class="min-w-[240px] max-w-[320px] sm:min-w-[300px] sm:max-w-[420px] md:max-w-[480px] lg:max-w-[560px]
             p-5 sm:p-6 bg-slate-900/95 backdrop-blur-xl
             border border-indigo-500/50 shadow-2xl shadow-indigo-900/50
             text-gray-200 text-sm sm:text-base leading-relaxed break-words"
      style="border-radius: 0;" 
    >
      {text}
    </div>
  </div>
</div>

<style>
  /* Icon sizes */
  .help-sm { width: 1.5rem; height: 1.5rem; font-size: 1rem; }
  .help-md { width: 1.75rem; height: 1.75rem; font-size: 1.125rem; }
  .help-lg { width: 2rem; height: 2rem; font-size: 1.25rem; }

  /* Tooltip text positioning */
  .tt-top {
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    margin-bottom: 1.25rem;
  }
  .tt-bottom {
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 1.25rem;
  }
  .tt-left {
    right: 100%;
    top: 50%;
    transform: translateY(-50%);
    margin-right: 1.25rem;
  }
  .tt-right {
    left: 100%;
    top: 50%;
    transform: translateY(-50%);
    margin-left: 1.25rem;
  }

  /* Mobile: center and widen, keep square shape */
  @media (max-width: 640px) {
    .tt-top,
    .tt-bottom,
    .tt-left,
    .tt-right {
      left: 50% !important;
      right: auto !important;
      transform: translateX(-50%) !important;
      width: 88vw !important;
      max-width: 380px !important;
      margin: 1rem auto 0 !important;
    }
    .tt-left,
    .tt-right {
      top: 100% !important;
      margin-top: 1rem !important;
    }
  }
</style>