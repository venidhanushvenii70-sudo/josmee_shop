import { Home, Grid, ShoppingBag, User } from "lucide-react"
import Link from "next/link"

export function BottomNav() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200 pb-safe">
      <div className="flex justify-around items-center h-16">
        <Link href="/" className="flex flex-col items-center justify-center w-full h-full space-y-1 text-primary">
          <Home className="h-6 w-6" />
          <span className="text-[10px] font-medium">Home</span>
        </Link>
        <Link
          href="/categories"
          className="flex flex-col items-center justify-center w-full h-full space-y-1 text-gray-500 hover:text-primary transition-colors"
        >
          <Grid className="h-6 w-6" />
          <span className="text-[10px] font-medium">Categories</span>
        </Link>
        <Link
          href="/orders"
          className="flex flex-col items-center justify-center w-full h-full space-y-1 text-gray-500 hover:text-primary transition-colors"
        >
          <ShoppingBag className="h-6 w-6" />
          <span className="text-[10px] font-medium">Orders</span>
        </Link>
        <Link
          href="/account"
          className="flex flex-col items-center justify-center w-full h-full space-y-1 text-gray-500 hover:text-primary transition-colors"
        >
          <User className="h-6 w-6" />
          <span className="text-[10px] font-medium">Account</span>
        </Link>
      </div>
    </nav>
  )
}
