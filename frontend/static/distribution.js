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
            body: JSON.stringify({email: email, source: 'exit-popup', status: 'lead', notes: 'Requested free EU AI Act checklist'})
        }).then(function(response) {
            if (!response.ok) throw new Error('Lead request failed');
            return response.json();
        }).then(function(result) {
            if (!result.success) throw new Error('Lead request failed');
            var popup = document.getElementById('exit-popup');
            popup.innerHTML = '<div style="background:#fff;border-radius:16px;padding:40px;max-width:480px;width:90%;text-align:center;"><h3 style="margin:0 0 8px;color:#111827;">Your checklist is ready</h3><p style="color:#6B7280;">Use the button below to download it. No email has been sent.</p><a href="/api/resource/checklist.pdf" download style="display:inline-block;padding:12px 18px;background:#2563EB;color:#fff;border-radius:8px;text-decoration:none;">Download checklist PDF</a></div>';
        }).catch(function() {
            alert('We could not process your request. Please try again.');
        });
    };

    // Removed fabricated social-proof notifications; show only verified activity.

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
