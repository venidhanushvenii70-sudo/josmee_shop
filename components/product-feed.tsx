import { Heart, Star } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import Image from "next/image"

export function ProductFeed() {
  // Mock data inspired by the templates
  const products = [
    {
      id: 1,
      title: "Classic Linen Shirt",
      price: 1299,
      originalPrice: 2499,
      discount: 48,
      image: "/fashion-sale.jpg",
      rating: 4.5,
    },
    {
      id: 2,
      title: "Ceramic Vase Set",
      price: 899,
      originalPrice: 1599,
      discount: 43,
      image: "/new-arrivals.jpg",
      rating: 4.0,
    },
    {
      id: 3,
      title: "Wireless Headphones",
      price: 2499,
      originalPrice: 4999,
      discount: 50,
      image: "/electronics-components.png",
      rating: 4.8,
    },
    {
      id: 4,
      title: "Cotton Bed Sheet",
      price: 699,
      originalPrice: 1299,
      discount: 46,
      image: "/placeholder.svg?key=gkkcf",
      rating: 4.2,
    },
    {
      id: 5,
      title: "Leather Wallet",
      price: 499,
      originalPrice: 999,
      discount: 50,
      image: "/placeholder.svg?key=m1p4d",
      rating: 4.7,
    },
    {
      id: 6,
      title: "Smart Watch Series",
      price: 3999,
      originalPrice: 7999,
      discount: 50,
      image: "/placeholder.svg?key=cp0qu",
      rating: 4.9,
    },
  ]

  return (
    <div className="px-2 md:px-0 py-2">
      <div className="bg-white p-3 mb-2 rounded-sm shadow-sm border border-gray-100 flex items-center justify-between">
        <h3 className="font-bold text-gray-800 text-base md:text-xl">Products For You</h3>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" className="h-7 text-xs border-gray-300 bg-transparent">
            Sort
          </Button>
          <Button variant="outline" size="sm" className="h-7 text-xs border-gray-300 bg-transparent">
            Filter
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 md:gap-4">
        {products.map((product) => (
          <div
            key={product.id}
            className="group bg-card rounded-lg overflow-hidden border border-border/50 hover:border-border transition-all hover:shadow-lg duration-300 flex flex-col h-full"
          >
            <div className="relative aspect-square overflow-hidden bg-secondary/20">
              <Image
                src={product.image || "/placeholder.svg"}
                alt={product.title}
                fill
                className="object-cover transition-transform duration-500 group-hover:scale-105"
              />
              <button className="absolute top-2 right-2 p-1.5 rounded-full bg-white/90 hover:bg-white text-stone-400 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100">
                <Heart className="w-4 h-4" />
              </button>
              <div className="absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-black/60 to-transparent text-white text-xs font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                Quick View
              </div>
            </div>

            <div className="p-3 flex flex-col flex-1">
              <h3 className="text-sm font-medium text-foreground/90 line-clamp-2 mb-2 min-h-[40px] group-hover:text-primary transition-colors">
                {product.title}
              </h3>
              <div className="flex items-center gap-0.5 mb-2">
                {[...Array(Math.floor(product.rating))].map((_, i) => (
                  <Star key={i} className="w-3 h-3 fill-yellow-400 text-yellow-400" />
                ))}
                <span className="text-xs text-muted-foreground ml-1">({product.rating})</span>
              </div>

              <div className="mt-auto">
                <div className="flex items-center flex-wrap gap-1.5 mb-1.5">
                  <span className="text-lg font-bold text-foreground">₹{product.price}</span>
                  <span className="text-xs text-muted-foreground line-through">₹{product.originalPrice}</span>
                </div>
                <div className="flex items-center justify-between gap-2">
                  <Badge variant="destructive" className="text-[10px] px-1.5 py-0.5">
                    {product.discount}% OFF
                  </Badge>
                  <p className="text-[10px] uppercase tracking-wide text-green-600 font-medium">Free Delivery</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
