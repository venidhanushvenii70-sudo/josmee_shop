"use client"

import * as React from "react"
import Autoplay from "embla-carousel-autoplay"
import { Carousel, CarouselContent, CarouselItem } from "@/components/ui/carousel"
import { Card, CardContent } from "@/components/ui/card"

export function HeroSlider() {
  const plugin = React.useRef(Autoplay({ delay: 4000, stopOnInteraction: true }))

  const slides = [
    {
      id: 1,
      title: "Big Summer Sale",
      subtitle: "Up to 80% Off on Fashion",
      color: "bg-pink-50",
      image: "/fashion-sale.jpg",
    },
    {
      id: 2,
      title: "New Arrivals",
      subtitle: "Check out the latest trends",
      color: "bg-blue-50",
      image: "/new-arrivals.jpg",
    },
    {
      id: 3,
      title: "Electronics",
      subtitle: "Best deals on gadgets",
      color: "bg-purple-50",
      image: "/electronics-components.png",
    },
  ]

  return (
    <div className="w-full px-3 md:px-0 py-2 mb-2">
      <Carousel
        plugins={[plugin.current]}
        className="w-full"
        onMouseEnter={plugin.current.stop}
        onMouseLeave={plugin.current.reset}
      >
        <CarouselContent className="-ml-2 md:-ml-4">
          {slides.map((slide) => (
            <CarouselItem key={slide.id} className="pl-2 md:pl-4">
              <div className="p-0">
                <Card className="border-0 shadow-none">
                  <CardContent
                    className={`flex aspect-[2/1] md:aspect-[3/1] items-center justify-between p-4 md:p-8 rounded-lg ${slide.color} relative overflow-hidden`}
                  >
                    <div className="z-10 space-y-1 md:space-y-3 max-w-[65%]">
                      <h2 className="text-lg md:text-4xl font-extrabold tracking-tight text-gray-900 leading-tight">
                        {slide.title}
                      </h2>
                      <p className="text-xs md:text-lg text-gray-600 font-medium bg-white/50 backdrop-blur-sm inline-block px-2 py-0.5 rounded-sm">
                        {slide.subtitle}
                      </p>
                      <button className="mt-2 text-[10px] md:text-sm font-bold bg-gray-900 text-white px-3 py-1.5 rounded-sm uppercase tracking-wide">
                        Shop Now
                      </button>
                    </div>
                    <div className="absolute right-0 top-0 bottom-0 w-1/2 opacity-20">
                      {/* Placeholder for background image */}
                      <div className="w-full h-full bg-gradient-to-l from-black/10 to-transparent" />
                    </div>
                  </CardContent>
                </Card>
              </div>
            </CarouselItem>
          ))}
        </CarouselContent>
      </Carousel>
    </div>
  )
}
