<!-- src/lib/components/HelpTooltip.svelte -->
<script>
  export let text = "Explain what this step is about..."; // main help text
  export let position = "top"; // top, bottom, left, right
  export let size = "sm";      // sm, md, lg (icon size)
  export let icon = "❓";      // default emoji – can be SVG or text
</script>

<div class="relative inline-flex items-center group">
  <!-- Trigger icon -->
  <button
    type="button"
    aria-label="Help"
    class="focus:outline-none transition-transform duration-200 hover:scale-110"
  >
    <span
      class="flex items-center justify-center rounded-full bg-indigo-600/30 text-indigo-300
             hover:bg-indigo-500/50 hover:text-white transition-colors duration-200"
      class:help-sm={size === "sm"}
      class:help-md={size === "md"}
      class:help-lg={size === "lg"}
    >
      {icon}
    </span>
  </button>

  <!-- Tooltip / Popover -->
  <div
    class="absolute z-50 invisible group-hover:visible opacity-0 group-hover:opacity-100
           transition-all duration-200 pointer-events-none whitespace-pre-wrap"
    class:tooltip-top={position === "top"}
    class:tooltip-bottom={position === "bottom"}
    class:tooltip-left={position === "left"}
    class:tooltip-right={position === "right"}
  >
    <div
      class="max-w-xs sm:max-w-sm p-4 rounded-xl bg-slate-900/95 backdrop-blur-lg
             border border-indigo-500/40 shadow-2xl shadow-indigo-900/30
             text-gray-200 text-sm sm:text-base leading-relaxed"
    >
      {text}
    </div>
  </div>
</div>

<style>
  .help-sm { @apply w-6 h-6 text-base; }
  .help-md { @apply w-7 h-7 text-lg; }
  .help-lg { @apply w-8 h-8 text-xl; }

  /* Positioning */
  .tooltip-top {
    @apply bottom-full left-1/2 -translate-x-1/2 mb-3;
  }
  .tooltip-bottom {
    @apply top-full left-1/2 -translate-x-1/2 mt-3;
  }
  .tooltip-left {
    @apply right-full top-1/2 -translate-y-1/2 mr-3;
  }
  .tooltip-right {
    @apply left-full top-1/2 -translate-y-1/2 ml-3;
  }

  /* Mobile adjustments */
  @media (max-width: 640px) {
    .tooltip-top, .tooltip-bottom {
      @apply left-0 right-0 mx-auto w-11/12;
    }
    .tooltip-left, .tooltip-right {
      @apply top-full left-1/2 -translate-x-1/2 mt-3;
    }
  }
</style>