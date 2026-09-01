// Razorpay Payment Integration
let razorpayKeyId = '';
const PLAN_DISPLAY = { starter: 'Starter', professional: 'Professional', enterprise: 'Enterprise' };

async function initPayment() {
    try {
        const res = await fetch('/api/payment/config');
        const config = await res.json();
        razorpayKeyId = config.key_id;
    } catch (e) {
        console.error('Payment config failed:', e);
    }
}

async function buy(plan) {
    if (!razorpayKeyId) {
        alert('Payment system is warming up. Please try again in a moment.');
        return;
    }
    document.getElementById('payPlanName').textContent = PLAN_DISPLAY[plan] || plan;
    document.getElementById('payPlan').value = plan;
    document.getElementById('paymentModal').style.display = 'flex';
}

async function submitPayment() {
    const plan = document.getElementById('payPlan').value;
    const company = document.getElementById('payCompany').value.trim();
    const email = document.getElementById('payEmail').value.trim();

    if (!company || !email) {
        alert('Please enter your company name and work email.');
        return;
    }
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    const btn = document.getElementById('paySubmit');
    btn.disabled = true;
    btn.textContent = 'Processing...';

    try {
        const res = await fetch('/api/payment/create-order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ plan: plan, price: 0, company: company, email: email })
        });
        const data = await res.json();

        if (!data.order_id) {
            btn.disabled = false;
            btn.textContent = 'Start Payment';
            alert('Payment system error. Please contact support.');
            return;
        }

        openCheckout(data, plan, company, email);
    } catch (e) {
        console.error('Order creation failed:', e);
        btn.disabled = false;
        btn.textContent = 'Start Payment';
        alert('Payment system error. Please contact support.');
    }
}

function openCheckout(data, plan, company, email) {
    const options = {
        key: data.key_id,
        amount: data.amount,
        currency: data.currency,
        name: 'AI Compliance Shield',
        description: PLAN_DISPLAY[plan] + ' plan — ' + company,
        order_id: data.order_id,
        prefill: { email: email },
        notes: { plan: plan, company: company, email: email },
        theme: { color: '#2563EB' },
        handler: function (response) {
            verifyPayment(response, plan, company, email);
        },
        modal: { ondismiss: function () {
            document.getElementById('paySubmit').disabled = false;
            document.getElementById('paySubmit').textContent = 'Start Payment';
        } }
    };
    const rzp = new Razorpay(options);
    rzp.open();
}

async function verifyPayment(response, plan, company, email) {
    closeModal();
    const statusEl = document.getElementById('payStatus');
    statusEl.style.display = 'block';
    statusEl.textContent = 'Verifying payment...';

    try {
        const res = await fetch('/api/payment/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature
            })
        });
        const data = await res.json();

        if (data.success) {
            try {
                await fetch('/api/leads', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: company,
                        email: email,
                        company: company,
                        status: 'qualified',
                        notes: 'PAID ' + PLAN_DISPLAY[plan] + ' via Razorpay. Payment ID: ' + response.razorpay_payment_id
                    })
                });
            } catch (e) { /* log failure is not critical */ }

            statusEl.style.color = '#22c55e';
            statusEl.textContent = 'Payment successful! Your plan is being activated. We will contact you within 24 hours.';
        } else {
            statusEl.style.color = '#ef4444';
            statusEl.textContent = 'Payment verification failed. Contact support with payment ID: ' + response.razorpay_payment_id;
        }
    } catch (e) {
        statusEl.style.color = '#ef4444';
        statusEl.textContent = 'Could not verify payment. Contact support with payment ID: ' + response.razorpay_payment_id;
    }
}

function closeModal() {
    document.getElementById('paymentModal').style.display = 'none';
    document.getElementById('paySubmit').disabled = false;
    document.getElementById('paySubmit').textContent = 'Start Payment';
    document.getElementById('payCompany').value = '';
    document.getElementById('payEmail').value = '';
}

document.addEventListener('DOMContentLoaded', function () {
    initPayment();

    document.querySelectorAll('.buy-btn').forEach(function (button) {
        button.addEventListener('click', function () {
            const plan = this.dataset.plan;
            if (plan === 'free') return;
            buy(plan);
        });
    });

    const paySubmit = document.getElementById('paySubmit');
    if (paySubmit) {
        paySubmit.addEventListener('click', submitPayment);
    }

    const payCancel = document.getElementById('payCancel');
    if (payCancel) {
        payCancel.addEventListener('click', closeModal);
    }
});