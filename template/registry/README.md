# OCI Distribution Specification Registry and GUI-Registry

## Overview

The registry is an implementation of the [OCI Distribution Specification](https://github.com/opencontainers/distribution-spec), providing a standards-based solution for storing and distributing container images.

The `gui-registry` is a web UI for managing the registry, offering a user-friendly interface for common tasks such as pushing, pulling, and managing images.

### Default Credentials

- **Username:** `root`
- **Password:** `root`

## Example Configuration

### External Network Addresses

- **Registry:** [https://registry.cloud.sealos.io](https://registry.cloud.sealos.io)
- **GUI-Registry:** [https://gui-registry.cloud.sealos.io](https://gui-registry.cloud.sealos.io)

### Pushing an Image to the Registry

1. **Login to the Registry:**
    ```sh
    docker login registry.cloud.sealos.io
    ```
    - **Username:** `root`
    - **Password:** `root`

2. **Tag the Image:**
    ```sh
    docker tag nginx:latest registry.cloud.sealos.io/nginx:latest
    ```

3. **Push the Image:**
    ```sh
    docker push registry.cloud.sealos.io/nginx:latest
    ```

4. **Change the root password:**
    Edit the `registry_htpasswd` file in applaunchpad's registry app to change the `root` password using [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt).

    Note: you can ues https://httpd.apache.org/docs/2.4/programs/htpasswd.html to generate the htpasswd file.

5. **Config the registry**
    See: https://distribution.github.io/distribution/about/configuration for more configuration

### Web Management

- **Access Address:** [https://gui-registry.cloud.sealos.io](https://gui-registry.cloud.sealos.io)
- **Username:** `root`
- **Password:** `root`

This setup allows you to manage your container images easily through both command-line operations and a graphical web interface. Make sure to replace the default credentials with more secure options in a production environment.
