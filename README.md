### [MyCakeBox](https://mycakebox.herokuapp.com) a Simple rider booking app built with Django.

This web application is ideal for startups in logistics/delivery sector who are looking for rider booking and CMS for their merchants, riders and for themselves.

##### Features include:

* Google map integration to calculate distance and duration at `datetime.now()`
* Complete Booking list with Datatable.
* Booking details page with Google map integrated to display Origin and Destination of that order.
* Booking status notification to rider and customer (SMS notification is currently turned OFF).

##### Futures impletements:

* Real Time Tracking (Not implement because of paid [Google API Services](https://developers.google.com/maps/pricing-and-plans/)).
* REST API for extending services in Android & iOS.
* Rider Dashboard.
* Superadmin Dashboard.

Visit merchant dashboard [here](https://mycakebox.herokuapp.com/dashboard/merchant/login/)
With login credentials as username: merchant-1 and password: @dmin123

Note: Order status can be changed only from django admin.
Visit admin dashboard [here](https://mycakebox.herokuapp.com/admin)
With login credentials as username: admin-1 and password: @dmin123