# Laravel Support in Stedding

This role enables Laravel application deployment using the Stedding infrastructure (Trellis fork). It works alongside the WordPress configuration and allows you to deploy Laravel applications with the same robust, zero-downtime deployment approach.

## Usage

### 1. Define your Laravel site

Laravel sites are defined within the `wordpress_sites.yml` file, just like WordPress sites, but with a `type: laravel` property to distinguish them:

```yaml
wordpress_sites:
  # Normal WordPress site
  example.com:
    # WordPress site configuration...
    
  # Laravel site
  laravel-app:
    type: laravel  # Specify this is a Laravel site
    site_hosts:
      - canonical: laravel-app.test
        redirects:
          - www.laravel-app.test
    local_path: ../laravel-app  # path to your Laravel project
    admin_email: admin@laravel-app.test  # required field but unused for Laravel
    ssl:
      enabled: false
      provider: self-signed
    cache:
      enabled: false
    env:
      # Laravel-specific environment variables
      APP_NAME: "Laravel App"
      APP_ENV: local
      APP_DEBUG: true
      APP_URL: http://laravel-app.test
      MAIL_HOST: mailhog
      MAIL_PORT: 1025
```

### 2. Customizing Nginx Configuration

You can customize the Nginx configuration for your Laravel application by creating a file at:

```
nginx-includes/your-site-name/laravel-site.conf.j2
```

This will be automatically included in your site's server block. A typical Laravel Nginx configuration should set the webroot to `/public` and configure proper URL handling.

### 3. Provisioning

Use the standard Stedding provisioning command:

```bash
ansible-playbook server.yml -e env=<environment>
```

This will detect Laravel sites based on the `type: laravel` property and provision them appropriately.

### 4. Deployment

Deploy Laravel sites using the standard Stedding command:

```bash
ansible-playbook deploy.yml -e "site=your-laravel-site env=<environment>"
```

The deployment process will:
1. Clone your Git repository
2. Install Composer dependencies
3. Set up your .env file
4. Run key generation (if needed)
5. Run migrations (if enabled)
6. Configure proper permissions and symlinks

## Laravel-specific Options

In your site configuration, you can use these Laravel-specific options:

- `run_migrations`: Set to `false` to skip database migrations during deployment (default: `true`)
- `cache_config`: Set to `false` to skip config caching during deployment (default: `true`)

## Directory Structure

Laravel applications expect a directory structure with public-facing files in a `/public` directory. The deployment creates the following structure:

```
/srv/www/your-laravel-site/
├── current -> ./releases/20230424123456
├── releases/
│   └── 20230424123456/
│       ├── app/
│       ├── bootstrap/
│       ├── config/
│       ├── database/
│       ├── public/
│       ├── resources/
│       ├── routes/
│       ├── storage/
│       └── ...
├── shared/
└── logs/
```