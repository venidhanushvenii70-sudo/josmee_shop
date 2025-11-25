import { Facebook, Instagram, Twitter, Youtube, Phone, Mail, MessageCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function SiteFooter() {
  return (
    <footer className="bg-stone-900 text-stone-400 pt-16 pb-8 text-sm">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-16">
          {/* Brand Column */}
          <div className="space-y-6">
            <div className="flex items-center gap-2 text-stone-100">
              <div className="h-8 w-8 bg-stone-100 text-stone-900 flex items-center justify-center font-bold text-lg rounded-sm">
                J
              </div>
              <span className="text-xl font-serif font-bold tracking-tight">Josmee</span>
            </div>
            <p className="leading-relaxed max-w-xs">
              Curated essentials for the modern lifestyle. Quality, sustainability, and design in every detail.
            </p>
            <div className="flex gap-4">
              <a
                href="https://wa.me/919442085847?text=Welcome%20to%20Josmee%20Online%20Shopping"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-green-400 transition-colors"
                aria-label="Contact us on WhatsApp"
              >
                <MessageCircle className="w-5 h-5" />
              </a>
              <a href="#" className="hover:text-white transition-colors">
                <Facebook className="w-5 h-5" />
              </a>
              <a href="#" className="hover:text-white transition-colors">
                <Instagram className="w-5 h-5" />
              </a>
              <a href="#" className="hover:text-white transition-colors">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="#" className="hover:text-white transition-colors">
                <Youtube className="w-5 h-5" />
              </a>
            </div>
            {/* </CHANGE> */}
          </div>

          {/* Links Column */}
          <div>
            <h3 className="text-stone-100 font-medium mb-6 uppercase tracking-wider text-xs">Shop</h3>
            <ul className="space-y-4">
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  New Arrivals
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Best Sellers
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Sale
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Gift Cards
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-stone-100 font-medium mb-6 uppercase tracking-wider text-xs">Contact Us</h3>
            <ul className="space-y-4">
              <li className="flex items-center gap-2">
                <Phone className="w-4 h-4 text-stone-100" />
                <a href="tel:+919442085847" className="hover:text-white transition-colors">
                  +91 9442085847
                </a>
              </li>
              <li className="flex items-center gap-2">
                <Phone className="w-4 h-4 text-stone-100" />
                <a href="tel:04636250411" className="hover:text-white transition-colors">
                  04636 250411
                </a>
              </li>
              <li className="flex items-center gap-2">
                <Mail className="w-4 h-4 text-stone-100" />
                <a href="mailto:devasindainfoods@gmail.com" className="hover:text-white transition-colors break-all">
                  devasindainfoods@gmail.com
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Help Center
                </a>
              </li>
            </ul>
          </div>
          {/* </CHANGE> */}

          {/* Newsletter */}
          <div>
            <h3 className="text-stone-100 font-medium mb-6 uppercase tracking-wider text-xs">Stay Updated</h3>
            <p className="mb-4 text-xs leading-relaxed">
              Subscribe to our newsletter for exclusive offers and design updates.
            </p>
            <div className="flex gap-2">
              <Input
                placeholder="Enter your email"
                className="bg-stone-800 border-stone-700 text-stone-200 placeholder:text-stone-500 h-10"
              />
              <Button className="bg-stone-100 text-stone-900 hover:bg-stone-200 h-10 px-4">Join</Button>
            </div>
          </div>
        </div>

        <div className="border-t border-stone-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-xs">
          <p>&copy; 2025 Josmee Inc. All rights reserved.</p>
          <div className="flex gap-6">
            <a href="#" className="hover:text-white transition-colors">
              Privacy Policy
            </a>
            <a href="#" className="hover:text-white transition-colors">
              Terms of Service
            </a>
            <a href="#" className="hover:text-white transition-colors">
              Cookie Policy
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}
