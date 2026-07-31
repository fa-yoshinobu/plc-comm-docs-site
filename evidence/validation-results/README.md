# Public validation evidence

Add one directory per accepted run. Each directory contains only:

- `validation-result.json`
- `evidence-manifest.json`

Both files must be the unchanged public artifacts produced by the validation
console. Do not place endpoints, device addresses, raw values, logs, target
snapshots, or other internal diagnostics here.

Regenerate the public page with:

```sh
python scripts/generate_validation_results.py
```
