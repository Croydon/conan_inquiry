App.wishlist = {};
App.wishlist.$ = $('#wishlistView');
App.wishlist.$wishlistPackages = $('#wishlistPackages')
App.initialized = false;
App.wishlist.onEnter = function() {
    if (this.initialized) {
        return;
    }
    this.initialized = true;

    let generatedhtml = "";
    let sortedWishlist = [];

    $("#numPackagesWishes").text(Object.keys(wishlist_data).length);

    Object.keys(wishlist_data).forEach((key) => {
        sortedWishlist.push([wishlist_data[key]["upvotes"], wishlist_data[key]["issue"], wishlist_data[key]["issuetitle"]]);
    });

    sortedWishlist.sort((a, b) => {
        return b[0] - a[0];
    });

    for(let wish of sortedWishlist) {
        let upvotesOutput = wish[0].toString();
        generatedhtml += "<li><span class='wishlist-upvotes'>👍 " + upvotesOutput + "</span> <a href='https://github.com/conan-io/wishlist/issues/" + wish[1] + "' target='_blank'><span class='wishlist-icons'></span><span class='wishlist-title'>" + wish[2] + "</span></a></li>";
    }

    this.$wishlistPackages.html(generatedhtml);
};
App.wishlist.onEntered = function() {
    $(window).trigger('resize');
};
