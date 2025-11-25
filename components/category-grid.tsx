import { Shirt, Smartphone, Home, Watch, User, Gift, Music } from "lucide-react"

export function CategoryGrid() {
  const categories = [
    { name: "Women", icon: Shirt, color: "bg-stone-100" },
    { name: "Men", icon: User, color: "bg-stone-100" },
    { name: "Kids", icon: Gift, color: "bg-stone-100" },
    { name: "Home", icon: Home, color: "bg-stone-100" },
    { name: "Beauty", icon: User, color: "bg-stone-100" },
    { name: "Accessories", icon: Watch, color: "bg-stone-100" },
    { name: "Footwear", icon: Music, color: "bg-stone-100" },
    { name: "Electronics", icon: Smartphone, color: "bg-stone-100" },
  ]

  return (
    <div className="w-full overflow-x-auto pb-4 scrollbar-hide">
      <div className="flex md:grid md:grid-cols-8 gap-6 md:gap-8 min-w-max md:min-w-0 px-2 md:px-0">
        {categories.map((category, index) => (
          <div key={index} className="flex flex-col items-center gap-3 group cursor-pointer min-w-[70px]">
            <div
              className={`w-16 h-16 md:w-20 md:h-20 rounded-full ${category.color} flex items-center justify-center shadow-sm group-hover:shadow-md transition-all duration-300 group-hover:scale-105 border border-transparent group-hover:border-stone-200`}
            >
              <category.icon className="h-6 w-6 md:h-8 md:w-8 text-stone-600" />
            </div>
            <span className="text-xs md:text-sm font-medium text-stone-600 group-hover:text-stone-900 transition-colors">
              {category.name}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
