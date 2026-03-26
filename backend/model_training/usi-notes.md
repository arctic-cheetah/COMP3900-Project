# Edit distance

# What to do
## 1) hostname vs full URL
Similarity should usually be computed on domain name, not the fkin full URL string!

Reason: paths/queries vary widely and create noise.

Example:
- Requires retraining
- Blacklist, whitelist or allowlist => size can impactperformanc

## 2) Need to normalise/canonicalise URL 

Input: URL String 
Output: Normalised domain name string:

### What to normalise:
1) Parse url 
2) Normalise 
    - Lower case
    - Strip trailing dot?
    - drop www.?
3) IDN + Punycode convert 
    - decode utf-8 characters to xn--....
    - reduces homograph attacks
    - or even NKFC 
```python
import unicodedata
# Example with a 
ligaturetext = "ﬁle"
nfkc_text = unicodedata.normalize('NFKC', text)
# Output: "file"
```
## 3) Apply Edit distance definition
d=lev(a,b)
L=max⁡(∣a∣,∣b∣)

Similarity ratio 
s = 1 - d/L
USI = 100 * max(0, min(1,s))


## 4) Determine if whitelist vs blacklist required
Most likely need two list or one as a feature variable

USI-bad and USI-good 

1) Blacklist 

Exact membership check: domain ∈ BLACKLIST ⇒ block
Usually NOT used for fuzzy similarity (attackers rarely imitate malicious domains)

2) Whitelist 
Used for similarity checks: attacker imitates a known good brand/domain




