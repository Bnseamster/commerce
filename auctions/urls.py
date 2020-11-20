from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.all_categories, name="all categories"),
    path("categories/<str:category>", views.display_category, name="category"),
    path("watchlist", views.show_watchlist, name="watchlist"),
    path("createlisting", views.create_listing, name="create listing"),
    path("listings/<str:listing_id>", views.listing_page, name="show listing"),
    path("addtowatch/<str:listing_id>", views.addToWatchlist, name="add to watchlist")

]
