from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import Cart
import uuid

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty')
        return redirect('cart:cart_view')
    
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.error(request, 'Your cart is empty')
        return redirect('cart:cart_view')
    
    addresses = request.user.addresses.all()
    total = sum(item.total_price for item in cart_items)
    
    if request.method == 'POST':
        address_id = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        
        if not address_id:
            messages.error(request, 'Please select a delivery address')
            return render(request, 'orders/checkout.html', {
                'cart_items': cart_items,
                'addresses': addresses,
                'total': total
            })
        
        if not payment_method:
            messages.error(request, 'Please select a payment method')
            return render(request, 'orders/checkout.html', {
                'cart_items': cart_items,
                'addresses': addresses,
                'total': total
            })
        
        order = Order.objects.create(
            user=request.user,
            order_number=f'JOS{uuid.uuid4().hex[:10].upper()}',
            address_id=address_id,
            total_amount=total,
            payment_method=payment_method
        )
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.selling_price
            )
        
        cart_items.delete()
        messages.success(request, f'Order placed successfully! Order ID: {order.order_number}')
        return redirect('orders:order_detail', order_id=order.id)
    
    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'addresses': addresses,
        'total': total
    })

@login_required
def order_list(request):
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
