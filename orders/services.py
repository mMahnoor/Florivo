from orders.models import OrderItem, Order
from cart.models import Cart
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class EmailService:
    @staticmethod
    def send_order_confirmation_email(user, order):
        """
        Sends a styled HTML confirmation email to the user upon order placement.
        """
        
        context = {
            'user': user,
            'order': order,
            'order_items': order.items.all(),
            'total': order.total_price,
        }

        text_content = render_to_string("emails/order_confirmation.txt", context)
        html_content = render_to_string("emails/order_confirmation.html", context)

        email = EmailMultiAlternatives(
            f"Order Confirmation - #{order.id}", # email subject
            text_content, 
            "florivo.zamtech@gmail.com", # from
            [user.email] # to
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

    @staticmethod
    def send_status_update_email(user, order):
        print(f"Sending status update email to {user.email} for order {order.id}")
        context = {
            'user': user,
            'order': order,
        }

        text_content = render_to_string("emails/status_update.txt", context)
        html_content = render_to_string("emails/status_update.html", context)

        email = EmailMultiAlternatives(
            f"Status Update For - #{order.id}", # email subject
            text_content, 
            "florivo.zamtech@gmail.com", # from
            [user.email] # to
        )
        email.attach_alternative(html_content, "text/html")
        email.send()


class OrderService:
    @staticmethod
    def create_order(user_id, cart_id):
        with transaction.atomic():
            cart = Cart.objects.select_related('user').prefetch_related('items__flower').get(pk=cart_id)
            cart_items = cart.items.all()

            if not cart_items.exists():
                raise ValidationError({"detail": "Your cart is empty."})

            # Checking stock
            for item in cart_items:
                if item.quantity > item.flower.stock:
                    raise ValidationError({
                        "detail": f"Not enough stock for {item.flower.title}. Only {item.flower.stock} left."
                    })

            total_price = sum(item.flower.price * item.quantity for item in cart_items)

            # Create order
            order = Order.objects.create(user_id=user_id, total_price=total_price)

            # Create order items & update stock
            order_items = []
            for item in cart_items:
                flower = item.flower
                flower.stock -= item.quantity

                if flower.stock <= 0:
                    flower.is_available = False

                flower.save(update_fields=["stock", "is_available"])

                order_items.append(OrderItem(
                    order=order,
                    flower=flower,
                    price=flower.price,
                    quantity=item.quantity,
                    total_price=flower.price * item.quantity
                ))

            OrderItem.objects.bulk_create(order_items)

            cart.delete()
            order.refresh_from_db()
            return order

    @staticmethod
    def cancel_order(order, user):
        with transaction.atomic():
            if order.user != user and not user.is_staff:
                raise PermissionDenied({"detail": "You can only cancel your own order."})

            if order.status in [Order.CANCELLED, Order.DELIVERED]:
                raise ValidationError({"detail": f"You cannot cancel an order that is {order.status.lower()}."})

            # Restore stock
            order_items = order.items.select_related('flower').all()
            for item in order_items:
                flower = item.flower
                flower.stock += item.quantity
                if flower.stock > 0:
                    flower.is_available = True
                flower.save(update_fields=["stock", "is_available"])

            order.status = Order.CANCELLED
            order.save(update_fields=["status"])

            return order