from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse

from .forms import CheckoutForm
from .models import Products, Category, Order, OrderItem, BillingAddress
from django.conf import settings


# Create your views here.


def shop(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('login', request.path))
    else:
        order = Order.objects.get(customer=request.user, order_ordered=False)
        # request.session['order'] = {order}
        if not order:
            request.session['order'] = {}
        products = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Products.get_all_products_by_categoryid(categoryID)
        else:
            products = Products.get_all_products()

        context = {'order': order, 'products': products, 'categories': categories, 'user': request.user}
        # add the dictionary during initialization
        # ctx = {'entries': entries, 'another_obj': some_value}
        return render(request, 'index-shop.html', context)


def detail(request, pk):
    order = Order.objects.get(customer=request.user, order_ordered=False)
    # order_items = order.get_items_in_order()
    product = Products.objects.get(pk=pk)
    categoryID = product.Category
    products = Products.get_all_products_by_categoryid(categoryID)
    context = {'order': order, 'Product': product, 'Products': products, 'user': request.user}
    return render(request, 'detail.html', context)


@login_required
def view_cart(request):
    try:
        order = Order.objects.get(customer=request.user, order_ordered=False)
        context = {
            'order': order
        }
        order_items = order.get_items_in_order()
        for items in order_items:
            print(items.item.name)

        return render(request, 'cart.html', context)
    except ObjectDoesNotExist:
        context = {
            'message': messages.error(request, "You do not have any items added in the cart")
        }
        return render(request, 'cart.html', context)
        # return redirect("/")


def test(request):
    return render(request, 'test.html', {'shop': shop})


# This function will add your product to OrderItem database and add detail order to Order database
@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Products, pk=pk)
    qty = 1
    if request.method == "POST":
        print(request.POST.get('qty'))
        qty = int(request.POST.get('qty'))
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        customer=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(customer=request.user, order_ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += qty
            order_item.save()
            messages.info(request, "Added quantity Item")
            context = {'order': order, 'customer': request.user}
            # return redirect("core:product", pk=pk)
            return render(request, 'cart.html', context)
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            context = {'order': order, 'customer': request.user}
            # return redirect("core:product", pk=pk)
            return render(request, 'cart.html', context)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(customer=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        context = {'order': order, 'customer': request.user}
        # return redirect("core:product", pk=pk)
        return render(request, 'cart.html', context)


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Products, pk=pk)
    order_qs = Order.objects.filter(
        customer=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                customer=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "Item \"" + order_item.item.name + "\" remove from your cart")
            # return redirect("core:product")
            context = {'order': order, 'customer': request.user}
            return render(request, 'cart.html', context)
        else:
            messages.info(request, "This Item not in your cart")
            context = {'order': order, 'customer': request.user}
            return render(request, 'cart.html', context)
    else:
        # add message doesn't have order
        messages.info(request, "You do not have an Order")
        context = {'order': None, 'customer': request.user}
        return render(request, 'cart.html', context)


@login_required
def reduce_quantity_item(request, pk):
    product = get_object_or_404(Products, pk=pk)
    order_qs = Order.objects.filter(
        customer=request.user,
        order_ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=product.pk).exists():
            order_item = OrderItem.objects.filter(
                item=product,
                customer=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item quantity was updated")
            context = {'order': order, 'customer': request.user}
            return render(request, 'cart.html', context)
        else:
            messages.info(request, "This Item not in your cart")
            context = {'order': order, 'customer': request.user}
            return render(request, 'cart.html', context)
    else:
        # add message doesn't have order
        messages.info(request, "You do not have an Order")
        context = {'order': None, 'customer': request.user}
        return render(request, 'cart.html', context)


def checkout(request):
    order = Order.objects.get(customer=request.user, order_ordered=False)
    if request.method == "POST":
        form = CheckoutForm(request.POST or None)

        # try:
        order = Order.objects.get(customer=request.user, order_ordered=False)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zipcode = form.cleaned_data.get('zipcode')
            # TODO: add functionality for these fields
            # same_billing_address = form.cleaned_data.get('same_billing_address')
            # save_info = form.cleaned_data.get('save_info')
            payment_option = form.cleaned_data.get('payment_option')

            billing_address = BillingAddress(
                customer=request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                city=city,
                state=state,
                zipcode=zipcode
            )
            billing_address.save()
            order.shipping_address = billing_address
            order.save()
            if payment_option == 'S':
                context = {
                    'form': form,
                    'order': order,
                    'customer': request.user,
                    'payment_option': 'stripe'
                }
                return render(request, 'checkout.html', context)

            elif payment_option == 'P':
                context = {
                    'form': form,
                    'order': order,
                    'customer': request.user,
                    'payment_option': 'stripe'
                }
                return redirect('core:payment', payment_option='paypal')
            else:
                messages.warning(request, "Invalid Payment option")
                return redirect('core:checkout')

    # messages.warning(request, "Failed Checkout")
    form = CheckoutForm()
    context = {
        'form': form,
        'order': order,
        'customer': request.user
    }
    return render(request, 'checkout.html', context)

    # except ObjectDoesNotExist:
    #   messages.error(self.request, "You do not have an order")
    #   return redirect("core:order-summary")
