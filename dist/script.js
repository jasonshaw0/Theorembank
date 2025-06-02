document.addEventListener("DOMContentLoaded", () => {
  /* ----- Mobile Menu Toggle ----- */
  const sidebar = document.querySelector(".sidebar");
  const hMenu = document.getElementById("hamburger-menu");
  const themeBtn = document.getElementById("theme-toggle");
  
  // Mobile hamburger menu toggle
  if (hMenu) { 
    hMenu.onclick = () => sidebar.classList.toggle("active"); 
  }
  
  // Close sidebar when clicking outside on mobile
  document.addEventListener("click", e => {
    if (sidebar.classList.contains("active") && !sidebar.contains(e.target) && e.target !== hMenu) {
      sidebar.classList.remove("active");
    }
  });

  /* ----- Current Page Highlighting ----- */
  const currentPath = window.location.pathname;
  const filename = currentPath.substring(currentPath.lastIndexOf('/') + 1);
  
  // Highlight current page in navigation
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    
    // Check if this link matches the current page
    if (href === filename || 
        href === `../${filename}` || 
        href.includes(filename) ||
        (filename === 'index.html' && href.includes('index.html'))) {
      link.classList.add('active');
    }
  });

  /* ----- Copy LaTeX Button Functionality ----- */
  document.querySelectorAll(".copy-btn").forEach(btn => {
    btn.onclick = async () => {
      try {
        await navigator.clipboard.writeText(btn.dataset.tex);
        const original = btn.textContent;
        btn.textContent = "✓ Copied";
        btn.classList.add("copied");
        setTimeout(() => {
          btn.textContent = original;
          btn.classList.remove("copied");
        }, 1500);
      } catch (err) {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = btn.dataset.tex;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        btn.textContent = "✓ Copied";
        setTimeout(() => btn.textContent = "📋", 1500);
      }
    };
  });

  /* ----- Theme Toggle ----- */
  const toggleTheme = () => {
    const root = document.documentElement;
    const currentTheme = root.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    
    // Update theme button icon
    if (themeBtn) {
      themeBtn.textContent = newTheme === "dark" ? "☀️" : "🌙";
    }
  };
  
  // Initialize theme from localStorage
  const savedTheme = localStorage.getItem("theme") || "light";
  document.documentElement.setAttribute("data-theme", savedTheme);
  if (themeBtn) {
    themeBtn.textContent = savedTheme === "dark" ? "☀️" : "🌙";
    themeBtn.onclick = toggleTheme;
  }

  /* ----- Formula Search (Ctrl+K) ----- */
  const allCards = [...document.querySelectorAll(".formula-card")];
  let searchBox = null;
  
  function search(query) {
    if (!query.trim()) {
      allCards.forEach(c => c.style.display = "block");
      return;
    }
    const re = new RegExp(query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "i");
    allCards.forEach(c => {
      const hit = re.test(c.innerText);
      c.style.display = hit ? "block" : "none";
    });
  }
  
  function createSearchBox() {
    if (searchBox) return;
    searchBox = document.createElement("input");
    searchBox.className = "search-box";
    searchBox.placeholder = "Search formulas... (ESC to close)";
    searchBox.type = "text";
    document.body.appendChild(searchBox);
    
    searchBox.oninput = () => search(searchBox.value);
    searchBox.onkeydown = (e) => {
      if (e.key === "Escape") {
        closeSearch();
      }
    };
    
    // Auto-focus and select all
    setTimeout(() => {
      searchBox.focus();
      searchBox.select();
    }, 100);
  }
  
  function closeSearch() {
    if (searchBox) {
      searchBox.remove();
      searchBox = null;
      search(""); // Reset all cards to visible
    }
  }
  
  // Keyboard shortcuts
  document.addEventListener("keydown", e => {
    // Ctrl+K for search
    if (e.ctrlKey && e.key === "k") {
      e.preventDefault();
      createSearchBox();
    }
    // Ctrl+J for theme toggle
    if (e.ctrlKey && e.key === "j") {
      e.preventDefault();
      toggleTheme();
    }
    // ESC to close search when search box doesn't have focus
    if (e.key === "Escape" && searchBox && document.activeElement !== searchBox) {
      closeSearch();
    }
  });

  /* ----- Smooth Scrolling for Anchor Links ----- */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  /* ----- Enhanced Navigation UX ----- */
  
  // Add subtle hover effects and loading states
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
      // Add loading state if navigating to new page
      if (!this.classList.contains('active')) {
        this.style.opacity = '0.6';
        this.textContent = this.textContent + ' ⟳';
      }
    });
  });

  // Preload critical pages for better performance
  const criticalPages = [
    '../math/index.html',
    '../physics/index.html',
    '../math/algebra.html',
    '../math/calculus.html'
  ];
  
  criticalPages.forEach(page => {
    const link = document.createElement('link');
    link.rel = 'prefetch';
    link.href = page;
    document.head.appendChild(link);
  });

  console.log('🎯 Modern navigation initialized - no more collapsing menus!');
}); 