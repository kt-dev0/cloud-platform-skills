# Read-only Azure Resource Graph queries

Run these with `az graph query -q "<query>" --first 1000`. This needs the `resource-graph` CLI extension: `az extension add --name resource-graph`. Add `--subscriptions <id>` or `--management-groups <id>` to stay within the user's scope.

All of these are read-only.

## Inventory

```kusto
resources
| summarize count() by type, location
| order by count_ desc
```

## Advisor recommendations by pillar

```kusto
advisorresources
| where type == 'microsoft.advisor/recommendations'
| extend category = tostring(properties.category), impact = tostring(properties.impact), problem = tostring(properties.shortDescription.problem)
| summarize count() by category, impact, problem
| order by category asc, impact asc
```

## Security: storage accounts allowing public blob access or weak TLS

```kusto
resources
| where type =~ 'microsoft.storage/storageaccounts'
| extend publicBlob = tobool(properties.allowBlobPublicAccess), minTls = tostring(properties.minimumTlsVersion), publicNetwork = tostring(properties.publicNetworkAccess)
| where publicBlob == true or minTls != 'TLS1_2' or publicNetwork =~ 'Enabled'
| project name, resourceGroup, publicBlob, minTls, publicNetwork
```

## Security: Key Vaults without purge protection

```kusto
resources
| where type =~ 'microsoft.keyvault/vaults'
| extend purgeProtection = tobool(properties.enablePurgeProtection)
| where purgeProtection != true
| project name, resourceGroup
```

## Security: public IP addresses

```kusto
resources
| where type =~ 'microsoft.network/publicipaddresses'
| project name, resourceGroup, ipAddress = tostring(properties.ipAddress), attached = isnotnull(properties.ipConfiguration)
```

## Cost: unattached managed disks

```kusto
resources
| where type =~ 'microsoft.compute/disks'
| where tostring(properties.diskState) =~ 'Unattached'
| project name, resourceGroup, sku = tostring(sku.name), sizeGb = toint(properties.diskSizeGB)
```

## Cost / governance: untagged resources

```kusto
resources
| where isnull(tags) or tostring(tags) == '{}'
| summarize untagged = count() by type
| order by untagged desc
```

## Reliability: virtual machines without availability zones

```kusto
resources
| where type =~ 'microsoft.compute/virtualmachines'
| where isnull(zones) or array_length(zones) == 0
| project name, resourceGroup, location, size = tostring(properties.hardwareProfile.vmSize)
```
