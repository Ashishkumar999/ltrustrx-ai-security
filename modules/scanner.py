import requests


def run_healthcare_scan(target):

    issues = []

    high = 0

    medium = 0

    low = 0

    info = 0


    # CHECK SECURITY HEADERS

    try:

        response = requests.get(target, timeout=5)

        headers = response.headers


        required_headers = [

            "Content-Security-Policy",

            "X-Content-Type-Options",

            "X-Frame-Options"

        ]


        for header in required_headers:

            if header not in headers:

                issues.append({

                    "issue": f"Missing Security Header: {header}",

                    "severity": "Medium",

                    "payload": "HTTP Header Analysis",

                    "recommendation": f"Add {header} header"

                })

                medium += 1


        # CHECK SERVER DISCLOSURE

        if "Server" in headers:

            issues.append({

                "issue": "Server Version Disclosure",

                "severity": "Low",

                "payload": headers.get("Server"),

                "recommendation": "Hide backend server details"

            })

            low += 1


        # CHECK ADMIN PANEL

        admin_paths = [

            "/admin",

            "/dashboard",

            "/debug"

        ]


        for path in admin_paths:

            url = target.rstrip("/") + path

            try:

                r = requests.get(url, timeout=3)

                if r.status_code == 200:

                    issues.append({

                        "issue": f"Exposed Endpoint: {path}",

                        "severity": "High",

                        "payload": url,

                        "recommendation": "Restrict admin access"

                    })

                    high += 1

            except:

                pass


    except Exception as e:

        issues.append({

            "issue": "Connection Error",

            "severity": "Info",

            "payload": str(e),

            "recommendation": "Verify target availability"

        })

        info += 1


    summary = {

        "total": len(issues),

        "high": high,

        "medium": medium,

        "low": low,

        "info": info

    }


    return {

        "target": target,

        "issues": issues,

        "summary": summary,

        "pdf_report": ""

    }
