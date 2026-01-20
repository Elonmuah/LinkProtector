<script>
  import * as d3 from "d3";
  import { onMount, onDestroy } from 'svelte';
  import { API_BASE } from '$lib/env';

  let clicksCanvas;
  let selectedTimeframe = "7d";
  let isLoading = false;
  let chartOpacity = 1;
  let resizeTimeout;

  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");

  const timeframes = [
    { value: "24h", label: "24h" },
    { value: "7d",  label: "7d" },
    { value: "30d", label: "30d" },
    { value: "90d", label: "90d" },
    { value: "all", label: "All" }
  ];

  onMount(() => {
    fetchClicks(selectedTimeframe);
    window.addEventListener('resize', handleResize);
    // Give the DOM a moment to render the container
    setTimeout(() => handleResize(), 300);
  });

  onDestroy(() => {
    window.removeEventListener('resize', handleResize);
    if (resizeTimeout) clearTimeout(resizeTimeout);
  });

  function handleResize() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      if (clicksCanvas) {
        fetchClicks(selectedTimeframe);
      }
    }, 150);
  }

  function selectTimeframe(tf) {
    selectedTimeframe = tf;
    fetchClicks(tf);
  }

  // The only and correct fetchClicks function
  async function fetchClicks(tf) {
    isLoading = true;
    chartOpacity = 0.4; // fade out effect
    await new Promise(resolve => setTimeout(resolve, 300));

    let x = [];
    let y = [];
    let isHourly = false;

    try {
      if (tf === "24h") {
        const data = await fetchHours();
        const hourlyDict = data.hourlyData || {};
        x = Object.keys(hourlyDict).sort(); // chronological order
        y = Object.values(hourlyDict);
        isHourly = true;
      } else {
        const data = await fetchDays(tf);
        const dict = data.dateDaysDictionary || {};
        x = Object.keys(dict).sort();
        y = Object.values(dict);
        isHourly = false;
      }

      if (x.length === 0) {
        showNoData();
      } else {
        makeChart(x, y, isHourly);
      }
    } catch (err) {
      console.error("Error fetching chart data:", err);
      showNoData();
    } finally {
      isLoading = false;
      chartOpacity = 1; // fade in
    }
  }

  function showNoData() {
    if (!clicksCanvas) return;
    d3.select(clicksCanvas).selectAll("*").remove();
    d3.select(clicksCanvas)
      .append("div")
      .attr("class", "flex items-center justify-center h-full text-slate-500 text-lg sm:text-xl")
      .text("No click data yet");
  }

  const fetchDays = async (tf) => {
    try {
      const res = await fetch(`${API_BASE}/api/${token}/getDays`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ timeframe: tf })
      });
      if (!res.ok) {
        throw new Error(`Days fetch failed: ${res.status}`);
      }
      return await res.json();
    } catch (e) {
      console.error("fetchDays error:", e);
      return {};
    }
  };

  const fetchHours = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/${token}/getHours`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ timeframe: "24h" }) // Only current timeframe
      });
      if (!res.ok) {
        throw new Error(`Hours fetch failed: ${res.status}`);
      }
      return await res.json();
    } catch (e) {
      console.error("fetchHours error:", e);
      return { hourlyData: {} };
    }
  };

  function makeChart(x, y, isHourly = false) {
    if (!clicksCanvas) return;

    const container = clicksCanvas;
    d3.select(container).selectAll("*").remove();

    const yNums = y.map(v => Number(v) || 0);

    let parseFunc = isHourly 
      ? d3.timeParse("%Y-%m-%d %H") 
      : d3.timeParse("%Y-%m-%d");

    let timeFormatTick = isHourly 
      ? d3.timeFormat("%H:00") 
      : d3.timeFormat("%b %d");

    const dates = x.map(d => parseFunc(d)).filter(Boolean);

    if (dates.length === 0) {
      showNoData();
      return;
    }

    // Responsive sizing
    const rect = container.getBoundingClientRect();
    const width = Math.max(rect.width, 320);
    const aspectRatio = 1.65;
    let height = Math.round(width / aspectRatio);
    height = Math.min(Math.max(height, 240), 520);

    const margin = {
      top:    width < 500 ? 32 : 40,
      right:  width < 500 ? 16 : 60,
      bottom: width < 500 ? 60 : 90,
      left:   width < 500 ? 48 : 70
    };

    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const svg = d3.select(container)
      .append("svg")
      .attr("width", "100%")
      .attr("height", height)
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("preserveAspectRatio", "xMidYMid meet");

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    const xScale = d3.scaleTime()
      .domain(d3.extent(dates))
      .range([0, innerWidth]);

    const maxY = Math.max(5, d3.max(yNums));
    const yScale = d3.scaleLinear()
      .domain([0, maxY])
      .nice()
      .range([innerHeight, 0]);

    // Area & Line
    const area = d3.area()
      .x((_, i) => xScale(dates[i]))
      .y0(innerHeight)
      .y1((_, i) => yScale(yNums[i]))
      .curve(d3.curveMonotoneX);

    const line = d3.line()
      .x((_, i) => xScale(dates[i]))
      .y((_, i) => yScale(yNums[i]))
      .curve(d3.curveMonotoneX);

    // Gradient
    const gradient = g.append("defs").append("linearGradient")
      .attr("id", "areaGradient")
      .attr("x1", "0%").attr("y1", "0%")
      .attr("x2", "0%").attr("y2", "100%");

    gradient.append("stop").attr("offset", "0%").attr("stop-color", "#a78bfa").attr("stop-opacity", 0.35);
    gradient.append("stop").attr("offset", "100%").attr("stop-color", "#a78bfa").attr("stop-opacity", 0);

    g.append("path").attr("fill", "url(#areaGradient)").attr("d", area(yNums));
    g.append("path")
      .attr("fill", "none")
      .attr("stroke", "#a78bfa")
      .attr("stroke-width", width < 500 ? 3 : 4)
      .attr("stroke-linecap", "round")
      .attr("d", line(yNums));

    // X Axis
    const tickCount = isHourly ? Math.min(12, dates.length) : Math.min(8, dates.length);
    const xAxis = d3.axisBottom(xScale)
      .ticks(tickCount)
      .tickFormat(timeFormatTick);

    g.append("g")
      .attr("transform", `translate(0,${innerHeight})`)
      .call(xAxis)
      .call(g => g.select(".domain").attr("stroke", "#475569"))
      .call(g => g.selectAll("text")
        .attr("fill", "#94a3b8")
        .attr("font-size", width < 500 ? "11px" : "13px")
        .attr("dy", "10")
        .style("text-anchor", isHourly ? "end" : "middle"))
      .call(g => {
        if (isHourly) {
          g.selectAll("text").attr("transform", "rotate(-45)");
        }
      });

    // Y Axis
    g.append("g")
      .call(d3.axisLeft(yScale).ticks(6).tickFormat(d3.format("d")))
      .call(g => g.select(".domain").attr("stroke", "#475569"))
      .call(g => g.selectAll("text")
        .attr("fill", "#e2e8f0")
        .attr("font-size", width < 500 ? "11px" : "13px"));

    // →→→ Paste your tooltip, points, grid, hover logic here ←←←
    // (the rest of your original tooltip + hover code goes here)
  }
</script>

<section class="w-full min-h-screen py-8 px-4 sm:px-6 lg:px-8 bg-slate-950">
  <div class="max-w-7xl mx-auto">
    <!-- Header -->
    <div class="text-center mb-10 sm:mb-12">
      <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold text-white mb-3 sm:mb-4">
        Clicks Over Time
      </h1>
      <p class="text-lg sm:text-xl text-slate-400">
        Beautiful, real-time click analytics
      </p>
    </div>

    <!-- Timeframe Selector -->
    <div class="flex justify-center mb-8 sm:mb-10 overflow-x-auto scrollbar-hide pb-2">
      <div class="
        inline-flex flex-nowrap gap-2.5 sm:gap-3
        bg-slate-800/70 backdrop-blur-xl 
        border border-slate-700/60 
        rounded-2xl p-2 sm:p-2.5 shadow-xl
      ">
        {#each timeframes as { value, label }}
          <button
            on:click={() => selectTimeframe(value)}
            class="
              px-4 sm:px-5 py-2.5 text-sm sm:text-base font-medium 
              rounded-xl transition-all duration-300 whitespace-nowrap
              {selectedTimeframe === value
                ? 'bg-gradient-to-r from-indigo-600 to-purple-700 text-white shadow-lg shadow-purple-500/40'
                : 'text-slate-300 hover:text-white hover:bg-slate-700/60'}
            "
          >
            {label}
          </button>
        {/each}
      </div>
    </div>

    <!-- Chart Container -->
    <div class="
      bg-slate-900/85 backdrop-blur-2xl 
      border border-slate-700/70 
      rounded-2xl sm:rounded-3xl 
      shadow-2xl shadow-black/50 
      overflow-hidden
    ">
      <div class="p-4 sm:p-6 md:p-8">
        <div
          bind:this={clicksCanvas}
          class="w-full relative bg-slate-950/40 rounded-lg overflow-hidden transition-opacity duration-500"
          style="
            aspect-ratio: 16 / 9.2;
            min-height: 240px;
            max-height: 520px;
            height: auto;
            opacity: {chartOpacity};
          "
        >
          {#if isLoading}
            <div class="absolute inset-0 flex items-center justify-center bg-slate-950/60 backdrop-blur-sm z-10">
              <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
            </div>
          {/if}
        </div>
      </div>
    </div>

    <!-- Back link -->
    <div class="mt-10 sm:mt-12 text-center">
      <a
        href="/analytics"
        class="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors duration-200 text-base sm:text-lg"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </a>
    </div>
  </div>
</section>

<style>
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
</style>