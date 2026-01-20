<script>
  import NavActions from "$lib/components/HeroSection/NavActions.svelte";
</script>

<nav class="relative z-40 w-full h-28 px-4 sm:px-6 lg:px-8">
  <div class="h-full w-full max-w-7xl mx-auto flex items-center justify-between">
    <div class="flex items-center">
      <h1 class="font-bold text-slate-100 tracking-tight text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl">
        URLock
      </h1>
    </div>
    
    <div class="flex items-center">
      <NavActions />
    </div>
  </div>
</nav>