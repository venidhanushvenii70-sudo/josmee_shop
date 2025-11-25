import { MobileHeader } from "@/components/mobile-header"
import { BottomNav } from "@/components/bottom-nav"
import { HeroSlider } from "@/components/hero-slider"
import { CategoryGrid } from "@/components/category-grid"
import { ProductFeed } from "@/components/product-feed"
import { SiteFooter } from "@/components/site-footer"
import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-background font-sans text-foreground">
      <MobileHeader />

      <main className="flex-1">
        {/* Top-to-bottom flow as requested: Hero -> Categories -> Content */}

        <section className="bg-background pt-8 pb-12 md:pt-16 md:pb-20">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-4xl md:text-6xl font-serif font-medium tracking-tight text-primary mb-6">
              Optimal organization <br className="hidden md:block" />
              meets exquisite design
            </h1>
            <p className="text-muted-foreground text-lg md:text-xl max-w-2xl mx-auto mb-10 font-light">
              Transform your everyday essentials into functional works of art with our curated collection of premium
              goods.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="rounded-full px-8 text-base font-medium">
                Shop Collection
              </Button>
              <Button
                variant="outline"
                size="lg"
                className="rounded-full px-8 text-base font-medium border-primary/20 hover:bg-secondary bg-transparent"
              >
                View Lookbook
              </Button>
            </div>
          </div>
        </section>

        <div className="container mx-auto px-4 mb-12">
          <HeroSlider />
        </div>

        {/* Categories Section */}
        <div className="container mx-auto px-4 mb-16">
          <div className="flex items-center justify-between mb-8 border-b border-border pb-4">
            <h2 className="text-2xl font-serif font-medium">Shop by Category</h2>
            <a href="#" className="text-sm font-medium hover:text-primary/70 transition-colors">
              View All &rarr;
            </a>
          </div>
          <CategoryGrid />
        </div>

        <section className="bg-secondary/30 py-16 mb-16">
          <div className="container mx-auto px-4">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div className="space-y-6">
                <span className="text-xs font-bold tracking-widest uppercase text-muted-foreground">Limited Offer</span>
                <h2 className="text-3xl md:text-4xl font-serif font-medium">
                  Allier innovation, durabilité et efficacité
                </h2>
                <p className="text-muted-foreground leading-relaxed">
                  Discover our exclusive sustainable collection. Hand-picked items that blend modern aesthetics with
                  eco-conscious materials for the discerning individual.
                </p>
                <Button className="rounded-full px-8 mt-4" variant="default">
                  Explore Deals
                </Button>
              </div>
              <div className="relative aspect-[4/3] overflow-hidden rounded-lg bg-muted">
                <img
                  src="/fashion-sale.jpg"
                  alt="Featured Collection"
                  className="object-cover w-full h-full transition-transform duration-700 hover:scale-105"
                />
              </div>
            </div>
          </div>
        </section>

        {/* Product Feed: Recommendations & Trending */}
        <div className="container mx-auto px-4 mb-20">
          <div className="flex items-center justify-between mb-8 border-b border-border pb-4">
            <h2 className="text-2xl font-serif font-medium">Trending Now</h2>
            <div className="flex gap-4 text-sm font-medium text-muted-foreground">
              <span className="text-primary cursor-pointer border-b border-primary pb-4 -mb-4.5">New Arrivals</span>
              <span className="cursor-pointer hover:text-primary transition-colors">Best Sellers</span>
              <span className="cursor-pointer hover:text-primary transition-colors">On Sale</span>
            </div>
          </div>
          <ProductFeed />
        </div>

        <section className="bg-[#5a5746] text-[#e3e1d5] py-20 mb-16">
          <div className="container mx-auto px-4">
            <div className="flex justify-between items-end mb-16">
              <h2 className="text-4xl md:text-5xl font-mono tracking-tighter opacity-90">IN THE PRESS.</h2>
              <Button
                variant="outline"
                className="text-[#e3e1d5] border-[#e3e1d5]/30 hover:bg-[#e3e1d5] hover:text-[#5a5746] rounded-full hidden md:flex bg-transparent"
              >
                Read All News
              </Button>
            </div>

            <div className="grid gap-0 divide-y divide-[#e3e1d5]/20 border-t border-b border-[#e3e1d5]/20">
              {[
                { date: "JUN 6 2025", title: "How minimal design is reshaping e-commerce", source: "Forbes" },
                { date: "APR 13 2025", title: "The untold story of sustainable fashion", source: "Vogue" },
                { date: "MAR 26 2025", title: "Why simplicity is the ultimate sophistication", source: "Design Week" },
              ].map((item, i) => (
                <div
                  key={i}
                  className="group py-8 md:py-10 grid md:grid-cols-[200px_1fr_auto] gap-6 items-center hover:bg-[#e3e1d5]/5 transition-colors cursor-pointer"
                >
                  <span className="font-mono text-xs tracking-widest opacity-60 uppercase">{item.date}</span>
                  <div>
                    <h3 className="text-xl md:text-2xl font-serif mb-2 group-hover:translate-x-2 transition-transform duration-300">
                      {item.title}
                    </h3>
                    <span className="font-mono text-xs tracking-widest opacity-60 uppercase">{item.source}</span>
                  </div>
                  <span className="text-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 transform group-hover:translate-x-2">
                    →
                  </span>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <SiteFooter />
      <BottomNav />
    </div>
  )
}
