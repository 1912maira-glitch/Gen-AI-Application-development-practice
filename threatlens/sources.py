from __future__ import annotations

import base64
import os
from typing import Any
from urllib.parse import urlsplit

import requests
from ipwhois import IPWhois
from monovm_whois import WhoisHandler


VT_BASE_URL = "https://www.virustotal.com/api/v3"
REQUEST_TIMEOUT = 15


def _result(
    source: str,
    success: bool,
    data: dict[str, Any] | None = None,
    error: str | None = None,
) -> dict:
    return {
        "source": source,
        "success": success,
        "data": data or {},
        "error": error,
    }


def _get_virustotal_key() -> str | None:
    """
    Read the VirusTotal key from the environment.

    app.py may bridge Streamlit secrets into this process environment,
    keeping this module completely independent of Streamlit.
    """
    return os.getenv("VIRUSTOTAL_API_KEY")


def _vt_get(
    path: str,
    api_key: str,
) -> dict:
    response = requests.get(
        f"{VT_BASE_URL}{path}",
        headers={
            "x-apikey": api_key,
            "Accept": "application/json",
        },
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    payload = response.json()

    if not isinstance(payload, dict):
        raise ValueError(
            "VirusTotal returned a non-object response."
        )

    if not isinstance(
        payload.get("data"),
        (dict, list),
    ):
        raise ValueError(
            "VirusTotal returned an unexpected response structure."
        )

    return payload


def _compact_vt_object(
    payload: dict,
) -> dict:
    """
    Extract useful intelligence while avoiding unnecessarily huge
    scanner payloads.
    """
    obj = payload.get("data", {})

    if not isinstance(obj, dict):
        raise ValueError(
            "VirusTotal object data is missing."
        )

    attributes = obj.get(
        "attributes",
        {},
    )

    if not isinstance(attributes, dict):
        raise ValueError(
            "VirusTotal object attributes are missing."
        )

    stats = attributes.get(
        "last_analysis_stats",
        {},
    )

    if not isinstance(stats, dict):
        stats = {}

    result = {
        "type": obj.get("type"),
        "id": obj.get("id"),
        "reputation": attributes.get("reputation"),
        "last_analysis_stats": stats,
        "last_analysis_date": attributes.get(
            "last_analysis_date"
        ),
        "first_submission_date": attributes.get(
            "first_submission_date"
        ),
    }

    # Preserve useful provider-specific context when available.
    for field in (
        "country",
        "continent",
        "asn",
        "as_owner",
        "network",
        "registrar",
        "creation_date",
        "expiration_date",
        "categories",
        "times_submitted",
        "total_votes",
        "url",
    ):
        if field in attributes:
            result[field] = attributes[field]

    # Instead of forwarding potentially hundreds of scanner records,
    # retain the scanners that explicitly marked the target
    # malicious or suspicious.
    scanner_results = attributes.get(
        "last_analysis_results"
    )

    if isinstance(scanner_results, dict):
        flagged = {}

        for engine, engine_data in scanner_results.items():
            if not isinstance(engine_data, dict):
                continue

            category = engine_data.get(
                "category"
            )

            if category in {
                "malicious",
                "suspicious",
            }:
                flagged[engine] = {
                    "category": category,
                    "result": engine_data.get(
                        "result"
                    ),
                    "method": engine_data.get(
                        "method"
                    ),
                }

        result["flagged_engines"] = flagged

    return result


def get_virustotal(
    target_type: str,
    target: str,
) -> dict:
    """
    Collect VirusTotal intelligence.

    Returns:
        {
            "source": "VirusTotal",
            "success": True/False,
            "data": {...},
            "error": None or "..."
        }
    """
    api_key = _get_virustotal_key()

    if not api_key:
        return _result(
            "VirusTotal",
            False,
            error=(
                "VIRUSTOTAL_API_KEY is not configured."
            ),
        )

    try:
        if target_type == "IP Address":
            path = f"/ip_addresses/{target}"

        elif target_type == "Domain":
            path = f"/domains/{target}"

        elif target_type == "URL":
            # VirusTotal accepts the URL identifier as URL-safe
            # Base64 without "=" padding.
            url_id = (
                base64.urlsafe_b64encode(
                    target.encode("utf-8")
                )
                .decode("ascii")
                .rstrip("=")
            )

            path = f"/urls/{url_id}"

        else:
            return _result(
                "VirusTotal",
                False,
                error=(
                    f"Unsupported target type: {target_type}"
                ),
            )

        payload = _vt_get(
            path,
            api_key,
        )

        return _result(
            "VirusTotal",
            True,
            _compact_vt_object(payload),
        )

    except requests.Timeout:
        return _result(
            "VirusTotal",
            False,
            error="VirusTotal request timed out.",
        )

    except requests.HTTPError as exc:
        response = exc.response

        status = (
            response.status_code
            if response is not None
            else "unknown"
        )

        detail = ""

        if response is not None:
            try:
                body = response.json()
                error = body.get(
                    "error",
                    {},
                )

                if isinstance(error, dict):
                    detail = str(
                        error.get(
                            "message",
                            "",
                        )
                    )[:300]

            except (
                ValueError,
                AttributeError,
            ):
                pass

        suffix = (
            f": {detail}"
            if detail
            else ""
        )

        return _result(
            "VirusTotal",
            False,
            error=(
                f"VirusTotal HTTP error "
                f"{status}{suffix}"
            ),
        )

    except requests.RequestException as exc:
        return _result(
            "VirusTotal",
            False,
            error=(
                f"VirusTotal network error: {exc}"
            ),
        )

    except (
        ValueError,
        KeyError,
        TypeError,
    ) as exc:
        return _result(
            "VirusTotal",
            False,
            error=(
                f"VirusTotal response error: {exc}"
            ),
        )

    except Exception as exc:
        return _result(
            "VirusTotal",
            False,
            error=(
                f"Unexpected VirusTotal error: "
                f"{type(exc).__name__}: {exc}"
            ),
        )


def _domain_from_target(
    target_type: str,
    target: str,
) -> str | None:
    if target_type == "Domain":
        return target.rstrip(".").lower()

    if target_type == "URL":
        parsed = urlsplit(target)

        if parsed.hostname:
            return parsed.hostname.rstrip(".").lower()

    return None


def _json_safe(
    value: Any,
) -> Any:
    if value is None:
        return None

    if isinstance(
        value,
        (str, int, float, bool),
    ):
        return value

    if isinstance(
        value,
        (list, tuple, set),
    ):
        return [
            _json_safe(item)
            for item in value
        ]

    if isinstance(value, dict):
        return {
            str(key): _json_safe(item)
            for key, item in value.items()
        }

    return str(value)


def get_whois(
    target_type: str,
    target: str,
) -> dict:
    """
    Collect WHOIS/RDAP intelligence.

    IP addresses use the ipwhois library.
    Domains and URL hostnames use the domain WHOIS library.

    Returns:
        {
            "source": "WHOIS",
            "success": True/False,
            "data": {...},
            "error": None or "..."
        }
    """

    # ------------------------------------------------------------
    # IP ADDRESS
    # ------------------------------------------------------------
    if target_type == "IP Address":
        try:
            ip_result = IPWhois(
                target,
                timeout=15,
            ).lookup_rdap(
                inc_raw=True,
                retry_count=2,
            )

            if not isinstance(ip_result, dict):
                return _result(
                    "WHOIS",
                    False,
                    error="IP WHOIS returned an unexpected response.",
                )

            # Keep the useful network-registration information while
            # avoiding unnecessary raw payload size.
            data = {
                "query": target,
                "lookup_type": "RDAP",
                "asn": ip_result.get("asn"),
                "asn_description": ip_result.get(
                    "asn_description"
                ),
                "asn_country_code": ip_result.get(
                    "asn_country_code"
                ),
                "asn_registry": ip_result.get(
                    "asn_registry"
                ),
                "network": _json_safe(
                    ip_result.get("network")
                ),
                "entities": _json_safe(
                    ip_result.get("entities")
                ),
                "objects": _json_safe(
                    ip_result.get("objects")
                ),
                "raw": _json_safe(
                    ip_result.get("raw")
                ),
            }

            return _result(
                "WHOIS",
                True,
                data,
            )

        except Exception as exc:
            return _result(
                "WHOIS",
                False,
                error=(
                    f"IP WHOIS/RDAP lookup failed: "
                    f"{type(exc).__name__}: {exc}"
                ),
            )

    # ------------------------------------------------------------
    # DOMAIN / URL
    # ------------------------------------------------------------
    domain = _domain_from_target(
        target_type,
        target,
    )

    if not domain:
        return _result(
            "WHOIS",
            False,
            error=(
                "Could not extract a domain for WHOIS lookup."
            ),
        )

    try:
        record = WhoisHandler.whois(
            domain,
            socket_timeout=10.0,
            http_timeout=15.0,
            verify_ssl=True,
        )

        if record.is_available():
            availability_status = "available"
        elif record.is_premium():
            availability_status = "premium"
        else:
            availability_status = "unavailable"

        data = {
            "domain": domain,
            "availability_status": availability_status,
            "tld": record.get_tld(),
            "sld": record.get_sld(),
            "whois_message": (
                record.get_raw_whois_message()[:12000]
            ),
            "availability_details": _json_safe(
                record.get_availability_details()
            ),
        }

        return _result(
            "WHOIS",
            True,
            data,
        )

    except Exception as exc:
        return _result(
            "WHOIS",
            False,
            error=(
                f"WHOIS lookup failed: "
                f"{type(exc).__name__}: {exc}"
            ),
        )


# -------------------------------------------------------------------
# SOURCE REGISTRY
#
# This dictionary is the architectural abstraction boundary.
#
# To add a new source:
#
#   def get_abuseipdb(target_type, target):
#       ...
#
#   SOURCES["AbuseIPDB"] = get_abuseipdb
#
# No orchestration/UI/prompt/rendering changes are required.
# -------------------------------------------------------------------

SOURCES = {
    "VirusTotal": get_virustotal,
    "WHOIS": get_whois,
}
