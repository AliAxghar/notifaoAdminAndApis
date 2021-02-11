

// Get Stripe publishable key
fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
  $(".submitBtn").on("click", () => {
    fetch("/create-checkout-session/")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log("data" ,data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    
    .then((res) => {
      alert(res);
    });
  });
});