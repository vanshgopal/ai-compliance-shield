// AI Compliance Shield - Distribution System
(function() {

    // === EXIT INTENT POPUP ===
    var exitShown = false;
    document.addEventListener('mouseleave', function(e) {
        if (exitShown || e.clientY > 0) return;
        exitShown = true;
        showExitPopup();
    });

    function showExitPopup() {
        var popup = document.createElement('div');
        popup.id = 'exit-popup';
        popup.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.6);z-index:10000;display:flex;align-items:center;justify-content:center;font-family:Inter,sans-serif;';
        popup.innerHTML = '<div style="background:#fff;border-radius:16px;padding:40px;max-width:480px;width:90%;text-align:center;position:relative;"><button onclick="document.getElementById(\'exit-popup\').remove()" style="position:absolute;top:12px;right:16px;background:none;border:none;font-size:24px;cursor:pointer;color:#9CA3AF;">&times;</button><div style="width:64px;height:64px;background:#EFF6FF;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2"><path d="M12 2L2 7v10l10 5 10-5V7L12 2z"/><path d="M9 12l2 2 4-4"/></svg></div><h3 style="margin:0 0 8px;font-size:22px;color:#111827;">Get Your Free EU AI Act Checklist</h3><p style="color:#6B7280;margin:0 0 20px;font-size:15px;">Download the complete 2026 compliance checklist. Know exactly what your AI system needs.</p><input type="email" id="exit-email" placeholder="Enter your work email" style="width:100%;padding:12px 16px;border:1px solid #D1D5DB;border-radius:8px;font-size:15px;box-sizing:border-box;margin-bottom:12px;"><button onclick="submitExitEmail()" style="width:100%;padding:12px;background:#2563EB;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;">Download Free Checklist</button><p style="color:#9CA3AF;font-size:12px;margin-top:12px;">No spam. Unsubscribe anytime.</p></div>';
        document.body.appendChild(popup);
    }

    window.submitExitEmail = function() {
        var email = document.getElementById('exit-email').value;
        if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
            alert('Please enter a valid email address.');
            return;
        }
        fetch('/api/leads', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: email, source: 'exit-popup', status: 'lead', notes: 'Downloaded free EU AI Act checklist'})
        });
        document.getElementById('exit-popup').innerHTML = '<div style="background:#fff;border-radius:16px;padding:40px;max-width:480px;width:90%;text-align:center;"><div style="width:64px;height:64px;background:#F0FDF4;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2"><path d="M9 12l2 2 4-4"/></svg></div><h3 style="margin:0 0 8px;color:#111827;">Check Your Email!</h3><p style="color:#6B7280;">We sent the EU AI Act checklist to <strong>' + email + '</strong></p></div>';
    };

    // === SOCIAL PROOF NOTIFICATIONS ===
    var companies = ['TechCorp', 'DataFlow AI', 'CloudScale', 'InnoTech', 'AI Labs', 'SecureAI', 'ComplianceHub', 'RegTech Pro', 'EU Solutions', 'AI Guard', 'MindBridge', 'DeepLogic', 'NeuralNet Co', 'AlgoShield', 'CodeAudit'];
    var actions = ['just downloaded the compliance checklist', 'requested a demo', 'started a free scan', 'upgraded to Professional', 'is now compliant with EU AI Act'];

    function showNotification() {
        var company = companies[Math.floor(Math.random() * companies.length)];
        var action = actions[Math.floor(Math.random() * actions.length)];
        var notif = document.createElement('div');
        notif.style.cssText = 'position:fixed;bottom:24px;left:24px;background:#fff;border-radius:12px;padding:16px 20px;box-shadow:0 4px 20px rgba(0,0,0,0.15);z-index:9998;font-family:Inter,sans-serif;display:flex;align-items:center;gap:12px;max-width:360px;animation:slideIn 0.3s ease;';
        notif.innerHTML = '<div style="width:40px;height:40px;background:#EFF6FF;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div><div><strong style="color:#111827;">' + company + '</strong> <span style="color:#6B7280;">' + action + '</span><div style="color:#9CA3AF;font-size:12px;margin-top:2px;">Just now</div></div>';
        document.body.appendChild(notif);
        setTimeout(function() { notif.style.opacity = '0'; notif.style.transition = 'opacity 0.3s'; setTimeout(function() { notif.remove(); }, 300); }, 4000);
    }

    // Add CSS animation
    var style = document.createElement('style');
    style.textContent = '@keyframes slideIn { from { transform: translateX(-100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }';
    document.head.appendChild(style);

    // Show notifications periodically
    setTimeout(function() {
        showNotification();
        setInterval(showNotification, 25000 + Math.random() * 15000);
    }, 5000);

    // === REFERRAL TRACKING ===
    var params = new URLSearchParams(window.location.search);
    var ref = params.get('ref');
    if (ref) {
        localStorage.setItem('referral', ref);
        fetch('/api/referral/track', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({referral_code: ref, page: window.location.pathname})
        }).catch(function(){});
    }

})();
