from django.shortcuts import render 
from django.shortcuts import redirect

from .forms import ContactForm 

 

def contact_view(request): 

    if request.method == "POST": 

        form = ContactForm(request.POST) 

        if form.is_valid(): 

            form.save()  # Saves directly to the database 

            return redirect('success_page') 

    else: 

        form = ContactForm() 

     

    return render(request, 'contact.html', {'form': form}) 