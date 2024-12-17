# Airflow

## Airflow Astro
 - as alternative, it's possible to use dev container with Astro CLI
 - and follow this tutorial https://www.astronomer.io/docs/learn/get-started-with-airflow/

### The dev container image
```json
{
  "image": "mcr.microsoft.com/devcontainers/universal:2",
  "features": {
    "ghcr.io/astronomer/devcontainer-features/astro-cli:1": {
      "version": "v1.31.0"
    }
  },
  // "postCreateCommand": "bash -i -c 'astro dev start -n --wait 5m'",
  "forwardPorts": [
    8080
  ]
}
```