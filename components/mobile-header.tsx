import { Search, ShoppingBag, Menu, User } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import Link from "next/link"

export function MobileHeader() {
  return (
    <header className="sticky top-0 z-50 w-full bg-background/80 backdrop-blur-md border-b border-border/40">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between gap-4">
          {/* Left: Mobile Menu & Logo */}
          <div className="flex items-center gap-3 md:gap-6">
            <Button variant="ghost" size="icon" className="md:hidden -ml-2 text-foreground/80 hover:text-foreground">
              <Menu className="h-5 w-5" />
              <span className="sr-only">Menu</span>
            </Button>

            <a href="/" className="flex items-center gap-2">
              <div className="h-8 w-8 bg-primary text-primary-foreground flex items-center justify-center font-bold text-lg rounded-sm md:rounded-md">
                J
              </div>
              <span className="text-lg font-serif font-bold tracking-tight hidden sm:block">Josmee</span>
            </a>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-muted-foreground ml-4">
              <Link href="#" className="hover:text-primary transition-colors">
                Home
              </Link>
              <Link href="#" className="hover:text-primary transition-colors">
                Shop
              </Link>
              <Link href="#" className="hover:text-primary transition-colors">
                Collections
              </Link>
              <Link href="#" className="hover:text-primary transition-colors">
                About
              </Link>
              <Link href="#" className="hover:text-primary transition-colors text-red-500">
                Sale
              </Link>
            </nav>
          </div>

          {/* Center: Search (Hidden on very small screens, expanded on others) */}
          <div className="hidden sm:flex flex-1 max-w-md mx-auto">
            <div className="relative w-full">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Search products..."
                className="w-full pl-9 pr-4 bg-secondary/50 border-transparent focus:bg-background focus:border-border rounded-full h-10 transition-all font-light"
              />
            </div>
          </div>

          {/* Right: Actions */}
          <div className="flex items-center gap-1 md:gap-2">
            <Button variant="ghost" size="icon" className="sm:hidden text-foreground/80">
              <Search className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon" className="text-foreground/80 hover:text-foreground hidden sm:flex">
              <User className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon" className="text-foreground/80 hover:text-foreground relative">
              <ShoppingBag className="h-5 w-5" />
              <span className="absolute top-2 right-2 h-2 w-2 rounded-full bg-primary ring-2 ring-background"></span>
              <span className="sr-only">Cart</span>
            </Button>
          </div>
        </div>

        {/* Mobile Search Bar Row (only visible on mobile) */}
        <div className="pb-3 sm:hidden">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Search products..."
              className="w-full pl-9 bg-secondary/30 border-transparent rounded-lg h-10 font-light text-sm"
            />
          </div>
        </div>
      </div>
    </header>
  )
}
