from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('listing/<int:id>', views.listing, name='listing'),
    path('listing_close/<int:id>', views.listing_close, name='listing_close'),
    path('listing/new', views.new_listing, name='new_listing'),
    path('listings', views.listings, name='listings'),
    path('comment/new', views.new_comment, name='new_comment'),
    path('bid/new', views.new_bid, name="new_bid"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('watchlist/new', views.new_watchlist, name='new_watchlist'),
    path('watchlist/remove', views.remove_watchlist, name='remove_watchlist'),
    path('category/<str:name>', views.list_category, name='list_category'),
    path('categories', views.all_categories, name='all_categories')
]
