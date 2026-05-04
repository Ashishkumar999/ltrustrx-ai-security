import requests

def scan_api(url):
    result = {
        "target": url,
        "issues": []
    }

    try:
        response = requests.get(url)

        # 1. Check if no authentication
        if response.status_code == 200:
            result["issues"].append({
                "type": "No Authentication",
                "severity": "Medium",
                "description": "Endpoint accessible without authentication"
            })

        # 2. Basic IDOR pattern check (very simple)
        test_url = url + "?id=1"
        test_response = requests.get(test_url)

        if test_response.status_code == 200:
            result["issues"].append({
                "type": "Potential IDOR",
                "severity": "High",
                "description": "ID parameter manipulation possible"
            })

    except Exception as e:
        result["issues"].append({
            "type": "Error",
            "severity": "Low",
            "description": str(e)
        })

    return result
