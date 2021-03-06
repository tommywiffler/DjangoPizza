from django.shortcuts import render, redirect
from .models import Pizza, Topping, Comment
from .forms import CommentForm
# Create your views here.
def index(request):
    """The home page for Pizzas."""
    return render(request, 'pizzas/index.html')

def pizzas(request):
    """Show all pizza options available."""
    pizzas = Pizza.objects.order_by('date_added')
    context = {'pizzas': pizzas}
    return render(request, 'pizzas/pizzas.html', context)

def pizza(request, pizza_id):
    """Show a single pizza and all its toppings."""
    pizza = Pizza.objects.get(id=pizza_id)
    toppings = pizza.topping_set.order_by('-date_added')
    context = {'pizza': pizza, 'toppings': toppings}
    return render(request, 'pizzas/pizza.html', context)

def comment(request, pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.pizza = pizza
            comment.save()
            form.save()
            return redirect('pizzas:pizza',pizza_id=pizza_id)

    context = {'form': form, 'pizza': pizza}
    return render(request, 'pizzas/comment.html', context)