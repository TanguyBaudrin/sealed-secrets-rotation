# Purpose

A simple docker container to renew sealed secrets in a cluster with the latest sealed secret keys

# Status

For now this project will simply list your sealed secrets object as script output

# Next steps

- [ ] Check the latest date for the key generation
- [ ] Go over sealed secrets to reencrypt the one generated before the previous generation date
- [ ] Optionnal: Commit this change to an external repository based on some sealed-secrets annotations

# Usage

Simply build the container image with that command:

```docker build . -t sealed-secrets-rotation```

And run it locally with:

```docker run -v <my_kubeconfig_file>:/root/.kube/config:ro sealed-secrets-rotation```