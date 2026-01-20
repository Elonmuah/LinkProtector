<script>
  import Navbar from "$lib/components/HeroSection/Navbar.svelte";
  import Footer from '$lib/components/Footer.svelte'
</script>

<div class="relative flex flex-col min-h-screen min-w-screen text-gray-100 overflow-hidden">
  <!-- Background elements with very low z-index -->
  <div class="fixed inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 -z-50"></div>
  
  <!-- Background glows with very low z-index -->
  <div class="fixed inset-0 bg-[radial-gradient(circle_at_15%_20%,rgba(147,51,234,0.08),transparent_50%)] -z-50"></div>
  <div class="fixed inset-0 bg-[radial-gradient(circle_at_85%_80%,rgba(14,165,233,0.06),transparent_50%)] -z-50"></div>
  <div class="fixed inset-0 bg-[radial-gradient(circle_at_40%_85%,rgba(236,72,153,0.04),transparent_60%)] -z-50"></div>

  <!-- Navbar with moderate z-index -->
  <header class="relative z-30 w-full">
    <Navbar />
  </header>

  <!-- Main content -->
  <main class="flex-1 flex flex-col items-center justify-center px-4 relative z-10">
    <slot />
  </main>

  <!-- Footer with moderate z-index, but lower than mobile menu -->
  <footer class="relative z-20 w-full mt-auto">
    <Footer />
  </footer>
</div>