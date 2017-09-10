# Nginx as a Front-End Proxy

This project offers a out of the box pre-configured `nginx` server running in a docker image.
Simply customise the `nginx.conf` to redirect to the correct services


## Usage
- Customise the `nginx.conf`
- Run `docker-compose up --build -d`

To stop the `nginx`: `docker-compose down`


## Use HTTPS

It is possible and very simple to use `HTTPS` thanks to this project:
- [Certificate generation project](https://gitlab.com/the_blog/letsencrypt-docker-daemon)

### Initial setup
As explained in the `README.md` of the [certificate generation project](https://gitlab.com/the_blog/letsencrypt-docker-daemon).
We need to serve static content.

**To do so:**
- Create a directory.
  - For example in `/https/webroot`
- Serve this directory under `DOMAIN/.well-known/`
  - In the `nginx.conf`:
  ```
    ## SSL Security #####################################
    server {
        listen 80;

        # Serve static content (for the certificate challenge)
        location /.well-known/ {
            root /https/webroot/;
        }
    }
    ## END - SSL Security ###############################
  ```

### Generate the certificate & auto-renew
Follow the instructions on the [certificate generation project](https://gitlab.com/the_blog/letsencrypt-docker-daemon).
