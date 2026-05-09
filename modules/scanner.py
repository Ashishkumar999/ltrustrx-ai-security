import requests


def run_healthcare_scan(target):

    issues = []

    high = 0

    medium = 0

    low = 0

    info = 0


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


        if "Server" in headers:

            issues.append({

                "issue": "Server Version Disclosure",

                "severity": "Low",

                "payload": headers.get("Server"),

                "recommendation": "Hide backend server details"

            })

            low += 1


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


    # RISK SCORING

    risk_points = (

        (high * 15) +

        (medium * 8) +

        (low * 3) +

        (info * 1)

    )


    security_score = max(0, 100 - risk_points)


    risk_level = "LOW"


    if security_score < 40:

        risk_level = "CRITICAL"

    elif security_score < 60:

        risk_level = "HIGH"

    elif security_score < 80:

        risk_level = "MEDIUM"


    summary = {

        "total": len(issues),

        "high": high,

        "medium": medium,

        "low": low,

        "info": info,

        "security_score": security_score,

        "risk_level": risk_level

    }


    return {

        "target": target,

        "issues": issues,

        "summary": summary,

        "pdf_report": ""

    }
