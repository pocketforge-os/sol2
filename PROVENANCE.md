# Provenance

| Field | Value |
| --- | --- |
| Canonical upstream | `https://github.com/ThePhD/sol2.git` |
| Upstream base | `2b0d2fe8ba0074e16b499940c4f3126b9c7d3471` |
| Licence | `LICENSE.txt` |
| PocketForge patch | Restore string-view proxy conversion and functional associative iteration in the generated header source. |

The PocketForge patch series is based directly on the upstream commit above.
`tests/single_header_snapshot.py` regenerates the amalgamation twice with fixed
source metadata, normalizes only the generator timestamp, and checks the exact
corrected snapshot digest.
