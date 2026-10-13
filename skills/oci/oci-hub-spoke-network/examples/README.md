# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. Inspection

**Prompt:** "Route all spoke traffic through a firewall in OCI."

**Expected behaviour:** Designs DRG route tables, hub VCN ingress routing to Network Firewall, and validates with Network Path Analyzer.

## 2. Hybrid

**Prompt:** "Connect on-prem via FastConnect with VPN backup."

**Expected behaviour:** Designs redundant FastConnect virtual circuits plus IPSec VPN on the DRG with BGP.
