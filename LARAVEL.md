# Laravel Support in Stedding

Stedding has been extended to support Laravel applications alongside WordPress sites. This enables you to use the same robust server provisioning and zero-downtime deployment workflow for both Laravel and WordPress projects.

## How It Works

Laravel support is implemented by:

1. Adding Laravel-specific roles (`laravel-setup` and `laravel-install`) that handle Laravel's different requirements
2. Configuring Nginx to work with Laravel's `/public` web root
3. Using Artisan commands instead of WP-CLI
4. Supporting Laravel's `.env` file format and environment variables

## Usage

### 1. Define Laravel Sites

In your `wordpress_sites.yml` file (yes, we keep the same file structure), simply add a `type: laravel` property to sites that are Laravel projects:

```yaml
wordpress_sites:
  my-laravel-app:
    type: laravel  # This identifies the site as a Laravel project
    site_hosts:
      - canonical: my-laravel.test
        redirects: []
    local_path: ../laravel-app
    admin_email: admin@example.com  # Required but unused for Laravel
    ssl:
      enabled: false
    cache:
      enabled: false
    env:
      APP_NAME: "My Laravel App"
      APP_ENV: local
      APP_DEBUG: true
      APP_URL: http://my-laravel.test
      # Other Laravel environment variables
```

### 2. Customize Nginx (Optional)

You can create custom Nginx configurations for your Laravel site at:
```
nginx-includes/my-laravel-app/laravel-site.conf.j2
```

### 3. Provision & Deploy

Use the standard Stedding commands:

```bash
# Provision server
ansible-playbook server.yml -e env=development

# Deploy site
ansible-playbook deploy.yml -e "site=my-laravel-app env=development"
```

## What's Different for Laravel?

- Web root is `current/public` instead of `current/web`
- Using Laravel's scheduler instead of WP Cron
- Running Artisan commands during deployment (migrations, key generation, etc.)
- Laravel-specific Nginx configuration
- Laravel-friendly `.env` file formatting

## Advanced Options

In your site configuration, you can use these Laravel-specific options:

- `run_migrations: false` - Skip database migrations during deployment
- `cache_config: false` - Skip config caching during deployment