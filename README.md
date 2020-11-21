# commerce
An eBay-like e-commerce auction site that allows users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

## Features
- **Models:** The application utilizes django models to store information on an sqlite3 database. Multiple models were used to organize users, watchlists, comments, listings and other features.

- **Create Listing:** Users can create listings. They can specify a title for the listing, a text-based description, and what the starting bid should be. Users can also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).

- **Active Listings Page:** The default route of the web application lets users view all of the currently active auction listings. For each active listing, this page displays the title, description, current price, and photo (if one exists for the listing).

- **Listing Page:** Clicking on a listing takes users to a page specific to that listing. On that page, users are able to view all details about the listing, including the current price for the listing.
If the user is signed in, the user wil be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user can be able to remove it.
If the user is signed in, the user can also bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the bid is rejected.
If the user is signed in and is the one who created the listing, the user has the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
If a user is signed in on a closed listing page, and the user has won that auction, the page will say so.
Users who are signed in are able to add comments to the listing page. The listing page displays all comments that have been made on the listing.

- **Watchlist:** Users who are signed in are able to visit a their Watchlist page, which displays all of the listings that a user has added to their watchlist.

- **Categories:** Users will be able to visit a page that displays a list of all listing categories. Clicking on the name of any category will take the user to a page that displays all of the active listings in that category.

