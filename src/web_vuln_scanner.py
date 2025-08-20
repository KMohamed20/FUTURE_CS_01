# src/web_vuln_scanner.py
"""
Web Vulnerability Scanner for Task 1
Detects: SQL Injection, XSS, Weak Authentication
"""
import requests
import sys

# Target URL (must match where app.py is running)
TARGET = "http://localhost:5000"

def test_sql_injection():
    """Test for SQL Injection vulnerability"""
    payload = "' OR '1'='1"
    data = {"username": payload, "password": "random"}
    try:
        r = requests.post(TARGET, data=data)
        # Check if SQL-like behavior or error is exposed
        if "SELECT" in r.text or "syntax" in r.text.lower() or r.status_code == 500:
            return True, f"SQLi detected with payload: {payload}"
    except:
        return False, "Connection failed"
    return False, ""

def test_xss():
    """Test for Cross-Site Scripting vulnerability"""
    payload = "<script>alert('XSS')</script>"
    data = {"username": payload, "password": "test"}
    try:
        r = requests.post(TARGET, data=data)
        if payload in r.text:
            return True, f"XSS detected: {payload}"
    except:
        return False, "Connection failed"
    return False, ""

def test_weak_auth():
    """Test for weak/default credentials"""
    data = {"username": "admin", "password": "admin"}
    try:
        r = requests.post(TARGET, data=data)
        if "Login Successful" in r.text:
            return True, "Default credentials 'admin:admin' work"
    except:
        return False, "Connection failed"
    return False, ""

def main():
    print("[+] Starting Web Vulnerability Scan on", TARGET)
    issues = []

    # Run tests
    sql_result, sql_msg = test_sql_injection()
    if sql_result:
        issues.append("🔴 SQL Injection: User input not sanitized")

    xss_result, xss_msg = test_xss()
    if xss_result:
        issues.append("🔴 Cross-Site Scripting (XSS): Script execution possible")

    auth_result, auth_msg = test_weak_auth()
    if auth_result:
        issues.append("🔴 Weak Authentication: Default admin credentials work")

    # Print results
    if not issues:
        print("✅ No critical vulnerabilities found.")
    else:
        print(f"🚨 {len(issues)} vulnerabilities found:")
        for issue in issues:
            print(f"  {issue}")

    # Generate security report
    with open("../docs/security_report.md", "w") as f:
        f.write("# 🛡️ Security Assessment Report\n\n")
        f.write("## Target: Sample Flask Login App (http://localhost:5000)\n\n")
        f.write("### Vulnerability Scan Results\n\n")
        if issues:
            f.write("🔴 **Critical Issues Found**:\n\n")
            for issue in issues:
                f.write(f"- {issue}\n")
        else:
            f.write("✅ No critical issues detected.\n")
        f.write("\n### Recommendations\n\n")
        f.write("- Use parameterized queries to prevent SQLi\n")
        f.write("- Sanitize and escape user input to prevent XSS\n")
        f.write("- Enforce strong passwords and disable default accounts\n")
        f.write("- Implement rate limiting and logging\n")

    print("[+] Scan complete. Report saved to docs/security_report.md")

if __name__ == "__main__":
    main()
