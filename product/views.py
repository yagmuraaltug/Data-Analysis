from math import prod
from django.shortcuts import render
from sympy import content
from .models import Product,Purchase
import pandas as pd
from .utils import get_simple_plot, get_salesman_from_id, get_image
from .forms import PurchaseForm
from django.http import HttpResponse
import matplotlib.pyplot as plt
import seaborn as sns
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def sales_dist_view(request):
    df = pd.DataFrame(Purchase.objects.all().values())
    df["salesman_id"] = df["salesman_id"].apply(get_salesman_from_id)
    df.rename({'salesman_id' : 'salesman'}, axis=1, inplace=True)
    df['date'] = df['date'].apply(lambda x:x.strftime('%Y-%m-%d'))
    plt.switch_backend('Agg')
    plt.xticks(rotation=45)
    sns.barplot(x='date', y='total_price', hue='salesman', data=df)
    plt.tight_layout()
    graph = get_image()
    return render(request, 'products/sales.html', {'graph' : graph})

@login_required
def chart_select_view(request):
    error_message = None
    df = None
    graph = None
    price = None

    try:
        products = pd.DataFrame(Product.objects.all().values())
        purchase = pd.DataFrame(Purchase.objects.all().values())
        products['product_id'] = products['id']
    

        if purchase.shape[0] > 0:
            df = pd.merge(purchase, products, on='product_id').drop(['id_y', 'date_y'], axis=1).rename({'id_x':'id', 'date_x':'date'}, axis=1)
            price = df['price']
            if request.method == "POST":
                chart_type = request.POST["sales"]
                date_from  = request.POST['date_from']
                date_to    = request.POST['date_to']
                print(chart_type)
                df['date'] = df['date'].apply(lambda x:x.strftime('%m-%d-%y'))
                df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')

                if chart_type != "":
                    if date_from != "" and date_to != "":
                        df = df[(df['date']>date_from) & (df['date']< date_to)]
                        df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')

                    graph =  get_simple_plot(chart_type, x=df2['date'] , y=df2['total_price'], data=df)



                else:
                    error_message = "Please select a chart type to continue"

        else:
            error_message = "There is no records in the database"
    except:
        products = None
        purchase = None
        error_message = "There is no records in the database"

    context = {
        'price' : price,
        'graph' : graph,
        'error_message':error_message, 

    }
    return render(request, 'products/index.html', context)

@login_required
def add_purchase_view(request):
    added_message=None
    form = PurchaseForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.salesman = request.user
        obj.save()
  
        form = PurchaseForm()
        added_message = "The purchase has been added."

    context = {
        'form' : form,
        'added_message':added_message

    }
    return render(request, 'products/add.html', context)