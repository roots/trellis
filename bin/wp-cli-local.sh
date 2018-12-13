#!/bin/bash
vagrant_host=$1
vagrant_path=$2
wpcli_path=$3

# Add wp-cli.local.yml to site root if it doesn't exist with alias for @vagrant
pushd ${wpcli_path}

touch wp-cli.local.yml

if ! grep -Fxq "@vagrant" wp-cli.local.yml
then

cat << EOF > wp-cli.local.yml
@vagrant:
  ssh: vagrant@${vagrant_host}${vagrant_path}
  path: web/wp
EOF

fi

popd
