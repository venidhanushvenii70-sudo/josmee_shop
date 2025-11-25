// Josmee Modern JavaScript Enhancements

document.addEventListener("DOMContentLoaded", () => {
  // Smooth scroll behavior
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })

  // Navbar scroll effect
  const navbar = document.querySelector(".josmee-navbar")
  if (navbar) {
    let lastScroll = 0
    window.addEventListener("scroll", () => {
      const currentScroll = window.pageYOffset

      if (currentScroll > 100) {
        navbar.style.padding = "10px 0"
        navbar.style.boxShadow = "0 10px 30px rgba(0, 0, 0, 0.15)"
      } else {
        navbar.style.padding = "16px 0"
        navbar.style.boxShadow = "0 10px 15px rgba(0, 0, 0, 0.1)"
      }

      lastScroll = currentScroll
    })
  }

  // Add to cart animation
  const addToCartButtons = document.querySelectorAll('[href*="add_to_cart"]')
  addToCartButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      // Visual feedback
      const icon = this.querySelector("i")
      if (icon) {
        icon.classList.add("fa-bounce")
        setTimeout(() => {
          icon.classList.remove("fa-bounce")
        }, 1000)
      }

      // Show toast notification
      showToast("Product added to cart!", "success")
    })
  })

  // Product card lazy loading
  const observerOptions = {
    root: null,
    rootMargin: "0px",
    threshold: 0.1,
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1"
        entry.target.style.transform = "translateY(0)"
        observer.unobserve(entry.target)
      }
    })
  }, observerOptions)

  document.querySelectorAll(".josmee-product-card").forEach((card) => {
    card.style.opacity = "0"
    card.style.transform = "translateY(30px)"
    card.style.transition = "all 0.5s ease"
    observer.observe(card)
  })

  // Search functionality enhancement
  const searchInput = document.querySelector(".josmee-search-wrapper input")
  if (searchInput) {
    let searchTimeout
    searchInput.addEventListener("input", function () {
      clearTimeout(searchTimeout)
      const searchIcon = document.querySelector(".josmee-search-btn i")

      if (this.value.length > 0) {
        searchIcon.classList.remove("fa-search")
        searchIcon.classList.add("fa-spinner", "fa-spin")

        searchTimeout = setTimeout(() => {
          searchIcon.classList.remove("fa-spinner", "fa-spin")
          searchIcon.classList.add("fa-search")
        }, 500)
      }
    })
  }

  // Category card hover effects
  document.querySelectorAll(".josmee-category-card").forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-8px) scale(1.02)"
    })

    card.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0) scale(1)"
    })
  })

  // Auto-dismiss alerts
  const alerts = document.querySelectorAll(".alert")
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.transition = "opacity 0.5s ease"
      alert.style.opacity = "0"
      setTimeout(() => {
        alert.remove()
      }, 500)
    }, 5000)
  })

  // Price animation
  function animatePrice(element) {
    const target = Number.parseInt(element.textContent.replace(/[^0-9]/g, ""))
    let current = 0
    const increment = target / 30
    const timer = setInterval(() => {
      current += increment
      if (current >= target) {
        element.textContent = "₹" + target
        clearInterval(timer)
      } else {
        element.textContent = "₹" + Math.floor(current)
      }
    }, 30)
  }

  // Discount badge animation
  document.querySelectorAll(".josmee-discount-badge").forEach((badge) => {
    badge.style.animation = "pulse 2s infinite"
  })

  // Image error handling
  document.querySelectorAll(".josmee-product-image").forEach((img) => {
    img.addEventListener("error", function () {
      this.src = "https://via.placeholder.com/280x280/9333ea/ffffff?text=No+Image"
    })
  })

  // Contact banner interaction
  const contactItems = document.querySelectorAll(".josmee-contact-item")
  contactItems.forEach((item) => {
    item.addEventListener("click", function () {
      const text = this.textContent.trim()
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
          showToast("Copied to clipboard!", "success")
        })
      }
    })
  })

  // Toast notification system
  function showToast(message, type = "info") {
    const toast = document.createElement("div")
    toast.className = `josmee-toast josmee-toast-${type}`
    toast.innerHTML = `
            <i class="fas fa-${type === "success" ? "check-circle" : "info-circle"}"></i>
            <span>${message}</span>
        `

    toast.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: ${type === "success" ? "#10b981" : "#3b82f6"};
            color: white;
            padding: 16px 24px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 600;
            z-index: 10000;
            animation: slideInUp 0.3s ease;
        `

    document.body.appendChild(toast)

    setTimeout(() => {
      toast.style.animation = "slideOutDown 0.3s ease"
      setTimeout(() => {
        toast.remove()
      }, 300)
    }, 3000)
  }

  // Add animation keyframes
  const style = document.createElement("style")
  style.textContent = `
        @keyframes slideInUp {
            from {
                transform: translateY(100px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        @keyframes slideOutDown {
            from {
                transform: translateY(0);
                opacity: 1;
            }
            to {
                transform: translateY(100px);
                opacity: 0;
            }
        }
    `
  document.head.appendChild(style)

  console.log(
    "%c🛍️ Josmee Online Shopping - Powered by Modern Design",
    "color: #9333ea; font-size: 16px; font-weight: bold;",
  )
})

// Utility functions
function formatPrice(price) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(price)
}

function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Export for use in other scripts
window.josmeeUtils = {
  formatPrice,
  debounce,
}
