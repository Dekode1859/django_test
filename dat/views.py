from django.shortcuts import render, redirect
import pyrebase
from .forms import DataEntryForm
from .models import DataEntry
from .scraper import scrape

config = {
    "apiKey": "AIzaSyDLEGavxSdhssOpsTmiirtWMmCNDH4iOyk",
    "authDomain": "djangoweb-86c4c.firebaseapp.com",
    "databaseURL": "https://djangoweb-86c4c-default-rtdb.firebaseio.com",
    "projectId": "djangoweb-86c4c",
    "storageBucket": "djangoweb-86c4c.appspot.com",
    "messagingSenderId": "164781762526",
    "appId": "1:164781762526:web:d5ffff66266f5ec5675f4f",
    "measurementId": "G-YFME97TWS7"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# Create your views here.
# def index(request):
#     name = db.child("Data").child("Name").get().val()
#     age = db.child("Data").child("Age").get().val()
#     gender = db.child("Data").child("Gender").get().val()
#     return render(request, 'index.html', {
#         "name": name,
#         "age": age,
#         "gender": gender,
#     })
    
# dat/views.py
def index(request):
    if request.method == 'POST':
        form = DataEntryForm(request.POST)
        if form.is_valid():
            form.save()
            data_entries = DataEntry.objects.all()
            # get value of the 'name' attribute of each DataEntry object
            try:
                id = [data_entry.id for data_entry in data_entries]
                print(id)
            except:
                pass
            # name = [data_entry.name for data_entry in data_entries]
            url = [data_entry.url for data_entry in data_entries]
            if url:
                data = scrape(url[0])
                if data is None:
                    data_entries.delete()
                    return redirect('index')
                else:
                    # price = data['price']
                    # title = data['title']
                    # print(title, price)
                    # dbdata = {"name": name[0], "url": url[0], "title": title, "price": price}
                    # add the name and url to the dictionary "data"
                    # data["name"] = name[0]
                    try:
                        data["url"] = url[0]
                        print(data)
                        try:
                            db.child(id[0]).set(data)
                        except:
                            db.child("Items").set(data)
                    except:
                        print("Error")
                        pass
                    data_entries.delete()
                    return redirect('index')
            else:
                data_entries.delete()
                return redirect('index')
            # data = scrape(url)
            # print(data)
            # create a dictionary to pass to template
            # data = {"name": name, "url": url}
            # # empty the QuerySet
        # return render(request, 'done.html', {'name': form, 'url': data_entries})
    else:
        form = DataEntryForm()

    
    # # add the data to the database
    # db.child("Items").set(data)
    return render(request, 'index.html', {'form': form})

# {'form': form, 'data_entries': data_entries}