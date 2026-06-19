"""
Knowledge Base Repository - 60+ curated issue-solution records
Covers: Authentication, Payment, Upload, Notification, Profile, Reporting,
        System Errors, Search, Support Tickets, Account Management
"""

KNOWLEDGE_BASE = [
    # ── AUTHENTICATION (10 records) ──────────────────────────────────
    {
        "id": "KB-AUTH-001", "bucket": "Authentication", "issue_type": "Password Reset Failure",
        "solution": "Generate a new password reset link via the admin portal. Ensure the link is valid for 24 hours.",
        "steps": ["Go to Admin Portal > User Management", "Search for the user account", "Click 'Send Password Reset Link'", "Advise user to check spam folder", "Verify user resets within 24 hours"],
        "notes": "Most common cause: expired link or incorrect email used.", "confidence": 0.95, "risk_level": "Low", "avg_resolution_time": "15 mins"
    },
    {
        "id": "KB-AUTH-002", "bucket": "Authentication", "issue_type": "OTP Failure",
        "solution": "Resend OTP to registered mobile number. Verify number is correct in profile.",
        "steps": ["Verify mobile number in user profile", "Click 'Resend OTP'", "Wait 2 minutes before retry", "Check for network carrier delays", "If persists, switch to email OTP"],
        "notes": "OTP delays common with certain telecom operators. Email OTP as fallback.", "confidence": 0.92, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },
    {
        "id": "KB-AUTH-003", "bucket": "Authentication", "issue_type": "Account Locked",
        "solution": "Unlock account from Admin Console after identity verification.",
        "steps": ["Verify user identity via registered email", "Go to Admin Console > Accounts", "Select user and click 'Unlock Account'", "Reset failed attempt counter", "Advise user on password policy"],
        "notes": "Account locks after 5 failed attempts. Always verify identity first.", "confidence": 0.98, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },
    {
        "id": "KB-AUTH-004", "bucket": "Authentication", "issue_type": "MFA Verification Failed",
        "solution": "Re-enroll MFA device or provide temporary bypass code.",
        "steps": ["Check if device time is synced (TOTP is time-sensitive)", "Re-enroll authenticator app", "Generate temporary bypass code from admin panel", "Enable backup email OTP temporarily"],
        "notes": "TOTP failures often due to device clock drift. Sync device clock.", "confidence": 0.88, "risk_level": "Medium", "avg_resolution_time": "20 mins"
    },
    {
        "id": "KB-AUTH-005", "bucket": "Authentication", "issue_type": "Session Expired",
        "solution": "Adjust session timeout settings or clear browser cookies.",
        "steps": ["Clear browser cookies and cache", "Re-login to the application", "Check session timeout configuration", "Advise user to avoid multiple tabs"],
        "notes": "Session timeout default is 30 minutes of inactivity.", "confidence": 0.85, "risk_level": "Low", "avg_resolution_time": "5 mins"
    },
    {
        "id": "KB-AUTH-006", "bucket": "Authentication", "issue_type": "Login Page Not Loading",
        "solution": "Clear browser cache, try incognito mode, check DNS settings.",
        "steps": ["Open incognito/private window", "Navigate to login URL", "Clear browser cache and cookies", "Check DNS resolution", "Test with different browser"],
        "notes": "Often caused by stale cached redirect. Incognito resolves most cases.", "confidence": 0.90, "risk_level": "Low", "avg_resolution_time": "5 mins"
    },
    {
        "id": "KB-AUTH-007", "bucket": "Authentication", "issue_type": "Authentication Error",
        "solution": "Validate credentials and check SSO/LDAP sync status.",
        "steps": ["Confirm username format (email vs username)", "Check LDAP/AD sync logs", "Validate SSO configuration", "Test with local account if SSO", "Check firewall rules for auth service"],
        "notes": "SSO misconfigurations are frequent after AD password changes.", "confidence": 0.87, "risk_level": "Medium", "avg_resolution_time": "30 mins"
    },
    {
        "id": "KB-AUTH-008", "bucket": "Authentication", "issue_type": "Cannot Access Account",
        "solution": "Perform full account audit — check status, roles, and permissions.",
        "steps": ["Check account status (active/suspended)", "Verify role assignments", "Check IP whitelist restrictions", "Review access logs for anomalies", "Re-provision account if needed"],
        "notes": "Suspended accounts require manager approval to reactivate.", "confidence": 0.82, "risk_level": "Medium", "avg_resolution_time": "20 mins"
    },
    {
        "id": "KB-AUTH-009", "bucket": "Authentication", "issue_type": "Auto Logout Issue",
        "solution": "Investigate concurrent session limits and token refresh settings.",
        "steps": ["Check concurrent session policy", "Review JWT/token expiry settings", "Check for forced logout events in logs", "Increase session duration if policy allows"],
        "notes": "Concurrent session limit forces logout on new login from another device.", "confidence": 0.80, "risk_level": "Low", "avg_resolution_time": "15 mins"
    },
    {
        "id": "KB-AUTH-010", "bucket": "Authentication", "issue_type": "Password Reset Link Expired",
        "solution": "Generate new reset link immediately with extended validity.",
        "steps": ["Generate new reset link from admin portal", "Extend link validity to 48 hours if needed", "Send directly to verified email", "Confirm receipt with user"],
        "notes": "Default link validity is 24 hours. Can extend to 48 for special cases.", "confidence": 0.96, "risk_level": "Low", "avg_resolution_time": "5 mins"
    },

    # ── PAYMENT (8 records) ──────────────────────────────────────────
    {
        "id": "KB-PAY-001", "bucket": "Payment", "issue_type": "Payment Failed - Amount Deducted",
        "solution": "Initiate refund investigation. Amount typically returns in 5-7 business days.",
        "steps": ["Collect transaction ID and bank reference", "Check payment gateway logs", "Confirm deduction with bank", "Raise refund ticket with payment team", "Communicate 5-7 day SLA to user"],
        "notes": "Do not promise instant refund. Coordinate with finance team.", "confidence": 0.90, "risk_level": "Medium", "avg_resolution_time": "2 days"
    },
    {
        "id": "KB-PAY-002", "bucket": "Payment", "issue_type": "Refund Not Received",
        "solution": "Track refund status via payment gateway dashboard and escalate if delayed.",
        "steps": ["Get transaction ID from user", "Check refund status in gateway dashboard", "If initiated, share estimated date", "If not initiated, raise urgent refund request", "Provide bank trace ID if available"],
        "notes": "Refunds take 5-10 business days depending on bank.", "confidence": 0.88, "risk_level": "Medium", "avg_resolution_time": "1 day"
    },
    {
        "id": "KB-PAY-003", "bucket": "Payment", "issue_type": "Invoice Not Generated",
        "solution": "Manually trigger invoice generation from billing module.",
        "steps": ["Verify payment was successful", "Go to Billing > Orders", "Select order and click 'Generate Invoice'", "Email invoice to registered address", "Check invoice template settings"],
        "notes": "Auto-invoice triggers may fail during high load. Manual generation resolves.", "confidence": 0.92, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },
    {
        "id": "KB-PAY-004", "bucket": "Payment", "issue_type": "Payment Gateway Timeout",
        "solution": "Retry payment after clearing browser data. Check gateway status page.",
        "steps": ["Check payment gateway status page", "Clear browser cache", "Retry with fresh session", "Use alternate payment method if available", "Escalate to tech team if gateway down"],
        "notes": "Timeout during peak hours. Check gateway status before escalating.", "confidence": 0.85, "risk_level": "Low", "avg_resolution_time": "15 mins"
    },
    {
        "id": "KB-PAY-005", "bucket": "Payment", "issue_type": "Subscription Renewal Failed",
        "solution": "Update payment method and manually trigger renewal.",
        "steps": ["Check card expiry date in payment settings", "Update payment method", "Manually trigger subscription renewal", "Confirm renewal success email", "Set reminder 30 days before next renewal"],
        "notes": "Most failures due to expired cards. Proactive reminders recommended.", "confidence": 0.90, "risk_level": "Medium", "avg_resolution_time": "20 mins"
    },
    {
        "id": "KB-PAY-006", "bucket": "Payment", "issue_type": "Duplicate Payment",
        "solution": "Verify duplicate in transaction records and initiate refund for extra charge.",
        "steps": ["Pull all transactions for the order", "Identify duplicate transaction ID", "Initiate refund for second charge", "Notify user of refund timeline", "Investigate root cause to prevent recurrence"],
        "notes": "Duplicate payments often caused by double-click on pay button.", "confidence": 0.95, "risk_level": "Medium", "avg_resolution_time": "1 day"
    },
    {
        "id": "KB-PAY-007", "bucket": "Payment", "issue_type": "Card Validation Failed",
        "solution": "Verify card details and check with bank for restrictions.",
        "steps": ["Verify card number, CVV, expiry", "Check if card is enabled for online transactions", "Try alternate card", "Contact issuing bank for online restrictions", "Try different payment gateway if available"],
        "notes": "Some banks block international/online transactions by default.", "confidence": 0.82, "risk_level": "Low", "avg_resolution_time": "15 mins"
    },
    {
        "id": "KB-PAY-008", "bucket": "Payment", "issue_type": "Transaction Pending",
        "solution": "Wait 30 minutes; if still pending, check gateway and bank status.",
        "steps": ["Advise user to wait 30 minutes", "Check gateway for pending transaction status", "Contact bank if amount is debited", "If stuck, void and retry the transaction"],
        "notes": "Pending transactions usually auto-resolve within 30 minutes.", "confidence": 0.78, "risk_level": "Medium", "avg_resolution_time": "30 mins"
    },

    # ── UPLOAD (8 records) ───────────────────────────────────────────
    {
        "id": "KB-UPL-001", "bucket": "Upload", "issue_type": "Image Upload Failed",
        "solution": "Check file size limits and supported formats. Try compressing image.",
        "steps": ["Check image size (max 5MB)", "Verify format (JPG/PNG/WEBP only)", "Compress image using online tool", "Retry upload", "Check browser console for errors"],
        "notes": "Max file size 5MB. GIF and TIFF not supported.", "confidence": 0.92, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },
    {
        "id": "KB-UPL-002", "bucket": "Upload", "issue_type": "File Upload Slow",
        "solution": "Check internet speed, reduce file size, try chunked upload.",
        "steps": ["Test internet connection speed", "Split large files into smaller chunks", "Use desktop app if available", "Try different browser", "Contact admin if server-side bottleneck"],
        "notes": "Large file uploads should use chunked upload API.", "confidence": 0.85, "risk_level": "Low", "avg_resolution_time": "15 mins"
    },
    {
        "id": "KB-UPL-003", "bucket": "Upload", "issue_type": "Unsupported File Format",
        "solution": "Convert file to supported format using free tools.",
        "steps": ["Check list of supported formats in help docs", "Convert file using CloudConvert or similar", "Retry upload with converted file", "Request format addition if critical business need"],
        "notes": "Supported: PDF, DOCX, XLSX, JPG, PNG, CSV. No EXE or ZIP.", "confidence": 0.95, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },
    {
        "id": "KB-UPL-004", "bucket": "Upload", "issue_type": "Document Upload Stuck",
        "solution": "Cancel upload, clear browser cache, retry in incognito mode.",
        "steps": ["Cancel the current upload", "Clear browser cache and cookies", "Open incognito window", "Retry upload", "Check upload queue for conflicts"],
        "notes": "Stale upload sessions can freeze UI. Incognito clears state.", "confidence": 0.88, "risk_level": "Low", "avg_resolution_time": "5 mins"
    },
    {
        "id": "KB-UPL-005", "bucket": "Upload", "issue_type": "File Corrupted After Upload",
        "solution": "Re-upload original file; check storage service health.",
        "steps": ["Ask user to re-upload from original source", "Check storage service status", "Validate file hash before and after upload", "If recurring, escalate to infrastructure team"],
        "notes": "Corruption indicates possible storage layer issue. Monitor closely.", "confidence": 0.80, "risk_level": "Medium", "avg_resolution_time": "30 mins"
    },
    {
        "id": "KB-UPL-006", "bucket": "Upload", "issue_type": "Upload Limit Exceeded",
        "solution": "Request quota increase from admin or delete old files.",
        "steps": ["Check current storage usage in settings", "Delete unused files to free space", "Request quota increase from admin", "Consider archiving old uploads"],
        "notes": "Default quota is 2GB per account. Admin can extend to 10GB.", "confidence": 0.93, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },
    {
        "id": "KB-UPL-007", "bucket": "Upload", "issue_type": "Bulk Upload Failed",
        "solution": "Use batch upload API with retry logic. Check for format inconsistencies.",
        "steps": ["Validate CSV/spreadsheet format matches template", "Check for special characters in filenames", "Upload in batches of 50 instead of bulk", "Use API with retry on failure", "Check server logs for specific error"],
        "notes": "Bulk upload limit is 100 files per batch.", "confidence": 0.82, "risk_level": "Low", "avg_resolution_time": "30 mins"
    },
    {
        "id": "KB-UPL-008", "bucket": "Upload", "issue_type": "Image Preview Not Showing",
        "solution": "Clear image cache and force re-render of preview.",
        "steps": ["Hard refresh the page (Ctrl+Shift+R)", "Clear image CDN cache", "Check if image URL is accessible", "Re-upload if preview still missing"],
        "notes": "CDN caching delays can cause 15-30 min preview latency.", "confidence": 0.85, "risk_level": "Low", "avg_resolution_time": "5 mins"
    },

    # ── NOTIFICATION (6 records) ─────────────────────────────────────
    {
        "id": "KB-NOT-001", "bucket": "Notification", "issue_type": "Email Notification Not Received",
        "solution": "Check spam folder, verify email in profile, resend notification.",
        "steps": ["Ask user to check spam/junk folder", "Verify registered email address", "Resend notification from admin panel", "Check email delivery logs (SendGrid/SES)", "Whitelist sender domain"],
        "notes": "Most emails land in spam if sender domain not whitelisted.", "confidence": 0.90, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },
    {
        "id": "KB-NOT-002", "bucket": "Notification", "issue_type": "SMS Notification Not Received",
        "solution": "Verify mobile number, check SMS gateway delivery report.",
        "steps": ["Verify mobile number format (+country code)", "Check SMS gateway logs", "Test with manual SMS trigger", "Check carrier DND registry", "Switch to email notification as fallback"],
        "notes": "DND (Do Not Disturb) registration blocks promotional SMS.", "confidence": 0.87, "risk_level": "Low", "avg_resolution_time": "15 mins"
    },
    {
        "id": "KB-NOT-003", "bucket": "Notification", "issue_type": "Push Notification Delayed",
        "solution": "Check device notification permissions and app background refresh settings.",
        "steps": ["Check app notification permissions", "Enable background app refresh", "Check FCM/APNs service status", "Re-register device token", "Clear app cache"],
        "notes": "iOS background refresh must be enabled for timely push notifications.", "confidence": 0.83, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },
    {
        "id": "KB-NOT-004", "bucket": "Notification", "issue_type": "Duplicate Notification",
        "solution": "Check event listener for duplicate triggers. Deduplicate at gateway level.",
        "steps": ["Check notification event logs for duplicates", "Identify duplicate trigger source", "Apply idempotency key to notification service", "Clear notification queue and reprocess"],
        "notes": "Duplicate notifications often caused by retry logic without idempotency.", "confidence": 0.80, "risk_level": "Low", "avg_resolution_time": "1 hour"
    },
    {
        "id": "KB-NOT-005", "bucket": "Notification", "issue_type": "Webhook Notification Failed",
        "solution": "Validate webhook URL, SSL cert, and retry failed events.",
        "steps": ["Test webhook endpoint with POST request", "Verify SSL certificate validity", "Check firewall/IP whitelist for webhook server", "Retry failed webhook events from dashboard", "Review webhook payload format"],
        "notes": "Webhooks require HTTPS with valid SSL. Self-signed certs rejected.", "confidence": 0.85, "risk_level": "Medium", "avg_resolution_time": "30 mins"
    },
    {
        "id": "KB-NOT-006", "bucket": "Notification", "issue_type": "Alert Preferences Not Saving",
        "solution": "Clear browser storage and re-save preferences.",
        "steps": ["Clear browser localStorage", "Re-navigate to notification settings", "Re-select preferences", "Save and verify with test notification", "Check for browser extension conflicts"],
        "notes": "Browser extensions can block preference save API calls.", "confidence": 0.82, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },

    # ── PROFILE & ACCOUNT (5 records) ────────────────────────────────
    {
        "id": "KB-PRF-001", "bucket": "Profile", "issue_type": "Profile Update Not Saving",
        "solution": "Clear cache, validate input fields, retry profile update.",
        "steps": ["Check for validation errors on fields", "Clear browser cache", "Retry save with minimal changes", "Check if field has character limit", "Report to dev team if persistent"],
        "notes": "Phone number must include country code. Email must be unique.", "confidence": 0.88, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },
    {
        "id": "KB-PRF-002", "bucket": "Profile", "issue_type": "Phone Number Update Failed",
        "solution": "Verify format with country code. Trigger OTP verification.",
        "steps": ["Format number as +[country code][number]", "Trigger OTP to new number", "Verify OTP to confirm change", "Update in backend if OTP bypass needed"],
        "notes": "Phone change requires OTP verification for security.", "confidence": 0.92, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },
    {
        "id": "KB-PRF-003", "bucket": "Profile", "issue_type": "Email Address Update Failed",
        "solution": "Send verification to new email. Confirm old email owns the account.",
        "steps": ["Send verification link to new email", "User must click link within 24 hours", "Old email receives notification of change", "Update confirmed after both steps"],
        "notes": "Email change is a two-step verification process for security.", "confidence": 0.90, "risk_level": "Medium", "avg_resolution_time": "15 mins"
    },
    {
        "id": "KB-PRF-004", "bucket": "Profile", "issue_type": "Avatar Not Updating",
        "solution": "Re-upload image meeting requirements (< 2MB, JPG/PNG).",
        "steps": ["Check image size (max 2MB)", "Verify JPG or PNG format", "Crop to square (1:1 ratio)", "Hard refresh after upload (Ctrl+Shift+R)", "Clear CDN cache if needed"],
        "notes": "Avatars are cached for 24h. Hard refresh usually resolves.", "confidence": 0.88, "risk_level": "Low", "avg_resolution_time": "5 mins"
    },
    {
        "id": "KB-PRF-005", "bucket": "Profile", "issue_type": "User Preferences Reset",
        "solution": "Restore preferences from last saved snapshot in user settings.",
        "steps": ["Check settings revision history", "Restore from last saved state", "Identify trigger of reset (logout/session expiry)", "Enable auto-save preference sync"],
        "notes": "Preferences linked to browser session can reset on logout.", "confidence": 0.78, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },

    # ── REPORTING (5 records) ─────────────────────────────────────────
    {
        "id": "KB-RPT-001", "bucket": "Reporting", "issue_type": "Report Generation Error",
        "solution": "Reduce date range, check data source connectivity, retry generation.",
        "steps": ["Reduce the report date range to < 3 months", "Check data source/database connectivity", "Retry report generation", "Check for memory-intensive filters", "Schedule report for off-peak hours"],
        "notes": "Large date ranges (>6 months) may timeout. Use scheduled reports.", "confidence": 0.85, "risk_level": "Low", "avg_resolution_time": "20 mins"
    },
    {
        "id": "KB-RPT-002", "bucket": "Reporting", "issue_type": "Report Download Failed",
        "solution": "Generate report in smaller chunks or use CSV format.",
        "steps": ["Try CSV instead of PDF/XLSX", "Reduce number of columns", "Generate for smaller date range", "Use email delivery for large reports", "Check browser download permissions"],
        "notes": "Large reports (>50MB) should use async email delivery.", "confidence": 0.87, "risk_level": "Low", "avg_resolution_time": "15 mins"
    },
    {
        "id": "KB-RPT-003", "bucket": "Reporting", "issue_type": "QR Code Not Scannable",
        "solution": "Regenerate QR with higher resolution export setting.",
        "steps": ["Re-export PDF at 300 DPI minimum", "Ensure QR code size is at least 2x2 cm", "Test with multiple scanning apps", "Regenerate QR code from source"],
        "notes": "QR codes below 200px are unreliable. Always export at 300 DPI.", "confidence": 0.90, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },
    {
        "id": "KB-RPT-004", "bucket": "Reporting", "issue_type": "Dashboard Not Loading",
        "solution": "Clear cache, check widget data sources, reload dashboard.",
        "steps": ["Hard refresh dashboard (Ctrl+Shift+R)", "Check if underlying data source is accessible", "Disable filters temporarily", "Reload individual widgets", "Contact dev team if all widgets fail"],
        "notes": "Dashboard load failures often due to stale data source connections.", "confidence": 0.82, "risk_level": "Low", "avg_resolution_time": "15 mins"
    },
    {
        "id": "KB-RPT-005", "bucket": "Reporting", "issue_type": "Incorrect Report Results",
        "solution": "Validate filters, date range, and data refresh schedule.",
        "steps": ["Verify filter configuration", "Check last data refresh timestamp", "Compare with raw data export", "Trigger manual data refresh", "Escalate to data team if mismatch persists"],
        "notes": "Data in reports reflects last scheduled refresh, not real-time.", "confidence": 0.80, "risk_level": "Medium", "avg_resolution_time": "1 hour"
    },

    # ── SYSTEM ERRORS (6 records) ─────────────────────────────────────
    {
        "id": "KB-SYS-001", "bucket": "System", "issue_type": "Application Crash on Startup",
        "solution": "Clear app data, reinstall, check compatibility with OS version.",
        "steps": ["Clear application cache and data", "Reinstall latest version", "Check OS/browser compatibility", "Disable antivirus temporarily", "Check event viewer / crash logs"],
        "notes": "Crashes on startup often due to corrupted local data or version mismatch.", "confidence": 0.85, "risk_level": "Low", "avg_resolution_time": "20 mins"
    },
    {
        "id": "KB-SYS-002", "bucket": "System", "issue_type": "Internal Server Error",
        "solution": "Check server logs, restart affected service, escalate if persistent.",
        "steps": ["Capture exact error message and timestamp", "Check application server logs", "Restart the affected microservice", "Check database connection pool", "Escalate to dev team with logs"],
        "notes": "500 errors need immediate escalation. Do not ask user to retry repeatedly.", "confidence": 0.88, "risk_level": "High", "avg_resolution_time": "1 hour"
    },
    {
        "id": "KB-SYS-003", "bucket": "System", "issue_type": "API Timeout",
        "solution": "Check service health, increase timeout threshold, retry with exponential backoff.",
        "steps": ["Check API service health dashboard", "Identify which API endpoint is timing out", "Increase client timeout if configurable", "Retry with exponential backoff", "Escalate to backend team"],
        "notes": "API timeouts > 30 seconds need backend investigation.", "confidence": 0.83, "risk_level": "Medium", "avg_resolution_time": "30 mins"
    },
    {
        "id": "KB-SYS-004", "bucket": "System", "issue_type": "High Memory / CPU Usage",
        "solution": "Identify resource-heavy processes and optimize or scale infrastructure.",
        "steps": ["Run top/htop to identify process", "Check for memory leaks in application logs", "Restart memory-heavy service", "Scale up instance if needed", "Schedule performance optimization sprint"],
        "notes": "CPU > 85% sustained requires immediate infrastructure action.", "confidence": 0.80, "risk_level": "High", "avg_resolution_time": "2 hours"
    },
    {
        "id": "KB-SYS-005", "bucket": "System", "issue_type": "Database Connection Failed",
        "solution": "Check DB server status, connection pool, and network routes.",
        "steps": ["Check database server status", "Verify connection string and credentials", "Check connection pool limits", "Review network firewall rules", "Restart DB connection pool service"],
        "notes": "DB failures affect all users. Treat as P1 incident.", "confidence": 0.90, "risk_level": "High", "avg_resolution_time": "30 mins"
    },
    {
        "id": "KB-SYS-006", "bucket": "System", "issue_type": "Service Unavailable",
        "solution": "Check deployment status, rollback if recent deployment caused outage.",
        "steps": ["Check service status page", "Identify if recent deployment triggered issue", "Rollback to last stable version if needed", "Notify stakeholders via incident channel", "Post-mortem after recovery"],
        "notes": "Service outages are P1. Follow incident management process.", "confidence": 0.88, "risk_level": "High", "avg_resolution_time": "1 hour"
    },

    # ── SEARCH (4 records) ────────────────────────────────────────────
    {
        "id": "KB-SCH-001", "bucket": "Search", "issue_type": "Search Not Working",
        "solution": "Check search index status and trigger reindex if outdated.",
        "steps": ["Test search with simple keyword", "Check search service health", "Trigger index rebuild if stale", "Clear search cache", "Verify search API is returning results"],
        "notes": "Search index updates every 15 minutes. Reindex takes ~5 minutes.", "confidence": 0.85, "risk_level": "Low", "avg_resolution_time": "15 mins"
    },
    {
        "id": "KB-SCH-002", "bucket": "Search", "issue_type": "Incorrect Search Results",
        "solution": "Review search relevance scoring and filter configurations.",
        "steps": ["Test with exact match query", "Check applied filters", "Review relevance scoring weights", "Clear search filters and retry", "Report to search team if algorithm issue"],
        "notes": "Search uses TF-IDF scoring. Recent data may need re-indexing.", "confidence": 0.78, "risk_level": "Low", "avg_resolution_time": "30 mins"
    },
    {
        "id": "KB-SCH-003", "bucket": "Search", "issue_type": "Advanced Filter Failing",
        "solution": "Reset filters to default and re-apply one at a time to isolate issue.",
        "steps": ["Reset all search filters", "Apply filters one at a time", "Identify conflicting filter combination", "Report specific filter bug to dev team"],
        "notes": "Certain filter combinations create invalid queries. Isolate the conflict.", "confidence": 0.80, "risk_level": "Low", "avg_resolution_time": "20 mins"
    },
    {
        "id": "KB-SCH-004", "bucket": "Search", "issue_type": "No Results Found",
        "solution": "Broaden search terms, check spelling, verify data exists.",
        "steps": ["Check spelling of search term", "Try synonyms or partial match", "Verify data exists in the system", "Check if data is within indexed date range", "Remove special characters from query"],
        "notes": "Empty results may indicate data not yet indexed or incorrect search term.", "confidence": 0.82, "risk_level": "Low", "avg_resolution_time": "5 mins"
    },

    # ── SUPPORT TICKET (4 records) ────────────────────────────────────
    {
        "id": "KB-TKT-001", "bucket": "Support", "issue_type": "Cannot Create Ticket",
        "solution": "Check user role permissions for ticket creation and retry.",
        "steps": ["Verify user has ticket creation permissions", "Check if support portal is accessible", "Clear browser cache", "Try alternate browser", "Admin can create ticket on behalf of user"],
        "notes": "Ticket creation requires 'Support User' role minimum.", "confidence": 0.90, "risk_level": "Low", "avg_resolution_time": "10 mins"
    },
    {
        "id": "KB-TKT-002", "bucket": "Support", "issue_type": "Ticket Status Not Updating",
        "solution": "Manually refresh ticket status from admin panel.",
        "steps": ["Hard refresh the ticket page", "Check ticket status from admin view", "Manually update status if sync issue", "Notify user of correct status via email"],
        "notes": "Status sync issues occur during high ticket volumes.", "confidence": 0.85, "risk_level": "Low", "avg_resolution_time": "5 mins"
    },
    {
        "id": "KB-TKT-003", "bucket": "Support", "issue_type": "Ticket Attachment Upload Failed",
        "solution": "Check file size limit (10MB max) and supported formats for attachments.",
        "steps": ["Check file size (max 10MB per attachment)", "Verify supported formats (PDF, JPG, PNG, DOCX)", "Compress large files before attaching", "Use file sharing link if over limit"],
        "notes": "Ticket attachments max 10MB. Use cloud storage link for larger files.", "confidence": 0.88, "risk_level": "Low", "avg_resolution_time": "5 mins"
    },
    {
        "id": "KB-TKT-004", "bucket": "Support", "issue_type": "Escalation Workflow Not Triggered",
        "solution": "Manually escalate ticket and verify escalation rules configuration.",
        "steps": ["Manually set ticket priority to 'Critical'", "Assign to escalation team", "Check escalation rule configuration", "Verify SLA breach threshold settings", "Test escalation workflow end-to-end"],
        "notes": "Escalation triggers on SLA breach or manual P1 flagging.", "confidence": 0.83, "risk_level": "Medium", "avg_resolution_time": "30 mins"
    },

    # ── ACCOUNT MANAGEMENT (4 records) ───────────────────────────────
    {
        "id": "KB-ACC-001", "bucket": "Account", "issue_type": "Account Suspension",
        "solution": "Review suspension reason, verify compliance, reinstate after review.",
        "steps": ["Check account suspension reason in admin panel", "Collect required documentation from user", "Review with compliance team", "Reinstate account after approval", "Notify user via email"],
        "notes": "Suspended accounts require management approval to reinstate.", "confidence": 0.88, "risk_level": "High", "avg_resolution_time": "1 day"
    },
    {
        "id": "KB-ACC-002", "bucket": "Account", "issue_type": "Account Details Mismatch",
        "solution": "Perform identity verification and correct account data from authoritative source.",
        "steps": ["Collect government ID for verification", "Compare with account records", "Update correct information via admin panel", "Send confirmation to registered email"],
        "notes": "Never update account details without proper identity verification.", "confidence": 0.85, "risk_level": "Medium", "avg_resolution_time": "30 mins"
    },
    {
        "id": "KB-ACC-003", "bucket": "Account", "issue_type": "Slow Account Page",
        "solution": "Profile data optimization — archive old activity logs.",
        "steps": ["Clear browser cache and cookies", "Test on different network", "Archive old activity data in account", "Contact dev team if API response > 3 seconds"],
        "notes": "Account pages slow down with >5000 activity records. Archive periodically.", "confidence": 0.80, "risk_level": "Low", "avg_resolution_time": "15 mins"
    },
    {
        "id": "KB-ACC-004", "bucket": "Account", "issue_type": "Unsubscribe Not Working",
        "solution": "Process manual unsubscribe from email preferences panel.",
        "steps": ["Check if user clicked correct unsubscribe link", "Manually unsubscribe from admin > Email Preferences", "Allow 48h for propagation across systems", "Confirm unsubscription via final confirmation email"],
        "notes": "Unsubscribe propagation takes up to 48 hours across all email lists.", "confidence": 0.90, "risk_level": "Low", "avg_resolution_time": "5 mins"
    },
]

# Bucket taxonomy
BUCKET_LIST = ["Authentication", "Payment", "Upload", "Notification", "Profile", "Reporting", "System", "Search", "Support", "Account"]

# Issue type map per bucket
ISSUE_TYPE_MAP = {
    "Authentication": ["Password Reset Failure", "OTP Failure", "Account Locked", "MFA Verification Failed", "Session Expired", "Login Page Not Loading", "Authentication Error", "Auto Logout Issue"],
    "Payment": ["Payment Failed - Amount Deducted", "Refund Not Received", "Invoice Not Generated", "Payment Gateway Timeout", "Subscription Renewal Failed", "Duplicate Payment", "Card Validation Failed", "Transaction Pending"],
    "Upload": ["Image Upload Failed", "File Upload Slow", "Unsupported File Format", "Document Upload Stuck", "File Corrupted After Upload", "Upload Limit Exceeded", "Bulk Upload Failed", "Image Preview Not Showing"],
    "Notification": ["Email Notification Not Received", "SMS Notification Not Received", "Push Notification Delayed", "Duplicate Notification", "Webhook Notification Failed", "Alert Preferences Not Saving"],
    "Profile": ["Profile Update Not Saving", "Phone Number Update Failed", "Email Address Update Failed", "Avatar Not Updating", "User Preferences Reset"],
    "Reporting": ["Report Generation Error", "Report Download Failed", "QR Code Not Scannable", "Dashboard Not Loading", "Incorrect Report Results"],
    "System": ["Application Crash on Startup", "Internal Server Error", "API Timeout", "High Memory / CPU Usage", "Database Connection Failed", "Service Unavailable"],
    "Search": ["Search Not Working", "Incorrect Search Results", "Advanced Filter Failing", "No Results Found"],
    "Support": ["Cannot Create Ticket", "Ticket Status Not Updating", "Ticket Attachment Upload Failed", "Escalation Workflow Not Triggered"],
    "Account": ["Account Suspension", "Account Details Mismatch", "Slow Account Page", "Unsubscribe Not Working"],
}
