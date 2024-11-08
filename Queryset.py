# ------------------------------------------------------------------------------------
# -------------------------- Methods that return new QuerySets -----------------------
# ------------------------------------------------------------------------------------

# ----------- filter -------------
# stu = StudentModel.objects.filter(id=1)

# ----------- exclude -------------
# stu = StudentModel.objects.all().exclude(name='Raj)

# ----------- annotate -----------
# here we count how many articles (published = True) for all categories
# from django.db.models import Count,Min,Max,Avg,Sum,StdDev,Variance  # we can do this all operation with annotate
# EXAMPLE:-

final_output = DemoModel.objects.values('uid').annotate(
    completed = Count('status', filter=Q(status="Completed")),
    new=Count('status', filter=Q(status="New")),
    in_progress=Count('status', filter=Q(status="InProgress"))).order_by('uid')

# OUTPUT:-
# <QuerySet [{'uid': 1, 'completed': 0, 'hold': 3, 'in_progress': 1}, {'uid': 2, 'completed': 0, 'hold': 0, 'in_progress': 2}, {'uid': 3, 'completed': 1, 'hold': 0, 'in_progress': 0}]>



class Category(models.Model):
    title = models.Charfield(max_length=255)


class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    category = models.ForeignKey(Category)
    published = models.BooleanField(default=False)
    read_min = models.IntegerField()


def get_categories():
    filters = Q(published=True)
    return Category.objects.all().annotate(Count('article', filters))

# ----------- order_by -----------
stu = StudentModel.objects.all().order_by('date') # accending order (10-04-22 to 20-04-22)
stu = StudentModel.objects.all().order_by('-date') # descending order (10-04-22 to 20-04-22)
stu = StudentModel.objects.all().order_by('roll') # accending order (1-100)
stu = StudentModel.objects.all().order_by('-roll') # descending order (1-100)
stu = StudentModel.objects.all().order_by('name') # accending order (A-Z)
stu = StudentModel.objects.all().order_by('-name') # descending order (A-Z)

# ----------- reverse -----------
# use for do reverse order queryset
stu = StudentModel.objects.all().reverse()

# ----------- distinct -----------
# display records unique vales of name fields
stu = StudentModel.objects.values('name').distinct()

# fetch all unique records
stu = StudentModel.objects.all().distinct()

# ----------- exclude -----------
# exclude specific record and show all remain
all_orders = Orders.objects.all().exclude(id=10)

# ----------- values -----------
stu = StudentModel.objects.values('name','roll')
# get queryset with values of (name,roll)
<QuerySet [{'name': 'Ramu', 'roll': 104}, {'name': 'Mehul', 'roll': 102}, {'name': 'Ramu', 'roll': 101}]>

# ----------- value_list -----------
stu = StudentModel.objects.value_list('name','roll')
<QuerySet [('Ramu', 104), ('Mehul', 102), ('suraj', 103), ('Manoj', 104), ('Ramu', 101)]>

# ----------- dates -----------
Entry.objects.dates('created_at', 'year') # all year data entered 
[datetime.date(2005, 1, 1)]
Entry.objects.dates('created_at', 'month') # all month data entered 
[datetime.date(2005, 2, 1), datetime.date(2005, 3, 1)]
Entry.objects.dates('created_at', 'week') # all week data entered 
[datetime.date(2005, 2, 14), datetime.date(2005, 3, 14)]
Entry.objects.dates('created_at', 'day') # all day data entered 
[datetime.date(2005, 2, 20), datetime.date(2005, 3, 20)]
Entry.objects.dates('created_at', 'day', order='DESC') # all day data entered decending order
Entry.objects.dates('created_at', 'day', order='ASC') # all day data entered acending order
[datetime.date(2005, 3, 20), datetime.date(2005, 2, 20)] 
Entry.objects.filter(headline__contains='Lennon').dates('created_at', 'day') # all day data entered by filter
[datetime.date(2005, 3, 20)]

# ----------- none -----------
# Create an empty QuerySet
stu = StudentModel.objects.none()

# ----------- all() -----------
# fetch all record from table
stu = StudentModel.objects.all()

# ----------- union() -----------
d1 = StudentModel.objects.all()
d2 = EmployeeModel.objects.all()
q = q1.union(q2) #q will contain all unique records of q1 + q2
q = q1.union(q2, all=True) #q will contain all records of q1 + q2 including duplicates
q = q1.union(q2,q3) # more than 2 queryset union
# EXAMPLE
>>> print q1
<QuerySet [<MyModel: A>, <MyModel: B>, <MyModel: C>, <MyModel: D>, <MyModel: E>]>
>>> print q2
<QuerySet [<MyModel: A>, <MyModel: B>]>
>>> print q3
<QuerySet [<MyModel: C>, <MyModel: D>]>

>>> q4 = q2.union(q3)
>>> print q4
<QuerySet [<MyModel: A>, <MyModel: B>, <MyModel: C>, <MyModel: D>]>
>>>
>>> q5 = q1.union(q2, q3) #Only distinct objects selected by default
>>> print q5
<QuerySet [<MyModel: A>, <MyModel: B>, <MyModel: C>, <MyModel: D>, <MyModel: E>]>
>>>
>>> q6 = q1.union(q2, q3, all=True) #Include duplicate objects
>>> print q6
<QuerySet [<MyModel: A>, <MyModel: B>, <MyModel: C>, <MyModel: D>, <MyModel: E>, <MyModel: A>, <MyModel: B>, <MyModel: C>, <MyModel: D>]>

students = Student.objects.all().values_list("name", "gender")
authors = Authors.objects.all().values_list("name", "gender")
all = student.union(authors)

# ----------- intersection() -----------
q= q1.intersection(qs2) # return same record in q1 & q2  
q= q1.intersection(qs2, qs3) # return same record in with multiple queryset

# EXAMPLE
>>> q7 = q1.intersection(q2)
>>> print q7
<QuerySet [<MyModel: A>, <MyModel: B>]>
>>> 
>>> q8 = q2.intersection(q3)
>>> print q8
<QuerySet [ ]>
>>> 
>>> q9 = q1.intersection(q2, q3)
>>> print q9
<QuerySet [ ]>
>>>

# ----------- difference() -----------
>>> q10 = q1.difference(q2) #q1 - q2
>>> print q10
<QuerySet [<MyModel: C>, <MyModel: D>, <MyModel: E>]>
>>>
>>> q11 = q1.difference(q2, q3) #q1 - (q2 + q3)
>>> print q11
<QuerySet [<MyModel: E>]>
>>>
>>> q12 = q2.difference(q3) #Will return q2 as q2 and q3 are mutually exclussive
>>> print q12
<QuerySet [<MyModel: A>, <MyModel: B>]>
>>>
>>> q13 = q1.difference(q1) #q1 - q1
>>> print q13
<QuerySet [ ]>

# ----------- select_related() -----------
# select_related used for N+1 SQL Problem soluction
# it is performance Btooster Query
# it convert many query in single query
from django.db import models
class Author(models.Model):
   first_name = models.CharField(max_length=512)
   last_name = models.CharField(max_length=512)
class Book(models.Model):
   title = models.CharField(max_length=512)
   author = models.ForeignKey(Author, on_delete=models.CASCADE)

books = Book.objects.select_related('author') # it's generate single query using INNER JOIN
<QuerySet [<Book: Book object (1)>, <Book: Book object (2)>, <Book: Book object (3)>, <Book: Book object (4)>]>

# ----------- prefetch_related() -----------
# not generate any JOIN
# it's give output for Author without any relationship
# it's generate multiple quries same time 
from django.db import models
class Author(models.Model):
   first_name = models.CharField(max_length=512)
   last_name = models.CharField(max_length=512)

class Book(models.Model):
   title = models.CharField(max_length=512)
   author = models.ForeignKey(Author, on_delete=models.CASCADE)

books = Author.objects.prefetch_related('author') # reverse lookup for ForeignKey
<QuerySet [<Book: Book object (1)>, <Book: Book object (2)>, <Book: Book object (3)>, <Book: Book object (4)>]>

# ----------- transaction.atomic() -----------
# The transaction.atomic function allows you to wrap a code block in a single transaction. 
# If everything in the block executes successfully, the changes are committed to the database. 
# If an error occurs anywhere in the block, all changes are rolled back, and nothing is saved to the database.
from django.db import transaction
from django.core.exceptions import ValidationError

def transfer_funds(sender, receiver, amount):
    try:
        with transaction.atomic():
            # Deduct amount from sender's account
            if sender.balance < amount:
                raise ValidationError("Insufficient funds")
            sender.balance -= amount
            sender.save()

            # Add amount to receiver's account
            receiver.balance += amount
            receiver.save()

    except ValidationError as e:
        print("Transaction failed:", e)



# ------------------------------------------------------------------------------------
# -------------------------- Operators that return new QuerySets ---------------------
# ------------------------------------------------------------------------------------
# ------ AND (&) and OR (|) used for handle complex queries in django ----------------
# ---------------- AND (&) --------------------------  
from django.db.models import Q
criterion1 = Q(question__contains="software")
criterion2 = Q(question__contains="java")
q = Question.objects.filter(criterion1 & criterion2) ----- way-1
q = Question.objects.filter(criterion1 and criterion2) ----- way-2
# ---------------- OR (|) --------------------------  
from django.db.models import Q
User.objects.filter(Q(income__gte=5000) | Q(income__isnull=True)) ----- way-1
User.objects.filter(Q(income__gte=5000) or Q(income__isnull=True)) ----- way-2
# ---------------- NOT (~) --------------------------  
criterion1 = Q(question__contains="software")
criterion2 = Q(question__contains="java")

# Using the & operator with negation
q = Question.objects.filter(~criterion1 & ~criterion2)

# ------------------------------------------------------------------------------------
# -------------------------- Methods that do not return QuerySets --------------------
# ------------------------------------------------------------------------------------
stu = StudentModel.objects.get() # get single object form database
stu = StudentModel.objects.create(name='Rahul', mobile='9999999999', email = 'rahul@email.com' ) # create single object form database
stu = StudentModel.objects.get(name = 'Rahul').update(name="Mehul") # update single object form database
stu, created = StudentModel.objects.get_or_create(first_name='Rahul', mobile='9999999999') # stu = get object ||||| # created = if created object return it

stu, created, updated = StudentModel.objects.update_or_create(
    name='Rahul', mobile='9999999999', email = 'rahul@email.com',
    defaults={'name': 'Mehul'},
)
# created = True / Flase 
# updated = True / Flase
# updated = If person exists with first_name='Rahul' & mobile='9999999999', email = 'rahul@email.com' then update first_name='Mehul'
# Else created=  create new person with first_name='Bob' & last_name='Lennon'


#  -------------- Bulk Create ----------------------
StudentModel.objects.bulk_create([
    StudentModel(name='Rahul', mobile='9999999999', email = 'rahul@email.com'),
    StudentModel(name='Mehul', mobile='8888888888', email = 'mehul@email.com'),
    StudentModel(name='Sharul', mobile='7777777777', email = 'sharul@email.com')
])

#  -------------- Bulk Update ----------------------
update_list = []
model_qs= ModelClass.objects.filter(name = 'bar')
for obj in model_qs:
    model_obj =ModelClass.object.get(id=obj.id)
    model_obj.name = "foo" # Or what ever the value is for simplicty im providing foo only
    update_list.append(model_obj)
    
ModelClass.objects.bulk_update(update_list,['name'])

#  -------------- count() ---------------------
count= StudentModel.objects.all().count() # count all student' object

# ---------------- in_bulk -----------------------
# get which values available in queryset values
>>> Blog.objects.in_bulk([1])
{1: <Blog: Beatles Blog>}
>>> Blog.objects.in_bulk([1, 2])
{1: <Blog: Beatles Blog>, 2: <Blog: Cheddar Talk>}
>>> Blog.objects.in_bulk([])
{}
>>> Blog.objects.in_bulk()
{1: <Blog: Beatles Blog>, 2: <Blog: Cheddar Talk>, 3: <Blog: Django Weblog>}
>>> Blog.objects.in_bulk(['beatles_blog'], field_name='slug')
{'beatles_blog': <Blog: Beatles Blog>}
>>> Blog.objects.distinct('name').in_bulk(field_name='name')
{'Beatles Blog': <Blog: Beatles Blog>, 'Cheddar Talk': <Blog: Cheddar Talk>, 'Django Weblog': <Blog: Django Weblog>}

# ---------------- iterator() -----------------------
stu_set = StudentModel.objects.all()
# The `iterator()` method ensures only a few rows are fetched from the database at a time, saving memory.
for student in stu_set.iterator():
    print(student.name)

# ---------------- latest() -----------------------
# Returns the latest object in the table based on the given field(s).
# This example returns the latest Entry in the table, according to the created_date field:
stu = StudentModel.objects.latest('created_date')


# ---------------- earliest() -----------------------
# Returns the Oldest object in the table based on the given field(s).
# This example returns the Oldest Entry in the table, according to the created_date field:
stu = StudentModel.objects.earliest('created_date')

# ---------------- first() -----------------------
stu = StudentModel.objects.first()

# ---------------- last() -----------------------
stu = StudentModel.objects.last()

# ---------------- aggregate() -----------------------
from django.db.models import Avg, Max, Min, Sum
pro = Product.objects.all().aggregate(Avg('price'))
{'price__avg': 124.0}

pro = Product.objects.all().aggregate(Min('price'))
# {'price__min': 9}

pro = Product.objects.all().aggregate(Sum('price'))
# {'price__sum':92456}

pro = Product.objects.all().aggregate(Max('price'))
# {'price__max':599} 

# ---------------- exists() -----------------------
pro = Product.objects.filter(name='Raj').exists() # True / False (Check object available or not)


# ---------------- update() -----------------------
# Approach 1
MyModel.objects.filter(field1='Computer').update(field2='cool')

#Approach 2    
objects = MyModel.objects.filter(field1='Computer')
for obj in objects:
    obj.field2 = 'cool'
    obj.save()

# ---------------- delete() -----------------------
instance = SomeModel.objects.get(id=id)
instance.delete()



# ------------------------------------------------------------------------------------
# ------------------------------------- Field lookups --------------------------------
# ------------------------------------------------------------------------------------
# ---------------- exact & iexact ------------------------
o_data = Order.objects.filter(psize__iexact='s') # required string exact match, but not required case-sensitive 
o_data = Order.objects.filter(psize__exact='S') # required string exact match as well as case-sensitive 
o_data = Order.objects.filter(psize='S') # required string exact match as well as case-sensitive 

# ---------------- contains & icontains -----------------------
# The BINARY is the exact case (contains)
# the'i' in'icontains' means that case is ignored (icontains)
o_data = Order.objects.filter(psize__contains='S') # (case-sensitive required)
o_data = Order.objects.filter(psize__icontains='s') # (case-sensitive not required)

# ---------------- in -----------------------
stu = StudentModel.objects.filter(pk__in=[1, 2, 3]) # retun all object with matchin ids of list

# ---------------- gt,gte,lt,lte -----------------------
stu = StudentModel.objects.filter(score__gt = 100) # all record fetch with >100
stu = StudentModel.objects.filter(score__gte = 100) # all record fetch with >=100
stu = StudentModel.objects.filter(score__lt = 100) # all record fetch with < 100
stu = StudentModel.objects.filter(score__lte = 100) # all record fetch with <= 100

# ---------------- startswith -----------------------
stu = StudentModel.objects.filter(name__startswith = 'r') # all record get startswith rahul

# ---------------- isstartswith -----------------------
stu = StudentModel.objects.filter(name__isstartswith = 'r') # True / False

# ---------------- endswith -----------------------
stu = StudentModel.objects.filter(name__endswith = 'l') # all record get endswith rahul

# ---------------- isendswith -----------------------
stu = StudentModel.objects.filter(name__isendswith = 'l') # True / False

# ---------------- range -----------------------
stu = StudentModel.objects.filter(date__range=["2011-01-01", "2011-01-31"]) # return all record between dates

# ---------------- year,date,day,week,week_day,quater,hour,minute,second,time,iso_year -----------------------
>>> Entry.objects.dates('pub_date', 'year')
[datetime.date(2005, 1, 1)]
>>> Entry.objects.dates('pub_date', 'month')
[datetime.date(2005, 2, 1), datetime.date(2005, 3, 1)]
>>> Entry.objects.dates('pub_date', 'week')
[datetime.date(2005, 2, 14), datetime.date(2005, 3, 14)]
>>> Entry.objects.dates('pub_date', 'day')
[datetime.date(2005, 2, 20), datetime.date(2005, 3, 20)]
>>> Entry.objects.dates('pub_date', 'day', order='DESC')
[datetime.date(2005, 3, 20), datetime.date(2005, 2, 20)]
>>> Entry.objects.filter(headline__contains='Lennon').dates('pub_date', 'day')
[datetime.date(2005, 3, 20)]


Entry.objects.filter(pub_date__date=datetime.date(2005, 1, 1)) # date
Entry.objects.filter(pub_date__year=2005) # year
Entry.objects.filter(pub_date__iso_year=2005) # iso_year
Entry.objects.filter(pub_date__month=12) # month
Entry.objects.filter(pub_date__day=3) # day
Entry.objects.filter(pub_date__week=52) # week
Entry.objects.filter(pub_date__week_day=2) # week_day
Entry.objects.filter(pub_date__quarter=2) # quarter
Entry.objects.filter(pub_date__time=datetime.time(14, 30)) # time
Event.objects.filter(timestamp__hour=23) # hour
Event.objects.filter(timestamp__minute=29) # minute
Event.objects.filter(timestamp__second=31) # second

# ---------------- isnull -----------------------
Entry.objects.filter(pub_date__isnull=True)

# ---------------- regex -----------------------
Entry.objects.get(title__regex=r'^(An?|The) +') # Case-sensitive regular expression match.

# ---------------- iregex -----------------------
Entry.objects.get(title__iregex=r'^(an?|the) +') # Case-insensitive regular expression match.


# -----------------------------------------------------------------------------------
# -----------------------  Aggregation functions (link) -----------------------------
# -----------------------------------------------------------------------------------
# expression
# output_field
# filter
# **extra
# Avg
# Count
# Max
# Min
# StdDev
# Sum
# Variance

# -----------------------------------------------------------------------------------
# -----------------------  Query-related tools (link) -----------------------------
# -----------------------------------------------------------------------------------

from django.db.models import Q
# Q() objects
User.objects.filter(Q(first_name__startswith='R') | Q(last_name__startswith='D')
# Prefetch() objects
# prefetch_related_objects()
Question.objects.prefetch_related(Prefetch('choice_set')).all()
# FilteredRelation() objects
from django.db.models import FilteredRelation, Q
result_1 = Restaurant.objects.annotate(pizzas_vegetarian=FilteredRelation('pizzas', 
condition=Q(pizzas__vegetarian=True), ), ).filter(pizzas_vegetarian__name__icontains='mozzarella')
# -------------- Second Examle -------------------
class Publisher(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)



book = Book.objects.select_related('publisher').get(id=1)  # Using ForeignKey
book.publisher.name

publisher = Publisher.objects.prefetch_related('book_set').get(id=1) # Using Reverse ForeignKey
books = publisher.book_set.all()


# ------------------- .annotate() ---------------------------
# Counting Related Items
from django.db.models import Count

# Annotate each author with a count of their books
authors = Author.objects.annotate(book_count=Count('book'))

for author in authors:
    print(f"{author.name} has written {author.book_count} books.")

# Summing Values
from django.db.models import Sum

# Annotate each author with the total price of their books
authors = Author.objects.annotate(total_sales=Sum('book__price'))

for author in authors:
    print(f"{author.name} has total sales of ${author.total_sales}.")

# Averaging Values
from django.db.models import Avg

# Annotate each author with the average rating of their books
authors = Author.objects.annotate(average_rating=Avg('book__rating'))

for author in authors:
    print(f"{author.name} has an average book rating of {author.average_rating}.")


# Using Multiple Annotations
authors = Author.objects.annotate(
    book_count=Count('book'),
    total_sales=Sum('book__price')
)

for author in authors:
    print(f"{author.name} has written {author.book_count} books with total sales of ${author.total_sales}.")


# Conditional Annotations with Case and When
from django.db.models import Case, When, IntegerField

# Count only books with a rating of 5
authors = Author.objects.annotate(
    high_rated_books=Count(Case(
        When(book__rating=5, then=1),
        output_field=IntegerField()
    ))
)

for author in authors:
    print(f"{author.name} has {author.high_rated_books} highly-rated books.")

# Aggregation with Filters
from django.db.models import Sum

# Annotate each author with the total price of books published after 2020
authors = Author.objects.annotate(
    recent_books_total=Sum('book__price', filter=models.Q(book__published_year__gt=2020))
)

for author in authors:
    print(f"{author.name} has recent books worth ${author.recent_books_total}.")

# Grouping Data by Field
from django.db.models import Max

# Annotate each author with the highest rating of their books
authors = Author.objects.annotate(highest_rating=Max('book__rating'))

for author in authors:
    print(f"{author.name}'s highest-rated book has a rating of {author.highest_rating}.")


# Combining .annotate() with .filter()
from django.db.models import Count

# First, we annotate, then filter on the annotated field
authors = Author.objects.annotate(book_count=Count('book')).filter(book_count__gt=5)

for author in authors:
    print(f"{author.name} has written {author.book_count} books.")

# Using .annotate() with Mathematical Operations
from django.db.models import Count, Sum, F, FloatField

# Annotate with both total sales and book count, then calculate average price
authors = Author.objects.annotate(
    total_sales=Sum('book__price'),
    book_count=Count('book'),
    avg_price=F('total_sales') / F('book_count')
)

for author in authors:
    print(f"{author.name} has an average book price of ${author.avg_price:.2f}.")

# Conditional Annotation with Boolean Flags
from django.db.models import Case, When, BooleanField

# Annotate each author with a boolean field indicating if they have a book over $50
authors = Author.objects.annotate(
    has_expensive_book=Case(
        When(book__price__gt=50, then=True),
        default=False,
        output_field=BooleanField()
    )
)

for author in authors:
    print(f"{author.name} has an expensive book: {author.has_expensive_book}")



# ------------------- OuterRef and Subquery ---------------------------

from django.db.models import OuterRef, Subquery
from django.db.models import Max

# Subquery to get the latest published date for each author
latest_book_date = Book.objects.filter(author=OuterRef('pk')).order_by('-published_date').values('published_date')[:1]

# Annotate each Author with the date of their most recent book
authors = Author.objects.annotate(latest_book_date=Subquery(latest_book_date))

for author in authors:
    print(author.name, author.latest_book_date)

# ------------------- F Expression ---------------------------
from django.db.models import ExpressionWrapper, DecimalField

# Create a new field with a computed total cost as 'price * quantity'
Item.objects.annotate(
    total_cost=ExpressionWrapper(
        F('price') * F('quantity'),
        output_field=DecimalField()
    )
)


from django.db.models import Case, When, Value, IntegerField

# Annotate items with a flag based on whether quantity is greater than 10
Item.objects.annotate(
    is_in_stock=Case(
        When(quantity__gt=10, then=Value(1)),
        default=Value(0),
        output_field=IntegerField()
    )
)
# Get items where price is greater than cost
Item.objects.filter(price__gt=F('cost'))

# Get items where quantity is equal to items_sold
Item.objects.filter(quantity=F('items_sold'))
# Subtract 5 from the 'price' field
Item.objects.update(price=F('price') - 5)

# Multiply 'discount' by 0.1
Item.objects.update(discount=F('discount') * 0.1)

# Divide 'total' by 2
Item.objects.update(total=F('total') / 2)
