"""
OptiChroma Core Module Compatibility Layer (v2.2 -> v2.3)
=========================================================
Forwards all calls to the audited, implementation-corrected OptiChromaCoreV2_3 engine.
"""

from optichroma_v2_3_core import OptiChromaCoreV2_3 as OptiChromaCoreV2_2
from optichroma_v2_3_core import OptiChromaCoreV2_3

__all__ = ["OptiChromaCoreV2_2", "OptiChromaCoreV2_3"]
