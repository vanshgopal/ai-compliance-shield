// Stripe Payment Integration
// Replace with your actual Stripe publishable key
const STRIPE_PUBLIC_KEY = 'pk_live_YOUR_STRIPE_KEY_HERE';

let stripe;
let elements;
let paymentElement;

// Initialize Stripe
function initStripe() {
    if (STRIPE_PUBLIC_KEY === 'pk_live_YOUR_STRIPE_KEY_HERE') {
        console.log('Stripe key not configured. Using demo mode.');
        return;
    }
    stripe = Stripe(STRIPE_PUBLIC_KEY);
}

// Create payment session
async function createPaymentSession(plan, price) {
    try {
        const response = await fetch('/api/create-payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                plan: plan,
                price: price,
                success_url: window.location.origin + '/payment-success',
                cancel_url: window.location.origin + '/pricing'
            })
        });

        const data = await response.json();

        if (data.url) {
            // Redirect to Stripe Checkout
            window.location.href = data.url;
        } else if (data.session_id) {
            // Use Stripe Elements
            showPaymentForm(data.session_id);
        }
    } catch (error) {
        console.error('Payment error:', error);
        alert('Payment system not configured yet. Please contact support.');
    }
}

// Show payment form (if using Stripe Elements)
function showPaymentForm(sessionId) {
    const paymentModal = document.getElementById('paymentModal');
    if (paymentModal) {
        paymentModal.style.display = 'flex';
    }

    if (stripe) {
        elements = stripe.elements({ clientSecret: sessionId });
        paymentElement = elements.create('payment');
        paymentElement.mount('#payment-element');
    }
}

// Handle payment submission
async function handlePayment(event) {
    event.preventDefault();

    if (!stripe || !paymentElement) {
        alert('Payment system not configured yet.');
        return;
    }

    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            return_url: window.location.origin + '/payment-success',
        },
    });

    if (error) {
        alert(error.message);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initStripe();

    // Add click handlers to buy buttons
    document.querySelectorAll('.buy-btn').forEach(button => {
        button.addEventListener('click', function() {
            const plan = this.dataset.plan;
            const price = this.dataset.price;
            createPaymentSession(plan, price);
        });
    });

    // Add payment form handler
    const paymentForm = document.getElementById('paymentForm');
    if (paymentForm) {
        paymentForm.addEventListener('submit', handlePayment);
    }
});
