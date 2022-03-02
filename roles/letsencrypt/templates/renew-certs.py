#!/usr/bin/env python3

import os
import sys
import time

from subprocess import CalledProcessError, check_output, STDOUT

failed = False
letsencrypt_cert_ids = {{ letsencrypt_cert_ids }}

for site in {{ sites_using_letsencrypt }}:
    csr_path = os.path.join('{{ acme_tiny_data_directory }}', 'csrs', '{}-{}.csr'.format(site, letsencrypt_cert_ids[site]))
    bundled_cert_path = os.path.join('{{ letsencrypt_certs_dir }}', '{}-bundled.cert'.format(site))
    bundled_hashed_cert_path = os.path.join('{{ letsencrypt_certs_dir }}', '{}-{}-bundled.cert'.format(site, letsencrypt_cert_ids[site]))

    # Generate or update root cert if needed
    if not os.access(csr_path, os.F_OK):
        failed = True
        print('The required CSR file {} does not exist. This could happen if you changed site_hosts and have '
              'not yet rerun the letsencrypt role. Create the CSR file by re-provisioning (running the Trellis '
              'server.yml playbook) with `--tags letsencrypt`'.format(csr_path), file=sys.stderr)
        continue

    elif os.access(bundled_hashed_cert_path, os.F_OK) and time.time() - os.stat(bundled_hashed_cert_path).st_mtime < {{ letsencrypt_min_renewal_age }} * 86400:
        print('Certificate file {} already exists and is younger than {{ letsencrypt_min_renewal_age }} days. '
              'Not creating a new certificate.'.format(bundled_hashed_cert_path))

    else:
        cmd = ('/usr/bin/env python3 {{ acme_tiny_software_directory }}/acme_tiny.py '
            '--quiet '
            '--ca {{ letsencrypt_ca }} '
            '--account-key {{ letsencrypt_account_key }} '
            '--csr {} '
            '--contact {{ letsencrypt_contact_emails | map('regex_replace', '(^.*$)', 'mailto:\\1') | join (' ') }} '
            '--acme-dir {{ acme_tiny_challenges_directory }}'
        ).format(csr_path)

        try:
            new_bundled_cert = check_output(cmd, stderr=STDOUT, shell=True, universal_newlines=True)
        except CalledProcessError as e:
            failed = True
            print('Error while generating certificate for {}\n{}'.format(site, e.output), file=sys.stderr)
            continue
        else:
            with open(bundled_hashed_cert_path, 'w') as bundled_hashed_cert_file:
                bundled_hashed_cert_file.write(new_bundled_cert)
            with open(bundled_cert_path, 'w') as bundled_cert_file:
                bundled_cert_file.write(new_bundled_cert)

    if not os.access(bundled_cert_path, os.F_OK):
        with open(bundled_hashed_cert_path, 'rb') as bundled_hashed_cert_file:
            bundled_hashed_cert = bundled_hashed_cert_file.read()

            with open(bundled_cert_path, 'w') as bundled_cert_file:
                bundled_cert_file.write(bundled_hashed_cert)
                print('Created bundled certificate {}'.format(bundled_cert_path))


if failed:
    sys.exit(1)
