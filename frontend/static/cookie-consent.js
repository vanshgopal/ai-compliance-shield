(function() {
    if (localStorage.getItem('cookieConsent') === 'accepted') return;
    var banner = document.createElement('div');
    banner.id = 'cookie-banner';
    banner.style.cssText = 'position:fixed;bottom:0;left:0;right:0;background:#1F2937;color:#fff;padding:16px 24px;display:flex;align-items:center;justify-content:space-between;z-index:9999;font-family:Inter,sans-serif;font-size:14px;box-shadow:0 -2px 10px rgba(0,0,0,0.1);';
    banner.innerHTML = '<span>We use cookies for analytics (Google Analytics). By continuing, you agree to our <a href="/privacy-policy" style="color:#60A5FA;text-decoration:underline;">Privacy Policy</a>.</span><div><button onclick="acceptCookies()" style="background:#2563EB;color:#fff;border:none;padding:8px 20px;border-radius:6px;cursor:pointer;margin-left:12px;font-weight:600;">Accept</button></div>';
    document.body.appendChild(banner);
    window.acceptCookies = function() {
        localStorage.setItem('cookieConsent', 'accepted');
        banner.remove();
    };
})();
