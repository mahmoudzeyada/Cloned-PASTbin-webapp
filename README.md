This is the back end project of clone Pastbin website :

to install it in your local machine 

1- make a virtual environment 
    virtualenv -p python3

2-install the dependencies :
    pip install -r requirements.txt

3-make the migrations 
    
    python manage.py migrate

4-run the server 
     
    python manage.py runserver

5-if you want to reset all short code for pasts

    python manage.py refreshcodes --items(optional)  number => put the most recent number of url you want to reset it optional and if you dont put it it resets all  