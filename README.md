# passwnd

Check for breached passwords with k-anonymity

# Usage

To get prompted to enter the password securely, simply run:

    passwnd.py

Alternatively, you can specify the password directly:

    passwnd.py <password>

The latter is not recommended, as it might leak the password to the shell history.

# How it works

1. The password will be hashed with SHA1 and turned to human-readable hex (ASCII)
2. That hex will be trimmed to just the first 5 characters
3. That trimmed result will be submitted to the pwnedpasswords.com database
4. pwnedpasswords.com will return all hashes that begin with that trim
5. We download all returned hashes, and perform a full search locally

This way, we can check if a password was breached, without revealing said password. While simultaneously only requiring
to download a few kB of data instead of GB.
